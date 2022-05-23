cmake_minimum_required(VERSION 3.5)

project(open_simulation_interface)

# Toplevel check
set(OSI_IS_TOP_LEVEL OFF)
if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  set(OSI_IS_TOP_LEVEL ON)
endif()

# Set the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optional Flatbuffer support
option(OSI_BUILD_FLATBUFFER "Build flatbuffer versions of libraries" OFF)
option(OSI_BUILD_DOCUMENTATION "Build flatbuffer versions of libraries" ${OSI_IS_TOP_LEVEL})

# Set a default build type if none was specified
set(default_build_type "Release")
if(EXISTS "${CMAKE_SOURCE_DIR}/.git")
  set(default_build_type "Debug")
endif()

# read the version number from the file "VERSION"
file(STRINGS "VERSION" VERSION_CONTENTS)
foreach(LINE ${VERSION_CONTENTS})
  string(REGEX REPLACE " |\t" "" LINE ${LINE})
  string(REGEX MATCH "^[^=]+" VERSION_NAME ${LINE})
  string(REPLACE "${VERSION_NAME}=" "" VERSION_VALUE ${LINE})
  set(${VERSION_NAME} "${VERSION_VALUE}")
endforeach()
set(OPEN_SIMULATION_INTERFACE_VERSION ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH})

set(${PROJECT_NAME}_SOVERSION "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}")
set(${PROJECT_NAME}_LIBVERSION "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}")

# configure build version
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
               "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Offer the user the choice of overriding the installation directories
set(OSI_INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(OSI_INSTALL_INCLUDE_DIR include CACHE PATH "Installation directory for header files")

if(WIN32 AND NOT CYGWIN)
  set(DEF_INSTALL_CMAKE_DIR CMake/${PROJECT_NAME}-${VERSION_MAJOR})
else()
  set(DEF_INSTALL_CMAKE_DIR lib/cmake/${PROJECT_NAME}-${VERSION_MAJOR})
endif()
set(OSI_INSTALL_CMAKE_DIR ${DEF_INSTALL_CMAKE_DIR} CACHE PATH "Installation directory for CMake files")

set(OSI_INSTALL_LIB_DIR ${OSI_INSTALL_LIB_DIR}/osi${VERSION_MAJOR})
set(OSI_INSTALL_INCLUDE_DIR ${OSI_INSTALL_INCLUDE_DIR}/osi${VERSION_MAJOR})

configure_file(osi_version.proto.in osi_version.proto)

find_package(Protobuf 2.6.1 REQUIRED)
set(PROTOBUF_IMPORT_DIRS ${PROTOBUF_INCLUDE_DIRS})

set(OSI_PROTO_FILES
    ${CMAKE_CURRENT_BINARY_DIR}/osi_version.proto
    osi_common.proto
    osi_datarecording.proto
    osi_detectedtrafficsign.proto
    osi_detectedtrafficlight.proto
    osi_detectedroadmarking.proto
    osi_detectedlane.proto
    osi_detectedobject.proto
    osi_detectedoccupant.proto
    osi_environment.proto
    osi_groundtruth.proto
    osi_hostvehicledata.proto
    osi_trafficsign.proto
    osi_trafficlight.proto
    osi_trafficupdate.proto
    osi_trafficcommand.proto
    osi_referenceline.proto
    osi_roadmarking.proto
    osi_lane.proto
    osi_logicallane.proto
    osi_featuredata.proto
    osi_logicaldetectiondata.proto
    osi_object.proto
    osi_occupant.proto
    osi_sensordata.proto
    osi_sensorviewconfiguration.proto
    osi_sensorspecific.proto
    osi_sensorview.proto
)

protobuf_generate_cpp(PROTO_SRCS PROTO_HEADERS ${OSI_PROTO_FILES})
set(FLAT_HEADERS "")
if(OSI_BUILD_FLATBUFFER)
  set(FLAT_FBS "")
  add_subdirectory("flatbuffers"
                   ${CMAKE_CURRENT_BINARY_DIR}/flatbuffers-build
                   EXCLUDE_FROM_ALL)
  file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/descriptor.fbs" "namespace osi3;")
  file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/include")
  list(APPEND FLAT_FBS "${CMAKE_CURRENT_BINARY_DIR}/descriptor.fbs")
  foreach (proto ${OSI_PROTO_FILES})
    get_filename_component(proto_base ${proto} NAME_WE)
    set(fbs "${proto_base}.fbs")
    add_custom_command(
      OUTPUT "${fbs}"
      COMMAND $<TARGET_FILE:flatc> -I "${PROTOBUF_IMPORT_DIRS}" -o "${CMAKE_CURRENT_BINARY_DIR}" --proto "${CMAKE_CURRENT_SOURCE_DIR}/${proto}"
      DEPENDS "${proto}" flatc
      WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
      COMMENT "Convert ${proto} to ${fbs} using flatc"
    )
    list(APPEND FLAT_FBS "${CMAKE_CURRENT_BINARY_DIR}/${fbs}")
  endforeach()

  foreach (flat ${FLAT_FBS})
    get_filename_component(flat_base ${flat} NAME_WE)
    set(fbs "${flat_base}.fbs")
    set(fbh "${flat_base}_generated.h")
    add_custom_command(
      OUTPUT "include/${fbh}"
      COMMAND $<TARGET_FILE:flatc> -o "${CMAKE_CURRENT_BINARY_DIR}/include" --cpp --gen-mutable --gen-name-strings --scoped-enums "${fbs}"
      DEPENDS "${FLAT_FBS}" flatc
      WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
      COMMENT "Process ${fbs} to ${fbh} using flatc"
    )
    list(APPEND FLAT_HEADERS "${CMAKE_CURRENT_BINARY_DIR}/include/${fbh}")
  endforeach()

  add_custom_target(${PROJECT_NAME}_fbs_build ALL DEPENDS "${FLAT_HEADERS}")
  add_library(${PROJECT_NAME}_fbs INTERFACE)
  target_include_directories(${PROJECT_NAME}_fbs INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include/>)
  target_include_directories(${PROJECT_NAME}_fbs SYSTEM INTERFACE $<INSTALL_INTERFACE:$<INSTALL_PREFIX>/include>)
  target_link_libraries(${PROJECT_NAME}_fbs INTERFACE flatbuffers)
endif()

add_library(${PROJECT_NAME}_static STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
add_library(${PROJECT_NAME}::${PROJECT_NAME}_static ALIAS ${PROJECT_NAME}_static)
target_include_directories(${PROJECT_NAME}_static
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${OSI_INSTALL_INCLUDE_DIR}>
)
target_link_libraries(${PROJECT_NAME}_static PUBLIC ${PROTOBUF_LIBRARY})
install(TARGETS ${PROJECT_NAME}_static
        EXPORT ${PROJECT_NAME}_targets
        ARCHIVE DESTINATION "${OSI_INSTALL_LIB_DIR}" COMPONENT lib)


add_library(${PROJECT_NAME}_obj OBJECT ${PROTO_SRCS} ${PROTO_HEADERS})
add_library(${PROJECT_NAME}::${PROJECT_NAME}_obj ALIAS ${PROJECT_NAME}_obj)
target_include_directories(${PROJECT_NAME}_obj
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${OSI_INSTALL_INCLUDE_DIR}>
)
set_property(TARGET ${PROJECT_NAME}_obj PROPERTY POSITION_INDEPENDENT_CODE ON)


add_library(${PROJECT_NAME}_pic STATIC $<TARGET_OBJECTS:${PROJECT_NAME}_obj>)
add_library(${PROJECT_NAME}::${PROJECT_NAME}_pic ALIAS ${PROJECT_NAME}_pic)
target_include_directories(${PROJECT_NAME}_pic
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${OSI_INSTALL_INCLUDE_DIR}>
)
target_link_libraries(${PROJECT_NAME}_pic PUBLIC ${PROTOBUF_LIBRARY})

set_property(TARGET ${PROJECT_NAME}_pic PROPERTY POSITION_INDEPENDENT_CODE ON)

install(TARGETS ${PROJECT_NAME}_pic
        EXPORT ${PROJECT_NAME}_targets
        ARCHIVE DESTINATION "${OSI_INSTALL_LIB_DIR}" COMPONENT lib)

add_library(${PROJECT_NAME} SHARED $<TARGET_OBJECTS:${PROJECT_NAME}_obj>)
add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${OSI_INSTALL_INCLUDE_DIR}>
)

set_property(
    TARGET ${PROJECT_NAME}
    PROPERTY SOVERSION ${${PROJECT_NAME}_SOVERSION}
)
set_property(
    TARGET ${PROJECT_NAME}
    PROPERTY VERSION ${${PROJECT_NAME}_LIBVERSION}
)

target_link_libraries(${PROJECT_NAME} PUBLIC ${PROTOBUF_LIBRARY})
install(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}_targets
        DESTINATION "${OSI_INSTALL_LIB_DIR}" COMPONENT lib)

