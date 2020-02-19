.. _iconventions:

Interface Conventions
======================

When adding new messages, enums, field messages and field enums to OSI we enforce a few naming conventions for each type like in the `style guide <https://developers.google.com/protocol-buffers/docs/style>`_ from protobuf.

Message Naming
---------------
A message definition should always be in camel case. This means that the first letter of each word in a message should be upper case without any spaces. See example below:

.. code-block:: protobuf

    message EnvironmentalConditions
    {
    }

Top-Level Messages
-------------------
All messages that are intended to be exchanged as a stand-alone message, i.e. not required to be embedded in another message, like e.g. ``SensorView`` or ``SensorViewConfiguration``, are required to carry an ``InterfaceVersion`` field as their first field, and a ``Timestamp`` field as their second field, e.g.:

.. code-block:: protobuf

    message TopLevel
    {
        // The interface version used by the sender (simulation environment).
        //
        optional InterfaceVersion version = 1;
        
        // The data timestamp of the simulation environment. Zero time is arbitrary
        // but must be identical for all messages. Zero time does not need to
        // coincide with the UNIX epoch. Recommended is the starting time point of
        // the simulation.
        //
        optional Timestamp timestamp = 2;
    }

Field Message Naming
---------------------
After defining a message fields can be added to it in snake case format. This means every letter is lower case and the words are connected through an underline character. See example below:

.. code-block:: protobuf

    message EnvironmentalConditions
    {
        optional double atmospheric_pressure = 1;
    }

Field Numbering
----------------

Fields should be numbered consecutively starting from 1 on first definition. During maintenance, the rules of backward/forward-compatibility require that fields are never renumbered, and field numbers never re-used unless a major release is performed.

All field numbers of 10000 and above are reserved for user-defined extensions and will thus never be used by OSI message fields.

Enum Naming
------------
The naming of an enum should be camel case. See example below:

.. code-block:: protobuf

    message EnvironmentalConditions
    {
        optional double atmospheric_pressure = 1;

        enum AmbientIllumination
        {
        }
    }

Enum Field Naming
------------
The naming of an enum field should be all in upper case. The start should be converted from the enum name camel case to upper case snake case. It is mandatory to add to the first enum field name the postfix ``_UNKNOWN`` and to the second the postfix ``_OTHER``. After that the naming can be decided by the user. It is often mentioned that the value ``_UNKNOWN`` should not be used in a ``GroundTruth`` message as there are now uncertanties by definition in ``the truth``. These values are mostly used in messages like ``SensorData`` where the content is subject to interpretation. See example below:

.. code-block:: protobuf

    message EnvironmentalConditions
    {
        optional double atmospheric_pressure = 1;

        enum AmbientIllumination
        {
            AMBIENT_ILLUMINATION_UNKNOWN = 0;
            
            AMBIENT_ILLUMINATION_OTHER = 1;

            AMBIENT_ILLUMINATION_LEVEL1 = 2;
        }
    }

Summary
--------
Here a small summary for the naming conventions:

Messages: camel case

Message Fields: snake case

Enum: camel case

Enum Fields: upper case, name of enum converted in upper case snake case and then following the specified name

After defining the messages do not forget to comment them. See also the `section for commenting <https://opensimulationinterface.github.io/osi-documentation/open-simulation-interface/doc/commenting.html>`_ of fields and messages.
