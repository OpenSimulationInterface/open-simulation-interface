Windows
=======
C++
------
All the following steps are to be executed with admin rights:

1. Install cmake (v3.7 or higher required):

- Go to the `cmake download page <https://cmake.org/download/>`_
- Download and install `cmake 3.8.0 <https://cmake.org/files/v3.8/cmake-3.8.0-rc2-win64-x64.msi>`_

2. Install Protobuf (v2.6.1 or higher required):

- Go to the `ProtoBuffer Download Page <https://github.com/protocolbuffers/protobuf/releases/tag/v2.6.1>`_
- Download and unzip `protobuf-2.6.1.zip <https://github.com/google/protobuf/releases/download/v2.6.1/protobuf-2.6.1.zip>`_
- Open the ``protobuf.sln`` file in the unzipped ``protobuf-2.6.1\vsprojects`` with Visual Studio
- Build ``libprotobuf``, ``libprotobuf-lite`` , ``libprotoc and protoc``
- Set the environmental variables:

    - ``PATH += path-to-the-directory-containing-the-just-created-protoc.exe-file``
    - ``PROTOBUF = path-to-the-unzipped-protobuf-2.6.1-directory``
    - ``PROTOBUF_SRC_ROOT_FOLDER = %PROTOBUF%``
    - ``CMAKE_INCLUDE_PATH = path-to-the-directory-protobuf-2.6.1\src-containing-the-folder-google``
    - ``CMAKE_LIBRARY_PATH = path-to-the-directory-containing-the-three-created-library-files``

3. Now you are ready to build and install OSI (v2.1.1 or higher required):

- Clone `open simulation interface <https://github.com/OpenSimulationInterface/open-simulation-interface>`_ from GitHub and navigate to this directory using a terminal.
- Create a new directory ``build`` and navigate into it using the following command:`` mkdir build & cd build``
- Generate a Visual Studio solution file suitable for your version and set the ``CMAKE_INSTALL_PREFIX`` to a directory where the OSI library and headers should be installed.

    - When no generator is mentioned: cmake would opt for the newest version of Visual Studio available. To see all supported generators please run: ``cmake -–help``.
    - To build a 64-bit OSI library, please add to the generator name the desired target platform Win64. In this case please make sure that the ``protoc.exe`` executable and protobuf libraries are also 64-bit and set the environmental variables to the appropriate paths.
    - When ``CMAKE_INSTALL_PREFIX`` is not set: cmake would opt for the configured default install directory.

.. code-block:: shell

    cmake .. [-G <generator>] [-DCMAKE_INSTALL_PREFIX=<osi-install-directory>]

Example using Visual Studio 12 2013 and C:/Libraries/open_simulation_interface as an install directory:

.. code-block:: shell

    cmake .. -G "Visual Studio 12 2013" -DCMAKE_INSTALL_PREFIX=C:/Libraries/open_simulation_interface

Now you can build and install OSI using the following commands:

.. code-block:: shell

    cmake --build . [--config Release]
    cmake --build . --target install

As an alternative way you can use Visual Studio to build and install OSI.
P.S.: If you build in a Release configuration, please make sure that the protobuf libraries and executable are also compiled with release settings.

Python
-----------

1. Go to the python download page and download the executable installer.
2. Run the installer (with admin rights).
3. In the first step of the installer check ‘Add Python 3.6 to PATH’, then finish installation.
4. Clone open simulation interface from GitHub and navigate to this directory using a terminal.
5. Run the following command: python setup.py install
