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
##### Reading and writing an OSI message in `C++`
```
#include <iostream>
#include <string.h>
#include "osi_sensorview.pb.h"
#include "osi_sensordata.pb.h"
using namespace std;

int main(int argc, char* argv[]) {

    // Initialize SensorView and SensorData
    osi3::SensorView sensorview;
    osi3::SensorData sensordata;

    // Receive a serialized buffer string (for simplicity here nothing)
    string string_buffer = "";

    // Parse the received string
    sensorview.ParseFromString(string_buffer);

    // Clear SensorData
    sensordata.Clear();

    // Set the timestamp
    sensordata.mutable_timestamp()->set_seconds((long long int)floor(1000));

    // Iterate through the existing Moving Objects
    for (auto moving_obj : sensorview.global_ground_truth().moving_object())
    {
        // Create a moving object
        osi3::DetectedMovingObject* detected_moving_obj =  sensordata.add_moving_object();

        // Set the id of the detected moving object
        detected_moving_obj->mutable_header()->add_ground_truth_id()->set_value(moving_obj.id().value());
    }

    // Serialize 
    string new_string_buffer = "";
    sensordata.SerializeToString(&new_string_buffer);

  return 0;
}
```

##### Reading and writing an OSI message in `Python`
```
import osi3.osi_sensorview_pb2 as sv
import osi3.osi_sensordata_pb2 as sd

def main():
    # Initialize SensorView and SensorData
    sensorview = sv.SensorView()
    sensordata = sd.SensorData()

    # Receive a serialized buffer string (for simplicity here nothing)
    string_buffer = ""

    # Parse the received string
    sensorview.ParseFromString(string_buffer)

    # Clear SensorData
    sensordata.Clear()

    # Set the timestamp
    sensordata.timestamp.seconds = 1000

    # Iterate through the existing Moving Objects of SensorView from the received string
    for moving_object in sensorview.global_ground_truth.moving_object:
        # Create a moving object
        detected_moving_obj = sensordata.moving_object.add()

        # Set the id of the detected moving object
        detected_moving_obj.header.ground_truth_id.add().value = moving_object.id.value

    # Serialize
    new_string_buffer = sensordata.SerializeToString()

if __name__ == "__main__":
    main()
```

## Installation
##### Dependencies
Install cmake 3.10.2:
```
$ sudo apt-get install cmake
```
Install pip3 and missing python packages:
```
$ sudo apt-get install python3-pip python-setuptools
```
Install protobuf 3.0.0:
```
$ sudo apt-get install libprotobuf-dev protobuf-compiler
```


##### Build and install for `C++` usage:
```
$ cd open-simulation-interface
$ mkdir build
$ cd build
$ cmake ..
$ make
$ sudo make install
```

##### Build and install for `Python` usage:
Local:
```
$ cd open-simulation-interface
$ sudo pip3 install virtualenv 
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ sudo pip install .
```

Global:
```
$ cd open-simulation-interface
$ sudo pip3 install .
```

