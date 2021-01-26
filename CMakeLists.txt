cmake_minimum_required(VERSION 3.5)

project(open_simulation_interface)

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
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_INCLUDE_DIR include CACHE PATH "Installation directory for header files")

if(WIN32 AND NOT CYGWIN)
  set(DEF_INSTALL_CMAKE_DIR CMake/${PROJECT_NAME}-${VERSION_MAJOR})
else()
  set(DEF_INSTALL_CMAKE_DIR lib/cmake/${PROJECT_NAME}-${VERSION_MAJOR})
endif()
set(INSTALL_CMAKE_DIR ${DEF_INSTALL_CMAKE_DIR} CACHE PATH
    "Installation directory for CMake files")

set(INSTALL_LIB_DIR ${INSTALL_LIB_DIR}/osi${VERSION_MAJOR})
set(INSTALL_INCLUDE_DIR ${INSTALL_INCLUDE_DIR}/osi${VERSION_MAJOR})

configure_file(osi_version.proto.in ${CMAKE_CURRENT_SOURCE_DIR}/osi_version.proto)

find_package(Protobuf 2.6.1 REQUIRED)
set(PROTOBUF_IMPORT_DIRS ${PROTOBUF_INCLUDE_DIRS})

set(OSI_PROTO_FILES
    osi_version.proto
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
    osi_roadmarking.proto
    osi_lane.proto
    osi_featuredata.proto
    osi_object.proto
    osi_occupant.proto
    osi_sensordata.proto
    osi_sensorviewconfiguration.proto
    osi_sensorspecific.proto
    osi_sensorview.proto
)

protobuf_generate_cpp(PROTO_SRCS PROTO_HEADERS ${OSI_PROTO_FILES})

add_library(${PROJECT_NAME}_static STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_include_directories(${PROJECT_NAME}_static
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${INSTALL_INCLUDE_DIR}>
)
target_link_libraries(${PROJECT_NAME}_static PUBLIC ${PROTOBUF_LIBRARY})
install(TARGETS ${PROJECT_NAME}_static
        EXPORT ${PROJECT_NAME}_targets
        ARCHIVE DESTINATION "${INSTALL_LIB_DIR}" COMPONENT lib)


add_library(${PROJECT_NAME}_obj OBJECT ${PROTO_SRCS} ${PROTO_HEADERS})
target_include_directories(${PROJECT_NAME}_obj
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${INSTALL_INCLUDE_DIR}>
)
set_property(TARGET ${PROJECT_NAME}_obj PROPERTY POSITION_INDEPENDENT_CODE ON)


add_library(${PROJECT_NAME}_pic STATIC $<TARGET_OBJECTS:${PROJECT_NAME}_obj>)

target_include_directories(${PROJECT_NAME}_pic
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${INSTALL_INCLUDE_DIR}>
)
target_link_libraries(${PROJECT_NAME}_pic PUBLIC ${PROTOBUF_LIBRARY})

set_property(TARGET ${PROJECT_NAME}_pic PROPERTY POSITION_INDEPENDENT_CODE ON)

install(TARGETS ${PROJECT_NAME}_pic
        EXPORT ${PROJECT_NAME}_targets
        ARCHIVE DESTINATION "${INSTALL_LIB_DIR}" COMPONENT lib)

add_library(${PROJECT_NAME} SHARED $<TARGET_OBJECTS:${PROJECT_NAME}_obj>)
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:${INSTALL_INCLUDE_DIR}>
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
        DESTINATION "${INSTALL_LIB_DIR}" COMPONENT lib)

# Create the open_simulation_interface.cmake and open_simulation_interface-version files

# ... for the build tree
set(CONF_INCLUDE_DIRS "${PROJECT_SOURCE_DIR}" "${PROJECT_BINARY_DIR}")
configure_file(open_simulation_interface-config.cmake.in
               "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake" @ONLY)
# ... for the install tree
set(CONF_INCLUDE_DIRS ${CMAKE_INSTALL_PREFIX}/${INSTALL_INCLUDE_DIR} ${PROTOBUF_INCLUDE_DIR})
configure_file(open_simulation_interface-config.cmake.in
               "${PROJECT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/open_simulation_interface-config.cmake" @ONLY)
# ... for both
configure_file(open_simulation_interface-config-version.cmake.in
               "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake" @ONLY)

# Install the *cmake files
install(FILES
        "${PROJECT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/open_simulation_interface-config.cmake"
        "${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake"
        DESTINATION "${INSTALL_CMAKE_DIR}"
        COMPONENT dev)

# Header files
install(FILES ${PROTO_HEADERS}
        DESTINATION "${INSTALL_INCLUDE_DIR}")

# Install the export set for use with the install-tree
install(EXPORT ${PROJECT_NAME}_targets
        DESTINATION "${INSTALL_CMAKE_DIR}"
        COMPONENT dev)

# add a target to generate API documentation with Doxygen
# Dependencies: Doxygen and proto2cpp.py
FIND_PACKAGE(Doxygen)
set(FILTER_PROTO2CPP_PY_PATH CACHE PATH "directory to the filter proto2cpp.py")

if(NOT DOXYGEN_FOUND)

    message(WARNING  "Doxygen could not be found.")

else()

    if(NOT EXISTS ${FILTER_PROTO2CPP_PY_PATH}/proto2cpp.py)

    message(WARNING  "${FILTER_PROTO2CPP_PY_PATH}/proto2cpp.py could not be found.")

    else()

        set(doxyfile_in ${CMAKE_CURRENT_SOURCE_DIR}/doxygen_config.cmake.in)
        set(doxyfile ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)

        configure_file(${doxyfile_in} ${doxyfile} @ONLY)

        ADD_CUSTOM_TARGET(api_doc ALL
        COMMAND ${DOXYGEN_EXECUTABLE} ${doxyfile}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

    endif(NOT EXISTS ${FILTER_PROTO2CPP_PY_PATH}/proto2cpp.py)

endif(NOT DOXYGEN_FOUND)
