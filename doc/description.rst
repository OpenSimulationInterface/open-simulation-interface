General description
======================

`TUM Department of Electrical and Computer Engineering`_

Global remarks
--------------

All fields in the interface are set to optional and required is not
used. This has been done to allow backward compatible changes in the
field. Additionally, this is the default behavior in protobuf version 3
that does no longer have the required type and therefore ensures update
compatibility. However, this does not mean that filling the field is
optional. For the purpose of providing a complete interface, all
existing fields should be set, unless not setting a field carries a
specific meaning as indicated in the accompanying comment.

Compatibility
-------------

Definition: FAITHFULLY "All recorded data is correctly interpreted by
the interface"

Forward compatibility: Definition: "An older version of the code can be
used to read new files" Data recorded with a higher minor or patch
version can be interpreted by code built using the same major version of
the interface but lower minor and/or patch version. In this case,
additional fields of a newer minor version are silently ignored. All
patch versions of the same major and minor version are FAITHFULLY
forward compatible.

Backward compatibility: Definition: "A newer version of code can be used
to read old files" All files that have been recorded in the past with a
specific major version are FAITHFULLY valid with all combinations of
higher minor and patch versions of the same major version.

.. # Old way of OSI 2 to inject errors
.. Fault injection: how-to
.. -----------------------

.. Injection of predefined sensor errors should be handled by a
.. specialized "fault injector" component that acts like a sensor model
.. component, i.e. it takes a SensorData message as input and returns a
.. modified SensorData message as output. Specific errors should be handled
.. as follows:

.. -  Ghost objects / false positive: An additional SensorDataObject is
..    added to the list of objects in SensorData.object with
..    SensorDataObject.model_internal_object.ground_truth_type set to
..    kTypeGhost.
.. -  False negative: The object is marked as not seen by the sensor by
..    setting the property SensorDataObject.model_internal_object.is_seen
..    to false. The implementation of field-of-view calculation modules
..    should respect this flag and never reset an object marked as not-seen
..    to seen.

Proto3 Support
--------------

For users that need to use proto3 syntax, for example because the
language binding of choice only supports proto3 syntax out of the box, a
shell script called `convert-to-proto3.sh <https://github.com/OpenSimulationInterface/open-simulation-interface/blob/master/convert-to-proto3.sh>`_ is supplied that converts
all proto files to proto3 syntax. If this is run prior to building, the
resulting libraries will use proto3, with the on-the-wire format
remaining compatible between proto2 and proto3 libraries.

Packaging
---------

A specification to package sensor models using OSI as (extended)
Functional Mock-up Units (FMUs) for use in simulation environments is
available `here`_.

Vector Images
--------------
The vector images for the open-simulation-interface documentation are provided in the .svg-format.

Creating vector images
~~~~~~~~~~~~~~~~~~~~~~~

Objects such as roads, vehicles, signs, etc. that are embedded in the graphics are based on realistic high detailed 3D models.
The overall scene and 3D objects are modelled using the 3D modelling software `Blender <https://www.blender.org/>`_.
The Freestyle SVG Exporter from Blender is used to convert the modelled 3D scene into vector graphics.

The Freestyle SVG Exporter add-on from Blender can be activated via the Render user settings. 
The GUI for the Exporter is located in the Render tab of the Properties Editor. After rendering, the exported .svg file is written to the output path.

For more information about Blender's Freestyle SVG Exporter add-on see: `docs.blender.org <https://docs.blender.org/manual/en/latest/render/freestyle/export_svg.html>`_

Following settings are used for exporting:
Freestyle SVG Export:
Frame, Round;
LineThickness = Absolute, 1.000px;

Freestyle Line Set: 
Visibility = Visible, 
Edgetype = Inclusive, 
Silhouette = true,
Border = true;

Editing vector images
~~~~~~~~~~~~~~~~~~~~~~~

The exported 3D vector graphics can be opened and edited with any image editing program. (e.g. `Inkscape <https://inkscape.org/de/>`_)
The vectors and labels are placed accordingly.
The graphics should generally be kept in a grayscale style.
RGBA code for grey: b3b3b3ff


.. Doxygen Reference Documentation
.. --------------------------------

.. The doxygen reference documentation of the GitHub master branch is `online`_
.. available.


.. In order to generate the doxygen documentation for OSI, please follow
.. the following steps:

.. 1. Install `Doxygen`_, set an environmental variable 'doxygen' with the
..    path to the binary file and add it to the PATH variable:
..    ``PATH += %doxygen%``.
.. 2. Download the `proto2cpp`_ repo. Copy the content of the repo
..    proto2cpp to your desired ``<path-to-proto2cpp.py>``
.. 3. Install `graphviz`_, set an environmental variable 'graphviz' with
..    the path to the binary file and add it to the PATH variable:
..    ``PATH += %graphviz%``.
.. 4. From the cmd navigate to the build directory and run:
..    ``cmd cmake -DFILTER_PROTO2CPP_PY_PATH=<path-to-proto2cpp.py> <path-to-CMakeLists.txt>``
.. 5. The build process will then generate the doxygen documentation under
..    the directory doc.

Citing
------

Use the following citation for referencing the OSI interface in your
scientific work:

.. code-block:: latex

    @misc{osi.2017, author = {Hanke, Timo and
    Hirsenkorn, Nils and {van[STRIKEOUT:Driesten}, Carlo and
    {Garcia]\ Ramos}, Pilar and Schiementz, Mark and Schneider, Sebastian},
    year = {2017}, title = {{Open Simulation Interface: A generic interface
    for the environment perception of automated driving functions in virtual
    scenarios.}}, url = {http://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/},
    note = {{Accessed: 2017-08-28}} }

.. _here: https://github.com/OpenSimulationInterface/osi-sensor-model-packaging
.. _online: https://opensimulationinterface.github.io/open-simulation-interface/
.. _Doxygen: http://www.doxygen.nl/download.html
.. _proto2cpp: https://github.com/OpenSimulationInterface/proto2cpp
.. _graphviz: https://graphviz.gitlab.io/_pages/Download/Download_windows.html
.. _`http://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/}`: http://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/}
.. _Online Doxygen Documentation: https://opensimulationinterface.github.io/open-simulation-interface/
.. _TUM Department of Electrical and Computer Engineering: https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/

.. |Travis Build Status| image:: https://travis-ci.org/OpenSimulationInterface/open-simulation-interface.svg?branch=master
   :target: https://travis-ci.org/OpenSimulationInterface/open-simulation-interface