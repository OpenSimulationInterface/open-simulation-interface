.. _commenting:

Commenting
===========

During the building process of open simulation interface (using the `proto2cpp <https://github.com/OpenSimulationInterface/proto2cpp>`_ filter), doxygen is creating a `reference documentation <https://opensimulationinterface.github.io/open-simulation-interface/>`_ processing all comments written in the code of the interface. In order to do that doxygen needs the comments to be written in a certain way. Please follow these rules to achieve that the reference documentation is created correctly. You will find further information on doxygen `here <http://www.doxygen.nl/manual/docblocks.html>`_.

For any additional comment styles see `list <http://www.doxygen.nl/manual/commands.html>`_ of doxygen commands.


Commenting with block syntax
-----------------------------
Start every comment with ``//`` and do not use ``///``.


Commenting on messages
------------------------
When writing comments specifying messages please use the following template:

.. code-block:: protobuf

    // <Add your single line comment like this>
    //
    message ExampleMessage
    {
    }

Doxygen will interpret a comment consisting just of one single line as a brief description.
However to keep the style of the documentation coherent there should not be any brief description when commenting on fields and enums. That is why adding one more empty line when commenting becomes necessary. There is no need for an extra empty line if you are commenting more than one line anyways.

.. code-block:: proto
    
    // <If you write two or more lines of comments...>
    // <... you do not need to add an empty line>
    message ExampleMessage
    {
    }

The commenting for messages follows the following order:

1. Brief description
2. Image
3. Detailed description
4. Note

First you define the message.

.. code-block:: protobuf

    message EnvironmentalConditions
    {
    }

Next provide a brief description of the message with ``\brief``.

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    message EnvironmentalConditions
    {
    }

Then you can optionally provide an image to explain the message better. A picture is worth a thousand words.

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    message EnvironmentalConditions
    {
    }

You can optionally add a detailed description which can have multiple lines.

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    message EnvironmentalConditions
    {
    }

Lastly you can add a small note about the message and have a completely commented message.

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    // \note These conditions apply locally around the host vehicle.
    //
    message EnvironmentalConditions
    {
    }

Commenting on fields and enums
--------------------------------
The commenting for fields and enums follows the following order:

1. Explanation
2. Unit
3. Note
4. Reference
5. Rule

First you add a field into a message with an appropriate index number.

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    // \note These conditions apply locally around the host vehicle.
    //
    message EnvironmentalConditions
    {
        optional double atmospheric_pressure = 1;
    }

    

Then you describe the field by adding an explanation. 

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    // \note These conditions apply locally around the host vehicle.
    //
    message EnvironmentalConditions
    {
        // Atmospheric pressure in Pascal at z=0.0 in world frame (about 101325 [Pa]).
        //
        optional double atmospheric_pressure = 1;
    }

Next you decide the unit of the field. 

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    // \note These conditions apply locally around the host vehicle.
    //
    message EnvironmentalConditions
    {
        // Atmospheric pressure in Pascal at z=0.0 in world frame (about 101325 [Pa]).
        //
        // Unit: [Pa]
        //
        optional double atmospheric_pressure = 1;
    }

You can optionally add a note to the field to describe the field better. 

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    // \note These conditions apply locally around the host vehicle.
    //
    message EnvironmentalConditions
    {
        // Atmospheric pressure in Pascal at z=0.0 in world frame (about 101325 [Pa]).
        //
        // Unit: [Pa]
        //
        // \note 100000 Pa = 1 bar
        //
        optional double atmospheric_pressure = 1;
    }

If you want to provide a reference to a DIN or to web page which helps in understanding the field you can add a reference.

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    // \note These conditions apply locally around the host vehicle.
    //
    message EnvironmentalConditions
    {
        // Atmospheric pressure in Pascal at z=0.0 in world frame (about 101325 [Pa]).
        //
        // Unit: [Pa]
        //
        // \note 100000 Pa = 1 bar
        //
        // \par Reference:
        // - [1] [Definition atmospheric pressure](https://en.wikipedia.org/wiki/Atmospheric_pressure)
        //
        optional double atmospheric_pressure = 1;
    }

Finally you can provide a set of rules which this field needs to be followed. The available rules can be found below. When adding rules to \*.proto files make sure that the rules are encapsulated between the ``\rules`` and ``\endrules`` tags. Now you have a fully commented message with a fully commented field.

