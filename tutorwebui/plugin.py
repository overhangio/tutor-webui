from tutor import hooks as tutor_hooks
from .__about__ import __version__
from . import cli

tutor_hooks.Filters.CLI_COMMANDS.add_items(
    [
        cli.shell,
        cli.webui,
    ]
)
