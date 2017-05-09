import templates
import exception
import node_registry
import settings
import vendor.cgLogging as logger
__all__ = ['rig_lib', 'node_registry', 'settings', 'vendor', 'exception', 'core', 'rig']


LOG = logger.cgLogging.getLogger(__name__, level=logger.cgLogging.INFO, shell=False)

registry = node_registry.Registry()
register_node = registry.register_node
shapes = node_registry.MayaControlShapeFactory

import forge.core.core_utils.base_utils
import forge.core.core_utils.maya_utils

# Registering all necessary functions/nodes with registry.
LOG.info('starting set_default_utils')
registry.set_default_utils(mode=settings.MODE)
LOG.info('starting control shapes registration')
import forge.core.core_utils.maya_utils.control_shapes
LOG.info('starting nodes registration')
LOG.info('starting set_default_nodes')
registry.set_default_nodes(mode=settings.MODE)


def log_function_call(func):
    def wrapped(instance):
        LOG.info('Running test %s' % func.__name__)
        return func(instance)
    wrapped.__name__ = func.__name__+'_logoutput'
    return wrapped