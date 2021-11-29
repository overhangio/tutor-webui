WebUI plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================

This is a plugin for Tutor that allows you to manage a Tutor-powered `Open edX <https://open.edx.org/>`__ installation from a browser -- a web user interface! In other words, it is no longer necessary to SSH to a remote server to manage a running instance.

Installation
------------

::

    pip install tutor-webui

Usage
-----

Enable the plugin::

    tutor plugins enable webui

Start the web user interface::

    tutor webui start

You can then access the interface at http://localhost:3737, or http://youserverurl:3737.

.. image:: https://overhang.io/static/catalog/screenshots/webui.png

All ``tutor`` commands can be executed from this web UI: you just don't need to prefix the commands with ``tutor``. For instance, to deploy a local Open edX instance, run::

    local quickstart

instead of ``tutor local quickstart``.

Instead of running the interactive `repl <https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop>`__ in a web browser, you can also run tutor interactively directly from your shell::

    tutor shell

Authentication
~~~~~~~~~~~~~~

**WARNING** Once you launch the web UI, it is accessible by everyone, which means that your Open edX platform is at risk. If you are planning to leave the web UI up for a long time, you should setup a user and password for authentication::

    tutor webui configure

License
-------

This software is licensed under the terms of the AGPLv3.

This project depends on the `Gotty <https://github.com/yudai/gotty/>`_ binary, which is provided under the terms of the `MIT license <https://github.com/yudai/gotty/blob/master/LICENSE>`_.
