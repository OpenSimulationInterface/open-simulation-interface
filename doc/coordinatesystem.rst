Coordinate systems and reference points
============================================

Coordinate systems
-------------------

Currently three coordinate systems exist.

- world frame (for all quantities which are part of groundtruth)
- sensor frame (for all quantities which are part of sensordata)
- object frame (for local object coordinates like axle offset vectors)

The transformation between frames for a specific vehicle/sensor is performed using the information in

- ``GroundTruth::moving_object::base::position and ::orientation``: These define the position and orientation of the vehicle's reference point, i.e. center of bounding box.
- ``GroundTruth::moving_object::vehicle_attributes::bbcenter_to_rear``: This defines the vehicle frame origin resp. the relative frame of the vehicle, i.e. it defines the offset of the rear axis center relative to the vehicle's reference point (center of bounding box). This offset is static and given in vehicle coordinates.
- ``SensorData::mounting_position``: This defines the sensor's position and orientation relative to the vehicle frame's origin, i.e. rear axis center, and therefore defines sensor frame origin resp. the relative frame of the sensor.


Reference points
------------------

All position coordinates refer to the center of the bounding box of the object (vehicle or otherwise). This does not depend on the reference frame and is identical for all objects without exceptions.


Example: Position vectors of vehicles
---------------------------------------

A position vector consists of two points + orientation / coordinate system:

**start point**: This is the origin of the coordinate system. (i.e. sensor frame or world frame).

**end point**: often referred to as reference point. It is always the middle of the bounding box.

**orientation**: captured by the coordinate system. (i.e. sensor frame or world frame).

Open Simulation Interface uses DIN ISO 8855:2013-11 for coordinate systems and transformations between coordinate systems.