Discrete Radon Transform for Line Detection
===========================================

An implementation of the Discrete Radon Transform and its application for Line Detection.

Can be used as a python module or a command line tool.


Usage as a python module
------------------------

See the example in `examples/example_usage.py </examples/example_usage.py>`_.


Command line interface
----------------------

Dradon's usage looks like:

.. code-block:: console

   $ poetry run dradon [OPTIONS] <file>

.. option:: --radon_img <file>

   Save the radon image to file.

.. option:: --lines_img <file>

   Save the original image with marked lines to file.

.. option:: --version

   Display the version and exit.

.. option:: --help

   Display a short usage message and exit.