.. code-block:: protobuf

    // \brief The conditions of the environment.
    //
    // \image html EnvironmentalConditions.svg
    //
    // Definition of light, weather conditions and other environmental conditions.
    //
    // \note These conditions apply locally around the host vehicle.
    //
    message EnvironmentalConditions
    {
        // Atmospheric pressure in Pascal at z=0.0 in world frame (about 101325 [Pa]).
        //
        // Unit: [Pa]
        //
        // \note 100000 Pa = 1 bar
        //
        // \par Reference:
        // - [1] [Definition atmospheric pressure](https://en.wikipedia.org/wiki/Atmospheric_pressure)
        //
        // \rules
        // is_optional
        // is_greater_than_or_equal_to: 90000
        // is_less_than_or_equal_to: 200000
        // \endrules
        //
        optional double atmospheric_pressure = 1;
    }


The rule definition must follow the syntax which is defined by a regex search which you can see below:

.. code-block:: python
    
    'is_greater_than':              r'\b(is_greater_than)\b: \d+(\.\d+)?'                                                   # is_greater_than: 1
    'is_greater_than_or_equal_to':  r'\b(is_greater_than_or_equal_to)\b: \d+(\.\d+)?'                                       # is_greater_than_or_equal_to: 1
    'is_less_than_or_equal_to':     r'\b(is_less_than_or_equal_to)\b: \d+(\.\d+)?'                                          # is_less_than_or_equal_to: 10
    'is_less_than':                 r'\b(is_less_than)\b: \d+(\.\d+)?'                                                      # is_less_than: 2
    'is_equal':                     r'\b(is_equal)\b: \d+(\.\d+)?'                                                          # is_equal: 1
    'is_different':                 r'\b(is_different)\b: \d+(\.\d+)?'                                                      # is_different: 2
    'is_global_unique':             r'\b(is_global_unique)\b'                                                               # is_global_unique
    'refers':                       r'\b(refers)\b'                                                                         # refers
    'is_iso_country_code':          r'\b(is_iso_country_code)\b'                                                            # is_iso_country_code
    'first_element':                r'\b(first_element)\b: \{.*: \d+\.\d+\}'                                                # first_element: {is_equal: 0.13, is_greater_than: 0.13}
    'last_element':                 r'\b(last_element)\b: \{.*: \d+\.\d+\}'                                                 # last_element: {is_equal: 0.13, is_greater_than: 0.13}
    'is_optional':                  r'\b(is_optional)\b'                                                                    # is_optional
    'check_if':                     r'\b(check_if)\b: \[\{.*: \d+(\.\d+)?, target: .*}, \{do_check: \{.*: \d+(\.\d+)?}}]'   # check_if: [{is_equal: 2, is_greater_than: 3, target: this.y}, {do_check: {is_equal: 1, is_less_than: 3}}]

You can check the correctness of these regular expression on `regex101 <https://regex101.com/r/6tomm6/16>`_.


.. is_greater_than: 2
.. is_greater_than: 2.23
.. is_greater_than_or_equal_to: 1
.. is_greater_than_or_equal_to: 1.12
.. is_less_than_or_equal_to: 10
.. is_less_than_or_equal_to: 10.123
.. is_less_than: 2
.. is_less_than: 2.321
.. is_equal: 1
.. is_equal: 1.312
.. is_different: 2
.. is_different: 2.2122
.. is_global_unique
.. refers
.. is_iso_country_code
.. first_element: {is_equal: 3, is_greater: 2}
.. first_element: {is_equal: 0.13, is_greater: 0.13}
.. last_element: {is_equal: 3, is_greater: 2}
.. last_element: {is_equal: 0.13, is_greater: 0.13}
.. check_if: [{is_equal: 2, is_greater_than: 3, target: this.y}, {do_check: {is_equal: 1, is_less_than: 3}}]
.. is_set
 

Commenting with doxygen references
------------------------------------
If you need to reference to another message etc., you can achieve that by just using the exact same name of this message (upper and lower case sensitive) in your comment and put '\c' in front of the message name.

.. code-block:: proto

    // A reference to \c GroundTruth message.

If you want to reference a nested message, use '::' instead of '.' as separators in comments.

If you want to reference message fields and enums add '#' to the enum/field name.

.. code-block:: proto

    // A reference to a enum e.g. \c #COLOR_GREEN.

Commenting with links
----------------------
With ``[<add name of your link>](<add url of your link>)`` you can integrate a link to a certain homepage while commenting.

Commenting with images
----------------------
To include images write your comment similar to this ``// \image html <Add name of your image> "<Add optional caption here>"``
Please place all your included images in ``./open-simulation-interface/docs/images``.

