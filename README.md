Open Simulation Interface (OSI)
===============================

[![Travis Build Status](https://travis-ci.org/OpenSimulationInterface/open-simulation-interface.svg?branch=master)](https://travis-ci.org/OpenSimulationInterface/open-simulation-interface)


General description
-------------------
[TUM Department of Electrical and Computer Engineering](https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/)


Global remarks
--------------
All fields in the interface are set to optional and required is not used. This has been done to allow backward
compatible changes in the field. Additionally, this is the default behavior in protobuf version 3 that does no longer
have the required type and therefore ensures update compatibility.
However, this does not mean that filling the field is optional. For the purpose of providing a complete interface, all
existing fields should be set, unless not setting a field carries a specific meaning as indicated in the accompanying
comment.


Compatibility
--------------
Defintion: FAITHFULLY "All recorded data is correctly interpreted by the interface"

Forward compatibility:
Definition: "An older version of the code can be used to read new files"
Data recorded with a higher minor or patch version can be interpreted by code built using the same major version of the interface but lower minor and/or patch version.
In this case, additional fields of a newer minor version are silently ignored. All patch versions of the same major and minor version are FAITHFULLY forward compatible.

Backward compatibility:
Definition: "A newer version of code can be used to read old files"
All files that have been recorded in the past with a specific major version are FAITHFULLY valid with all combinations of
higher minor and patch versions of the same major version.


Fault injection: how-to
------------------------
Injection of pre-defined sensor errors should be handled by a specialized "fault injector" component that acts like a
sensor model component, i.e. it takes a SensorData message as input and returns a modified SensorData message as output.
Specific errors should be handled as follows:
- Ghost objects / false positive:
    An additional SensorDataObject is added to the list of objects in SensorData.object
    with SensorDataObject.model_internal_object.ground_truth_type set to kTypeGhost.
- False negative:
    The object is marked as not seen by the sensor by setting the property 
    SensorDataObject.model_internal_object.is_seen to false. The implementation 
    of field-of-view calculation modules should respect this flag and never reset 
    an object marked as not-seen to seen.


Versioning
----------
The version number is defined in InterfaceVersion::version_number in osi_common.proto as the field's default value.

Major:
A change of the major version results in an incompatibility of code and recorded proto messages.
- An existing field with a number changes its meaning 
  optional double field = 1; -> repeated double field = 1;
  Changing the definition of units of a field
- Deleting a field  and reusing the field number
- Changing the technology
  ProtoBuffer -> FlatBuffer

Minor:
A change of the minor version indicates remaining compatibility to previously recorded files. The code on the other hand needs fixing.
- Renaming of a field without changing the field number
- Changing the names of messages
- Adding a new field in a message without changing the numbering of other fields

Patch:
The compatibility of both recorded files and code remains.
- File or folder structure which does not affect including the code in other projects
- Changing or adding comments
- Clarification of text passages explaining the message content


Packaging
---------

A specification to package sensor models using OSI as (extended)
Functional Mock-up Units (FMUs) for use in simulation environments
is available [here](https://github.com/OpenSimulationInterface/osi-sensor-model-packaging).


Documentation
-------------

In order to generate the doxygen documentation for OSI, please follow the following steps: 
1. Install [Doxygen](http://www.stack.nl/~dimitri/doxygen/download.html), set an environmental variable 'doxygen' with the path to the binary file and add it to the PATH variable: `PATH += %doxygen%`.
2. Download the [vg-1.5.0.zip](https://github.com/vgteam/vg/releases/tag/v1.5.0). Unpack and copy the content of folder /vg-1.5.0/contrib/proto2cpp to your desired `<path-to-proto2cpp.py>`
3. Install [graphviz-2.38](http://www.graphviz.org/Download_windows.php ), set an environmental variable 'graphviz' with the path to the binary file and add it to the PATH variable: `PATH += %graphviz%`.
4. From the cmd navigate to the build directory and run: 
```cmd
cmake -DFILTER_PROTO2CPP_PY_PATH=<path-to-proto2cpp.py> <path-to-CMakeLists.txt>
```
5. The build process will then generate the doxygen documentation under the directory doc.
