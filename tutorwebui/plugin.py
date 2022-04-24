from tutor import hooks
from .__about__ import __version__
from . import cli

hooks.Filters.CLI_COMMANDS.add_items(
    [
        cli.shell,
        cli.webui,
    ]
)
