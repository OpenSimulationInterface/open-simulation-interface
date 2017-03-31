cmake_minimum_required(VERSION 3.7)

# set name and version of the project 
project(open_simulation_interface)
set(VERSION_MAJOR 2)
set(VERSION_MINOR 2)
set(VERSION_PATCH 1)


find_package(Protobuf 2.6.1 REQUIRED)

set(OSI_PROTO_FILES
    osi_common.proto
    osi_datarecording.proto
    osi_detectedlandmark.proto
    osi_detectedlane.proto
    osi_detectedobject.proto
    osi_detectedoccupant.proto
    osi_environment.proto
    osi_groundtruth.proto
    osi_landmark.proto
    osi_lane.proto
    osi_lowleveldata.proto
    osi_modelinternal.proto
    osi_object.proto
    osi_occupant.proto
    osi_sensordata.proto
    osi_sensorspecific.proto
)

protobuf_generate_cpp(PROTO_SRCS PROTO_HEADERS ${OSI_PROTO_FILES})

add_library(${PROJECT_NAME}_static STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_include_directories(${PROJECT_NAME}_static
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(${PROJECT_NAME}_static PUBLIC ${PROTOBUF_LIBRARY})


add_library(${PROJECT_NAME}_obj OBJECT ${PROTO_SRCS} ${PROTO_HEADERS})
target_include_directories(${PROJECT_NAME}_obj
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
set_property(TARGET ${PROJECT_NAME}_obj PROPERTY POSITION_INDEPENDENT_CODE ON)


add_library(${PROJECT_NAME}_pic STATIC $<TARGET_OBJECTS:${PROJECT_NAME}_obj>)
target_include_directories(${PROJECT_NAME}_pic
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(${PROJECT_NAME}_pic PUBLIC ${PROTOBUF_LIBRARY})
set_property(TARGET ${PROJECT_NAME}_pic PROPERTY POSITION_INDEPENDENT_CODE ON)


add_library(${PROJECT_NAME} SHARED $<TARGET_OBJECTS:${PROJECT_NAME}_obj>)
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(${PROJECT_NAME} PUBLIC ${PROTOBUF_LIBRARY})


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