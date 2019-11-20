OSI File Format
----------------

To save multiple serialized OSI messages into one trace file we use the length of each OSI message and save it before each OSI message. 
The length is represented by the first four bytes which are a little endian unsigned int that represents the length of the followed message, not including the integer itself.
If you happen to have a trace file which uses ``$$__$$`` separation you can convert it to the official OSI trace file by running ``python3 txt2osi.py trace.txt``.

If you want to generate a valid OSI trace file which can be used as an input for the `osi-validator <https://github.com/OpenSimulationInterface/osi-validation>`_ or the `osi-visualizer <https://github.com/OpenSimulationInterface/osi-visualizer>`_ see the example script in python below:

.. code-block:: python

    from osi3.osi_sensorview_pb2 import SensorView
    import struct

    def main():
        """Initialize SensorView"""
        f = open("test_trace.osi", "ab")
        sensorview = SensorView()

        sv_ground_truth = sensorview.global_ground_truth
        sv_ground_truth.version.version_major = 3
        sv_ground_truth.version.version_minor = 0
        sv_ground_truth.version.version_patch = 0

        sv_ground_truth.timestamp.seconds = 4
        sv_ground_truth.timestamp.nanos = 54999999

        stationary_object = sv_ground_truth.stationary_object.add()
        stationary_object.id.value = 114

        for i in range(11):
            
            stationary_object.base.dimension.length = 3
            stationary_object.base.dimension.width = 0.5
            stationary_object.base.dimension.height = 0.89

            stationary_object.base.position.x = 0.0 + i
            stationary_object.base.position.y = 0.0 
            stationary_object.base.position.z = 0.0

            stationary_object.base.orientation.roll = 0.0
            stationary_object.base.orientation.pitch = 0.0
            stationary_object.base.orientation.yaw = 0.0 

            stationary_object.classification.type = 1
            stationary_object.classification.material = 0
            stationary_object.classification.density = 0
            stationary_object.classification.color = 0

            """Serialize"""
            bytes_buffer = sensorview.SerializeToString()
            f.write(struct.pack("<L", len(bytes_buffer)) + bytes_buffer)   

        f.close()
    
    if __name__ == "__main__":
        main()

In the script we initialize the type we want to use for the messages. Here we use the type ``SensorView``. 
For the ``SensorView`` it is mandatory to define the version and the timestamp. After that we can add objects. 
Here we add a stationary object with the ID 114. For this object we generate in a for loop 10 OSI messages which all have different x values. 
This means the object is changing the position in the x direction through the iteration. 
Each time we change a value we append the length of the OSI message and the serialized OSI message itself to a file called ``test_trace.osi``. 
After finishing the loop we now have a ``test_trace.osi`` file which can be `validated <https://github.com/OpenSimulationInterface/osi-validation>`_ and `visualized <https://github.com/OpenSimulationInterface/osi-visualizer>`_.