__author__ = "Lekan Ogunmolu"
__description__ = "Lekan generated this file on 02/13/2020"
__examples__ = "See SoftRobotsPlugin Examples  \
                (i)  /sofa/applications/plugins/SoftRobots/docs/\
                examples/component/constraint/SurfacePressureConstraint/SurfacePressureConstraint.pyscn \
                (ii) python/pneunets.py"


import sys
import Sofa
import os
from os.path import join

pwd = os.getcwd()
meshes_dir = join(pwd, '../..', 'ros/srs_traj_opt/patient_description/meshes')
# sys.path.add(pwd)

'''Convention:
    Bottom IABs: {{neck_left, neck_right},{skull_left, skull_right}}
    Side   IABs: {{fore_left, chin_left}, {fore_right, chin_right}}
'''
# translation vectors for domes
trans = dict(neck_left='-100 -80 10', # base iabs
            neck_right='-100 -80 -90',
            skull_left='20 -80 10',
            skull_right='20 -80 -110',
            fore_left='20 50 80',  # side iabs
            fore_right='20 50 -180',
            chin_left='100 40 80',
            chin_right='-100 40 -180',
            patient='-300 25 -50')

# rotation vectors
rot = dict(neck_left='0 0 0', # base iabs
            neck_right='-90 0 0',
            skull_left='-90 0 0',
            skull_right='-90 0 0',
            fore_left='180 0 0',  # side iabs
            fore_right='-180 0 0',
            chin_left='-180 0 0',
            chin_right='0 0 0',
            patient='-90 -90 0')

dome = {}
dome['scale'] = 36 # same as in xml files being read in c++
dome['mass'] = .04 # as measured by newly fabricated soft robot, in Kg

poisson=0.3   # poisson from pneunet parameters
youngs=18000  # using pneunet parameters
youngModulusDomes = 500
youngModulusStiffLayerDomes = 1500

