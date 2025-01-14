
'''
# UP key :
if ord(c)==19:
bnl_mv = moveRestPos(self.base_neck_left.rest_position, move_dist)
bnr_mv = moveRestPos(self.base_neck_right.rest_position, move_dist)
bsl_mv = moveRestPos(self.base_skull_left.rest_position, move_dist)
bsr_mv = moveRestPos(self.base_skull_right.rest_position, move_dist)
self.base_neck_left.findData('rest_position').value = bnl_mv
self.base_neck_left.findData('rest_position').value = bnr_mv
self.base_neck_left.findData('rest_position').value = bsl_mv
self.base_neck_left.findData('rest_position').value = bsr_mv

self.update_head_pose()

# DOWN key : rear
if ord(c)==21:
bnl_mv = moveRestPos(self.base_neck_left.rest_position, -move_dist)
bnr_mv = moveRestPos(self.base_neck_right.rest_position, -move_dist)
bsl_mv = moveRestPos(self.base_skull_left.rest_position, -move_dist)
bsr_mv = moveRestPos(self.base_skull_right.rest_position, -move_dist)
self.base_neck_left.findData('rest_position').value = bnl_mv
self.base_neck_left.findData('rest_position').value = bnr_mv
self.base_neck_left.findData('rest_position').value = bsl_mv
self.base_neck_left.findData('rest_position').value = bsr_mv

self.update_head_pose()

# LEFT key : left
if ord(c)==20:
mv_left = (0, 10, 10)
test = moveRestPos(self.base_neck_left.rest_position, 0.0, dy, dz)
self.base_neck_left.findData('rest_position').value = test

# RIGHT key : right
if ord(c)==18:
dy = -3.0*math.cos(self.rotAngle)
dz = -3.0*math.sin(self.rotAngle)
test = moveRestPos(self.neck_left_mech.rest_position, 0.0, dy, dz)
self.neck_left_mech.findData('rest_position').value = test

# a key : direct rotation
if (ord(c) == 65):
test = rotateRestPos(self.neck_left_mech.rest_position, math.pi/16, self.centerPosY,self.centerPosZ)
self.neck_left_mech.findData('rest_position').value = test

# q key : indirect rotation
if (ord(c) == 81):
test = rotateRestPos(self.neck_left_mech.rest_position, -math.pi/16, self.centerPosY,self.centerPosZ)
self.neck_left_mech.findData('rest_position').value = test
self.rotAngle = self.rotAngle - math.pi/16


def onMouseButtonLeft(self, mouseX,mouseY,isPressed):
# usage e.g.
if isPressed :
print ("Control+Left mouse button pressed at position "+str(mouseX)+", "+str(mouseY))
return 0;

def onKeyReleased(self, c):
# usage e.g.
if c=="A" :
print ("You released a")
return 0;

def onMouseWheel(self, mouseX,mouseY,wheelDelta, isPressed):
# usage e.g.
if isPressed :
print ("Control button pressed+mouse wheel turned at position "+str(mouseX)+", "+str(mouseY)+", wheel delta"+str(wheelDelta))
return 0;

def storeResetState(self):
## Please feel free to add an example for a simple usage in /home/lex/catkin_ws/src/superchicko/sofa/python/xml_2_scn.py
return 0;

def cleanup(self):
## Please feel free to add an example for a simple usage in /home/lex/catkin_ws/src/superchicko/sofa/python/xml_2_scn.py
return 0;

def onGUIEvent(self, strControlID,valueName,strValue):
## Please feel free to add an example for a simple usage in /home/lex/catkin_ws/src/superchicko/sofa/python/xml_2_scn.py
return 0;


	# def onKeyPressed(self,c):
	# 	self.dt = self.root.findData('dt').value
	# 	incr = self.dt*1000.0;
	#
	# 	if (c == "+"):
	# 		print(' raising head using base IABs')
	# 		bnl_val = self.base_neck_left_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	# 		bnr_val = self.base_neck_right_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	# 		bsl_val = self.base_skull_left_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	# 		bsr_val = self.base_skull_right_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	#
	# 		bnl_val = max_pressure if bnl_val > max_pressure else bnl_val
	# 		bnr_val = max_pressure if bnr_val > max_pressure else bnr_val
	# 		bsl_val = max_pressure if bsl_val > max_pressure else bsl_val
	# 		bsr_val = max_pressure if bsr_val > max_pressure else bsr_val
	#
	# 		self.base_neck_left_dofs.pressure_constraint.findData('value').value = str(bnl_val)
	# 		self.base_neck_right_dofs.pressure_constraint.findData('value').value = str(bnr_val)
	# 		self.base_skull_left_dofs.pressure_constraint.findData('value').value = str(bsl_val)
	# 		self.base_skull_right_dofs.pressure_constraint.findData('value').value = str(bsr_val)
	#
	# 		self.update_head_pose()
	# 		plt.ion()
	# 		plt.show()
	#
	# 	if (c == "-"):
	# 		print('lowering head using base IABs')
	# 		bnl_val = self.base_neck_left_dofs.pressure_constraint.findData('value').value[0][0] - self.growth_rate
	# 		bnr_val = self.base_neck_right_dofs.pressure_constraint.findData('value').value[0][0] - self.growth_rate
	# 		bsl_val = self.base_skull_left_dofs.pressure_constraint.findData('value').value[0][0] - self.growth_rate
	# 		bsr_val = self.base_skull_right_dofs.pressure_constraint.findData('value').value[0][0] - self.growth_rate
	#
	# 		bnl_val = max_pressure if bnl_val > max_pressure else bnl_val
	# 		bnr_val = max_pressure if bnr_val > max_pressure else bnr_val
	# 		bsl_val = max_pressure if bsl_val > max_pressure else bsl_val
	# 		bsr_val = max_pressure if bsr_val > max_pressure else bsr_val
	#
	# 		self.base_neck_left_dofs.pressure_constraint.findData('value').value = str(bnl_val)
	# 		self.base_neck_right_dofs.pressure_constraint.findData('value').value = str(bnr_val)
	# 		self.base_skull_left_dofs.pressure_constraint.findData('value').value = str(bsl_val)
	# 		self.base_skull_right_dofs.pressure_constraint.findData('value').value = str(bsr_val)
	#
	# 		self.update_head_pose()
	# 		plt.ion()
	# 		plt.show()
'''

