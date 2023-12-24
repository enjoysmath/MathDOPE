from .settings import MAX_BAD_CONN_RETRIES

def call_with_retry(func, *args, **kwargs):
    tries = 0
    while tries < MAX_BAD_CONN_RETRIES:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tries += 1

def full_qualname(o):
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__
    return module + '.' + o.__class__.__name__


def deep_get(d:dict, keys, default=None, create=True):
    if not keys:
        return default
    
    for key in keys[:-1]:
        if key in d:
            d = d[key]
        elif create:
            d[key] = {}
            d = d[key]
        else:
            return default
    
    key = keys[-1]
    
    if key in d:
        return d[key]
    elif create:
        d[key] = default
    
    return default


def deep_set(d:dict, keys, value, create=True):
    assert(keys)
    
    for key in keys[:-1]:
        if key in d:
            d = d[key]
        elif create:
            d[key] = {}
            d = d[key]
    
    d[keys[-1]] = value 
    return value


