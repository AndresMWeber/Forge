from .base_test import TestBase
import maya.standalone as ms
import maya.cmds as mc
import forge

ms.initialize(name='forge')


class TestElementRename(TestBase):
    def test_encapsulation(self):
        element = forge.registry.MayaElement(forge.registry.maya_group(),
                                             forge.registry.maya_group(),
                                             forge.registry.maya_group(),
                                             forge.registry.maya_group(),
                                             forge.registry.maya_group(),
                                             forge.registry.maya_group())
        element.rename(name='blame', side='right')
        self.assertTrue(element.group_top.name_short, 'r_blame_GRP')
        self.fixtures.extend([node.node for node in element.hierarchy if hasattr(node, 'node')])

    def test_creation(self):
        element = forge.registry.MayaElement.create(name='name', side='left')
        self.assertEquals(element.group_top.name_short, 'l_name_GRP')
        element.rename(name='blame')
        self.assertEquals(element.group_top.name_short, 'l_blame_GRP')
        print(element.hierarchy)


class TestElementDel(TestBase):
    @forge.log_function_call
    def test_delete(self):
        universal = forge.registry.Universal.create(side='left')
        nodes = list(universal.yield_nodes)
        del universal
        self.assertFalse(all([mc.objExists(node) for node in nodes]))
