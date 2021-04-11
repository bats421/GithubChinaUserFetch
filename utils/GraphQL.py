from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import config


transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers={
            'Authorization': 'bearer %s' % config.config["token"]})
client = Client(transport=transport,
                             fetch_schema_from_transport=True)

def execute(query):
    return client.execute(gql(query))