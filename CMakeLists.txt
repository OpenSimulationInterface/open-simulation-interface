cmake_minimum_required(VERSION 3.7)

project(open_simulation_interface)

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

add_library(${PROJECT_NAME} STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(${PROJECT_NAME} PUBLIC ${PROTOBUF_LIBRARY})


add_library(${PROJECT_NAME}_pic STATIC ${PROTO_SRCS} ${PROTO_HEADERS})
target_include_directories(${PROJECT_NAME}_pic
    PUBLIC
        ${PROTOBUF_INCLUDE_DIR}
        ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(${PROJECT_NAME}_pic PUBLIC ${PROTOBUF_LIBRARY})


set_property(TARGET ${PROJECT_NAME}_pic PROPERTY POSITION_INDEPENDENT_CODE ON)
