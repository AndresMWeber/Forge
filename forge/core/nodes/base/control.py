import forge
from .curve import AbstractCurve
from forge.core.channels import (VISIBILITY, LEVEL_PRIMARY, SCALE)


@forge.register_node
class AbstractControl(AbstractCurve):
    """
    class for building templates control
    """
    INTERNAL_TYPE = 'control'

    def __init__(self, node_dag='', control_offset_grp='', control_con_grp='', scale=1.0, rename=False, **kwargs):
        """
        Encapsulates a given transform with templates control functionality.
        :param maya_transform: str, transform for control
        :param control_offset_grp: str, transform for parent offset group
        :param control_con_grp: str, transform for child connection group
        :param scale: float, value for scale of control
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        """
        forge.LOG.debug('initialized with kwargs %s %s %s' % (node_dag, control_offset_grp, control_con_grp))
        super(AbstractControl, self).__init__(node_dag=node_dag, **kwargs)

        self.group_offset = None
        self.group_connection = None
        self.scale = float(scale)  # Ensuring we cast back to float in case it was serialized

        if control_offset_grp:
            self.group_offset = forge.registry.transform.factory(control_offset_grp)
            self.group_offset.INTERNAL_TYPE = 'offset_group'

        if control_con_grp:
            self.group_connection = forge.registry.transform.factory(control_con_grp)
            self.group_connection.INTERNAL_TYPE = 'connection_group'

        if rename:
            self.rename(**kwargs)

        if scale != 1.0:
            self.scale_shapes(scale)

    @classmethod
    def create(cls, shape='cube', scale=1.0, lock_channelbox=None, parent='', **kwargs):
        """
        Creates a Control object with given name
        :param name: str, starting main name of the control
        :param shape: str, given shape from list in rig_lib.core.nodes.maya_utils.factory.MayaControlShapeFactory
        :param scale: float, scale of control to create
        :param lock_channelbox: list(str), list of attributes to lock and hide
        :param parent: str, possible parent transform for the control
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: Control
        """
        forge.LOG.info('Creating a control with parent %r, kwargs %s' % (parent, kwargs))

        control = super(AbstractControl, cls).create(shape)
        offset = forge.registry.transform.create()
        connection = forge.registry.transform.create()

        control.parent(offset)
        connection.parent(control)
        offset.parent(parent)

        control_instance = cls(node_dag=control.node,
                               control_offset_grp=offset,
                               control_con_grp=connection,
                               scale=scale,
                               **kwargs)

        control_instance.rename(**kwargs)
        control_instance.set_color(level=kwargs.get('level', LEVEL_PRIMARY))
        control_instance.swap_shape(shape=shape)

        lock_channelbox = [SCALE, VISIBILITY] if lock_channelbox is None else lock_channelbox
        flattened_channels = control_instance.flatten_compound_channels(control_instance.node, lock_channelbox)
        control_instance.lock_channels(flattened_channels)
        control_instance.scale_shapes(scale)

        forge.LOG.debug('Control that was created is named %s' % control_instance.node)
        return control_instance

    def rename(self, **kwargs):
        """
        Renames the Control transform, connection group and offset groups with the given nomenclate kwargs 
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: None
        """
        forge.LOG.debug('Renaming this control with kwargs %s' % str(kwargs))
        self.nom.merge_dict(kwargs)
        super(AbstractControl, self).rename(**self.nom.state)

        if self.group_connection:
            self.group_connection.rename(**self.nom.state)

        if self.group_offset:
            self.group_offset.rename(**self.nom.state)

        self.nom.type = self.INTERNAL_TYPE

    def get_parent(self, level=0):
        if self.group_offset:
            return self.group_offset.get_parent()
        else:
            return super(AbstractControl, self).get_parent()

    def parent(self, target_parent, use_offset_group=True, **kwargs):
        target_parent = target_parent.group_connection if isinstance(target_parent, self.__class__) else target_parent

        if use_offset_group and self.group_offset:
            self.group_offset.parent(target_parent=target_parent)
            forge.LOG.debug('Parenting control offset group to %r' % target_parent)
        else:
            super(AbstractControl, self).parent(target_parent=target_parent)
            forge.LOG.debug('Parenting control transform to %r' % target_parent)

    def scale_shapes(self, scale_value):
        raise NotImplementedError

    def swap_shape(self, shape='cube', maintain_offset=True, add=False):
        raise NotImplementedError

    @classmethod
    def factory(cls, node_dag='', control_offset_grp='', control_con_grp='', **kwargs):
        if isinstance(node_dag, dict):
            forge.LOG.debug('control.factory: serialzation input, deserializing and instancing with args %s' % node_dag)
            node_dag.update(kwargs)
            return cls(**node_dag)

        elif issubclass(type(node_dag), cls):
            forge.LOG.debug('control.factory: input is subclass of %s using...' % cls.__name__)
            return node_dag

        else:
            forge.LOG.debug('control.factory: normal usage %r' % node_dag)
            return cls(node_dag=node_dag,
                       control_offset_grp=control_offset_grp,
                       control_con_grp=control_con_grp,
                       **kwargs)

    def serialize(self):
        return {self.class_rep(): {'node_dag': super(AbstractControl, self).serialize(),
                                   'control_offset_grp': self.group_offset.serialize(),
                                   'control_con_grp': self.group_connection.serialize(),
                                   'scale': self.scale}}
