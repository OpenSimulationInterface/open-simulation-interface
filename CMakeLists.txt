cmake_minimum_required(VERSION 3.7)

project(open_simulation_interface)

find_package(Protobuf 2.6.1 REQUIRED)

set(OSI_PROTO_FILES
    osi/common.proto
    osi/detected_landmark.proto
    osi/detected_lane.proto
    osi/detected_object.proto
    osi/detected_occupant.proto
    osi/environment.proto
    osi/ground_truth.proto
    osi/landmark.proto
    osi/lane.proto
    osi/low_level_data.proto
    osi/model_internal.proto
    osi/object.proto
    osi/occupant.proto
    osi/sensor_data_for_recording.proto
    osi/sensor_data.proto
    osi/sensor_specific_object_data.proto
)

protobuf_generate_cpp(PROTO_SRCS PROTO_HEADERS ${OSI_PROTO_FILES})

add_library(${PROJECT_NAME} STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(${PROJECT_NAME} PUBLIC ${PROTOBUF_LIBRARY})

add_library(${PROJECT_NAME}_pic STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
set_property(TARGET ${PROJECT_NAME}_pic PROPERTY POSITION_INDEPENDENT_CODE ON)
target_include_directories(${PROJECT_NAME}_pic
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(${PROJECT_NAME}_pic PUBLIC ${PROTOBUF_LIBRARY})
