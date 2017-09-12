DeepL commandline client
========================

A simple python commandline client for deepl.com/translate.

This is *NOT* an official API and might break at any moment.

.. code-block::

    Usage: deepl.py [-h] [-s lang] [-t lang] [-v] [text [text ...]]

    Translate text to other languages using deepl.com

    positional arguments:
      text

    optional arguments:
      -h, --help               show this help message and exit
      -s lang, --source lang   Source language
      -t lang, --target lang   Target language
      -v, --verbose            Print additional information


This can also be used as a library:

.. code-block:: python

    import deepl

    translation, extra_data = deepl.translate("This is a test", target="DE")

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with DeepL GmbH,
or any of its subsidiaries or its affiliates.