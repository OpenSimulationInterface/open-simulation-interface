Open Simulation Interface (OSI)
===============================

[![ProtoBuf CI Builds](https://github.com/OpenSimulationInterface/open-simulation-interface/actions/workflows/protobuf.yml/badge.svg)](https://github.com/OpenSimulationInterface/open-simulation-interface/actions/workflows/protobuf.yml)

The Open Simulation Interface <sup>[[1]](https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/)</sup> (OSI) is a generic interface based on [Google's protocol buffers](https://developers.google.com/protocol-buffers/) for the environmental perception of automated driving functions in virtual scenarios.

As the complexity of automated driving functions rapidly increases, the requirements for test and development methods are growing. Testing in virtual environments offers the advantage of completely controlled and reproducible environment conditions.

For more information on OSI see the [official documentation](https://opensimulationinterface.github.io/osi-documentation/) or the [official reference documentation](https://opensimulationinterface.github.io/open-simulation-interface/) for defined protobuf messages.

<!-- TODO: Update with new Antora hosting -->

[1] Hanke, T., Hirsenkorn, N., van-Driesten, C., Garcia-Ramos, P., Schiementz, M., Schneider, S. & Biebl, E. (2017, February 03). *A generic interface for the environment perception of automated driving functions in virtual scenarios.* Retrieved January 25, 2020, from https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/

## Usage
##### Example of generating OSI messages in `Python`
```python
# generate_osi_messages.py
from osi3.osi_sensorview_pb2 import SensorView
import struct

NANO_INCREMENT = 10000000
MOVING_OBJECT_LENGTH = 5
MOVING_OBJECT_WIDTH = 2
MOVING_OBJECT_HEIGHT = 1

def main():
    """Initialize SensorView"""
    f = open("sv_330_361_1000_movingobject.osi", "ab")
    sensorview = SensorView()

    sv_ground_truth = sensorview.global_ground_truth
    sv_ground_truth.version.version_major = 3
    sv_ground_truth.version.version_minor = 5
    sv_ground_truth.version.version_patch = 0

    sv_ground_truth.timestamp.seconds = 0
    sv_ground_truth.timestamp.nanos = 0

    moving_object = sv_ground_truth.moving_object.add()
    moving_object.id.value = 42

    # Generate 1000 OSI messages for a duration of 10 seconds
    for i in range(1000):

        # Increment the time
        if sv_ground_truth.timestamp.nanos > 1000000000:
            sv_ground_truth.timestamp.seconds += 1
            sv_ground_truth.timestamp.nanos = 0
        sv_ground_truth.timestamp.nanos += NANO_INCREMENT

        moving_object.vehicle_classification.type = 2

        moving_object.base.dimension.length = MOVING_OBJECT_LENGTH
        moving_object.base.dimension.width = MOVING_OBJECT_WIDTH
        moving_object.base.dimension.height = MOVING_OBJECT_HEIGHT

        moving_object.base.position.x += 0.5
        moving_object.base.position.y = 0.0
        moving_object.base.position.z = 0.0

        moving_object.base.orientation.roll = 0.0
        moving_object.base.orientation.pitch = 0.0
        moving_object.base.orientation.yaw = 0.0

        """Serialize"""
        bytes_buffer = sensorview.SerializeToString()
        f.write(struct.pack("<L", len(bytes_buffer)))
        f.write(bytes_buffer)

    f.close()

if __name__ == "__main__":
    main()
```

To run the script execute the following command in the terminal:
```bash
python3 generate_osi_messages.py
```

This will output an osi file (`sv_330_361_1000_movingobject.osi`) which can be visualized and played back by the [osi-visualizer](https://github.com/OpenSimulationInterface/osi-visualizer).

See Google's documentation for more tutorials on how to use protocol buffers with [Python](https://developers.google.com/protocol-buffers/docs/pythontutorial) or [C++](https://developers.google.com/protocol-buffers/docs/cpptutorial).
## Installation
##### Dependencies
Install `cmake` 3.10.2:
```bash
$ sudo apt-get install cmake
```
Install `pip3` and missing python packages:
```bash
$ sudo apt-get install python3-pip python3-setuptools
```
Install `protobuf`:
```bash
$ sudo apt-get install libprotobuf-dev protobuf-compiler
```


##### Build and install for `C++` usage:
```bash
$ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
$ cd open-simulation-interface
$ mkdir build
$ cd build
$ cmake ..
$ make
$ sudo make install
```

##### Install for `Python` usage:
Local:
```bash
$ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
$ cd open-simulation-interface
$ sudo pip3 install virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ python3 -m pip install .
```

Global:
```bash
$ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
$ cd open-simulation-interface
$ sudo pip3 install .
```
For Windows installation see [here](https://opensimulationinterface.github.io/osi-documentation/open-simulation-interface/doc/windows.html) for more information.
