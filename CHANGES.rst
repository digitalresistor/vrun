0.4 (2017-09-27)
================

- You may now create command aliases by creating a new configuration file named
  ``vrun.cfg`` or adding a section to an existing ``setup.cfg`` named ``[vrun]``.

  .. code::

      [vrun]
      python.version = python --version
      shell = /bin/bash
      echo = /bin/bash -c 'echo ${@}' _ {posargs} echo off the bare walls

  Which may then be used like so:

  .. code::

      vrun python.version
      vrun echo the soft voices
      vrun shell -c 'echo $PATH'

- New tests have been added, and coverage is now 100%. All new features from
  now on will have to meet the same coverage requirements to verify there are
  no breaking changes.

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
