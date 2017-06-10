from . import settings
from . import templates
from . import exception
from . import core
from . import registration

__all__ = ['rig_lib', 'registration', 'settings', 'vendor', 'exception', 'core', 'components', 'templates']

LOG = settings.get_module_logger(__name__, module_override_level=settings.INFO)
LOG.info('Utils module has these components %s' % dir(core.core_utils.maya_utils))
registry = registration.Registry()
register_node = registry.register_node

LOG.info('Starting nodes registration')
import forge.core.nodes
LOG.info('Successfully loaded module %s' % forge.core.nodes.__name__)

registry.swap_mode(settings.MODE)

LOG.info('Importing all rig components')
import forge.components
LOG.info('Successfully loaded module %s' % forge.components.__name__)

LOG.info('Importing all rig elements')
import forge.elements
LOG.info('Successfully loaded module %s' % forge.elements.__name__)


def log_function_call(func):
    def wrapped(instance):
        LOG.info('Running test %s' % func.__name__)
        return func(instance)

    wrapped.__name__ = func.__name__
    return wrapped
