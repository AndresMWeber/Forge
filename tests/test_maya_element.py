from base_test import TestBase
import maya.standalone as ms
import maya.cmds as mc
import forge
from pprint import pformat
import json

ms.initialize(name='forge')


class TestBaseElement(TestBase):
    @staticmethod
    def encapsulation_node_creation():
        return {'group_top': forge.registry.maya_group(),
                'group_model': forge.registry.maya_group(),
                'group_joint': forge.registry.maya_group(),
                'group_controls': forge.registry.maya_group(),
                'group_nodes': forge.registry.maya_group(),
                'group_world': forge.registry.maya_group()
                }


class TestElementRename(TestBaseElement):
    def test_encapsulation(self):
        element = forge.registry.Element(**self.encapsulation_node_creation())
        element.rename(name='blame', side='right')
        self.assertTrue(element.group_top.name_short, 'r_blame_GRP')
        self.fixtures.extend([node.node for node in element.hierarchy if hasattr(node, 'node')])

    def test_creation(self):
        element = forge.registry.Element.create(name='name', side='left')
        self.assertEquals(element.group_top.name_short, 'l_name_GRP')
        element.rename(name='blame')
        self.assertEquals(element.group_top.name_short, 'l_blame_GRP')
        print(element.hierarchy)


class TestElementDel(TestBaseElement):
    @forge.log_function_call
    def test_delete(self):
        element = forge.registry.Element.create(side='left')
        nodes = list(element.yield_nodes)
        del element
        self.assertFalse(all([mc.objExists(node) for node in nodes]))


class TestElementSerialize(TestBaseElement):
    @forge.log_function_call
    def test_creation_serialization(self):
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        element = forge.registry.Element.create(side='left')
        element.imprint_serialization()
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        self.assertEquals(self.deep_sort(element.group_top.get_attr(forge.settings.DEFAULT_TAG_ATTR)),
                          self.deep_sort(json.loads(json.dumps(element.serialize()))))

    @forge.log_function_call
    def test_creation_serialization_encapsulation(self):
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        element = forge.registry.Element(**self.encapsulation_node_creation())
        element.imprint_serialization()
        element_other = forge.registry.Element.factory(element.group_top.get_attr(forge.settings.DEFAULT_TAG_ATTR))
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        self.assertEquals(element, element_other)


class TestElementFromSerial(TestBaseElement):
    def test_encapsulation(self):
        element = forge.registry.Element(**self.encapsulation_node_creation())
        element.rename(name='blame', side='right', childtype='fucker')
        self.assertEquals(forge.registry.Element.from_serial(element.serialize()), element)

    def test_creation(self):
        element = forge.registry.Element.create(name='name', side='left', childtype='fucker')
        self.assertEquals(forge.registry.Element.from_serial(element.serialize()), element)
