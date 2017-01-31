Open Simulation Interface (OSI)
===============================

General description
-------------------
https://www.hot.ei.tum.de/forschung/automotive-veroeffentlichungen/


Global remarks
--------------
All fields in the interface are set to optional and required is not used. This has been done to allow backward
compatible changes in the field. Additionally, this is the default behavior in protobuf version 3 that does no longer
have the required type and therefore ensures update compatibility.
However, this does not mean that filling the field is optional. For the purpose of providing a complete interface, all
existing fields should be set, unless not setting a field carries a specific meaning as indicated in the accompanying
comment.


Fault injection: how-to
------------------------
Injection of pre-defined sensor errors should be handled by a specialized "fault injector" component that acts like a
sensor model component, i.e. it takes a SensorData message as input and returns a modified SensorData message as output.
Specific errors should be handled as follows:
-- Ghost objects / false positive: An additional SensorDataObject is added to the list of objects in SensorData.object
      with SensorDataObject.model_internal_object.ground_truth_type set to kTypeGhost.
-- False negative: The object is marked as not seen by the sensor by setting the property
      SensorDataObject.model_internal_object.is_seen to false. The implementation of field-of-view calculation modules
      should respect this flag and never reset an object marked as not-seen to seen.

	  
Versioning
----------
The version number is defined in InterfaceVersion::version_number in osi_common.proto as the field's default value.