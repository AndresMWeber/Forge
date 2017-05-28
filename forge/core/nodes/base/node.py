import nomenclate
import forge
from six import iteritems

utils = forge.registry.utils


@forge.register_node
class AbstractNode(object):
    INTERNAL_TYPE = 'node'
    ENGINE_TYPE = None
    NAME_DEFAULTS = {'name': 'untitled'}
    _char_hierarchy = '|'
    _char_namespace = ':'
    _char_attr = '.'

    def __init__(self, node_dag='', **kwargs):
        forge.LOG.debug('Initializing a node <%s> with node_dag %r and kwargs %s' % (self.__class__.__name__,
                                                                                     node_dag,
                                                                                     kwargs))
        self.nom = nomenclate.Nom()
        self.validate_node(node_dag)
        self._dag_path = node_dag

    @staticmethod
    def create_engine_instance(*args, **kwargs):
        return str()

    @classmethod
    def factory(cls, node_dag='', **kwargs):
        forge.LOG.debug('<%s>.factory running with dag node reference: %r' % (cls.__name__, node_dag))
        if isinstance(node_dag, dict):
            forge.LOG.debug('\t\tDetected serialzation, deserializing and instancing with args %s' % node_dag)
            kwargs.update(node_dag)
            return cls.from_serial(kwargs)

        elif issubclass(type(node_dag), cls):
            forge.LOG.debug('\t\tDetected subclass of %s...using input: %r' % (cls.__name__, node_dag))
            return node_dag

        else:
            forge.LOG.debug(
                '\t\tNo subclass or serialization, <%s>.__init__ as normal with %r' % (cls.__name__, node_dag))
            return cls(node_dag, **kwargs)

    @classmethod
    def create(cls, *args, **kwargs):
        forge.LOG.debug('Creating a node <%s> and kwargs %s' % (cls.__name__, kwargs))
        node = cls.create_engine_instance(*args, **kwargs)
        node_instance = cls(node, **kwargs)
        node_instance.rename(**kwargs)
        forge.LOG.debug('Created node <%s> with dag path: %s' % (node_instance.__class__.__name__,
                                                                node_instance._dag_path))

        return node_instance

    @property
    def node(self):
        return str(self._dag_path).decode('utf-8')

    def rename(self, **kwargs):
        nom_defaults = self.NAME_DEFAULTS.copy()
        nom_defaults.update(kwargs)
        self.nom.merge_dict(nom_defaults)
        self.nom.type = self.INTERNAL_TYPE
        forge.LOG.debug('Renaming node \"%s\" with state:\n\t%s' % (self.node, self.nom.state))
        orig_name = self.node
        new_name = self.nom.get()
        forge.registry.utils.scene.rename(self._dag_path, new_name)

        if new_name != self.name_short:
            forge.LOG.debug("Could not rename %s -> %s -> %s due to clash" % (orig_name, new_name, self.name_short))

        forge.LOG.debug('Renamed %s -> %s' % (orig_name, self.name_short))
        return self.name_short

    def attr_exists(self, attr):
        return forge.registry.utils.scene.exists(self.get_attr_dag(attr))

    def get_attr_dag(self, attr=''):
        return '{NODE}{SEP}{ATTR}'.format(NODE=self.node, SEP=self._char_attr, ATTR=attr)

    def add_attr(self, node, value, **kwargs):
        raise NotImplementedError

    def set_attr(self, attr, value):
        raise NotImplementedError

    def lock_channels(self, channels):
        raise NotImplementedError

    def set_color(self, nomenclate_object=None, level=0):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def insert_parent(self, replacement_parent):
        raise NotImplementedError

    def parent(self, target_parent, **kwargs):
        raise NotImplementedError

    def get_parent(self, level=1):
        raise NotImplementedError

    def get_children(self, type='transform'):
        raise NotImplementedError

    def strip_namespace(self, name):
        return name.split(self._char_namespace)[-1]

    def name(self, short=True, remove_namespace=True):
        result_name = self.name_short if short else self.name_long
        result_name = self.strip_namespace(result_name) if remove_namespace else result_name
        return result_name

    @property
    def name_short(self):
        return self.node.split(self._char_hierarchy)[-1]

    @property
    def name_long(self):
        return self._dag_path

    @property
    def exists(self):
        return forge.registry.utils.scene.exists(self.node)

    def delete(self):
        forge.registry.utils.scene.safe_delete(self.node)

    @staticmethod
    def validate_node(node_name):
        raise NotImplementedError

    @staticmethod
    def flatten_compound_channels(xform, channels):
        raise NotImplementedError

    def __repr__(self):
        if hasattr(self, '__str__'):
            return '<%s @ 0x%x (%s)>' % (self.__class__.__name__, id(self), str(self))
        else:
            return '<%s @ 0x%x>' % (self.__class__.__name__, id(self))

    def __str__(self):
        return self._dag_path

    def __getattr__(self, item):
        try:
            return super(AbstractNode, self).__getattribute__('nom').__getattr__(item)
        except AttributeError:
            return super(AbstractNode, self).__getattribute__(item)

    def __setattr__(self, key, value):
        try:
            hasattr(self, '_dag_path')
            utils.attr.set_attr(self.get_attr_dag(key), value)
            forge.LOG.debug('Detected existing attribute from engine: %s.%s = %s' % (self.node, key, value))
        except (AttributeError, RuntimeError):
            forge.LOG.debug('Attribute %s = %s' % (key, value))
            super(AbstractNode, self).__setattr__(key, value)

    def __eq__(self, other):
        try:
            return self.node == other.node
        except AttributeError:
            return self.node == str(other)

    @staticmethod
    def imprint_serialization(instance, target_node=None, serialization=None, tag_attr=forge.settings.DEFAULT_TAG_ATTR):
        """
        :param instance: forge.registry.node - instance that inherits node or has forge attr/serialization functionality
        :param target_node: (forge.registry.MayaTransform) - Target maya node to add/set the attribute
        :param serialization: (str) - default is a serialized string to recreate the node, override to custom tag
        :param tag_attr: (str) - The name for the tag attribute (default='forge')
        :return: (None)
        """
        if target_node is None:
            target_node = instance.group_top
            print("default use %s" % target_node)
        serialized_data = instance.serialize() if serialization is None else serialization
        target_node.add_attr(tag_attr, serialized_data, dt='string')
        forge.LOG.info('%r --> Imprinted serialization to node.attr %s.%s=%s' % (instance,
                                                                                 target_node,
                                                                                 tag_attr,
                                                                                 serialized_data))
        return target_node.get_attr(tag_attr)

    def serialize(self):
        return {self.__class__.__name__: {'node_dag': self.node}}

    @classmethod
    def from_serial(cls, serialization, _depth=0):
        """ Resolves entries in a dict that represent class serializations
        
        :param serialization: {str: dict}, dictionary 
        :param _depth: int, depth marker, for internal use only 
        :return: dict
        """
        if _depth == 0: forge.LOG.debug('Initial serial before resolution: %s' % serialization)
        forge.LOG.debug('%sfrom_serial: working with dictionary %s ' % ('\t' * _depth, serialization))
        _depth += 1

        for k, v in iteritems(serialization):
            forge.LOG.debug('%sRunning through k=%s, v=%s' % ('\t' * _depth, k, v))
            if isinstance(v, dict):
                serialization[k] = cls.from_serial(v, _depth=_depth)
            class_resolution = forge.registry.get_class_by_id(k)
            if class_resolution:
                forge.LOG.debug('%s-----> Found class <%s> serialization, resolving...' % ('\t' * (_depth + 1),
                                                                                          class_resolution.__name__))
                serialization = class_resolution(**v)
        if _depth == 1: forge.LOG.info('Final serial resolution: %r' % serialization)
        return serialization
