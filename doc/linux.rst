Linux
=====
Install ``cmake`` 3.10.2:

.. code-block:: shell

    $ sudo apt-get install cmake

Install ``pip3`` and missing python packages:

.. code-block:: shell

    $ sudo apt-get install python3-pip python-setuptools

Install ``protobuf`` 3.0.0:

.. code-block:: shell

    $ sudo apt-get install libprotobuf-dev protobuf-compiler

C++
------

.. code-block:: shell

    $ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
    $ cd open-simulation-interface
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make
    $ sudo make install


P.S.: To build a 32-bit target under 64-bit linux, please add ``-DCMAKE_CXX_FLAGS="-m32"`` to the ``cmake`` command. In this case, please make sure that ``protobuf`` is in a 32-bit mode too.

Python
-----------
**Local**:

.. code-block:: shell

    $ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
    $ cd open-simulation-interface
    $ sudo pip3 install virtualenv 
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install .

**Global**:

.. code-block:: shell

    $ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
    $ cd open-simulation-interface
    $ sudo pip3 install .