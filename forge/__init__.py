import settings
import templates
import exception
import core
import registration

module_override_level = settings.CRITICAL

__all__ = ['rig_lib', 'registration.py', 'settings', 'vendor', 'exception', 'core', 'components', 'templates']

LOG = settings.get_module_logger(__name__, module_override_level=module_override_level)

shapes = registration.MayaControlShapeFactory
registry = registration.Registry()
register_node = registry.register_node

import forge.core.core_utils.base_utils

LOG.info('Successfully loaded module %s' % forge.core.core_utils.base_utils.__name__)
import forge.core.core_utils.maya_utils

LOG.info('Successfully loaded module %s' % forge.core.core_utils.maya_utils.__name__)

# Registering all necessary functions/nodes with registry.
LOG.info('starting set_default_utils')
registry.set_default_utils(mode=settings.MODE)

LOG.info('starting control shapes registration')
import forge.core.core_utils.maya_utils.control_shapes

LOG.info('Successfully loaded module %s' % forge.core.core_utils.maya_utils.control_shapes.__name__)

LOG.info('starting nodes registration')
import forge.core.nodes

LOG.info('Successfully loaded module %s' % forge.core.nodes.__name__)

LOG.info('starting set_default_nodes')
registry.set_default_nodes(mode=settings.MODE)

# LOG.info('Importing all rig components')
import forge.components

# LOG.info('Successfully loaded module %s' % forge.components.__name__)

LOG.info('Importing all rig elements')
import forge.elements

LOG.info('Successfully loaded module %s' % forge.elements.__name__)


def log_function_call(func):
    def wrapped(instance):
        LOG.info('Running test %s' % func.__name__)
        return func(instance)

    wrapped.__name__ = func.__name__
    return wrapped
