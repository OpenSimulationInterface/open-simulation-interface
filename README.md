ASAM OSI® 
===============================

[![ProtoBuf CI Builds](https://github.com/OpenSimulationInterface/open-simulation-interface/actions/workflows/protobuf.yml/badge.svg)](https://github.com/OpenSimulationInterface/open-simulation-interface/actions/workflows/protobuf.yml)

ASAM OSI (Open Simulation Interface) <sup>[[1]](https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/)</sup> is a generic interface based on [Google's protocol buffers](https://developers.google.com/protocol-buffers/) for the environmental perception of automated driving functions in virtual scenarios.

As the complexity of automated driving functions rapidly increases, the requirements for test and development methods are growing. Testing in virtual environments offers the advantage of completely controlled and reproducible environment conditions.

For more information on ASAM OSI see the [official documentation](https://opensimulationinterface.github.io/osi-antora-generator/asamosi/latest/specification/index.html) or the [class list](https://opensimulationinterface.github.io/osi-antora-generator/asamosi/latest/gen/annotated.html) for defined protobuf messages.

[1] Hanke, T., Hirsenkorn, N., van-Driesten, C., Garcia-Ramos, P., Schiementz, M., Schneider, S. & Biebl, E. (2017, February 03). *A generic interface for the environment perception of automated driving functions in virtual scenarios.* Retrieved January 25, 2020, from https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/

## Usage
For usage examples, please refer to the official documentation:
- [Trace file generation with python](https://opensimulationinterface.github.io/osi-antora-generator/asamosi/latest/interface/architecture/trace_file_example.html)
- [OSMP examples](https://opensimulationinterface.github.io/osi-antora-generator/asamosi/latest/sensor-model/setup/build_install_example.html), including the code found at [osi-sensor-model-packaging](https://github.com/OpenSimulationInterface/osi-sensor-model-packaging):
  - [OSMPDummySource](https://github.com/OpenSimulationInterface/osi-sensor-model-packaging/tree/master/examples/OSMPDummySource)
  - [OSMPDummySensor](https://github.com/OpenSimulationInterface/osi-sensor-model-packaging/tree/master/examples/OSMPDummySensor)
  - [OSMPCNetworkProxy](https://github.com/OpenSimulationInterface/osi-sensor-model-packaging/tree/master/examples/OSMPCNetworkProxy)

## Setup

For detailed setup instructions, please refer to the official documentation:

- [OSI C++ Bindings](https://opensimulationinterface.github.io/osi-antora-generator/asamosi/latest/interface/setup/setting_up_osi_cpp.html)
- [OSI Python Bindings](https://opensimulationinterface.github.io/osi-antora-generator/asamosi/latest/interface/setup/setting_up_osi_python.html)

## About ASAM
ASAM e.V. (Association for Standardization of Automation and Measuring Systems) is a not-for-profit organization that promotes standardization of tool chains in automotive development and testing. Our members are international car manufacturers, suppliers, tool vendors, engineering service providers, and research institutes. ASAM standards are developed by experts from our member companies and are based on real use cases. ASAM is the legal owner of these standards and is responsible for their distribution and marketing.

ASAM standards span a wide range of use cases in automotive development, test, and validation.
They define file formats, data models, protocols, and interfaces.
The standards enable easy exchange of data and tools within and across tool chains.
They are applied worldwide.
