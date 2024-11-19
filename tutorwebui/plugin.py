from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from . import cli
from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

tutor_hooks.Filters.CLI_COMMANDS.add_items(
    [
        cli.shell,
        cli.webui,
    ]
)
