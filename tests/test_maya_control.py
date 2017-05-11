from .base_test import TestBase
import maya.standalone as ms
import maya.cmds as mc
import forge

ms.initialize(name='forge')


class TestControlRename(TestBase):
    def test_encapsulation(self):
        crv = mc.curve(p=((0, 0, 0), (0, 1, 0), (1, 0, 0), (0, 0, 1)))
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
        controlA = forge.registry.control.create(side='right', name='bert', purpose='killer', childtype='meth')
        controlB = forge.registry.control.create(side='right', name='bert', purpose='killer', childtype='meth')

        self.assertTrue(controlA.name_short, 'r_blame_CTR')
        self.assertTrue(controlB.name_short, 'r_blame_CTR')

        self.assertEquals(controlA.group_offset.name_short, 'r_bert_meth_killer_OGP')
        self.assertEquals(controlB.group_offset.name_short, 'r_bert_meth_killer_OGP1')

        self.fixtures.append(controlA.name_long)
        self.fixtures.append(controlB.name_long)
