0.3 (2017-06-13)
================

- Adds Windows support, so now you can use:

  .. code::

      Script\vrun.exe python -c "import os; print(os.environ['PATH'])"

  To run Windows binaries with their ``%PATH%`` modified.

  vrun will also automatically add the `.exe` when passing the name of a script
  that exists in the ``Scripts`` folder.

  So the following are the same:

  .. code::
      
      Script\vrun.exe python

  and:

  .. code::

      Script\vrun.exe python.exe
  
0.2 (2017-06-08)
================

- Also export the environment variable ``VIRTUAL_ENV`` pointing to the virtual
  environment.

0.1 (2017-06-08)
================

- Initial release and implementation of the vrun functionality
