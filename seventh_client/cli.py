import sys
import click
import importlib

from seventh_client import Seventh


def load_client(client):
    if client == "default":
        return Seventh

    module, app = client.split(":")
    client_module = importlib.import_module(module)

    return client_module.__dict__[app]


@click.command()
@click.option("-a", "--addr", default="localhost", type=str)
@click.option("-p", "--port", default=8000)
@click.option("-d", "--days", default=10)
@click.option("-c", "--client", default="default")
def cli(addr, port, days, client):
    path = f"http://{addr}:{port}"
    trader = load_client(client)(path)

    trader.run(days)
    print(trader.eval())
