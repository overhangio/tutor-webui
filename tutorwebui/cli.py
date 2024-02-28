import io
import os
import platform
import subprocess
import sys
import tarfile
from typing import Dict, Optional
from urllib.request import urlopen

import click
import click_repl

# Note: it is important that this module does not depend on config, such that
# the web ui can be launched even where there is no configuration.
from tutor import env as tutor_env
from tutor import exceptions, fmt, serialize
from tutor.commands.context import Context
from tutor.types import Config

# Check if it was upgraded since 2022
# https://github.com/sorenisanerd/gotty/releases
GOTTY_RELEASE = "v1.5.0"


@click.group(
    short_help="Web user interface", help="""Run Tutor commands from a web terminal"""
)
def webui() -> None:
    pass


@click.command(help="Start the web UI")
@click.option(
    "-p",
    "--port",
    default=3737,
    type=int,
    show_default=True,
    help="Port number to listen",
)
@click.option(
    "-h", "--host", default="0.0.0.0", show_default=True, help="Host address to listen"
)
@click.pass_obj
def start(context: Context, port: int, host: str) -> None:
    check_gotty_binary(context.root)
    fmt.echo_info(f"Access the Tutor web UI at http://{host}:{port}")
    while True:
        config = load_config(context.root)
        user = config["user"]
        password = config["password"]
        command = [
            gotty_path(context.root),
            "--permit-write",
            "--address",
            host,
            "--port",
            str(port),
            "--title-format",
            "Tutor web UI - {{ .Command }} ({{ .Hostname }})",
        ]
        if user and password:
            credential = f"{user}:{password}"
            command += ["--credential", credential]
        else:
            fmt.echo_alert(
                "Running web UI without user authentication. Run 'tutor webui configure' to setup authentication"
            )
        command += [sys.argv[0], "shell"]
        p = subprocess.Popen(command)
        while True:
            try:
                p.wait(timeout=2)
            except subprocess.TimeoutExpired:
                new_config = load_config(context.root)
                if new_config != config:
                    click.echo(
                        "WARNING configuration changed. Tutor web UI is now going to restart. Reload this page to continue."
                    )
                    p.kill()
                    p.wait()
                    break


@click.command(help="Configure authentication")
@click.option("-u", "--user", prompt="User name", help="Authentication user name")
@click.option(
    "-p",
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Authentication password",
)
@click.pass_obj
def configure(context: Context, user: str, password: str) -> None:
    save_webui_config_file(context.root, {"user": user, "password": password})
    fmt.echo_info(
        f"The web UI configuration has been updated. "
        f"If at any point you wish to reset your username and password, "
        f"just delete the following file:\n\n    {config_path(context.root)}"
    )


@click.command(
    short_help="Interactive shell",
    help="Launch an interactive shell for launching Tutor commands",
)
def shell() -> None:
    click.echo(
        """Welcome to the Tutor interactive shell UI!
Type "help" to view all available commands.
Type "local launch" to configure and launch a new platform from scratch.
Type <ctrl-d> to exit."""
    )
    # Retrieve the current Click context. The context is used to manage the state
    # and pass around internal objects within the Click framework.
    ctx = click.get_current_context()

    while True:
        try:
            click_repl.repl(ctx)
            return  # this happens on a ctrl+d
        except exceptions.TutorError as e:
            fmt.echo_error(f"Error: {e.args[0]}")
        except KeyboardInterrupt:
            pass
        except Exception as e:  # pylint: disable=broad-except
            print(e)
            raise e


def check_gotty_binary(root: str) -> None:
    path = gotty_path(root)
    if os.path.exists(path):
        return
    fmt.echo_info(f"Downloading gotty to {path}...")

    # Generate release url
    architecture_map = {"x86_64": "amd64", "i386": "386", "aarch64": "arm64"}
    architecture = architecture_map.get(platform.uname().machine)
    if not architecture:
        raise exceptions.TutorError(
            f"Unsupported architecture: {platform.uname().machine}"
        )

    url = (
        f"https://github.com/sorenisanerd/gotty/releases/download/{GOTTY_RELEASE}/"
        f"gotty_{GOTTY_RELEASE}_{platform.system().lower()}_{architecture}.tar.gz"
    )

    # Download
    response = urlopen(url)

    # Decompress
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    compressed = tarfile.open(fileobj=io.BytesIO(response.read()))
    compressed.extract("./gotty", dirname)


def load_config(root: str) -> Dict[str, Optional[str]]:
    path = config_path(root)
    if not os.path.exists(path):
        save_webui_config_file(root, {"user": None, "password": None})
    with open(config_path(root), encoding="utf-8") as f:
        config = serialize.load(f)
    if not isinstance(config, dict):
        raise exceptions.TutorError(
            f"Invalid webui: expected dict, got {config.__class__}"
        )
    return config


def save_webui_config_file(root: str, config: Config) -> None:
    path = config_path(root)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w", encoding="utf-8") as of:
        serialize.dump(config, of)


def gotty_path(root: str) -> str:
    return get_path(root, "gotty")


def config_path(root: str) -> str:
    return get_path(root, "config.yml")


def get_path(root: str, filename: str) -> str:
    return tutor_env.pathjoin(root, "webui", filename)


webui.add_command(start)
webui.add_command(configure)
