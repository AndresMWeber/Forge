import forge
from forge.core.nodes.maya.curve import MayaCurve
from forge.core.channels import (VISIBILITY, LEVEL_PRIMARY, SCALE)


@forge.register_node
class MayaControl(MayaCurve):
    """
    class for building templates control
    """
    TYPE = 'control'

    def __init__(self, node_dag='', control_offset_grp='', control_con_grp='', scale=1.0, rename=False, **kwargs):
        """
        Encapsulates a given maya_utils transform with templates control functionality.
        :param node_dag: str, maya_utils transform for control
        :param control_offset_grp: str, maya_utils transform for parent offset group
        :param control_con_grp: str, maya_utils transform for child connection group
        :param scale: float, value for scale of control
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: MayaControl
        """
        forge.LOG.debug('initialized with kwargs %s %s %s' % (node_dag, control_offset_grp, control_con_grp))
        super(MayaControl, self).__init__(node_dag=node_dag, **kwargs)

        self.group_offset = None
        self.group_connection = None
        self.scale = float(scale)  # Ensuring we cast back to float in case it was serialized

        if control_offset_grp:
            self.group_offset = forge.registry.transform.factory(control_offset_grp)
            self.group_offset.TYPE = 'offset_group'

        if control_con_grp:
            self.group_connection = forge.registry.transform.factory(control_con_grp)
            self.group_connection.TYPE = 'connection_group'

        if rename:
            self.rename(**kwargs)

        if scale != 1.0:
            self.scale_shapes(scale)

    @classmethod
    def create(cls, shape='cube', scale=1.0, lock_channelbox=None, parent='', **kwargs):
        """
        Creates a MayaControl object with given name
        :param shape: str, given shape from list in rig_lib.core.nodes.maya_utils.factory.MayaControlShapeFactory
        :param scale: float, scale of control to create
        :param lock_channelbox: list(str), list of maya_utils attributes to lock and hide from the maya_utils channelbox
        :param parent: str, possible parent for the control
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: MayaControl
        """
        forge.LOG.debug('Creating a control with parent %r' % parent)

        node_dag = super(MayaControl, cls).create(**kwargs)

        connection_group = cls.create_engine_instance()
        offset_group = cls.create_engine_instance()

        lock_channelbox = [SCALE, VISIBILITY] if lock_channelbox is None else lock_channelbox

        control_instance = cls(node_dag=node_dag.node,
                               control_con_grp=connection_group,
                               control_offset_grp=offset_group,
                               scale=scale,
                               **kwargs)

        control_instance.parent(control_instance.group_offset, offset_group=False)
        control_instance.group_connection.parent(control_instance)
        control_instance.parent(parent)

        control_instance.swap_shape(shape=shape)
        control_instance.lock_channels(lock_channelbox)
        control_instance.scale_shapes(scale)

        control_instance.set_color(level=kwargs.get('level', LEVEL_PRIMARY))
        control_instance.rename(**kwargs)

        forge.LOG.debug('Control that was created is named %s' % control_instance.node)
        return control_instance

    def rename(self, **kwargs):
        """
        Renames the Control transform, connection group and offset groups with the given nomenclate kwargs 
        :param kwargs: dict, any possible extra naming kwargs for renaming this node as defined in env.yml in nomenclate
        :return: None
        """
        forge.LOG.debug('Renaming this control with kwargs %s' % str(kwargs))
        forge.LOG.debug('Renaming control %s->%s' % (self.node, self.nom.get(**kwargs)))
        super(MayaControl, self).rename(**kwargs)

        if self.group_connection:
            forge.LOG.debug('Renaming control connection group %s->%s' %
                            (self.group_connection.node, self.group_connection.nom.get(**kwargs)))
            self.group_connection.rename(**kwargs)

        if self.group_offset:
            forge.LOG.debug('Renaming control offset group %s->%s' %
                            (self.group_offset.node, self.group_offset.nom.get(**kwargs)))
            self.group_offset.rename(**kwargs)

    def get_parent(self, level=0):
        if self.group_offset:
            return self.group_offset.get_parent()
        else:
            return super(MayaControl, self).get_parent()

    def parent(self, target_parent, **kwargs):
        offset_group = kwargs.get('offset_group', True)
        target_parent = target_parent.group_connection if isinstance(target_parent, self.__class__) else target_parent

        if offset_group:
            self.group_offset.parent(target_parent=target_parent)
            forge.LOG.debug('Parenting control offset group to %r' % target_parent)
        else:
            super(MayaControl, self).parent(target_parent=target_parent)
            forge.LOG.debug('Parenting control transform to %r' % target_parent)

    def serialize(self):
        return {'node_dag': super(MayaControl, self).serialize()['node_dag'],
                'control_offset_grp': self.group_offset.serialize(),
                'control_con_grp': self.group_connection.serialize(),
                'scale': self.scale}

    @classmethod
    def factory(cls, maya_transform='', control_offset_grp='', control_con_grp='', **kwargs):
        if isinstance(maya_transform, dict):
            forge.LOG.debug('detected serialzation, deserializing and instancing with args %s' % maya_transform)
            maya_transform.update(kwargs)
            return cls(**maya_transform)

        elif issubclass(type(maya_transform), cls):
            forge.LOG.debug('Detected subclass of %s...using this' % cls.__name__)
            return maya_transform

        else:
            forge.LOG.debug('We are going with %r' % maya_transform)
            return cls(maya_transform,
                       control_offset_grp=control_offset_grp,
                       control_con_grp=control_con_grp,
                       **kwargs)
