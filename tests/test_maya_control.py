from base_test import TestBase
import maya.standalone as ms
import forge
import maya.cmds as mc

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
        control.rename(name='blame', side='right', purpose='holy')
        self.assertEquals(control.serialize(),
                          {'MayaControl': {'node_dag': control.name_short,
                                           'control_offset_grp': control.group_offset.serialize(),
                                           'control_con_grp': control.group_connection.serialize(),
                                           'scale': control.scale}
                           })

    def test_creation(self):
        self.maxDiff = 900
        control = forge.registry.control.create(name='name', side='left', purpose='grail')
        control.rename(name='blame')
        self.assertEquals(control.serialize(),
                          {'MayaControl': {'node_dag': control.name_short,
                                           'control_offset_grp': control.group_offset.serialize(),
                                           'control_con_grp': control.group_connection.serialize(),
                                           'scale': control.scale}
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


class TestControlParent(TestBaseControl):
    def test_encapsulation_after_setup_hierarchy(self):
        control = forge.registry.control(**self.encapsulation_node_creation())

        self.assertIsNone(mc.listRelatives(control.node, p=True))
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertIsNone(mc.listRelatives(control.group_connection, p=True))

        control.setup_hierarchy()

        self.assertEquals(mc.listRelatives(control.node, p=True),
                          [control.group_offset.name_short])
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertEquals(mc.listRelatives(control.group_connection, p=True),
                          [control.name_short])

    def test_encapsulation_after_parent(self):
        control = forge.registry.control(**self.encapsulation_node_creation())

        self.assertIsNone(mc.listRelatives(control.node, p=True))
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertIsNone(mc.listRelatives(control.group_connection, p=True))
        control.setup_hierarchy()

        self.assertEquals(mc.listRelatives(control.node, p=True),
                          [control.group_offset.name_short])
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertEquals(mc.listRelatives(control.group_connection, p=True),
                          [control.name_short])

    def test_encapsulation_after_parent_to_control(self):
        control = forge.registry.control.create(name='name', side='left', childtype='fucker')
        control.rename(name='blame')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)


class TestControlGetParent(TestBaseControl):
    def test_encapsulation(self):
        control = forge.registry.control(**self.encapsulation_node_creation())
        control.rename(name='default')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)

    def test_after_parent_to_group(self):
        control = forge.registry.control.create(name='default')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)

    def test_after_parent_to_control(self):
        control = forge.registry.control.create(name='default')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)


class TestControlFactory(TestBaseControl):
    def test_from_serial(self):
        control = forge.registry.control.factory(forge.registry.control.create().serialize())
        control.rename(name='blame', side='right', childtype='fucker')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)

    def test_from_subclass(self):
        control_a = forge.registry.control.create()
        control_b = forge.registry.control.factory(control_a)
        self.assertEquals(control_a, control_b)

    def test_from_non_subclass(self):
        control = forge.registry.transform.create()
        self.assertRaises(TypeError, forge.registry.control.factory, control)

    def test_from_encapsulation(self):
        control = forge.registry.control.factory(**self.encapsulation_node_creation())
        control.rename(name='blame')
        self.assertEquals(forge.registry.control.from_serial(control.serialize()),
                          control)


class TestControlCreate(TestBaseControl):
    def test_creation_no_kwargs(self):
        control = forge.registry.control.create()
        print(forge.registry.utils.scene.get_scene_tree())
        self.assertIsNone(control)

    def test_creation_scale(self):
        control = forge.registry.control.create(scale=4.0, name='name', side='left', childtype='fucker')
        self.assertEquals(control.scale, 4.0)

    def test_creation_parent(self):
        test_group = mc.group(em=True)
        control = forge.registry.control.create(parent=test_group, name='name', side='left', childtype='fucker')
        print(forge.registry.utils.scene.get_scene_tree())
        self.assertEquals(mc.listRelatives(control.group_offset, p=True)[0], test_group)

    def test_creation_parent_control(self):
        test_group = mc.group(em=True)
        control = forge.registry.control.create(parent=test_group, name='name', side='left', childtype='fucker')
        print(forge.registry.utils.scene.get_scene_tree())
        self.assertEquals(mc.listRelatives(control.group_offset, p=True)[0], test_group)

    def test_creation_shape(self):
        control = forge.registry.control.create(shape='arrow_directional', name='name', side='left', childtype='fucker')
        print(forge.registry.utils.scene.get_scene_tree())
        self.assertIsNone(len(mc.ls(control.node + '.cv[:]', fl=True)))


class TestControlSetupHierarchy(TestBaseControl):
    def test_encapsulation(self):
        control = forge.registry.control(**self.encapsulation_node_creation())

        self.assertIsNone(mc.listRelatives(control.node, p=True))
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertIsNone(mc.listRelatives(control.group_connection, p=True))
        control.setup_hierarchy()

        self.assertEquals(mc.listRelatives(control.node, p=True),
                          [control.group_offset.name_short])
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertEquals(mc.listRelatives(control.group_connection, p=True),
                          [control.name_short])

    def test_creation(self):
        control = forge.registry.control.create()

        self.assertEquals(mc.listRelatives(control.node, p=True),
                          [control.group_offset.name_short])
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertEquals(mc.listRelatives(control.group_connection, p=True),
                          [control.name_short])

        control.setup_hierarchy()

        self.assertEquals(mc.listRelatives(control.node, p=True),
                          [control.group_offset.name_short])
        self.assertIsNone(mc.listRelatives(control.group_offset, p=True))
        self.assertEquals(mc.listRelatives(control.group_connection, p=True),
                          [control.name_short])
