import unittest
import maya.standalone as ms

ms.initialize(name='forge')
import maya.cmds as mc
import forge

setUp_count = 0
tearDown_count = 0


class TestBase(unittest.TestCase):
    def setUp(self):
        global setUp_count
        self.fixtures = []
        test_parent_grp = 'test_parent'
        test_grp = '%s|test_GRP' % test_parent_grp

        self.test_group = test_grp if mc.objExists(test_grp) else forge.registry.maya_group(n='test', em=True)
        self.test_group_parent = test_parent_grp if mc.objExists(test_parent_grp) else forge.registry.maya_group(n='test_parent')

        self.fixtures.append(self.test_group)
        self.fixtures.append(self.test_group_parent)
        setUp_count += 1

    def tearDown(self):
        global tearDown_count
        if self.fixtures:
            self.fixtures = [fixture for fixture in self.fixtures if mc.objExists(fixture)]
            for fixture in self.fixtures:
                if mc.objExists(fixture):
                    for fix in mc.ls(fixture):
                        mc.delete(fix)
        tearDown_count += 1


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
