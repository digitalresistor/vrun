vrun
====

A small Python helper tool that will modify the ``PATH`` in the environment
before executing the provided executable. This is useful when programs expect
certain binaries to be available in ``PATH`` so they can execute them using
``os.popen()`` and friends or even for shell scripts that are executing Python
tools that one would prefer to not globally install.

Scripts may detect that vrun has been used by looking for the environment
variable ``VRUN_ACTIVATED`` which is set to ``1`` when run. It is not
recommended that script writers do this.

Use
---

.. code::

    $ python3 -mvenv ./env/
    $ ./env/bin/pip install vrun
    $ ./env/bin/vrun /bin/bash -c 'echo $PATH'


If for example there is a script that executes ``pip`` without explicitly
providing a PATH that includes a virtual environment the system installed
``pip`` may accidentally be invoked instead. With vrun the virtual environment
will come first in the search path and thus ``pip`` will be safely executed
within the context of the virtual environment.

.. code::

    $ ./env/bin/vrun ./myscript.sh

vrun or vexec
-------------

vrun installs itself as both ``vrun`` and ``vexec``. The later may be typed
with the left hand only and is slightly faster to roll off the keyboard!

License
-------

Please see the `LICENSE
<https://github.com/bertjwregeer/vrun/blob/master/LICENSE>`_ file in the source
code repository 
