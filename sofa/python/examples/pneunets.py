import Sofa
import math
import os
from os.path import join, expanduser

# See tutorial here https://github.com/SofaDefrost/Tutorials/blob/master/PneuNets-Gripper/docs/simulation.md
# mac osx
# path = os.path.join(expanduser('~'), 'sofa/v19.06/applications/plugins/SoftRobots/docs/tutorials/PneunetGripper/details/data/mesh/')
# linux office
path = os.path.join(expanduser('~'), 'sofa/applications/plugins/SoftRobots/docs/tutorials/PneunetGripper/details/data/mesh/')
print('path ', path, '\n\n')
youngModulusFingers = 500
youngModulusStiffLayerFingers = 1500
poissonRatioFingers = 0.3
fingersMass = 0.04

radius = 70
angle1 = 120*math.pi/180  # Angle between 1st and 2nd finger in radian
angle2 = 240*math.pi/180  # Angle between 1st and 3rd finger in radian
translateFinger1 = "0 0 0"
translateFinger2 = "0 " + str(radius + radius*math.sin(angle1-math.pi/2)) + " " + str(radius*math.cos(angle1-math.pi/2))
translateFinger3 = "0 " + str(radius + radius*math.sin(angle2-math.pi/2)) + " " + str(radius*math.cos(angle2-math.pi/2))

