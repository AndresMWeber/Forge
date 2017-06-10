from .base_test import TestBase
import maya.cmds as mc
import forge.core.core_utils.maya_utils.attr as maya_attr
import forge.core.core_utils.abstract_utils.attr as abstract_attr


class TestBaseAugment(TestBase):
    def create_test_maya_nodes(self):
        grp_a = mc.group(em=True)
        grp_b = mc.group(em=True)
        return [grp_a, grp_b]

    def create_test_maya_node(self):
        return mc.group(em=True)

    def create_test_abstract_nodes(self):
        return ['node_a', 'node_b']

    def create_test_abstract_node(self):
        return "node_a"


class TestConnectAttr(TestBaseAugment):
    """ def connect_attr(attr_source, attr_destination, **kwargs):
            return mc.connectAttr(attr_source, attr_destination, **kwargs)
    """
    def test_maya_valid_node(self):
        grp_a, grp_b = self.create_test_maya_nodes()
        maya_attr.connect_attr(grp_a + '.translateX', grp_b + '.translateX', )

    def test_maya_invalid_node(self):
        grp_a, grp_b = self.create_test_maya_nodes()
        self.assertRaises(RuntimeError, maya_attr.connect_attr, grp_a + '.manslateX', grp_b + '.translateX')

    def test_abstract_valid_node(self):
        grp_a, grp_b = self.create_test_abstract_nodes()
        abstract_attr.connect_attr(grp_a + '.translateX', grp_b + '.translateX', )

    def test_abstract_invalid_node(self):
        grp_a, grp_b = self.create_test_abstract_nodes()
        abstract_attr.connect_attr(grp_a + '.manslateX', grp_b + '.translateX')


class TestSetAttr(TestBaseAugment):
    """ def set_attr(node_attr_dag, *args, **kwargs):
            return mc.setAttr(node_attr_dag, *args, **kwargs)
    """
    def test_maya_valid_node(self):
        grp_a = self.create_test_maya_node()
        maya_attr.set_attr(grp_a + '.translateX', 3)

    def test_maya_invalid_node(self):
        grp_a = self.create_test_maya_node()
        self.assertRaises(RuntimeError, maya_attr.set_attr, grp_a + '.manslateX', 5)

    def test_abstract_valid_node(self):
        grp_a = self.create_test_abstract_node()
        abstract_attr.set_attr(grp_a + '.translateX', 3)

    def test_abstract_invalid_node(self):
        grp_a = self.create_test_abstract_node()
        abstract_attr.set_attr(grp_a + '.manslateX', 5)


class TestGetAttr(TestBaseAugment):
    """ def get_attr(node_attr_dag, *args, **kwargs):
            return mc.getAttr(node_attr_dag, *args, **kwargs)
    """
    def test_maya_valid_node(self):
        grp_a = self.create_test_maya_node()
        maya_attr.get_attr(grp_a + '.translateX')

    def test_maya_invalid_node(self):
        grp_a = self.create_test_maya_node()
        self.assertRaises(ValueError, maya_attr.get_attr, grp_a + '.manslateX')

    def test_abstract_valid_node(self):
        grp_a = self.create_test_abstract_node()
        abstract_attr.get_attr(grp_a + '.translateX')

    def test_abstract_invalid_node(self):
        grp_a = self.create_test_abstract_node()
        abstract_attr.get_attr(grp_a + '.manslateX')


class TestAddAttr(TestBaseAugment):
    """ def add_attr(node, **kwargs):
            return mc.addAttr(node, **kwargs)
    """
    def test_maya_valid_node(self):
        grp_a = self.create_test_maya_node()
        maya_attr.add_attr(grp_a, longName='fabulous')

    def test_maya_invalid_node(self):
        self.assertRaises(ValueError, maya_attr.add_attr, 'blah', longName='manslateX')

    def test_abstract_valid_node(self):
        grp_a = self.create_test_abstract_node()
        abstract_attr.add_attr(grp_a, longName='fabulous')

    def test_abstract_invalid_node(self):
        abstract_attr.add_attr('blah', longName='manslateX')
