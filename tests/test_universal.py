from base_test import TestBase
import maya.standalone as ms
import maya.cmds as mc
import forge
import json
from pprint import pformat

ms.initialize(name='forge')


class TestUniversalRename(TestBase):
    @forge.log_function_call
    def test_encapsulation(self):
        nodes = {'group_top': forge.registry.maya_group(),
                 'group_model': forge.registry.maya_group(),
                 'group_joint': forge.registry.maya_group(),
                 'group_controls': forge.registry.maya_group(),
                 'group_nodes': forge.registry.maya_group(),
                 'group_world': forge.registry.maya_group(),
                 'control_global_A': forge.registry.maya_curve(p=[(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)]),
                 'control_global_B': forge.registry.maya_curve(p=[(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)]),
                 }

        universal = forge.registry.Universal(**nodes)
        universal.rename(name='blame', side='right')
        self.assertTrue(universal.group_top.name_short, 'r_blame_GRP')
        self.fixtures.extend([node.node for node in universal.flat_hierarchy])

    @forge.log_function_call
    def test_creation(self):
        universal = forge.registry.Universal.create(name='base', side='left')
        self.assertEquals(universal.group_top.name_short, 'l_base_GRP')
        universal.rename(name='blame')
        self.assertEquals(universal.group_top.name_short, 'l_blame_GRP')
        self.fixtures.extend([node.node for node in universal.flat_hierarchy])

    @forge.log_function_call
    def test_creation_hierarchy(self):
        universal = forge.registry.Universal.create(side='left')

        self.assertIsNone(universal.group_top.get_parent())

        self.assertTrue(universal.group_model.get_parent() == universal.group_top)
        self.assertTrue(universal.group_nodes.get_parent() == universal.group_top)
        self.assertTrue(universal.group_joint.get_parent() == universal.group_top)
        self.assertTrue(universal.group_world.get_parent() == universal.group_top)
        self.assertTrue(universal.group_controls.get_parent() == universal.group_top)

        self.assertTrue(universal.control_global_A.get_parent() == universal.group_controls)
        self.assertTrue(universal.control_global_B.get_parent() == universal.control_global_A.group_connection)

        self.assertTrue(universal.group_top.get_children() == [universal.group_model,
                                                               universal.group_joint,
                                                               universal.group_nodes,
                                                               universal.group_world,
                                                               universal.group_controls])

    @forge.log_function_call
    def test_creation_serialization(self):
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        universal = forge.registry.Universal.create(side='left')
        universal.imprint_serialization()
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        self.assertEquals(universal.group_top.get_attr('forge'), json.loads(json.dumps(universal.serialize())))

    @forge.log_function_call
    def test_creation_serialization_encapsulation(self):
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        universal = forge.registry.Universal.create(side='left')
        universal.imprint_serialization()
        universal_other = forge.registry.Universal.factory(universal.group_top.get_attr('forge'))
        forge.LOG.info('\n%s' % pformat(forge.registry.utils.scene.get_scene_tree()))
        self.assertEquals(universal, universal_other)

    @forge.log_function_call
    def test_delete(self):
        universal = forge.registry.Universal.create(side='left')
        nodes = list(universal.yield_nodes)
        del universal
        self.assertFalse(all([mc.objExists(node) for node in nodes]))
