cmake_minimum_required(VERSION 3.7)

project(open_simulation_interface)
set(OPEN_SIMULATION_INTERFACE_VERSION 2.1.1s)

# Offer the user the choice of overriding the installation directories
set(INSTALL_LIB_DIR lib CACHE PATH "Installation directory for libraries")
set(INSTALL_INCLUDE_DIR include CACHE PATH "Installation directory for header files")
if(WIN32 AND NOT CYGWIN)
  set(DEF_INSTALL_CMAKE_DIR CMake)
else()
  set(DEF_INSTALL_CMAKE_DIR lib/CMake/${PROJECT_NAME})
endif()
set(INSTALL_CMAKE_DIR ${DEF_INSTALL_CMAKE_DIR} CACHE PATH
  "Installation directory for CMake files")

find_package(Protobuf 2.6.1 REQUIRED)

set(OSI_PROTO_FILES
    common.proto
    detected_landmark.proto
    detected_lane.proto
    detected_object.proto
    detected_occupant.proto
    environment.proto
    ground_truth.proto
    landmark.proto
    lane.proto
    low_level_data.proto
    model_internal.proto
    object.proto
    occupant.proto
    sensor_data_for_recording.proto
    sensor_data.proto
    sensor_specific_object_data.proto
)

protobuf_generate_cpp(PROTO_SRCS PROTO_HEADERS ${OSI_PROTO_FILES})

include_directories(
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)

add_library(${PROJECT_NAME} STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_link_libraries(${PROJECT_NAME} PUBLIC ${PROTOBUF_LIBRARY})
install(TARGETS ${PROJECT_NAME} 
	EXPORT ${PROJECT_NAME}_targets
	ARCHIVE DESTINATION "${INSTALL_LIB_DIR}" COMPONENT lib)
	
add_library(${PROJECT_NAME}_pic STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
set_property(TARGET ${PROJECT_NAME}_pic PROPERTY POSITION_INDEPENDENT_CODE ON)
target_link_libraries(${PROJECT_NAME}_pic PUBLIC ${PROTOBUF_LIBRARY})
install(TARGETS ${PROJECT_NAME}_pic
	EXPORT ${PROJECT_NAME}_targets
	ARCHIVE DESTINATION "${INSTALL_LIB_DIR}" COMPONENT lib)


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
	DESTINATION "${CMAKE_INSTALL_PREFIX}/${INSTALL_INCLUDE_DIR}/osi"
)

# Install the export set for use with the install-tree
install(EXPORT ${PROJECT_NAME}_targets
	DESTINATION "${INSTALL_CMAKE_DIR}" 
	COMPONENT dev)
