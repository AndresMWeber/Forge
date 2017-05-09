import unittest
import maya.standalone as ms

ms.initialize(name='forge')
import maya.cmds as mc
import forge

setUp_count = 0
tearDown_count = 0


class TestBase(unittest.TestCase):
    def setUp(self):
        print('Initializing maya_utils standalone...')

        global setUp_count
        print 'setup has run %d times.' % setUp_count
        print 'current state of scene: '
        print(mc.ls(type='transform'))

        self.fixtures = []
        test_parent_grp = 'test_parent'
        test_grp = '%s|test_GRP' % test_parent_grp

        self.test_group = test_grp if mc.objExists(test_grp) else forge.registry.maya_group(n='test', em=True)
        self.test_group_parent = test_parent_grp if mc.objExists(test_parent_grp) else forge.registry.maya_group(
            n='test_parent')

        self.fixtures.append(self.test_group)
        self.fixtures.append(self.test_group_parent)
        print 'current state of scene after creation: '
        print(mc.ls(type='transform'))
        print self.fixtures
        setUp_count += 1

    def tearDown(self):
        global tearDown_count
        print 'tearing down!!'
        if self.fixtures:
            self.fixtures = [fixture for fixture in self.fixtures if mc.objExists(fixture)]
            for fixture in self.fixtures:
                if mc.objExists(fixture):
                    for fix in mc.ls(fixture):
                        mc.delete(fix)
        tearDown_count += 1


class TestTransformRename(TestBase):
    def test_encapsulation(self):
        transform = forge.registry.MayaTransform(self.test_group)
        transform.rename(name='blame', side='right')
        self.assertTrue(transform.name_short, 'r_blame_GRP')
        self.fixtures.append(transform.name_long)

    def test_creation(self):
        transform = forge.registry.MayaTransform.create(name='name', side='left')
        transform.rename(name='blame')
        self.assertIn('l_blame_GRP', transform.name_short)
        self.fixtures.append(transform.name_long)


class TestTransformDelete(TestBase):
    def test_encapsulation(self):
        transform = forge.registry.MayaTransform('test')
        transform.rename(name='blame', side='right')
        self.assertTrue(transform.exists)
        transform.delete()
        self.assertFalse(mc.objExists(transform.node))
        self.fixtures.append(transform.name_long)

    def test_creation(self):
        transform = forge.registry.MayaTransform.create(name='name', side='left')
        transform.rename(name='blame')
        transform.delete()
        self.assertFalse(mc.objExists(transform.node))
        self.fixtures.append(transform.name_long)


class TestTransformProperties(TestBase):
    def setUp(self):
        super(TestTransformProperties, self).setUp()
        self.transform = forge.registry.MayaTransform(self.test_group, name=str(self.test_group))
        self.transform_par = forge.registry.MayaTransform(self.test_group_parent, name=str(self.test_group_parent))

        self.fixtures.append(self.transform.name_long)
        self.fixtures.append(self.transform_par.name_long)

    def reset_positions(self):
        mc.xform(self.transform.node, ws=True, t=[0.0] * 3)
        mc.xform(self.transform_par.node, ws=True, t=[0.0] * 3)

    def test_t_ws(self):
        self.reset_positions()
        self.assertEquals(self.transform.t_ws, [0.0] * 3)

    def test_r_ws(self):
        self.reset_positions()
        self.assertEquals(self.transform.r_ws, [0.0] * 3)

    def test_r(self):
        self.reset_positions()
        self.assertEquals(self.transform.r, [0.0] * 3)

    def test_t(self):
        self.reset_positions()
        self.assertEquals(self.transform.t, [0.0] * 3)

    def test_t_ws_parent_moved(self):
        self.reset_positions()
        mc.xform(self.transform_par.name_long, ws=True, t=[10.0, 0, 0])
        self.assertEquals(self.transform.t_ws, [10.0, 0, 0])

    def test_r_ws_parent_moved(self):
        self.reset_positions()
        mc.xform(self.transform_par.name_long, ws=True, ro=[10.0, 0, 0])
        self.assertEquals(self.transform.r_ws, [10.0, 0, 0])

    def test_r_parent_moved(self):
        self.reset_positions()
        mc.xform(self.transform_par.name_long, ws=True, ro=[10.0, 0, 0])
        self.assertEquals(self.transform.r, [0.0] * 3)

    def test_t_parent_moved(self):
        self.reset_positions()
        self.assertEquals(self.transform.t, [0.0] * 3)

    def test_name_long(self):
        self.assertEquals(self.transform.name_long, '|test_parent|test')

    def test_name_long_duplicate_name(self):
        mc.duplicate(self.test_group_parent)
        self.fixtures.append(self.test_group_parent + '1')
        self.assertEquals(self.transform.name_long, '|test_parent|test')

    def test_exists_true(self):
        self.assertTrue(self.transform.exists)

    def test_exists_false(self):
        self.transform.delete()
        self.assertFalse(self.transform.exists)