def createScene(rootNode):
    rootNode.createObject('RequiredPlugin', pluginName='SoftRobots')
    rootNode.createObject('RequiredPlugin', pluginName='SofaOpenglVisual')
    rootNode.createObject('RequiredPlugin', pluginName='SofaSparseSolver')
    rootNode.createObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels hideCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')
    rootNode.findData('gravity').value='-9810 0 0';
    rootNode.createObject('FreeMotionAnimationLoop')
    rootNode.createObject('GenericConstraintSolver', maxIterations="10000", tolerance="1e-3")
    rootNode.createObject('CollisionPipeline', verbose="0")
    rootNode.createObject('BruteForceDetection', name="N2")
    rootNode.createObject('CollisionResponse', response="FrictionContact", responseParams="mu=0.6")
    rootNode.createObject('LocalMinDistance', name="Proximity", alarmDistance="5", contactDistance="1", angleCone="0.01")

    rootNode.createObject('BackgroundSetting', color='0 0.168627 0.211765')
    rootNode.createObject('OglSceneFrame', style="Arrows", alignment="TopRight")
    rootNode.createObject('PythonScriptController', filename="controllerGripper.py", classname="controller")

    planeNode = rootNode.createChild('Plane')
    planeNode.createObject('MeshObjLoader', name='planeloader', filename="mesh/floorFlat.obj", triangulate="true", rotation="0 0 270", scale =10, translation="-122 0 0")
    planeNode.createObject('Mesh', src="@planeloader")
    planeNode.createObject('MechanicalObject', src="@loader")
    planeNode.createObject('Triangle', simulated="0", moving="0")
    planeNode.createObject('Line', simulated="0", moving="0")
    planeNode.createObject('Point', simulated="0", moving="0")
    planeNode.createObject('OglModel',name="@planeloader", color="1 0 0 1",rotation="0 0 270", scale =10, translation="-122 0 0")

    cube = rootNode.createChild('cube')
    cube.createObject('EulerImplicit', name='odesolver')
    cube.createObject('SparseLDLSolver', name='linearSolver')
    cube.createObject('MechanicalObject', template="Rigid", scale="4", position='-23 16 0 0 0 0 1')#, dx="47.0", dy="10", dz="8", rx="10" ,ry="10")
    cube.createObject('UniformMass', mass='0.0008  74088  0.2352 0 0  0 0.2352 0  0 0 0.2352')
    cube.createObject('UncoupledConstraintCorrection')

    #collision
    cubeCollis = cube.createChild('cubeCollis')
    cubeCollis.createObject('MeshObjLoader', name="cubeLoader", filename="mesh/smCube27.obj", triangulate="true",  scale="6")
    cubeCollis.createObject('Mesh', src="@cubeLoader")
    cubeCollis.createObject('MechanicalObject', translation='0 0 0')
    cubeCollis.createObject('Triangle')
    cubeCollis.createObject('Line')
    cubeCollis.createObject('Point')
    cubeCollis.createObject('RigidMapping')

    #visualization
    cubeVisu = cube.createChild('cubeVisu')
    cubeVisu.createObject('OglModel', name="Visual", src="@cubeLoader", color="0.0 0.1 0.5", scale="6.2")
    cubeVisu.createObject('RigidMapping')

    ##########################################
    # Finger 1 Model                         #
    ##########################################
    finger1 = rootNode.createChild('finger1')
    finger1.createObject('EulerImplicit', name='odesolver')
    finger1.createObject('SparseLDLSolver', name='preconditioner')

    finger1.createObject('MeshVTKLoader', name='loader', filename=path+'pneunetCutCoarse.vtk',translation = translateFinger1)
    finger1.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
    finger1.createObject('TetrahedronSetTopologyModifier')
    finger1.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d')
    finger1.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')

    finger1.createObject('MechanicalObject', name='tetras', template='Vec3d', showIndices='false', showIndicesScale='4e-5', rx='0', dz='0')
    finger1.createObject('UniformMass', totalMass=str(fingersMass))
    finger1.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus=str(youngModulusFingers), drawAsEdges="1")

    finger1.createObject('BoxROI', name='boxROI', box='-10 0 -20 0 30 20', drawBoxes='true',doUpdate='0')
    #finger1.createObject('BoxROI', name='boxROI', box='-50 0 -20 0 30 20', drawBoxes='true',doUpdate='0')
    finger1.createObject('BoxROI', name='boxROISubTopo', box='-100 22.5 -8 -19 28 8', drawBoxes='true')
    finger1.createObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    finger1.createObject('LinearSolverConstraintCorrection', solverName='preconditioner')

    ##########################################
    # Sub topology                           #
    ##########################################
    modelSubTopo = finger1.createChild('modelSubTopo')
    modelSubTopo.createObject('TetrahedronSetTopologyContainer', position='@loader.position', tetrahedra="@boxROISubTopo.tetrahedraInROI", name='container')
    modelSubTopo.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus=str(youngModulusStiffLayerFingers-youngModulusFingers))


    ##########################################
    # Constraint                             #
    ##########################################
    cavity = finger1.createChild('cavity')
    cavity.createObject('MeshSTLLoader', name='loader', filename=path+'pneunetCavityCut.stl',translation = translateFinger1)
    cavity.createObject('Mesh', src='@loader', name='topo')
    cavity.createObject('MechanicalObject', name='cavity')
    cavity.createObject('SurfacePressureConstraint', name="SurfacePressureConstraint", template='Vec3d', value="0.0001", triangles='@topo.triangles', drawPressure='0', drawScale='0.0002', valueType="pressure")
    cavity.createObject('BarycentricMapping', name='mapping',  mapForces='false', mapMasses='false')

    ##########################################
    # Collision                              #
    ##########################################

    collisionFinger = finger1.createChild('collisionFinger')
    collisionFinger.createObject('MeshSTLLoader', name='pneuLoader', filename=path+'pneunetCut.stl', translation = translateFinger1)
    collisionFinger.createObject('Mesh', src='@pneuLoader', name='topo')
    collisionFinger.createObject('MechanicalObject', name='collisMech')
    collisionFinger.createObject('Triangle', selfCollision="false")
    collisionFinger.createObject('Line',selfCollision="false")
    collisionFinger.createObject('Point', selfCollision="false")
    collisionFinger.createObject('BarycentricMapping')


    ##########################################
    # Visualization                          #
    ##########################################
    modelVisu = finger1.createChild('visu')
    modelVisu.createObject('OglModel', name="pneuLoader", src="@pneuLoader", template='Vec3d', color='0.7 0.7 0.7 0.6',translation = translateFinger1)
    modelVisu.createObject('BarycentricMapping')

    ##########################################
        # Finger 2 Model                         #
    ##########################################
    finger2 = rootNode.createChild('finger2')
    finger2.createObject('EulerImplicit', name='odesolver')
    finger2.createObject('SparseLDLSolver', name='preconditioner')

    finger2.createObject('MeshVTKLoader', name='loader', filename=path+'pneunetCutCoarse.vtk',rotation=str(360 - angle1*180/math.pi)+ " 0 0", translation=translateFinger2)
    finger2.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
    finger2.createObject('TetrahedronSetTopologyModifier')
    finger2.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d')
    finger2.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')

    finger2.createObject('MechanicalObject', name='tetras', template='Vec3d', showIndices='false', showIndicesScale='4e-5', rx='0', dz='0')
    finger2.createObject('UniformMass', totalMass=str(fingersMass))
    finger2.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus=str(youngModulusFingers), drawAsEdges="1")
    finger2.createObject('RestShapeSpringsForceField', points='@../finger1/boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    finger2.createObject('LinearSolverConstraintCorrection', solverName='preconditioner')

    ##########################################
    # Sub topology                           #
    ##########################################
    modelSubTopo = finger2.createChild('modelSubTopo')
    modelSubTopo.createObject('TetrahedronSetTopologyContainer', position='@loader.position', tetrahedra="@../../finger1/boxROISubTopo.tetrahedraInROI", name='container')
    modelSubTopo.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus=str(youngModulusStiffLayerFingers-youngModulusFingers))


    ##########################################
    # Constraint                             #
    ##########################################
    cavity = finger2.createChild('cavity')
    cavity.createObject('MeshSTLLoader', name='cavloader', filename=path+'pneunetCavityCut.stl',rotation=str(360 - angle1*180/math.pi)+ " 0 0" , translation=translateFinger2)
    cavity.createObject('Mesh', src='@cavloader', name='topo')
    cavity.createObject('MechanicalObject', name='cavity')
    cavity.createObject('SurfacePressureConstraint', name="SurfacePressureConstraint", template='Vec3d', value="0.0001", triangles='@topo.triangles', drawPressure='0', drawScale='0.0002', valueType="pressure")
    cavity.createObject('BarycentricMapping', name='mapping',  mapForces='false', mapMasses='false')

    ##########################################
    # Collision                              #
    ##########################################

    collisionFinger = finger2.createChild('collisionFinger')
    collisionFinger.createObject('MeshSTLLoader', name='loader', filename=path+'pneunetCut.stl',rotation=str(360 - angle1*180/math.pi)+ " 0 0", translation=translateFinger2)
    collisionFinger.createObject('Mesh', src='@loader', name='topo')
    collisionFinger.createObject('MechanicalObject', name='collisMech')
    collisionFinger.createObject('Triangle', selfCollision="false")
    collisionFinger.createObject('Line', selfCollision="false")
    collisionFinger.createObject('Point', selfCollision="false")
    collisionFinger.createObject('BarycentricMapping')


    ##########################################
    # Visualization                          #
    ##########################################
    modelVisu = finger2.createChild('visu')
    modelVisu.createObject('OglModel', name="cavloader", src="@cavloader", template='Vec3d', color='0.7 0.7 0.7 0.6',rotation=str(360 - angle1*180/math.pi)+ " 0 0", translation=translateFinger2)
    modelVisu.createObject('BarycentricMapping')

    ##########################################
    # Finger 3 Model                         #
    ##########################################
    finger3 = rootNode.createChild('finger3')
    finger3.createObject('EulerImplicit', name='odesolver')
    finger3.createObject('SparseLDLSolver', name='preconditioner')

    finger3.createObject('MeshVTKLoader', name='loader', filename=path+'pneunetCutCoarse.vtk',rotation=str(360 - angle2*180/math.pi)+ " 0 0", translation=translateFinger3)
    finger3.createObject('TetrahedronSetTopologyContainer', src='@loader', name='container')
    finger3.createObject('TetrahedronSetTopologyModifier')
    finger3.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d')
    finger3.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')

    finger3.createObject('MechanicalObject', name='tetras', template='Vec3d', showIndices='false', showIndicesScale='4e-5', rx='0', dz='0')
    finger3.createObject('UniformMass', totalMass=str(fingersMass))
    finger3.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus=str(youngModulusFingers), drawAsEdges="1")
    finger3.createObject('RestShapeSpringsForceField', points='@../finger1/boxROI.indices', stiffness='1e12', angularStiffness='1e12')

    finger3.createObject('LinearSolverConstraintCorrection', solverName='preconditioner')

    ##########################################
    # Sub topology                           #
    ##########################################
    modelSubTopo = finger3.createChild('modelSubTopo')
    modelSubTopo.createObject('TetrahedronSetTopologyContainer', position='@loader.position', tetrahedra="@../../finger1/boxROISubTopo.tetrahedraInROI", name='container')
    modelSubTopo.createObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large', poissonRatio='0.3',  youngModulus=str(youngModulusStiffLayerFingers-youngModulusFingers))


    ##########################################
    # Constraint                             #
    ##########################################
    cavity = finger3.createChild('cavity')
    cavity.createObject('MeshSTLLoader', name='loader', filename=path+'pneunetCavityCut.stl',rotation=str(360 - angle2*180/math.pi)+ " 0 0", translation=translateFinger3)
    cavity.createObject('Mesh', src='@loader', name='topo')
    cavity.createObject('MechanicalObject', name='cavity')
    cavity.createObject('SurfacePressureConstraint', name="SurfacePressureConstraint", template='Vec3d', value="0.0001", triangles='@topo.triangles', drawPressure='0', drawScale='0.0002', valueType="pressure")
    cavity.createObject('BarycentricMapping', name='mapping',  mapForces='false', mapMasses='false')

    ##########################################
    # Collision                              #
    ##########################################

    collisionFinger = finger3.createChild('collisionFinger')
    collisionFinger.createObject('MeshSTLLoader', name='collisloader', filename=path+'pneunetCut.stl',rotation=str(360 - angle2*180/math.pi)+ " 0 0", translation=translateFinger3)
    collisionFinger.createObject('Mesh', src='@collisloader', name='topo')
    collisionFinger.createObject('MechanicalObject', name='collisMech')
    collisionFinger.createObject('Triangle', selfCollision="false")
    collisionFinger.createObject('Line', selfCollision="false")
    collisionFinger.createObject('Point', selfCollision="false")
    collisionFinger.createObject('BarycentricMapping')


    ##########################################
    # Visualization                          #
    ##########################################
    modelVisu = finger3.createChild('visu')
    modelVisu.createObject('OglModel', name="collisloader", template='Vec3d', color='0.7 0.7 0.7 0.6',rotation=str(360 - angle2*180/math.pi)+ " 0 0", translation=translateFinger3)
    modelVisu.createObject('BarycentricMapping')

    return rootNode
