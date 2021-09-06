"""
\brief Simple performance evaluation example

Simple test application, which measures the execution time of different
parts of the open simulation interface and the protobuf implementation.

The regions of interests are the filling of the structure of a 
OSI GroundTruth message, the serialization and the parsing process using
the native Python interfaces of protobuf.

\author    Georg Seifert  <Georg.Seifert@carissma.eu>
\version   0.1
\date      2021

This Source Code Form is subject to the terms of the Mozilla
Public License v. 2.0. If a copy of the MPL was not distributed
with this file, you can obtain one at http://mozilla.org/MPL/2.0/
"""

import time
import random
import statistics
import argparse
import osi_groundtruth_pb2
import osi_object_pb2

## Default number of iterations of the benchmark
ITERATIONS = 1000

## Default number of moving objects used to fill the structure
OBJECTS = 10

if __name__ == "__main__":
    ts_ser = list()
    ts_deser = list()
    ts_gen = list()
    
    out = """{}:
\tmin = {} ns
\tmax = {} ns
\tmean = {} ns
\tstandard deviation = {} ns
"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--iterations",
        "-i",
        help="Iteration of the benchmark",
        default=ITERATIONS,
        type=int,
        required=False,
    )
    parser.add_argument(
        "--moving_objects",
        "-o",
        help="Count of the moving objects",
        default=OBJECTS,
        type=int,
        required=False,
    )
    args = parser.parse_args()
    iterations = args.iterations
    objects = args.moving_objects

    print("Iterationen: {} , Moving Objects: {}".format(iterations, objects))

    for i in range(iterations):
        gt_ser = osi_groundtruth_pb2.GroundTruth()
        gt_des = osi_groundtruth_pb2.GroundTruth()

        start = time.perf_counter_ns()
        for object in range(objects):
            mo = gt_ser.moving_object.add()
            mo.id.value = object
            mo.type = osi_object_pb2.MovingObject.TYPE_VEHICLE
            mo.vehicle_classification.type = osi_object_pb2.MovingObject.VehicleClassification.TYPE_SMALL_CAR
            mo.base.dimension.length = random.uniform(0, 12.0)
            mo.base.dimension.width = random.uniform(0, 2.55)
            mo.base.dimension.height = random.uniform(0, 4.0)
            mo.base.position.x = random.uniform(-512, 512)
            mo.base.position.y = random.uniform(-512, 512)
            mo.base.position.z = random.uniform(-512, 512)

            mo.base.orientation.roll = random.uniform(0, 6.28)
            mo.base.orientation.pitch = random.uniform(0, 6.28)
            mo.base.orientation.yaw = random.uniform(0, 6.28)
            mo.base.velocity.x = random.uniform(-20, 110)
            mo.base.velocity.y = random.uniform(-20, 110)
            mo.base.velocity.z = random.uniform(-20, 110)

            mo.base.acceleration.x = random.uniform(-12, 10)
            mo.base.acceleration.y = random.uniform(-12, 10)
            mo.base.acceleration.z = random.uniform(-12, 10)
        stop = time.perf_counter_ns()
        ts_gen.append(stop-start)

        start = time.perf_counter_ns()
        data = gt_ser.SerializeToString()
        stop = time.perf_counter_ns()
        ts_ser.append(stop-start)

        start = time.perf_counter_ns()
        gt_des.ParseFromString(data)
        stop = time.perf_counter_ns()
        ts_deser.append(stop-start)

    print(out.format("Fill", min(ts_gen), max(ts_gen),
                     statistics.mean(ts_gen), statistics.stdev(ts_gen)))
    print(out.format("Serialize", min(ts_ser), max(ts_ser),
                     statistics.mean(ts_ser), statistics.stdev(ts_ser)))
    print(out.format("Parse", min(ts_deser), max(ts_deser),
                     statistics.mean(ts_deser), statistics.stdev(ts_deser)))
