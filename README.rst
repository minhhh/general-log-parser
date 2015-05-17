General Log Parser
==================

.. image:: https://img.shields.io/pypi/v/general-log-parser.svg
        :target: https://pypi.python.org/pypi/general-log-parser


Introduction
------------
General log parser is a tool for simple parsing of log files line by line.

It offers 2 modes:

- Parsing from standard input.
- Parsing from a file or a list of files.

Usage examples
--------------
Parse from standard input

.. code-block:: bash

    cat logfile | logparser

Parse from single file

.. code-block:: bash

    logparser -l [logfile]

Parse from a list of files

.. code-block:: bash

    logparser -l {}.log --from 20150101 --to 20150405

Get all lines contains 'server1'

.. code-block:: bash

    logparser -l logfile --line-filter server1

Get all lines contains 'server1' OR 'server2'

.. code-block:: bash

    logparser -l logfile --line-filter server1

Get all lines where the third field > 9939928

.. code-block:: bash

    logparser -l logfile --line-filter server1 --cond-filter "{2} > 9939928"

Get all lines print only the second and third fields

.. code-block:: bash

    logparser -l logfile --line-filter server1 -o "{1} {2}"

Authors
---------

Ha.Minh_

License
-------

Uses the `MIT`_ license.

.. _MIT: http://opensource.org/licenses/MIT
.. _Ha.Minh: http://minhhh.github.io
.. _document: https://general-log-parser.readthedocs.org
