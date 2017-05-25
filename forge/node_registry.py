import maya.cmds as mc
from six import add_metaclass

import forge
from .exception import ValidationError
from .settings import MODE


class Registry(object):
    node_constructors = []
    required_nodes = ['Node', 'Transform', 'Curve', 'Control', 'Element', 'Joint']
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

    def set_default_nodes(self, mode=MODE):
        try:
            forge.LOG.info('Registering nodes for mode: %s' % mode)
            for required_node in self.required_nodes:
                setattr(self, required_node.lower(), getattr(forge.registry, MODE.title() + required_node))
                forge.LOG.info('Registered node as forge.registry.%s' % required_node.lower())
            forge.LOG.info('Successfully registered all required nodes')
        except ValidationError:
            forge.LOG.error('Could not register nodes; not all required nodes were registered.' % mode)

    def set_default_utils(self, mode=MODE):
        try:
            forge.LOG.info('Registering utils for mode: %s' % mode)
            self.utils = getattr(forge.core.core_utils, '%s_utils' % mode)
            forge.LOG.info('Successfully registered as forge.registry.utils')
        except ValidationError:
            forge.LOG.error('Could not register utils.' % mode)

    @staticmethod
    def maya_joint(*args, **kwargs):
        return mc.joint(*args, **kwargs)

    @staticmethod
    def maya_group(em=True, *args, **kwargs):
        return mc.group(em=em)

    @staticmethod
    def maya_curve(control_shape='cube', name='control', **kwargs):
        try:
            control = getattr(forge.shapes, control_shape)(**kwargs)
            control = mc.rename(control, name)
            return control
        except (RuntimeError, TypeError):
            return mc.curve(d=1, p=[(1, 0, 0), (0, 0, -1), (-1, 0, 0), (0, 0, 1), (1, 0, 0)])

    @staticmethod
    def maya_locator(*args, **kwargs):
        return mc.spaceLocator(*args, **kwargs)

    @staticmethod
    def maya_semi_circle(constructionHistory=True, *args, **kwargs):
        circle = mc.circle(constructionHistory=constructionHistory, *args, **kwargs)[0]
        median_cv = int(round(forge.registry.utils.curve.get_num_cvs(circle) / 2))
        mc.xform(forge.registry.utils.curve.get_cvs(circle, slice_start=median_cv), r=1, s=[0, 0, 1])
        return circle

    @staticmethod
    def maya_circle(constructionHistory=True, *args, **kwargs):
        return mc.circle(constructionHistory=constructionHistory, *args, **kwargs)[0]

    @staticmethod
    def maya_meta_node(*args, **kwargs):
        return mc.createNode('network', *args, **kwargs)

    def get_class_by_id(self, class_id):
        try:
            return getattr(self, class_id)
        except AttributeError:
            return None

    @classmethod
    def __iter__(cls):
        return iter(cls.node_constructors)

    def __getattr__(self, item):
        for node_constructor in self.node_constructors:
            if node_constructor.__name__ == item:
                return node_constructor
        else:
            self.__getattribute__(item)

    def __dir__(self):
        return dir(type(self)) + list(self.__dict__) + [node.__name__ for node in self.node_constructors]


class RegistryMetaclass(type):
    registered_methods = {}

    @classmethod
    def help(cls):
        return list(cls.registered_methods)

    def __getattr__(self, item):
        func = self.registered_methods.get(item)
        if func:
            return func
        raise AttributeError('No registered method:', item)


@add_metaclass(RegistryMetaclass)
class MayaControlShapeFactory(object):
    @staticmethod
    def register_shape(**kwargs_outer):
        strip_kwarg = lambda strip_key, kdict: kdict.pop(strip_key)

        def decorator(f):
            forge.LOG.debug('Registering Function %s to the MayaControlShapeFactory' % f.__name__)

            def union_the_kwargs_and_call(**kwargs):
                kwargs.update(kwargs_outer)
                try:
                    func = strip_kwarg('func', kwargs)
                    if func.__name__ == 'maya_curve':
                        kwargs['p'] = f()
                    return func(**kwargs)
                except KeyError:
                    return f(**kwargs)

            MayaControlShapeFactory.registered_methods[f.__name__] = union_the_kwargs_and_call
            return f

        return decorator

    @staticmethod
    def strip_kwarg(strip_key, kwargs):
        return kwargs.pop(strip_key)
