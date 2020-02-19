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

Field Message Naming
---------------------
After defining a message fields can be added to it in snake case format. This means every letter is lower case and the words are connected through an underline character. See example below:

.. code-block:: protobuf

    message EnvironmentalConditions
    {
        optional double atmospheric_pressure = 1;
    }

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
The naming of an enum field should be all in upper case. The start should be converted from the enum name camel case to upper case snake case. It is mandatory to have as a first enum field name the name ``_UNKNOWN`` and as the second the name ``_OTHER`` attached to it. After that the naming can be decided by the user. See example below:

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
