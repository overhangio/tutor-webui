from glob import glob
import os
import pkg_resources

from .__about__ import __version__
from .cli import webui as webui_command

templates = pkg_resources.resource_filename("tutorwebui", "templates")

config = {}

hooks = {}

command = webui_command


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename("tutorwebui", "patches")
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
