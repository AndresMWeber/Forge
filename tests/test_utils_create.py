from .base_test import TestBase
import maya.cmds as mc
import forge.core.core_utils.maya_utils.create as maya
import forge.core.core_utils.abstract_utils.create as abstract


class TestBaseAugment(TestBase):
    pass


class TestCreateJoint(TestBaseAugment):
    """
        def joint(*args, **kwargs):
    """

    def test_maya_creation(self):
        self.assertTrue(mc.objExists(maya.joint()))

    def test_abstract_creation(self):
        self.assertEquals(abstract.joint(), "joint")


class TestCreateGroup(TestBaseAugment):
    """
        def group(em=True, *args, **kwargs):
    """

    def test_maya_creation(self):
        self.assertTrue(mc.objExists(maya.group()))

    def test_abstract_creation(self):
        self.assertEquals(abstract.group(), "group")


class TestCreateCurve(TestBaseAugment):
    """
        def curve(**kwargs):
    """

    def test_maya_creation(self):
        self.assertTrue(mc.objExists(maya.curve()))

    def test_abstract_creation(self):
        self.assertEquals(abstract.curve(), "curve")


class TestCreateLocator(TestBaseAugment):
    """
        def locator(*args, **kwargs):
    """

    def test_maya_creation(self):
        self.assertTrue(mc.objExists(maya.locator()[0]))

    def test_abstract_creation(self):
        self.assertEquals(abstract.locator(), "locator")


class TestCreateSemiCircle(TestBaseAugment):
    """
        def semi_circle(constructionHistory=True, *args, **kwargs):
    """

    def test_maya_creation(self):
        self.assertTrue(mc.objExists(maya.semi_circle()))

    def test_abstract_creation(self):
        self.assertEquals(abstract.semi_circle(), "semi_circle")


class TestCreateCircle(TestBaseAugment):
    """
        def circle(constructionHistory=True, *args, **kwargs):
    """

    def test_maya_creation(self):
        self.assertTrue(mc.objExists(maya.circle()))

    def test_abstract_creation(self):
        self.assertEquals(abstract.circle(), "circle")


class TestCreateMetaNode(TestBaseAugment):
    """
        def meta_node(*args, **kwargs):
    """

    def test_maya_creation(self):
        self.assertTrue(mc.objExists(maya.meta_node()))

    def test_abstract_creation(self):
        self.assertEquals(abstract.meta_node(), "meta_node")
