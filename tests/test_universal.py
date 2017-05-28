from base_test import TestBase
import maya.standalone as ms
import maya.cmds as mc
import forge
import json
from pprint import pformat

ms.initialize(name='forge')


class TestBaseUniversal(TestBase):
    @staticmethod
    def encapsulation_node_creation():
        return {'group_top': forge.registry.maya_group(),
                'group_model': forge.registry.maya_group(),
                'group_joint': forge.registry.maya_group(),
                'group_controls': forge.registry.maya_group(),
                'group_nodes': forge.registry.maya_group(),
                'group_world': forge.registry.maya_group(),
                'control_global_a': forge.registry.maya_curve(p=[(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)]),
                'control_global_b': forge.registry.maya_curve(p=[(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)]),
                }


class TestUniversalCreation(TestBaseUniversal):
    @forge.log_function_call
    def test_encapsulation(self):
        universal = forge.registry.Universal(**self.encapsulation_node_creation())
        universal.rename(name='blame', side='right')
        self.assertTrue(universal.group_top.name_short, 'r_blame_GRP')
        self.fixtures.extend([node.node for node in universal.flat_hierarchy])

    @forge.log_function_call
    def test_creation(self):
        universal = forge.registry.Universal.create(name='base', side='left', purpose='grail')
        self.assertEquals(universal.group_top.name_short, 'l_base_grail_GRP')
        universal.rename(name='blame')
        self.assertEquals(universal.group_top.name_short, 'l_blame_grail_GRP')
        self.fixtures.extend([node.node for node in universal.flat_hierarchy])

    @forge.log_function_call
    def test_creation_check_hierarchy(self):
        universal = forge.registry.Universal.create(side='left')

        self.assertIsNone(universal.group_top.get_parent())

        self.assertTrue(universal.group_model.get_parent() == universal.group_top)
        self.assertTrue(universal.group_nodes.get_parent() == universal.group_top)
        self.assertTrue(universal.group_joint.get_parent() == universal.group_top)
        self.assertTrue(universal.group_world.get_parent() == universal.group_top)
        self.assertTrue(universal.group_controls.get_parent() == universal.group_top)

        self.assertTrue(universal.control_global_a.get_parent() == universal.group_controls)
        self.assertTrue(universal.control_global_b.get_parent() == universal.control_global_a.group_connection)

        self.assertTrue(universal.group_top.get_children() == [universal.group_model,
                                                               universal.group_joint,
                                                               universal.group_nodes,
                                                               universal.group_world,
                                                               universal.group_controls])


class TestUniversalSerialize(TestBaseUniversal):
    @forge.log_function_call
    def test_creation_serialization(self):
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        universal = forge.registry.Universal.create(side='left')
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))

        print(universal.group_top.metaforge)
        print(self.deep_sort(universal.group_top.get_attr(forge.settings.DEFAULT_TAG_ATTR)))
        print(self.deep_sort(json.loads(json.dumps(universal.serialize()))))
        self.assertEquals(self.deep_sort(universal.group_top.get_attr(forge.settings.DEFAULT_TAG_ATTR)),
                          self.deep_sort(json.loads(json.dumps(universal.serialize()))))

    @forge.log_function_call
    def test_creation_serialization_encapsulation(self):
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        universal = forge.registry.Universal(**self.encapsulation_node_creation())
        universal.imprint_serialization()
        universal_other = forge.registry.Universal.factory(universal.group_top.get_attr(forge.settings.DEFAULT_TAG_ATTR))
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        self.assertEquals(universal, universal_other)


class TestUniversalFromSerial(TestBaseUniversal):
    def test_encapsulation(self):
        universal = forge.registry.Universal(**self.encapsulation_node_creation())
        universal.rename(name='blame', side='right', childtype='fucker')
        self.assertEquals(forge.registry.Universal.from_serial(universal.serialize()), universal)

    def test_creation(self):
        universal = forge.registry.Universal.create(name='name', side='left', childtype='fucker')
        self.assertEquals(forge.registry.Universal.from_serial(universal.serialize()), universal)


class TestUniversalRename(TestBaseUniversal):
    def test_encapsulation(self):
        universal = forge.registry.Universal(**self.encapsulation_node_creation())
        universal.rename(name='john')
        self.assertEquals('john_GRP', universal.group_top)

    def test_creation(self):
        universal = forge.registry.Universal.create(name='name', side='left', childtype='fucker')
        universal.rename(name='john')
        self.assertEquals('l_john_fucker_GRP', universal.group_top)


class TestUniversalDelete(TestBaseUniversal):
    @forge.log_function_call
    def test_creation(self):
        universal = forge.registry.Universal(**self.encapsulation_node_creation())
        nodes = list(universal.yield_nodes)
        del universal
        self.assertFalse(all([mc.objExists(node) for node in nodes]))

    @forge.log_function_call
    def test_encapsulation(self):
        universal = forge.registry.Universal.create(side='left')
        nodes = list(universal.yield_nodes)
        del universal
        self.assertFalse(all([mc.objExists(node) for node in nodes]))
