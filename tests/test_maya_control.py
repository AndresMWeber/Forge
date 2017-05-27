from base_test import TestBase
import maya.standalone as ms
import maya.cmds as mc
import forge

ms.initialize(name='forge')


class TestBaseControl(TestBase):
    @staticmethod
    def encapsulation_node_creation():
        return {'node_dag': forge.registry.maya_curve(),
                'control_offset_grp': forge.registry.maya_group(),
                'control_con_grp': forge.registry.maya_group()
                }


class TestControlRename(TestBaseControl):
    def test_encapsulation(self):
        control = forge.registry.control(rename=True,
                                             name='blame',
                                             side='left',
                                             **self.encapsulation_node_creation())

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
        control_a = forge.registry.control.create(side='right', name='bert', purpose='killer', childtype='meth')
        control_b = forge.registry.control.create(side='right', name='bert', purpose='killer', childtype='meth')

        self.assertTrue(control_a.name_short, 'r_blame_CTR')
        self.assertTrue(control_b.name_short, 'r_blame_CTR')

        self.assertEquals(control_a.group_offset.name_short, 'r_bert_meth_killer_OGP')
        self.assertEquals(control_b.group_offset.name_short, 'r_bert_meth_killer_OGP1')

        self.fixtures.append(control_a.name_long)
        self.fixtures.append(control_b.name_long)


class TestControlSerialize(TestBaseControl):
    def test_encapsulation(self):
        self.maxDiff = 900
        control = forge.registry.control(**self.encapsulation_node_creation())
        control.rename(name='blame', side='right')
        self.assertEquals(control.serialize(),
                          {'MayaControl': {'node_dag': 'r_blame_CTR',
                                           'control_offset_grp': {'MayaTransform': {'node_dag': u'r_blame_OGP'}},
                                           'control_con_grp': {'MayaTransform': {'node_dag': u'r_blame_CGP'}},
                                           'scale': 1.0}
                           })

    def test_creation(self):
        self.maxDiff = 900
        control = forge.registry.control.create(name='name', side='left')
        control.rename(name='blame')
        self.assertEquals(control.serialize(),
                          {'MayaControl': {'node_dag': 'l_blame_CTR',
                                           'control_offset_grp': {'MayaTransform': {'node_dag': u'l_blame_OGP'}},
                                           'control_con_grp': {'MayaTransform': {'node_dag': u'l_blame_CGP'}},
                                           'scale': 1.0}
                           })


class TestControlFromSerial(TestBaseControl):
    def test_encapsulation(self):
        control = forge.registry.control(**self.encapsulation_node_creation())
        control.rename(name='blame', side='right', childtype='fucker')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)

    def test_creation(self):
        control = forge.registry.control.create(name='name', side='left', childtype='fucker')
        control.rename(name='blame')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)
