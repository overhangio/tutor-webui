import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutorwebui", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-webui",
    version=ABOUT["__package_version__"],
    url="https://overhang.io/overhangio/tutor-webui",
    project_urls={
        "Documentation": "https://docs.tutor.overhang.io/",
        "Code": "https://github.com/overhangio/tutor-webui",
        "Issue tracker": "https://github.com/overhangio/tutor-webui/issues",
        "Community": "https://discuss.openedx.org",
    },
    license="AGPLv3",
    author="Overhang.IO",
    author_email="contact@overhang.io",
    maintainer="Overhang.IO",
    maintainer_email="regis@overhang.io",
    description="Web-based user interface plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["tutor>=16.0.0,<17.0.0", "click_repl>=0.2.0"],
    entry_points={
        "tutor.plugin.v1": ["webui = tutorwebui.plugin"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
