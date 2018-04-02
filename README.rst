
AtomShields Cli
===============

What is AtomShields Cli?
------------------------

Command-Line Interface to use the software `AtomShields <https://github.com/ElevenPaths/AtomShields>`_

Installation
------------

.. code-block:: shell

  pip install atomshields-cli


Basic usage
-----------

.. code-block:: shell

  ascli <action> <context> --target <path> --name <project_name>

The allowed *action* values are:

- **install**: To install a checker or a report, depending the context setted.
- **uninstall**: To uninstall a checker or a report, depending the context setted.
- **run**: To run the scan.
- **show**: To show a checker list or a report list, depending the context setted.
- **help**: Show the help

The allowed *context* values are:

- **checkers**: Operate with checkers
- **reports**: Operate with reports

The *target* option set the path to scan, or the plugin (checker/report) to install/uninstall.


Show all checkers
-----------------

.. code-block:: shell

  ascli show checkers

------------------------------------------------------------------------------------------

Show all reports
----------------

.. code-block:: shell

  ascli show reports

------------------------------------------------------------------------------------------


Install checker
---------------

.. code-block:: shell

  ascli install checkers --target path/to/file.py

------------------------------------------------------------------------------------------

Install report
--------------

.. code-block:: shell

  ascli install reports --target path/to/file.py

------------------------------------------------------------------------------------------

Uninstall checker
-----------------

.. code-block:: shell

  ascli uninstall checkers --target path/to/file.py

or

.. code-block:: shell

  ascli uninstall checkers --target checker_name

------------------------------------------------------------------------------------------

Uninstall report
----------------

.. code-block:: shell

  ascli uninstall reports --target path/to/file.py

or

.. code-block:: shell

  ascli uninstall reports --target checker_name

------------------------------------------------------------------------------------------

Run the scan
------------

.. code-block:: shell

  ascli run --target path/to/file.py --name repo_name