def onBeginAnimationStep(self, deltaTime):
	self.deltaTime  += deltaTime

	# repopulate each iab at each time step
	self.base_neck_left		= 	self.root.getChild('base_neck_left')
	self.base_neck_right	= 	self.root.getChild('base_neck_right')
	self.base_skull_left	= 	self.root.getChild('base_skull_left')
	self.base_skull_right	= 	self.root.getChild('base_skull_right')
	# get side IABs
	self.side_fore_left		= 	self.root.getChild('side_fore_left')
	self.side_chin_left		= 	self.root.getChild('side_chin_left')
	self.side_fore_right	= 	self.root.getChild('side_fore_right')
	self.side_chin_right	= 	self.root.getChild('side_chin_right')
	# obtain associated dofs and cavity dofs
	self.base_neck_left_dofs 	= self.get_dome_dofs(self.base_neck_left)
	self.base_neck_right_dofs 	= self.get_dome_dofs(self.base_neck_right)
	self.base_skull_left_dofs 	= self.get_dome_dofs(self.base_skull_left)
	self.base_skull_right_dofs 	= self.get_dome_dofs(self.base_skull_right)

	# self.patient = self.root.getChild('patient')
	self.patient_dofs = self.patient.getObject('patient_dofs')

	if self.first_iter:
		pat_pose = self.patient_dofs.findData('rest_position').value
		self.thresholds['patient_trans'] = (np.linalg.norm(pat_pose, axis=0)+1000).tolist()
		self.thresholds.update(self.thresholds)
		logger.debug('rest_pat_pose: {}, '.format(np.linalg.norm(pat_pose, axis=0)))
		self.first_iter = False

	curr_pat_pose = np.linalg.norm(self.patient_dofs.position, axis=0)
	pose = (self.growth_rate, self.growth_rate, self.growth_rate)
	# if curr_pat_pose[2]>self.thresholds['patient_trans'][2]:
	# 	logger.warning('reached max z limit')
	# 	pose = (0.0, self.growth_rate, 0.0)
	# 	# self.is_inflated = False
	# 	if curr_pat_pose[1]>self.thresholds['patient_trans'][1]:
	# 		logger.warning('reached max z limit')
	# 		pose = (self.growth_rate, 0.0, 0.0)
	# 		# self.is_inflated = False
	# cond = curr_pat_pose>self.thresholds['patient_trans']
	test1 = moveRestPos(self.patient_dofs.rest_position, pose)
	self.patient_dofs.findData('rest_position').value = test1

	with open(self._pat_dofs_filename, 'a') as foo:
		np.savetxt(foo, np.linalg.norm(self.patient_dofs.position, axis=0), delimiter=' ', fmt='%1.4e')

	# curr_pat_pose = np.linalg.norm(self.patient_dofs.position, axis=0)
	# if np.all(curr_pat_pose>self.thresholds['patient_trans']):
	# 	self.root.getRootContext().animate = False
	# 		   # self.is_inflated = False
	# logger.debug('pat_dofs: {}\n\tthresholds: {}'.format(np.linalg.norm(self.patient_dofs.position, axis=0), self.thresholds['patient_trans']))

	# self.base_neck_left_dofs.pressure_constraint.findData('value').value = str(bnl_val)
	# self.base_neck_right_dofs.pressure_constraint.findData('value').value = str(bnr_val)
	# self.base_skull_left_dofs.pressure_constraint.findData('value').value = str(bsl_val)
	# self.base_skull_right_dofs.pressure_constraint.findData('value').value = str(bsr_val)

	# work directly with dome dofs
	# self.base_neck_left_dofs.dh_dofs.position = bnl_val.tolist()
	# self.base_neck_right_dofs.dh_dofs.position = bnr_val.tolist()
	# self.base_skull_left_dofs.dh_dofs.position = bsl_val.tolist()
	# self.base_skull_right_dofs.dh_dofs.position = bsr_val.tolist()
	# print(len(self.patient_dofs.rest_position), 'self.patient_dofs.rest_position')

	# if self.is_inflated:
	# 	# first move along z
	# 	test1 = moveRestPos(self.patient_dofs.rest_position, pose)
	# 	self.patient_dofs.findData('rest_position').value = test1
	# 	# cavity_pose = np.linalg.norm(self.base_neck_right_dofs.cav_dofs.position, axis=0)
	# 	# bnl_cav_dofs = self.base_neck_left_dofs.cav_dofs.position
	# # 	bnl_val = self.base_neck_left_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	# # 	bnr_val = self.base_neck_right_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	# 	bsl_val = self.base_skull_left_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	# 	bsr_val = self.base_skull_right_dofs.pressure_constraint.findData('value').value[0][0] + self.growth_rate
	# 	# try not using cavity
	# 	# bnl_val = np.array(self.base_neck_left_dofs.dh_dofs.position) + self.growth_rate
	# 	# bnr_val = np.array(self.base_neck_right_dofs.dh_dofs.position) + self.growth_rate
	# 	# bsl_val = np.array(self.base_skull_left_dofs.dh_dofs.position) + self.growth_rate
	# 	# bsr_val = np.array(self.base_skull_right_dofs.dh_dofs.position) + self.growth_rate
	#
	# 	logger.info('inflating base IABs to {} at time {}'.format(bnl_val, self.deltaTime))
	#

	# logger.debug('bnl pressure cons: {}\n'.format(self.base_neck_left_dofs.pressure_constraint.findData('value').value))
	# logger.debug('bnl cav position: {}\n'.format(np.linalg.norm(bnl_cav_dofs, axis=0)))
	# self.update_head_pose()

	# plt.ion()
	# plt.show()

	return 0;
