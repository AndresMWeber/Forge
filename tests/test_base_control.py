from .base_test import TestBase
import maya.standalone as ms
import forge
import forge.core.nodes.abstract as base

# forge\core\nodes\abstract\control.py
# 28-44, 60-83, 91-98, 101-104, 107-114, 117, 129-131, 134-139

ms.initialize(name='forge')


class TestBaseControl(TestBase):
    def setUp(self):
        self.original_mode = forge.registry.mode
        forge.registry.swap_mode(forge.settings.BASE)
        super(TestBaseControl, self).setUp()

    def tearDown(self):
        forge.registry.swap_mode(self.original_mode)
        super(TestBaseControl, self).setUp()

    @staticmethod
    def encapsulation_node_creation():
        return {'node_dag': forge.registry.utils.create.curve(),
                'control_offset_grp': forge.registry.utils.create.group(),
                'control_con_grp': forge.registry.utils.create.group()
                }


class TestControlInit(TestBaseControl):
    def test_no_other_nodes(self):
        nodes = self.encapsulation_node_creation()
        nodes.pop('control_offset_grp')
        nodes.pop('control_con_grp')
        control = forge.registry.AbstractControl(rename=True,
                                                   name='blame',
                                                   side='left',
                                                   **nodes)

        self.assertEquals(control.name_short, 'curve')
        self.assertIsNone(control.group_offset)
        self.assertIsNone(control.group_connection)

        self.fixtures.append(control.name_long)

    def test_offset_group(self):
        nodes = self.encapsulation_node_creation()
        nodes.pop('control_con_grp')

        control = forge.registry.AbstractControl(rename=True,
                                                   name='blame',
                                                   side='left',
                                                   **nodes)

        self.assertEquals(control.name_short, 'curve')
        self.assertEquals(control.group_offset.name_short, 'group')
        self.assertIsNone(control.group_connection)

        self.fixtures.append(control.name_long)

    def test_conn_group(self):
        nodes = self.encapsulation_node_creation()
        nodes.pop('control_offset_grp')

        control = forge.registry.AbstractControl(rename=True,
                                                   name='blame',
                                                   side='left',
                                                   **nodes)

        self.assertEquals(control.name_short, 'curve')
        self.assertIsNone(control.group_offset)
        self.assertEquals(control.group_connection.name_short, 'group')

        self.fixtures.append(control.name_long)

    def test_all_nodes(self):
        control = forge.registry.AbstractControl(**self.encapsulation_node_creation())

        self.assertEquals(control.name_short, 'curve')
        self.assertEquals(control.group_offset.name_short, 'group')
        self.assertEquals(control.group_connection.name_short, 'group')

        self.fixtures.append(control.name_long)


class TestControlCreate(TestBaseControl):
    def test_kwargs_shape(self):
        control = forge.registry.AbstractControl.create(rename=True,
                                                          name='blame',
                                                          side='left',
                                                          shape='arrow_directional')

        self.assertEquals(control.name_short, '')
        self.assertEquals(control.group_offset.name_short, '')
        self.assertEquals(control.group_connection.name_short, '')

        self.fixtures.append(control.name_long)

    def test_kwargs_scale(self):
        control = forge.registry.AbstractControl.create(rename=True,
                                                          name='blame',
                                                          side='left',
                                                          scale=4.0)

        self.assertEquals(control.scale, 4.0)
        self.fixtures.append(control.name_long)

    def test_kwargs_parent(self):
        control_a = forge.registry.AbstractControl.create(rename=True,
                                                            name='blame',
                                                            side='left')

        self.assertTrue(forge.registry.AbstractControl.create(rename=True, name='blame', side='left', parent=control_a))
        self.fixtures.append(control_a.name_long)