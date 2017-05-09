import unittest
import maya.standalone as ms
import forge
ms.initialize(name='forge')
import maya.cmds as mc

setUp_count = 0
tearDown_count = 0


class TestBase(unittest.TestCase):
    def setUp(self):
        print('Initializing maya_utils standalone...')

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


class TestControlRename(TestBase):
    def test_encapsulation(self):
        crv = mc.curve(p=((0,0,0), (0,1,0), (1,0,0), (0,0,1)))
        top = mc.group(em=True)
        conn = mc.group(em=True)

        control = forge.registry.MayaControl(crv, top, conn, rename=True, name='blame', side='left')

        self.assertEquals(control.name_short, 'l_blame_CTR')
        self.assertEquals(control.group_offset.name_short, 'l_blame_OGP')
        self.assertEquals(control.group_connection.name_short, 'l_blame_CGP')

        self.fixtures.append(control.name_long)

    def test_creation(self):
        control = forge.registry.control.create(name='blame', side='right')
        self.assertTrue(control.name_short, 'r_blame_CTR')
        self.assertEquals(control.group_offset.name_short, 'r_blame_OGP')
        self.assertEquals(control.group_connection.name_short, 'r_blame_CGP')

        self.fixtures.append(control.name_long)

    def test_double_creation(self):
        controlA = forge.registry.control.create(cls='right', name='bert', purpose='killer', childtype='meth')
        controlB = forge.registry.control.create(cls='right', name='bert', purpose='killer', childtype='meth')

        self.assertTrue(controlA.name_short, 'r_blame_CTR')
        self.assertTrue(controlB.name_short, 'r_blame_CTR')

        self.assertEquals(controlA.group_offset.name_short, 'r_bert_meth_killer_OGP')
        self.assertEquals(controlB.group_offset.name_short, 'r_bert_meth_killer_OGP1')

        self.fixtures.append(controlA.name_long)
        self.fixtures.append(controlB.name_long)
