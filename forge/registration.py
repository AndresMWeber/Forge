import forge
import yaml
import os
from .exception import ValidationError


class Registry(object):
    node_constructors = []
    registered_shapes = {}
    required_nodes = ['Node', 'Transform', 'Curve', 'Control', 'Joint']
    utils = None

    @classmethod
    def add(cls, other):
        if other not in cls.node_constructors:
            forge.LOG.debug('Successfully added Node %s to registry' % other.__name__)
            cls.node_constructors.append(other)

    def swap_mode(self, mode):
        forge.LOG.info('Converting registry to mode: %s' % mode)
        self.mode = mode
        self.set_default_utils()
        self.set_default_shapes()
        self.set_default_nodes()

    @classmethod
    def register_node(cls, node):
        forge.LOG.debug('Attempting to add Node %s to registry' % node.__name__)
        cls.add(node)
        return node

    def set_default_nodes(self):
        try:
            forge.LOG.info('Registering nodes for mode: %s' % self.mode)
            for required_node in self.required_nodes:
                setattr(self, required_node, getattr(forge.registry, self.mode.title() + required_node))
                forge.LOG.info('\t\tRegistered node as forge.registry.%s' % required_node)
            forge.LOG.info('\tSuccessfully registered all required nodes')
        except ValidationError:
            forge.LOG.error('\tCould not register nodes; not all required nodes were registered.' % self.mode)

    def set_default_utils(self):
        try:
            forge.LOG.info('Registering utils for mode: %s' % self.mode)
            self.utils = getattr(forge.core.core_utils, '%s_utils' % self.mode)
            forge.LOG.info('\tSuccessfully registered as forge.registry.utils with sub-modules %s' %
                           [func for func in dir(self.utils) if not func.startswith('__')])
        except ValidationError:
            forge.LOG.error('\tCould not register utils.' % self.mode)

    def set_default_shapes(self):
        forge.LOG.info('Registering shapes:')
        self.registered_shapes = self.get_shapes_config()
        forge.LOG.info('\tSuccessfully registered shapes %s' % list(self.registered_shapes))
        self.shape_constructors = list(self.registered_shapes)

    @staticmethod
    def get_shapes_config():
        stream = open(os.path.join(os.path.dirname(__file__), "shapes.yml"), "r")
        return yaml.load(stream)

    @classmethod
    def __iter__(cls):
        return iter(cls.node_constructors)

    def get_class_by_id(self, class_id):
        try:
            return getattr(self, class_id)
        except AttributeError:
            return None

    def __getattr__(self, item):
        # See whether it's a node constructor
        for node_constructor in self.node_constructors:
            if node_constructor.__name__ == item:
                return node_constructor

        # See if it's a registered shape
        shape_dict = self.registered_shapes.get(item, {}).copy()
        if shape_dict:
            func = getattr(self.utils.create, shape_dict.pop('constructor'))
            return func(**shape_dict)

        # Otherwise Default
        self.__getattribute__(item)

    def __dir__(self):
        node_constructors = [node.__name__ for node in self.node_constructors]
        registered_shapes = list(self.registered_shapes)
        return dir(type(self)) + list(self.__dict__) + node_constructors + registered_shapes
