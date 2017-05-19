from six import iteritems
from pprint import pformat
import forge
import forge.settings as settings
import nomenclate



@forge.register_node
class AbstractElement(object):
    LAYOUT_GUIDE_JOINTS = {}
    VISIBILITY_TYPES = [settings.MODEL_TYPE, settings.JOINT_TYPE, settings.CONTROL_TYPE]
    ENUM_DISPLAY_TYPE = 'normal:template:reference'
    ENUM_VISIBILITY = 'on:off'
    REGISTER_TYPES = [settings.CONTROL_TYPE,
                      settings.JOINT_TYPE,
                      settings.HIERARCHY_TYPE,
                      settings.METADATA_TYPE]
    SERIALIZABLE = []

    def __init__(self,
                 group_top='',
                 group_model='',
                 group_joint='',
                 group_controls='',
                 group_nodes='',
                 group_world='',
                 parent='',
                 scale=1.0,
                 **kwargs):
        for register_type in self.REGISTER_TYPES:
            setattr(self, register_type, list())
        self.nom = nomenclate.Nom(**kwargs)

        self.group_top = forge.registry.transform.factory(group_top)
        self.group_model = forge.registry.transform.factory(group_model)
        self.group_joint = forge.registry.transform.factory(group_joint)
        self.group_controls = forge.registry.transform.factory(group_controls)
        self.group_nodes = forge.registry.transform.factory(group_nodes)
        self.group_world = forge.registry.transform.factory(group_world)
        self.scale = scale

        self.register_nodes(['group_top', 'group_model', 'group_joint', 'group_nodes', 'group_world', 'group_controls'],
                            node_type=forge.settings.HIERARCHY_TYPE)
        self.register_nodes(['scale'], node_type=forge.settings.METADATA_TYPE)

        self.parent(parent)
        self.imprint_serialization()

    @classmethod
    def create(cls, **kwargs):
        forge.LOG.info('Creating AbstractElement, kwargs %s' % (pformat(kwargs, depth=1)))
        forge.LOG.info('Creating hierarchy...')
        kwargs.update(cls._create_hierarchy(**kwargs))
        forge.LOG.info('Creating joints...')
        kwargs.update(cls._create_joints(**kwargs))
        forge.LOG.info('Creating controls...')
        kwargs.update(cls._create_controls(**kwargs))

        element_instance = cls(**kwargs)
        forge.LOG.info('Setting up connections...')
        element_instance.setup_connections()
        forge.LOG.info('Renaming all child nodes...')
        element_instance.rename()

        forge.LOG.info('Finished creating AbstractElement %s' % pformat(element_instance.serialize()))
        return element_instance

    @property
    def yield_nodes(self):
        def yield_nodes_from_serialization(d):
            for k, v in iteritems(d):
                if isinstance(v, dict):
                    for item in yield_nodes_from_serialization(v):
                        yield item
                elif isinstance(v, (str, unicode)) and forge.registry.utils.scene.exists(v):
                    yield v
        return yield_nodes_from_serialization(self.serialize())

    @property
    def flat_hierarchy(self):
        return [self.__getattribute__(node) for node in self.hierarchy]

    def register_nodes(self, nodes, node_type=None):
        forge.LOG.debug('Registering attributes to %s of type %s: %s' % (self, node_type, str(nodes)))
        if node_type in self.REGISTER_TYPES:
            for node in nodes:
                self.__getattribute__(node_type).append(node)
        else:
            forge.LOG.warning('Node type specified %s not in registered types %s' % (node_type, self.REGISTER_TYPES))

    def parent(self, parent_target):
        self.group_top.parent(parent_target)

    def setup_connections(self):
        self.group_world.set_attr('inheritsTransform', 0)
        self.add_visibility_attrs(self.group_top)
        for group, vis_type in zip([self.group_model, self.group_joint, self.group_controls], self.VISIBILITY_TYPES):
            self.connect_visibility_toggles([group], vis_type)
            self.connect_display_type_toggles([group], vis_type)

    def add_visibility_attrs(self, transform):
        for vis_type in self.VISIBILITY_TYPES:
            display_attr = '{TYPE}_display'.format(TYPE=vis_type)
            visibility_attr = '{TYPE}_visibility'.format(TYPE=vis_type)
            transform.add_attr(display_attr, 0, at='enum', enumName=self.ENUM_DISPLAY_TYPE, k=True)
            transform.add_attr(visibility_attr, 0, at='enum', enumName=self.ENUM_VISIBILITY, k=True)

    def connect_visibility_toggles(self, transforms, target_type='model'):
        forge.LOG.debug('Connecting visibility toggles for MayaElement...')
        for transform in transforms:
            source_attr = self.group_top.get_attr_dag(attr='{TYPE}_visibility'.format(TYPE=target_type))
            target_attr = transform.get_attr_dag(attr='visibility')
            forge.LOG.debug('\tConnecting vis attribute %s -> %s' % (source_attr, target_attr))
            forge.registry.utils.attr.connect_attr(source_attr, target_attr)

    def connect_display_type_toggles(self, transforms, target_type='model'):
        for transform in transforms:
            forge.registry.utils.attr.connect_attr(self.group_top.get_attr_dag(attr='{TYPE}_display'.format(TYPE=target_type)),
                                                   transform.get_attr_dag(attr='overrideDisplayType'))
            transform.set_attr('overrideEnabled', 1)


    @classmethod
    def _create_hierarchy(cls, **kwargs):
        group_top = forge.registry.transform.create()
        group_model = forge.registry.transform.create(parent=group_top)
        group_joint = forge.registry.transform.create(parent=group_top)
        group_nodes = forge.registry.transform.create(parent=group_top)
        group_world = forge.registry.transform.create(parent=group_top)
        group_controls = forge.registry.transform.create(parent=group_top)

        return {'group_top': group_top,
                'group_model': group_model,
                'group_joint': group_joint,
                'group_nodes': group_nodes,
                'group_world': group_world,
                'group_controls': group_controls,
                }

    @classmethod
    def _create_joints(cls, **kwargs):
        return {}

    @classmethod
    def _create_controls(cls, **kwargs):
        return {}

    def layout(self):
        self._layout_guide()

    def _layout_guide(self):
        self._layout_guide_joints()
        self._layout_guide_controls()
        self._layout_guide_connections()
        self._layout_guide_cleanup()

    def _layout_guide_cleanup(self):
        raise NotImplementedError

    def _layout_guide_joints(self):
        raise NotImplementedError

    def _layout_guide_connections(self):
        raise NotImplementedError

    def _layout_guide_controls(self):
        raise NotImplementedError

    def class_rep(self):
        return str(self.__class__).split("'")[1]

    def rename(self, **kwargs):
        original_childtype = self.nom.childtype.label

        self.nom.merge_dict(kwargs)
        self.nom.type = 'group'
        self.group_top.rename(**self.nom.state)
        self.nom.childtype = 'model'
        self.group_model.rename(**self.nom.state)
        self.nom.childtype = 'joint'
        self.group_joint.rename(**self.nom.state)
        self.nom.childtype = 'nodes'
        self.group_nodes.rename(**self.nom.state)
        self.nom.childtype = 'world'
        self.group_world.rename(**self.nom.state)
        self.nom.childtype = 'controls'
        self.group_controls.rename(**self.nom.state)

        self.nom.childtype=original_childtype

    def imprint_serialization(self, target_node=None, serialization=None, tag_attr=forge.settings.DEFAULT_TAG_ATTR):
        """
        :param target_node: (forge.registry.MayaTransform) - Target maya node to add/set the attribute
        :param serialization: (str) - Serialized string representing the node's forge.settings to recreate
        :param tag_attr: (str) - The name for the tag attribute (default='forge')
        :return: (None)
        """
        if target_node is None:
            target_node = self.group_top
        serialized_data = self.serialize() if serialization is None else serialization
        target_node.add_attr(tag_attr, serialized_data, dt='string')
        return target_node.get_attr(tag_attr)

    def serialize(self):
        flattened_data = {}
        for k, v in iteritems({register_type: getattr(self, register_type) for register_type in self.REGISTER_TYPES}):
            if isinstance(v, list):
                for item in v:
                    try:
                        flattened_data[item] = getattr(self, item).serialize()
                    except AttributeError:
                        flattened_data[item] = str(getattr(self, item)).decode('utf-8')
            else:
                flattened_data[k] = v if type(v) in forge.settings.SERIALIZABLE_TYPES else str(v).decode("utf-8")

        return {self.class_rep(): flattened_data}

    @classmethod
    def factory(cls,
                group_top='',
                group_model='',
                group_joint='',
                group_controls='',
                group_nodes='',
                group_world='',
                *args,
                **kwargs):
        if isinstance(group_top, dict):
            kwargs.update(group_top)
            return cls(*args, **kwargs)
        elif issubclass(type(group_top), cls):
            return group_top
        else:
            return cls(group_top=group_top,
                       group_model=group_model,
                       group_joint=group_joint,
                       group_controls=group_controls,
                       group_nodes=group_nodes,
                       group_world=group_world,
                       *args,
                       **kwargs)

    def __del__(self):
        for node in self.yield_nodes:
            forge.LOG.debug('deleting sub node %s' % node)
            forge.registry.utils.scene.safe_delete(str(node))

    def __str__(self):
        return self.group_top.node

    def __eq__(self, other):
        return all([getattr(self, group) == getattr(other, group) for group in
                    self.hierarchy])