# Copy proto headers to where they are expected by the package config file
add_custom_command(
    TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory
    ${CMAKE_CURRENT_BINARY_DIR}/${OSI_INSTALL_INCLUDE_DIR}
    COMMAND ${CMAKE_COMMAND} -E copy
    ${PROTO_HEADERS}
    ${CMAKE_CURRENT_BINARY_DIR}/${OSI_INSTALL_INCLUDE_DIR})

# Create the package config files
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/open_simulation_interface-config-version.cmake"
    VERSION ${OPEN_SIMULATION_INTERFACE_VERSION}
    COMPATIBILITY SameMajorVersion
)

export(EXPORT ${PROJECT_NAME}_targets
    FILE "${CMAKE_CURRENT_BINARY_DIR}/open_simulation_interface-targets.cmake"
    NAMESPACE ${PROJECT_NAME}::
)

configure_package_config_file(open_simulation_interface-config.cmake.in
    "${CMAKE_CURRENT_BINARY_DIR}/open_simulation_interface-config.cmake"
    INSTALL_DESTINATION ${OSI_INSTALL_CMAKE_DIR}
    PATH_VARS OSI_INSTALL_INCLUDE_DIR
    NO_CHECK_REQUIRED_COMPONENTS_MACRO
)

# Install the *cmake files
install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/open_simulation_interface-config.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/open_simulation_interface-config-version.cmake"
    DESTINATION "${OSI_INSTALL_CMAKE_DIR}"
    COMPONENT dev)

# Header files
install(FILES ${PROTO_HEADERS} ${FLAT_HEADERS}
        DESTINATION "${OSI_INSTALL_INCLUDE_DIR}")

# Install the export set for use with the install-tree
install(EXPORT ${PROJECT_NAME}_targets
    FILE open_simulation_interface-targets.cmake
    NAMESPACE ${PROJECT_NAME}::
    DESTINATION "${OSI_INSTALL_CMAKE_DIR}"
    COMPONENT dev)

if(OSI_BUILD_DOCUMENTATION)
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
endif()
