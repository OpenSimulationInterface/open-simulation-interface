Open Simulation Interface (OSI)
===============================

[![Travis Build Status](https://travis-ci.org/OpenSimulationInterface/open-simulation-interface.svg?branch=master)](https://travis-ci.org/OpenSimulationInterface/open-simulation-interface)

The Open Simulation Interface <sup>[[1]](https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/)</sup> (OSI) is a generic interface based on [Google's protocol buffers](https://developers.google.com/protocol-buffers/) for the environmental perception of automated driving functions in virtual scenarios.

As the complexity of automated driving functions rapidly increases, the requirements for test and development methods are growing. Testing in virtual environments offers the advantage of completely controlled and reproducible environment conditions.

In this context, OSI defines generic interfaces to ensure modularity, integrability, and interchangeability of the individual components:
![](doc/images/osicontextwiki.png)

For more information on OSI see the [official documentation](https://opensimulationinterface.github.io/osi-documentation/) or the [official reference documentation](https://opensimulationinterface.github.io/open-simulation-interface/) for defined protobuf messages. 

[[1]](https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/) *A generic interface for the environment perception of automated driving functions in virtual scenarios.(Dated 03.02.2017) T. Hanke, N. Hirsenkorn, C. van-Driesten, P. Garcia-Ramos, M. Schiementz, S. Schneider, E. Biebl*

## Usage
##### Example of writing and reading an OSI message in `Python`
```python
from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_sensordata_pb2 import SensorData

def main():
    """Initialize SensorView and SensorData"""
    sensorview = SensorView()
    sensordata = SensorData()

    """Clear SensorData"""
    sensordata.Clear()

    """Get boundary line attributes from SensorView"""
    sv_ground_truth = sensorview.global_ground_truth
    sv_lane_boundary = sv_ground_truth.lane_boundary.add()
    sv_boundary_line = sv_lane_boundary.boundary_line.add()
    sv_boundary_line.position.x = 1699.20
    sv_boundary_line.position.y = 100.16
    sv_boundary_line.position.z = 0.0
    sv_boundary_line.width = 0.13
    sv_boundary_line.height = 0.0

    """Set boundary line attributes to SensorData"""
    sd_lane_boundary = sensordata.lane_boundary.add()
    sd_boundary_line = sd_lane_boundary.boundary_line.add()
    sd_boundary_line.position.x = sv_boundary_line.position.x
    sd_boundary_line.position.y = sv_boundary_line.position.y
    sd_boundary_line.position.z = sv_boundary_line.position.z
    sd_boundary_line.width = sv_boundary_line.width
    sd_boundary_line.height = sv_boundary_line.height

    """Serialize SensorData which can be send"""
    string_buffer = sensordata.SerializeToString()

    """Clear SensorData to show parsing from string"""
    sensordata.Clear()

    """The received string buffer can now be parsed"""
    sensordata.ParseFromString(string_buffer)

    """Print SensorData"""
    print(sensordata)

if __name__ == "__main__":
    main()
```
**Output**:
```bash
lane_boundary {
  boundary_line {
    position {
      x: 1699.2
      y: 100.16
      z: 0.0
    }
    width: 0.13
    height: 0.0
  }
}
```
See Google's documentation for more tutorials on how to use protocol buffers with [Python](https://developers.google.com/protocol-buffers/docs/pythontutorial) or [C++](https://developers.google.com/protocol-buffers/docs/cpptutorial).
## Installation
##### Dependencies
Install `cmake` 3.10.2:
```bash
$ sudo apt-get install cmake
```
Install `pip3` and missing python packages:
```bash
$ sudo apt-get install python3-pip python-setuptools
```
Install `protobuf` 3.0.0:
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
$ pip install .
```

Global:
```bash
$ git clone https://github.com/OpenSimulationInterface/open-simulation-interface.git
$ cd open-simulation-interface
$ sudo pip3 install .
```
For Windows installation see [here](https://opensimulationinterface.github.io/osi-documentation/osi/windows.html) for more information.
