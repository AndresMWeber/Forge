
def inject_default_key_value(kwargs, key, default):
    kwargs[key] = kwargs.get(key, default)
    return kwargs
