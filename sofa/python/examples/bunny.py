import os
import Sofa
from os.path import join, expanduser
# path = join(expanduser('~'), 'applications/plugins/SoftRobots/python/softrobots/parts/bunny/mesh/')
# path = join(expanduser('~'), 'sofa', 'v19.06', 'applications/plugins/SoftRobots/python/softrobots/parts/bunny/mesh/')
path = join(expanduser('~'), 'sofa', 'applications/plugins/SoftRobots/python/softrobots/parts/bunny/mesh/')

print(path)

def createScene(rootNode):
    rootNode.createObject('RequiredPlugin', pluginName='SoftRobots')
    rootNode.createObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels showCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')

    rootNode.createObject('FreeMotionAnimationLoop')
    rootNode.createObject('GenericConstraintSolver', maxIterations='100', tolerance = '0.0000001')
    rootNode.createObject('PythonScriptController', filename="bunnycontroller.py", classname="controller")

    bunny = rootNode.createChild('bunny')
    bunny.createObject('EulerImplicit', name='odesolver')
    bunny.createObject('ShewchukPCGLinearSolver', iterations='15', name='linearsolver', tolerance='1e-5', preconditioners='preconditioner', use_precond='true', update_step='1')

    bunny.createObject('MeshVTKLoader', name='loader', filename=path+'Hollow_Stanford_Bunny.vtu')
    bunny.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
    bunny.createObject('TetrahedronSetTopologyModifier')
    bunny.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d')
    bunny.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')

    bunny.createObject('MechanicalObject', name='tetras', template='Vec3d', showIndices='false', showIndicesScale='4e-5', rx='0', dz='0')
    bunny.createObject('UniformMass', totalMass='0.5')
    bunny.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus='18000')

    bunny.createObject('BoxROI', name='boxROI', box='-5 -15 -5  5 -4.5 5', drawBoxes='true', position="@tetras.rest_position", tetrahedra="@container.tetrahedra")
    bunny.createObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12')

    bunny.createObject('SparseLDLSolver', name='preconditioner')
    bunny.createObject('LinearSolverConstraintCorrection', solverName='preconditioner')
    #bunny.createObject('UncoupledConstraintCorrection')

    #bunny/cavity
    cavity = bunny.createChild('cavity')
    cavity.createObject('MeshObjLoader', name='loader', filename=path+'Hollow_Bunny_Body_Cavity.obj')
    cavity.createObject('Mesh', src='@loader', name='topo')
    cavity.createObject('MechanicalObject', name='cavity')
    cavity.createObject('SurfacePressureConstraint', triangles='@topo.triangles', value='40', valueType="1")
    # cavity.createObject('BarycentricMapping', name='mapping',  mapForces='false', mapMasses='false')
    cavity.createObject('BarycentricMapping', name='mapping',  mapForces='true', mapMasses='true')


    #bunny/bunnyVisu
    bunnyVisu = bunny.createChild('visu')
    bunnyVisu.createObject('TriangleSetTopologyContainer', name='container')
    bunnyVisu.createObject('TriangleSetTopologyModifier')
    bunnyVisu.createObject('TriangleSetTopologyAlgorithms', template='Vec3d')
    bunnyVisu.createObject('TriangleSetGeometryAlgorithms', template='Vec3d')
    bunnyVisu.createObject('Tetra2TriangleTopologicalMapping', name='Mapping', input="@../container", output="@container")

    bunnyVisu.createObject('OglModel', template='ExtVec3f', color='0.3 0.2 0.2 0.6')
    bunnyVisu.createObject('IdentityMapping')


    return rootNode
