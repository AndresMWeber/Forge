import forge
import forge.settings as settings
from pprint import pformat

utils = forge.registry.utils


@forge.register_node
class Universal(forge.registry.Element):
    def __init__(self,
                 control_global_a='',
                 control_global_b='',
                 scale=1.0,
                 **kwargs):
        scale = float(scale)  # Ensuring we cast back to float in case it was serialized
        kwargs['name'] = kwargs.get('name', 'universal')
        super(Universal, self).__init__(**kwargs)
        forge.LOG.debug(
            'Initializing <%s>\ncontrol_global_a=%r\ncontrol_global_b=%r\nkwargs=%s' % (self.__class__.__name__,
                                                                                        control_global_a,
                                                                                        control_global_b,
                                                                                        pformat(kwargs)))

        self.control_global_a = forge.registry.control.factory(node_dag=control_global_a, scale=scale)
        self.control_global_b = forge.registry.control.factory(node_dag=control_global_b, scale=scale * .8)
        self.register_nodes(['control_global_a', 'control_global_b'], node_type=settings.CONTROL_TYPE)

    def setup_connections(self):
        super(self.__class__, self).setup_connections()
        self.control_global_a.parent(self.group_controls)

    def rename(self, **kwargs):
        super(self.__class__, self).rename(**kwargs)
        original_purpose = self.nom.purpose.label

        self.nom.merge_dict(kwargs)
        self.nom.purpose = 'universalA'
        self.control_global_a.rename(**self.nom.state)
        self.nom.purpose = 'universalB'
        self.control_global_b.rename(**self.nom.state)

        self.nom.purpose = original_purpose

    @classmethod
    def _create_hierarchy(cls, **kwargs):
        return super(Universal, cls)._create_hierarchy(**kwargs)

    @classmethod
    def _create_joints(cls, parent_joints=None, **kwargs):
        return super(Universal, cls)._create_joints(parent_joints=None, **kwargs)

    @classmethod
    def _create_controls(cls, scale=3.0, **kwargs):
        serialized = super(Universal, cls)._create_controls(scale=3.0, **kwargs)
        control_global_a = forge.registry.control.create(shape='circle', scale=scale)
        control_global_b = forge.registry.control.create(shape='circle',
                                                         scale=scale * 0.8,
                                                         parent=control_global_a.group_connection)
        control_global_a.rotate_shapes((90, 0, 0))
        control_global_b.rotate_shapes((90, 0, 0))
        serialized.update({'control_global_a': control_global_a.serialize(),
                           'control_global_b': control_global_b.serialize()})
        forge.LOG.debug('Updated serialization for <%s> with controls %s' % (cls.__name__, serialized))
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
        base_eq = super(Universal, self).__eq__(other)
        return all([base_eq] + [getattr(self, group) == getattr(other, group) for group in self.control])
