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
        forge.LOG.info('Initializing a node with node_dag %r and kwargs %s' % (node_dag, kwargs))
        self.nom = nomenclate.Nom()
        self.validate_node(node_dag)
        self._dag_path = node_dag

    @staticmethod
    def create_engine_instance(*args, **kwargs):
        return str()

    @classmethod
    def factory(cls, node_dag='', **kwargs):
        forge.LOG.debug('Node.factory running with dag node reference: (type: %s), %r' % (type(node_dag), node_dag))
        if isinstance(node_dag, dict):
            forge.LOG.debug('detected serialzation, deserializing and instancing with args %s' % node_dag)
            kwargs.update(node_dag)
            return cls(**kwargs)
        elif issubclass(type(node_dag), cls):
            forge.LOG.debug('Detected subclass of %s...using this' % cls.__name__)
            return node_dag
        else:
            forge.LOG.debug('We are going with %r' % node_dag)
            return cls(node_dag, **kwargs)

    @classmethod
    def create(cls, *args, **kwargs):
        node = cls.create_engine_instance(*args, **kwargs)
        node_instance = cls(node, **kwargs)
        node_instance.rename(**kwargs)
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
        return self.dag_path

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

    def serialize(self):
        return {self.__class__.__name__: {'node_dag': self.node}}

    @classmethod
    def from_serial(cls, serialization):
        """ Only supports one node from the serialization...might have to refactor.  It has a for loop just to 
            enumerate for now.
        
        :param serialization: {str: dict}, dictionary 
        :return: AbstractNode
        """
        for class_id, class_kwargs in iteritems(serialization):
            forge.LOG.info('Reading data from serialization: %s: %s\nto instantiate node of type %s' %
                           (class_id, class_kwargs, cls.__name__))
            for k, v in iteritems(class_kwargs):
                if isinstance(v, dict) and forge.registry.get_class_by_id(k):
                    forge.LOG.info('Detected nested serialization, rebuilding node...')
                    class_kwargs[k] = forge.registry.get_class_by_id(k).from_serial(v)

            return forge.registry.get_class_by_id(class_id).factory(**class_kwargs)

    def __resolve_serializations(self, serialization):

        fields_found = []

        for key, value in iteritems(search_dict):
            if isinstance(value, dict):
                if forge.registry.get_class_by_id(value):
                    serialization[key] = forge.registry.get_class_by_id(key).from_serial(value)

                serialization[key] = self.__resolve_serializations(value)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        more_results = self.__resolve_serializations(item, field)
                        for another_result in more_results:
                            fields_found.append(another_result)

        return fields_found
