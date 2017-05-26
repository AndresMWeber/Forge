import forge
import forge.settings as settings
import string

utils = forge.registry.utils

@forge.register_node
class TwistInterpolators(forge.registry.Element):
    def __init__(self,
                 joints='',
                 scale=1.0,
                 **kwargs):
        super(TwistInterpolators, self).__init__(**kwargs)
        self.joints = [forge.registration.control.factory(joint) for joint_pair in joints for joint in joint_pair]
        print 'deserialized joints ', self.joints
        self.register_nodes(self.joints, node_type=settings.JOINT_TYPE)

    def setup_connections(self):
        super(self.__class__, self).setup_connections()
        for joint in self.joints:
            print 'parenting joint ', joint
            joint.parent(self.group_joints)

    def rename(self, **kwargs):
        super(self.__class__, self).rename(**kwargs)
        self.nom.merge_dict(kwargs)
        for index, joint_pair in enumerate(self.joints):
            self.nom.childtype = 'TwistInterpolators' + string.ascii_uppercase[index]
            self.nom.var = 'A'
            joint_pair[0].rename(**self.nom.state)
            self.nom.var = 'B'
            joint_pair[1].rename(**self.nom.state)

    @classmethod
    def _create_hierarchy(cls, **kwargs):
        return super(TwistInterpolators, cls)._create_hierarchy()

    @classmethod
    def _create_joints(cls, source_joints, **kwargs):
        joints = super(TwistInterpolators, cls)._create_joints()
        print 'creating jointsttststs'
        joints['twist_joint_chains'] = []

        if source_joints:
            for parent_joint in source_joints:
                parent_joint = forge.registration.joint.factory(parent_joint)
                parent_joint_first_child = forge.registration.joint.factory(parent_joint.get_children(type='joint')[0])
                twist_parent_joint = forge.registration.joint.factory(utils.scene.duplicate(parent_joint,
                                                                                            po=True))
                twist_child_joint = forge.registration.joint.factory(utils.scene.duplicate(parent_joint_first_child,
                                                                                           po=True))

                for twist_joint in [twist_parent_joint, twist_child_joint]:
                    twist_joint.color(color_index=1)
                    twist_joint.radius = parent_joint.radius

        return joints

    @classmethod
    def create(cls, source_joints=None, *args, **kwargs):
        super(TwistInterpolators, cls).create(source_joints=source_joints, *args, **kwargs)

    @classmethod
    def _create_controls(cls, scale=3.0, **kwargs):
        serialized = super(TwistInterpolators, cls)._create_controls()
        return serialized

    def _layout_guide_cleanup(self):
        raise NotImplementedError

    def _layout_guide_joints(self):
        raise NotImplementedError

    def _layout_guide_connections(self):
        raise NotImplementedError

    def _layout_guide_controls(self):
        raise NotImplementedError

    def __eq__(self, other):
        base_eq = super(TwistInterpolators, self).__eq__(other)
        return all([base_eq] + [getattr(self, group) == getattr(other, group) for group in self.control])
