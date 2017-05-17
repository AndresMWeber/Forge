import unittest
import maya.standalone as ms
import maya.cmds as mc
import forge
from pprint import pformat

ms.initialize(name='forge')

setUp_count = 0
tearDown_count = 0


class TestBase(unittest.TestCase):
    def setUp(self):
        print('Initializing maya_utils standalone...')

        global setUp_count
        forge.LOG.info('setup has run %d times.' % setUp_count)
        forge.LOG.info('setUp-Start state of scene: ')
        forge.LOG.info(pformat(forge.registry.utils.scene.get_scene_tree()))

        self.fixtures = []
        test_parent_grp = 'test_parent'
        test_grp = '%s|test_GRP' % test_parent_grp

        self.test_group = test_grp if mc.objExists(test_grp) else forge.registry.maya_group(n='test', em=True)
        self.test_group_parent = test_parent_grp if mc.objExists(test_parent_grp) else forge.registry.maya_group(
            n='test_parent')

        self.fixtures.append(self.test_group)
        self.fixtures.append(self.test_group_parent)
        forge.LOG.info('state of scene after initial node creation: ')
        forge.LOG.info(pformat(forge.registry.utils.scene.get_scene_tree()))
        forge.LOG.info('Registered nodes %s' % self.fixtures)
        setUp_count += 1

    def tearDown(self):
        global tearDown_count
        forge.LOG.info('Tearing down!! Deleting all nodes...')
        if self.fixtures:
            self.fixtures = [fixture for fixture in self.fixtures if mc.objExists(fixture)]
            for fixture in self.fixtures:
                if mc.objExists(fixture):
                    for fix in mc.ls(fixture):
                        mc.delete(fix)
        tearDown_count += 1
        #mc.quit()
        #ms.uninitialize()
