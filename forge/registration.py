import forge
import yaml
import os
from .exception import ValidationError
from .settings import MODE


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

    @classmethod
    def register_node(cls, node):
        forge.LOG.debug('Attempting to add Node %s to registry' % node.__name__)
        cls.add(node)
        return node

    def set_default_nodes(self):
        try:
            forge.LOG.info('Registering nodes for mode: %s' % MODE)
            for required_node in self.required_nodes:
                setattr(self, required_node, getattr(forge.registry, MODE.title() + required_node))
                forge.LOG.info('Registered node as forge.registry.%s' % required_node.lower())
            forge.LOG.info('Successfully registered all required nodes')
        except ValidationError:
            forge.LOG.error('Could not register nodes; not all required nodes were registered.' % MODE)

    def set_default_utils(self):
        try:
            forge.LOG.info('Registering utils for mode: %s' % MODE)
            self.utils = getattr(forge.core.core_utils, '%s_utils' % MODE)
            forge.LOG.info('Successfully registered as forge.registry.utils')
        except ValidationError:
            forge.LOG.error('Could not register utils.' % MODE)

    @staticmethod
    def get_shapes_config():
        stream = open(os.path.join(os.path.dirname(__file__), "shapes.yml"), "r")
        return yaml.load(stream)

    def set_default_shapes(self, mode=MODE):
        self.registered_shapes = self.get_shapes_config()
        self.shape_constructors = list(self.registered_shapes)

    def get_class_by_id(self, class_id):
        try:
            return getattr(self, class_id)
        except AttributeError:
            return None

    @classmethod
    def __iter__(cls):
        return iter(cls.node_constructors)

    def __getattr__(self, item):
        # See whether it's a node constructor
        for node_constructor in self.node_constructors:
            if node_constructor.__name__ == item:
                return node_constructor
        # See if it's a registered shape
        shape_dict = self.registered_shapes.get(item, {}).copy()
        print('Querying registry for shape %s with shape dict: %s' % (item, shape_dict))
        if shape_dict:
            func = getattr(self.utils.create, shape_dict.pop('constructor'))
            print('Construction function found and located in registry %s' % (func))
            return func(**shape_dict)

        # Otherwise Default
        self.__getattribute__(item)

    def __dir__(self):
        return dir(type(self)) + list(self.__dict__) + [node.__name__ for node in self.node_constructors]
