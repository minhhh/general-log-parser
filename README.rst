===============================
General Log Parser
===============================

.. image:: https://img.shields.io/travis/minhhh/general-log-parser.svg
        :target: https://travis-ci.org/minhhh/general-log-parser

.. image:: https://img.shields.io/pypi/v/general-log-parser.svg
        :target: https://pypi.python.org/pypi/general-log-parser


General Log Parser

* Free software: BSD license
* Documentation: `document`_

Introduction
-------------
General log parser is a tool for simple parsing of log files line by line.
It offers 2 modes
* Parsing from standard input.
* Parsing from a file or a list of files.

Usage examples
-------------
Parse from standard input

    cat logfile | logparser

Parse from single file

    logparser -l [logfile]

Parse from a list of files

    logparser -l {}.log --from 20150101 --to 20150405

Get all lines contains 'server1'

    logparser -l logfile --line-filter server1

Get all lines contains 'server1' OR 'server2'

    logparser -l logfile --line-filter server1

Get all lines where the third field > 9939928

    logparser -l logfile --line-filter server1 --cond-filter "{2} > 9939928"

Get all lines print only the second and third fields

    logparser -l logfile --line-filter server1 -o "{1} {2}"


.. _document: https://general-log-parser.readthedocs.org.
