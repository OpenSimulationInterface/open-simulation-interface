.. _commenting:

Commenting
===========

During the building process of open simulation interface (using the `proto2cpp <https://github.com/OpenSimulationInterface/proto2cpp>`_ filter), doxygen is creating a `reference documentation <https://opensimulationinterface.github.io/open-simulation-interface/>`_ processing all comments written in the code of the interface. In order to do that doxygen needs the comments to be written in a certain way. Please follow these rules to achieve that the reference documentation is created correctly. You will find further information on doxygen `here <http://www.doxygen.nl/manual/docblocks.html>`_.

For any additional comment styles see `list <http://www.doxygen.nl/manual/commands.html>`_ of doxygen commands.

Reference for writing values and units: ISO 80000-1:2013-08, Quantities and units – Part 1: General
Nice summary in German: `Rohde & Schwarz: Der korrekte Umgang mit Groessen, Einheiten und Gleichungen <https://karriere.rohde-schwarz.de/fileadmin/customer/downloads/PDF/Der_korrekte_Umgang_mit_Groessen_Einheiten_und_Gleichungen_bro_de_01.pdf>`_


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

.. code-block:: protobuf
    
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
        // Atmospheric pressure in Pascal at z = 0.0 m in world frame (about 101325 Pa).
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
        // Atmospheric pressure in Pascal at z = 0.0 m in world frame (about 101325 Pa).
        //
        // Unit: Pa
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
        // Atmospheric pressure in Pascal at z = 0.0 m in world frame (about 101325 Pa).
        //
        // Unit: Pa
        //
        // \note 100000 Pa = 1 bar
        //
        optional double atmospheric_pressure = 1;
    }

To help understanding the field, you should add a reference.
Every OSI message should be defined properly and should have a well cited reference.

**Citation style for different sources:**

