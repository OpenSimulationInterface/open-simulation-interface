cmake_minimum_required(VERSION 3.7)

project(open_simulation_interface)

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

include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

add_library(${PROJECT_NAME} STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_link_libraries(${PROJECT_NAME} PUBLIC ${PROTOBUF_LIBRARY})

add_library(${PROJECT_NAME}_pic STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_link_libraries(${PROJECT_NAME}_pic PUBLIC ${PROTOBUF_LIBRARY})

set_property(TARGET ${PROJECT_NAME}_pic PROPERTY POSITION_INDEPENDENT_CODE ON)
