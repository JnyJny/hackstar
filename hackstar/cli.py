"""
"""

import click

from .engine import TheGame


@click.command()
def cli():
    """
    """
    the_game = TheGame()

    the_game.run()
