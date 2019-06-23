"""
Caching module for Google API Client
*This is not a production ready caching but only serves as POC/MVP*
Some of the problems that should be solved :
    - With regards to key generation :
        * The key is constructed using the provided keywords arguments. If the cached functin is
        called with position arguments then the caching fails and might even cause some hard to debug issues.
        In this case this is mitigated because GoogleCloudApi methods were made keywords arguments only functions
        but this is done client code adapting to "library" code
        * The string representation of the values are used. But some edge cases are not properly assumed. Calls with
        key=dict(a=1, b=1) and key=dict(b=1,a=1) will yield two different keys when the underneath result might be the same. Also
        object arguments that have different property values might have the same string representation. Here again very
        hard to debug
    - With regards to Redis storage:
        * Redis provides many data structure that can be used to store information. The current implementation
        only uses the classic string SET directive
"""
from typing import Callable

from datetime import timedelta
from functools import wraps

import redis

from back.config import config


redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB
)


def build_caching_key_with_kwargs(f: Callable, kwargs):
    main_key = f.__name__
    sorted_keys = sorted(kwargs.keys())
    kwargs_subkey = "-".join(["{}.{}".format(k, kwargs[k]) for k in sorted_keys])
    return "{}:{}".format(main_key, kwargs_subkey)


def redis_cache(
        expiry: timedelta = None,
        serialize: Callable = lambda v: v,
        deserialize: Callable = lambda v: v.decode("utf-8"),
        ) -> Callable:

    def _cache(f: Callable) -> Callable:

        @wraps(f)
        def cached(*args, **kwargs):
            key = build_caching_key_with_kwargs(f, kwargs)
            cached = redis_client.get(key)
            if cached:
                return deserialize(cached)
            computed = f(*args, **kwargs)
            redis_client.set(
                name=key,
                value=serialize(computed),
                ex=expiry
            )
            return computed
        return cached
    return _cache
