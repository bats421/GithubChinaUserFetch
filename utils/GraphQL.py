import asyncio
import random
import time

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import config

transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers={
    'Authorization': 'bearer %s' % config.config["token"]})
client = Client(transport=transport,
                fetch_schema_from_transport=True)


def execute(query):
    try:
        result = client.execute(gql(query))
        return result
    except asyncio.CancelledError:
        print("interrupt")
        time.sleep(random.randint(1, 5) / 10.)
        print("continue")
        return execute(query)
    except Exception:
        return 0
