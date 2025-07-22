cmake_minimum_required(VERSION 3.10)

project(open_simulation_interface_doc)

# read the version number from the file "VERSION"
file(STRINGS "VERSION" VERSION_CONTENTS)
foreach(LINE ${VERSION_CONTENTS})
  string(REGEX REPLACE " |\t" "" LINE ${LINE})
  string(REGEX MATCH "^[^=]+" VERSION_NAME ${LINE})
  string(REPLACE "${VERSION_NAME}=" "" VERSION_VALUE ${LINE})
  set(${VERSION_NAME} "${VERSION_VALUE}")
endforeach()

configure_file(osi_version.proto.in osi_version.proto)

# add a target to generate API documentation with Doxygen
# Dependencies: Doxygen and proto2cpp.py
find_package(Doxygen)
if(Doxygen_FOUND)
  set(FILTER_PROTO2CPP_PY_PATH CACHE PATH "directory to the filter proto2cpp.py")
  if(NOT EXISTS ${FILTER_PROTO2CPP_PY_PATH}/proto2cpp.py)
    message(WARNING "${FILTER_PROTO2CPP_PY_PATH}/proto2cpp.py could not be found.")
  else()
    set(doxyfile_in ${CMAKE_CURRENT_SOURCE_DIR}/doxygen_config.cmake.in)
    set(doxyfile ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)

    configure_file(${doxyfile_in} ${doxyfile} @ONLY)

    add_custom_target(api_doc ALL
      COMMAND ${DOXYGEN_EXECUTABLE} ${doxyfile}
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
  endif()
endif()
