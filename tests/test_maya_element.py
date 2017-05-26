from base_test import TestBase
import maya.standalone as ms
import maya.cmds as mc
import forge

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
        universal = forge.registry.Universal.create(side='left')
        nodes = list(universal.yield_nodes)
        del universal
        self.assertFalse(all([mc.objExists(node) for node in nodes]))
