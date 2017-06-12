from .base_test import TestBase
import maya.cmds as mc
import forge.core.core_utils.maya_utils.joint as utils_joint


class TestBaseUtilsMayaJoint(TestBase):
    def setUp(self):
        super(TestBaseUtilsMayaJoint, self).setUp()

    def tearDown(self):
        super(TestBaseUtilsMayaJoint, self).setUp()

    def create_joints_straight(self):
        joint_chain_straight = []

        joint_chain_straight.append(mc.joint(None))
        for y in range(1,10):
            joint_chain_straight.append(mc.joint(p=(0, y, 0)))

        self.fixtures.append(joint_chain_straight)
        return joint_chain_straight

    def create_joints_branching(self):
        joint_chain_branching = []

        joint_chain_branching.append(mc.joint(None, p=[1,0,0]))
        for y in range(1, 7):
            joint_chain_branching.append(mc.joint(p=(1, y, 0)))

        branch_y = mc.joint(joint_chain_branching[4], q=True, p=True)
        branch_y[0] = 2
        branch_y[1] += 1

        joint_chain_branching.append(mc.joint(joint_chain_branching[4], p=branch_y))
        for y in range(1,4):
            position = [sum(x) for x in zip(*[branch_y, [0,y,0]])]
            joint_chain_branching.append(mc.joint(p=position))

        self.fixtures.append(joint_chain_branching)

        return joint_chain_branching


class TestUtilsMayaListHierarchy(TestBaseUtilsMayaJoint):
    def test_straight(self):
        straight_chain = self.create_joints_straight()
        self.checkEqual(utils_joint.list_hierarchy(straight_chain[0]), straight_chain)
        self.checkEqual(utils_joint.list_hierarchy(straight_chain[0], withEndJoints=False), straight_chain[1:])

    def test_branching(self):
        branching_chain = self.create_joints_branching()
        self.checkEqual(utils_joint.list_hierarchy(branching_chain[0]), branching_chain)
        self.checkEqual(utils_joint.list_hierarchy(branching_chain[0], withEndJoints=False), branching_chain[1:])

    def test_invalid_input(self):
        mc.group(em=True)
        mc.group()
        group = mc.group()
        self.assertRaises(AttributeError, utils_joint.list_hierarchy, group)

    def test_missing_input(self):
        self.assertRaises(ValueError, utils_joint.list_hierarchy, 'not_me')


class TestUtilsMayaMakeJointsAlongCurve(TestBaseUtilsMayaJoint):
    pass


class TestUtilsMayaBuildFromPoints(TestBaseUtilsMayaJoint):
    pass


class TestUtilsMayaBuildBetweenPoints(TestBaseUtilsMayaJoint):
    pass


class TestUtilsMayaInsertBetweenPoints(TestBaseUtilsMayaJoint):
    pass