- Within the text, the number system is used with the number of the source in brackets [#] for mentioning.
- We use the so called `"APA style" <https://apastyle.apa.org/>`_ from the American Psychological Association for referencing.
- In the references list, the number in brackets [#] is followed by a full citation.
- For writing the title in italic, use <em>title</em>.
- If the list contains more than one entry, add " \n " at the end of the line to create a line break within the list.
- Author names are written as <surname>, <initial(s)> like Authorname, A. A.
- Editor names are written as <initial(s)> <surname> like B. B. Editorname.
- Naming pages at the end is optional to enable finding in long texts or for direct citations.
- All citations should be primary citations. Sources like Wikipedia et al. are not allowed.
- Find filled-out examples under `https://apastyle.apa.org <https://apastyle.apa.org/style-grammar-guidelines/references/examples>`_ and in existing entries.
- The scheme of popular sources for the reference list is as follows (replace tags with corresponding values):

1. <author1>, <author2>, <author3> & <author4>. (<year>). Contribution in a compilation title. <em><Compilation Title></em>. <edition>. <page(s)>. <publisher>. <location>. <doi>. <page(s)>.

2. <author1>, <author2> & <author3>. (<year>). <em><book (monograph) title></em>. <edition>. <publisher>. <doi>. <page(s)>.

3. <author1> & <author2>. (<year>). <book chapter title>. In <editor1> & <editor2> (Eds.), <em><book title></em> (<page(s)>). <publisher>. <doi>. <page(s)>.

4. <author1> & <author2>. (<year>). <journal article title>. <em><journal title></em>. <page(s)>. <location>. <doi>. <page(s)>.

5. <author>. (<year>). <em><Phd thesis title></em>. Phd. thesis. <location>. <university>. <doi or url>. <page(s)>.

6. <author>. (<year>, <month> <day>). <em><internet article title></em>. Retrieved <month> <day>, <year>, from <url>.

7. <standarding organisation>. (<year>). <em><title of the standard></em>. (<standard identifier>). <location>.

8. <author>. (<year>). <em><patent title and id></em>. <location>. <organisation>.



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
        // Atmospheric pressure in Pascal at z = 0.0 m in world frame (about 101325 Pa) [1, 2].
        //
        // Unit: Pa
        //
        // \note 100000 Pa = 1 bar
        //
        // \par References:
        // [1] DIN Deutsches Institut fuer Normung e. V. (1982). <em>DIN 5031-3 Strahlungsphysik im optischen Bereich und Lichttechnik - Groessen, Formelzeichen und Einheiten der Lichttechnik</em>. (DIN 5031-3:1982-03). Berlin, Germany. \n
        // [2] Rapp, C. (2017). Grundlagen der Physik. In <em>Hydraulik fuer Ingenieure und Naturwissenschaftler</em> (pp.23-36). Springer Vieweg. Wiesbaden, Germany. https://doi.org/10.1007/978-3-658-18619-7_3. p. 105.
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
        // Atmospheric pressure in Pascal at z = 0.0 m in world frame (about 101325 Pa) [1, 2].
        //
        // Unit: Pa
        //
        // \note 100000 Pa = 1 bar
        //
        // \par References:
        // [1] DIN Deutsches Institut fuer Normung e. V. (1982). <em>DIN 5031-3 Strahlungsphysik im optischen Bereich und Lichttechnik - Groessen, Formelzeichen und Einheiten der Lichttechnik</em>. (DIN 5031-3:1982-03). Berlin, Germany. \n
        // [2] Rapp, C. (2017). Grundlagen der Physik. In <em>Hydraulik fuer Ingenieure und Naturwissenschaftler</em> (pp.23-36). Springer Vieweg. Wiesbaden, Germany. https://doi.org/10.1007/978-3-658-18619-7_3. p. 105.
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
    
    'is_greater_than':              r'^[ ]\b(is_greater_than)\b: ([\s\d]+)$'                # is_greater_than: 1
    'is_greater_than_or_equal_to':  r'^[ ]\b(is_greater_than_or_equal_to)\b: ([\s\d]+)$'    # is_greater_than_or_equal_to: 1
    'is_less_than_or_equal_to':     r'^[ ]\b(is_less_than_or_equal_to)\b: ([\s\d]+)$'       # is_less_than_or_equal_to: 10
    'is_less_than':                 r'^[ ]\b(is_less_than)\b: ([\s\d]+)$'                   # is_less_than: 2
    'is_equal':                     r'^[ ]\b(is_equal_to)\b: ([\s\d]+)$'                    # is_equal_to: 1
    'is_different':                 r'^[ ]\b(is_different_to)\b: ([\s\d]+)$'                # is_different_to: 2
    'is_global_unique':             r'^[ ]\b(is_globally_unique)\b'                         # is_globally_unique
    'refers':                       r'^[ ]\b(refers_to)\b'                                  # refers_to: DetectedObject
    'is_iso_country_code':          r'^[ ]\b(is_iso_country_code)\b'                        # is_iso_country_code
    'first_element':                r'^[ ]\b(first_element)\b'                              # first_element height is_equal_to 0.13
    'last_element':                 r'^[ ]\b(last_element)\b'                               # last_element width is_equal_to 0.13
    'check_if':                     r'^[ ](\bcheck_if\b)(.*\belse do_check\b)'              # check_if this.type is_equal_to 2 else do_check is_set

You can check the correctness of these regular expression on `regex101 <https://regex101.com/r/P4KeuO/1>`_.


Commenting with doxygen references
------------------------------------
If you need to reference to another message etc., you can achieve that by just using the exact same name of this message (upper and lower case sensitive) in your comment and put '\c' in front of the message name.

.. code-block:: protobuf

    // A reference to \c GroundTruth message.

If you want to reference a nested message, use '::' instead of '.' as separators in comments.

If you want to reference message fields and enums add '#' to the enum/field name.

.. code-block:: protobuf

    // A reference to a enum e.g. \c #COLOR_GREEN.

Commenting with links (e.g. in references)
------------------------------------------
With ``[<add name of your link>](<add url of your link>)`` you can integrate a link to a certain homepage while commenting.

Commenting with images
----------------------
To include images write your comment similar to this ``// \image html <Add name of your image> "<Add optional caption here>"``
Please place all your included images in ``./open-simulation-interface/docs/images``.

