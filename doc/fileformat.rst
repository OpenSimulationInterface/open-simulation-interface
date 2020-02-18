OSI File Format
===============
Formats
--------

\*.osi
~~~~~~~
To save multiple serialized OSI messages into one trace file we use the length of each OSI message and save it before the actual OSI message. 
The length is represented by the first four bytes which are a little endian unsigned int that represents the length of the followed message, not including the integer itself. 

\*.txt
~~~~~~~
If you happen to have a trace file which uses ``$$__$$`` separation you can convert it to the official OSI trace file by running:

.. code-block:: bash

    python3 txt2osi.py -d trace.txt

\*.txth
~~~~~~~
To read to content of a serialized txt/osi trace file we also provide a converter ``osi2read.py``.
See the usage below:

.. code-block:: bash

    python3 osi2read.py -d trace.osi -o readable_trace
    python3 osi2read.py -d trace.txt -f separated -o readable_trace

which outputs a ``readable_trace.txth`` which can be opened by any text editor.

Summary
~~~~~~~
In summary we have currently three types of formats:

1. ``*.osi`` trace files which are length separated.
2. ``*.txt`` trace files which are ``$$__$$`` separated.
3. ``*.txth`` files which are human readable trace files for just plausibility checks.

Trace file naming convention
-----------------------------
As best practice we recommend to name the trace files in the following format:

.. code-block:: txt

    <type>_<osi-version>_<protobuf-version>_<frame-number>_<custom-trace-name>.osi

For example a naming for a trace with the information below:

.. code-block:: txt

    Type = SensorView
    OSI Version= 3.1.2
    Protobuf Version = 3.0.0
    Number of frames = 1523
    Scenario name = highway

would then look like this:

.. code-block:: txt

    sv_312_300_1523_highway.osi

The type definition would only be possible for ``SensorView = sv``, ``SensorData = sd`` and ``GroundTruth = gt``.
By following this best practice users can understand the general content of a file. By comparing the information provided by the naming and the actual trace the user can check the overall validity of a trace file.

Generate OSI traces
--------------------
If you want to generate a valid OSI trace file which can be used as an input for the `osi-validator <https://github.com/OpenSimulationInterface/osi-validation>`_ or the `osi-visualizer <https://github.com/OpenSimulationInterface/osi-visualizer>`_ see the example script in python below:

.. code-block:: python

    from osi3.osi_sensorview_pb2 import SensorView
    import struct

    def main():
        """Initialize SensorView"""
        f = open("sv_312_320_10_movingobject.osi", "ab")
        sensorview = SensorView()

        sv_ground_truth = sensorview.global_ground_truth
        sv_ground_truth.version.version_major = 3
        sv_ground_truth.version.version_minor = 0
        sv_ground_truth.version.version_patch = 0

        sv_ground_truth.timestamp.seconds = 0
        sv_ground_truth.timestamp.nanos = 0

        moving_object = sv_ground_truth.moving_object.add()
        moving_object.id.value = 114

        # Generate 10 OSI messages for 9 seconds
        for i in range(10):

            # Increment the time
            sv_ground_truth.timestamp.seconds += 1
            sv_ground_truth.timestamp.nanos += 100000

            moving_object.vehicle_classification.type = 2
            
            moving_object.base.dimension.length = 5
            moving_object.base.dimension.width = 2
            moving_object.base.dimension.height = 1

            moving_object.base.position.x = 0.0 + i
            moving_object.base.position.y = 0.0 
            moving_object.base.position.z = 0.0

            moving_object.base.orientation.roll = 0.0
            moving_object.base.orientation.pitch = 0.0
            moving_object.base.orientation.yaw = 0.0 
            
            """Serialize"""
            bytes_buffer = sensorview.SerializeToString()
            f.write(struct.pack("<L", len(bytes_buffer)) + bytes_buffer)

        f.close()
    
    if __name__ == "__main__":
        main()

In the script we initialize the type we want to use for the messages. Here we use the type ``SensorView``. 
For the ``SensorView`` it is mandatory to define the version and the timestamp. After that we can add objects. 
Here we add a moving object with the ID 114. For this object we generate in a for loop 10 OSI messages which all have different x values over a time span of 9 seconds. 
This means the object is changing the position in the x direction through the iteration each second. 
Each time we change the x value and the timestamp we append the length of the OSI message and the serialized OSI message itself to a file called ``sv_312_320_10_movingobject.osi``. 
After finishing the loop we now have a ``sv_312_320_10_movingobject.osi`` file which can be `validated <https://github.com/OpenSimulationInterface/osi-validation>`_ and `visualized <https://github.com/OpenSimulationInterface/osi-visualizer>`_.