class dome_test (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) :
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):
        rootNode.createObject('APIVersion', level='19.06')
        # by default, the gravity is defined as "0 -9.81 0". redefined below
        rootNode.findData('gravity').value='0 0 -9810'; # define gravity is along z in mm/sec
        rootNode.createObject('BackgroundSetting', color='0 0.168627 0.211765')
        rootNode.createObject('OglSceneFrame', style='Arrows', alignment='BottomLeft')

        rootNode.createObject('RequiredPlugin', pluginName='IAB', name='IAB')
        rootNode.createObject('RequiredPlugin', pluginName='IABTetra', name='IABTetra')
        rootNode.createObject('RequiredPlugin', name='SofaPython', pluginName='SofaPython')
        rootNode.createObject('RequiredPlugin', name='SoftRobots', pluginName='SoftRobots')
        rootNode.createObject('RequiredPlugin', pluginName='CImgPlugin', name='CImgPlugin')
        rootNode.createObject('RequiredPlugin', name='SofaSparseSolver', pluginName='SofaSparseSolver')
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual', pluginName='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPreconditioner', pluginName='SofaPreconditioner')
        rootNode.createObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels showCollisionModels showBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')

        rootNode.createObject('FreeMotionAnimationLoop')
        rootNode.createObject('GenericConstraintSolver', maxIterations='100', tolerance = '0.0000001')
        rootNode.createObject('PythonScriptController', filename="diff_kine_controller.py", classname="controller")

        # Patient
        self.patient = rootNode.createChild('patient')
        self.patient.createObject('EulerImplicit', name='odesolver')
        self.patient.createObject('SparseLDLSolver', name='linearSolver')
        self.patient.createObject('MeshObjLoader', name='patient_loader', filename='{}/patient.obj'.format(meshes_dir))
        self.patient.createObject('MechanicalObject', src='@patient_loader', name='patient-states', template='Vec3d',\
                                    translation=trans['neck_left'], rotation=rot['neck_left'])
        self.patient.createObject('UniformMass', totalMass='95')
        self.patient.createObject('UncoupledConstraintCorrection')
        # self.patient.createObject('MeshObjLoader', name='patientCollisLoader', filename='{}/patient.obj'.format(meshes_dir))
        # rootNode/PatientCollis
        patientCollis = self.patient.createChild('patientCollis')
        patientCollis.createObject('Mesh', src="@../patient_loader")
        patientCollis.createObject('MechanicalObject', name='patient_dofs', template='Vec3d', scale="250",\
                                    translation=trans['neck_left'], rotation=rot['neck_left'])
        # rootNode/PatientVisu
        patientVisu = self.patient.createChild('patientVisu')
        patientVisu.createObject('OglModel', src='@../patient_loader', name='patientVisual',\
                                    scale="250", rx="-90", ry="-90", translation='-300 25 -50')

        # first dome
        self.DomeHead=rootNode.createChild('DomeHead')
        self.DomeHead.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        self.DomeHead.createObject('SparseLDLSolver', name='linearSolver')

        self.DomeHead.createObject('MeshVTKLoader', name='domeHeadVTKLoader', filename='{}/dome/dome.vtu'.format(meshes_dir),rotation=rot['neck_left'])#'-90 0 0')
        self.DomeHead.createObject('TetrahedronSetTopologyContainer', src='@domeHeadVTKLoader', name='TetraTopologyContainer') #createTriangleArray='true',
        self.DomeHead.createObject('TetrahedronSetTopologyModifier', name='TetraTopologyModifier')
        self.DomeHead.createObject('TetrahedronSetTopologyAlgorithms', name='TetraTopologyAlgo', template='Vec3d')
        self.DomeHead.createObject('TetrahedronSetGeometryAlgorithms', drawTetrahedra='1', name='TetraGeomAlgo', template='Vec3d')\

        self.DomeHead.createObject('MechanicalObject', name='dh_dofs', template='Vec3d', showIndices='false', showIndicesScale='4e-5',\
                                     scale=dome['scale'], translation=trans['neck_left'], rotation=rot['neck_left']) #src='@domeHeadVTKLoader',
        self.DomeHead.createObject('UniformMass', totalMass='{}'.format(dome['mass']))
        self.DomeHead.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='{}'.format(poisson),  youngModulus='{}'.format(youngs))

        # stiff layer identified indices from paraview
        self.DomeHead.createObject('BoxROI', name='boxROI', box='-2.75533 2.74354 -.1597 2.76615 -2.99312 2.99312', drawBoxes='true', doUpdate='1')#, position="@dh_dofs.rest_position", tetrahedra="@TetraTopologyContainer.tetrahedra")
        self.DomeHead.createObject('BoxROI', name='boxROISubTopo', box='-6.75533 4.74354 -4.7597 4.76615 -3.99312 3.99312', drawBoxes='false', doUpdate='0')#, position="@dh_dofs.rest_position", tetrahedra="@TetraTopologyContainer.tetrahedra")
        # this defines the boundary condition which creates springs between the current position of the body and its initial position
        self.DomeHead.createObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e5', angularStiffness='1e5') # stiffness was 1e12 after the pneunets demo

        self.DomeHead.createObject('SparseLDLSolver', name='preconditioner')

        # rootNode.createObject('TetrahedronMooneyRivlinFEMForceField', name='rootFEM', materialName='MooneyRivlinIncompressible', ParameterSet='1000 100', template='Vec3d', poissonRatio='0.45', youngModulus='10000')
        ##########################################2
        #             Sub topology               #
        ##########################################
        self.DomeHeadSubTopo = self.DomeHead.createChild('self.DomeHeadSubTopo')
        # create the mesh
        self.DomeHeadSubTopo.createObject('TetrahedronSetTopologyContainer', position='@../domeHeadVTKLoader.position', tetrahedra="@boxROISubTopo.tetrahedraInROI", name='container')
        self.DomeHeadSubTopo.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus=str(youngModulusStiffLayerDomes-youngModulusDomes))

        # rootNode/DomeCavity
        self.DomeCavity = self.DomeHead.createChild('DomeCavity')
        self.DomeCavity.createObject('MeshObjLoader', name='cavityLoader', filename='{}/dome/dome_cavity.obj'.format(meshes_dir), triangulate="true")
        self.DomeCavity.createObject('Mesh', src='@cavityLoader', name='cavityTopo')
        self.DomeCavity.createObject('MechanicalObject',  name='domeCavity', scale=dome['scale'], translation=trans['neck_left'], rotation=rot['neck_left'])
        self.DomeCavity.createObject('SurfacePressureConstraint', name='SurfacePressureConstraint', template="Vec3d", value="0.0001", triangles='@cavityTopo.triangles', drawPressure='0', drawScale='0.0002', valueType='pressure') #
        self.DomeCavity.createObject('BarycentricMapping',  name='mapping', mapForces='false', mapMasses='false')# , input='@../dh_dofs',  output='@DomeCavity', template="Vec3d")

        # rootNode/DomeHeadCollis
        self.DomeHeadCollis = self.DomeHead.createChild('DomeHeadCollis')
        self.DomeHeadCollis.createObject('MeshObjLoader', name='domeHeadCollisLoader', filename='{}/dome/dome_cavity.obj'.format(meshes_dir)) #src='@../domeHeadVTKLoader', scale='1', , rx='0', ry='0', rz='0', dz='0', dx='0', dy='0', template='Vec3d')
        self.DomeHeadCollis.createObject('Mesh', src='@domeHeadCollisLoader', name='topo')
        self.DomeHeadCollis.createObject('MechanicalObject', name='collisMech',  scale=dome['scale'], translation=trans['neck_left'], rotation=rot['neck_left'])
        self.DomeHeadCollis.createObject('Triangle', selfCollision="false")
        self.DomeHeadCollis.createObject('Line',selfCollision="false")
        self.DomeHeadCollis.createObject('Point', selfCollision="false")
        self.DomeHeadCollis.createObject('BarycentricMapping',  name='mapping', mapForces='false', mapMasses='false')# , input='@../dh_dofs',  output='@DomeCavity', template="Vec3d")

        # rootNode/DomeHeadVisu
        self.DomeHeadVisu = self.DomeHead.createChild('DomeHeadVisu')
        self.DomeHeadVisu.createObject('MeshObjLoader', name='domeHeadVisuLoader', filename='{}/dome/dome.obj'.format(meshes_dir)) #src='@../domeHeadVTKLoader', scale='1', , rx='0', ry='0', rz='0', dz='0', dx='0', dy='0', template='Vec3d')
        self.DomeHeadVisu.createObject('OglModel',  color='0.3 0.2 0.2 0.6') # name='@domeHeadVisuLoader', template='Vec3d', src="@../domeHeadCollisLoader", #dx="20", dy="-80", dz="10", rx="-90",
        # self.DomeHeadVisu.createObject('Mesh', src='@../domeHeadVTKLoader', name='topo')
        # self.DomeHeadVisu.createObject('MechanicalObject', name='domeHeadVizMech',  scale=dome['scale'], translation=trans['neck_left'], rotation=rot['neck_left'])
        self.DomeHeadVisu.createObject('BarycentricMapping', name='mapping')#, mapForces='false', mapMasses='false')

        # Dome Cover
        self.DomeCoverVisu = self.DomeHead.createChild('DomeCoverVisu')
        self.DomeCoverVisu.createObject('MeshSTLLoader', name='domeCoverLoader', filename='{}/dome/cover.stl'.format(meshes_dir))
        self.DomeCoverVisu.createObject('MechanicalObject', name='domeCoverVisu',  scale=dome['scale'], \
                                            translation=trans['neck_left'], rotation=rot['neck_left'])
        self.DomeCoverVisu.createObject('BarycentricMapping',  name='mapping', mapForces='false', mapMasses='false')
        self.DomeCoverVisu.createObject('OglModel', color='0.3 0.5 0.5 0.6')
        # DomeCoverCollis
        self.DomeCoverCollis = self.DomeHead.createChild('DomeCoverCollis')
        self.DomeCoverCollis.createObject('MeshObjLoader', name='domeCoverCollis', filename='{}/dome/cover.obj'.format(meshes_dir)) #src='@../domeHeadVTKLoader', scale='1', , rx='0', ry='0', rz='0', dz='0', dx='0', dy='0', template='Vec3d')
        self.DomeCoverCollis.createObject('Mesh', src='@domeCoverCollis', name='topo')
        self.DomeCoverCollis.createObject('MechanicalObject', name='collisMech',  scale=dome['scale'], \
                                            translation=trans['neck_left'], rotation=rot['neck_left'] )
        self.DomeCoverCollis.createObject('Triangle', selfCollision="false")
        self.DomeCoverCollis.createObject('Line',selfCollision="false")
        self.DomeCoverCollis.createObject('Point', selfCollision="false")
        self.DomeCoverCollis.createObject('BarycentricMapping',  name='mapping', mapForces='false', mapMasses='false')# , input='@../dh_dofs',  output='@DomeCavity', template="Vec3d")
        return rootNode;

    def initGraph(self, node):
        ## Please feel free to add an example for a simple usage in /home/lex/catkin_ws/src/superchicko/sofa/python/xml_2_scn.py
        return 0;

def createScene(rootNode):
    rootNode.findData('dt').value = '0.005'
    rootNode.findData('gravity').value = '0 -9 0'
    try :
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    mydome_test = dome_test(rootNode,commandLineArguments)
    return 0;