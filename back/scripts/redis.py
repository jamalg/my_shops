from click import Group

from back.extensions.google.caching import redis_client

redis_cli = Group("redis")


@redis_cli.command("flush")
def purge_redis():
    redis_client.flushdb()
