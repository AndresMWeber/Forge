from six import iteritems
import forge

MODULE_LOGGER_LEVEL_OVERRIDE = None


class SerializationMixin(object):
    LOG = forge.settings.get_module_logger(__name__, module_override_level=MODULE_LOGGER_LEVEL_OVERRIDE)
    REGISTER_TYPES = [forge.settings.CONTROL_TYPE,
                      forge.settings.JOINT_TYPE,
                      forge.settings.HIERARCHY_TYPE,
                      forge.settings.METADATA_TYPE]

    SERIALIZABLE = []

    def imprint_serialization(self,
                              target_node=None,
                              serialization=None,
                              tag_attr=forge.settings.DEFAULT_TAG_ATTR):
        """
        :param instance: registry.node - instance that inherits node or has forge attr/serialization functionality
        :param target_node: (registry.MayaTransform) - Target maya node to add/set the attribute
        :param serialization: (str) - default is a serialized string to recreate the node, override to custom tag
        :param tag_attr: (str) - The name for the tag attribute (default='forge')
        :return: (None)
        """
        if target_node is None:
            self.LOG.info("Default imprint serialization use %s" % target_node)
            target_node = self.group_top

        serialized_data = self.serialize() if serialization is None else serialization
        target_node.add_attr(tag_attr, serialized_data, dt='string')
        self.LOG.info('%r --> Imprinted serialization to node.attr %s.%s=%s' % (self,
                                                                               target_node,
                                                                               tag_attr,
                                                                               serialized_data))
        return target_node.get_attr(tag_attr)

    @classmethod
    def from_serial(cls, serialization, _depth=0):
        """ Resolves entries in a dict that represent class serializations

        :param serialization: {str: dict}, dictionary
        :param _depth: int, depth marker, for internal use only
        :return: dict
        """
        if _depth == 0:
            cls.LOG.debug('Initial serial before resolution: %s' % serialization)
        cls.LOG.debug('%sfrom_serial: working with dictionary %s ' % ('\t' * _depth, serialization))
        _depth += 1

        for k, v in iteritems(serialization):
            cls.LOG.debug('%sRunning through k=%s, v=%s' % ('\t' * _depth, k, v))
            if isinstance(v, dict):
                serialization[k] = cls.from_serial(v, _depth=_depth)
            class_resolution = forge.registry.get_class_by_id(k)
            if class_resolution:
                cls.LOG.debug('%s-----> Found class <%s> serialization, resolving...' % ('\t' * (_depth + 1),
                                                                                         class_resolution.__name__))
                serialization = class_resolution(**v)
        if _depth == 1:
            cls.LOG.info('Final serial resolution: %r' % serialization)
        return serialization

    def serialize_element(self):
        """ Serialization function to correctly serialize an element
            TODO: Merge this with the generic serializer.

        :return: dict, serialization of the Element instance
        """
        serialization = {}
        for k, v in iteritems({register_type: getattr(self, register_type) for register_type in self.REGISTER_TYPES}):
            v = v if isinstance(v, list) else list(v)
            for item in v:
                try:
                    serialization[item] = getattr(self, item).serialize()
                    self.LOG.debug('Serialized Element item using its own method %s' % serialization[item])
                except AttributeError:
                    serialization[item] = str(getattr(self, item)).decode('utf-8')
                    self.LOG.debug('Serialized Element item using decode %s' % serialization[item])
        self.LOG.debug('<%s>.serialize() = %s' % (self.__class__.__name__, serialization))
        return {self.__class__.__name__: serialization}

    def serialize_node(self):
        """ Serialization function to correctly serialize a node
            TODO: Merge this with the generic serializer.

        :return: dict, serialization of the Node instance (or subclass)
        """
        return {self.__class__.__name__: {'node_dag': self.node}}
