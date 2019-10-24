.. _versioning:

Versioning
=============

The version number is defined in ``InterfaceVersion::version_number`` in ``osi_common.proto`` as the field's default value.

`Link to Semantic Versioning <https://semver.org/>`_

**Major**: A change of the major version results in an incompatibility of code and recorded proto messages.

- An existing field with a number changes its meaning ``optional double field = 1;`` -> ``repeated double field = 1;`` Changing the definition of units or interpretation of a field
- Deleting a field and reusing the field number
- Changing the technology ProtoBuffer -> FlatBuffer

**Minor**: A change of the minor version indicates remaining compatibility to previously recorded files. The code on the other hand needs fixing.

- Renaming of a field without changing the field number
- Changing the names of messages
- Adding a new field in a message without changing the numbering of other fields

**Patch**: The compatibility of both recorded files and code remains.

- File or folder structure which does not affect including the code in other projects
- Changing or adding comments
- Clarification of text passages explaining the message content

