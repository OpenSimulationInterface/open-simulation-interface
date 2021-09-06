// \file performance.cpp
// \brief Simple performance evaluation example
//
// Simple test application, which measures the execution time of different
// parts of the open simulation interface and the protobuf implementation.
//
// The regions of interests are the filling of the structure of a 
// OSI GroundTruth message, the serialization and the parsing process using
// the native C++ interfaces of protobuf.
//
// \author    Georg Seifert  <Georg.Seifert@carissma.eu>
// \version   0.1
// \date      2021
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, you can obtain one at http://mozilla.org/MPL/2.0/
//

#include <random>
#include <ctime>
#include <iostream>
#include <limits>
#include <unistd.h>
#include <osi3/osi_groundtruth.pb.h>
#include <osi3/osi_object.pb.h>
#include "clock.h"

// \def ITERATIONS
// Default number of iterations of the benchmark
//
#define ITERATIONS (1000)

// \def OBJECTS
// Default number of moving objects used to fill the structure
//
#define OBJECTS (10)

int main(int argc, char** argv)
{
    uint64_t start, stop;
    int c;
    size_t i, num_object, num_object_max = OBJECTS, num_iterations_max = ITERATIONS;
    size_t *ts_ser;
    size_t *ts_deser;
    size_t *ts_gen;

    std::mt19937 generator(time(0));
    std::uniform_real_distribution<> distribution(0.0, 1.0);

    while ((c = getopt(argc, argv, "o:i:h")) != -1) {
        switch (c) {
        case 'o':
            num_object_max = atoi(optarg);
            break;
        case 'i':
            num_iterations_max = atoi(optarg);
            break;
        case '?':
        case 'h':
            std::cout << "Argumente:" << std::endl << 
                          "\t-o <num>\tCount of the moving objects, default = " << OBJECTS << std::endl <<
                          "\t-i <num>\tIteration of the benchmark, default = " << ITERATIONS << std::endl;
            return 1;
        default:
            break;
        }
    }
    
    std::cout << "Iterationen: " << num_iterations_max << 
                 ", Moving Objects: " << num_object_max << std::endl;
    
    ts_ser = new size_t[num_iterations_max];
    ts_deser = new size_t[num_iterations_max];
    ts_gen = new size_t[num_iterations_max];

    for(i = 0; i < num_iterations_max; i++)
    {
        osi3::GroundTruth gt_ser = osi3::GroundTruth();
        osi3::GroundTruth gt_deser = osi3::GroundTruth();
        std::string output;
        
        start = clock_get_ns();
        for(num_object = 0; num_object < num_object_max; num_object++)
        {
            osi3::MovingObject *mo = gt_ser.add_moving_object();
            mo->set_type(osi3::MovingObject_Type_TYPE_VEHICLE);
            
            osi3::MovingObject_VehicleClassification* vehicle_classification = new osi3::MovingObject_VehicleClassification();
            vehicle_classification->set_type(osi3::MovingObject_VehicleClassification_Type_TYPE_SMALL_CAR);
            mo->set_allocated_vehicle_classification(vehicle_classification);
            
            osi3::Identifier * id = new osi3::Identifier();
            id->set_value(num_object);
            mo->set_allocated_id(id);

            osi3::BaseMoving* base = new osi3::BaseMoving();
            
            // length = 12.0m (StVZO 32, 3,1)
            // width = 2.55 (StVZO 32, 3.1)
            // height = 4.0 (STVZO 32, 2),
            osi3::Dimension3d* dimension = new osi3::Dimension3d();
            dimension->set_length(12.0 * distribution(generator));
            dimension->set_width(2.55 * distribution(generator));
            dimension->set_height(4.0 * distribution(generator));
            base->set_allocated_dimension(dimension);
            
            // position: x, h, z (-512 -- 512)
            osi3::Vector3d* position = new osi3::Vector3d();
            position->set_x(1024 * distribution(generator) - 512);
            position->set_y(1024 * distribution(generator) - 512);
            position->set_z(1024 * distribution(generator) - 512);
            base->set_allocated_position(position);

            // roll, pitch, yaw (0 -- 2pi)
            osi3::Orientation3d* orientation = new osi3::Orientation3d();
            orientation->set_roll(6.28 * distribution(generator));
            orientation->set_pitch(6.28 * distribution(generator));
            orientation->set_yaw(6.28 * distribution(generator));
            base->set_allocated_orientation(orientation);

            // velocity (-30 -- 100) 
            osi3::Vector3d* velocity = new osi3::Vector3d();
            velocity->set_x(130.0 * distribution(generator) - 20.0);
            velocity->set_y(130.0 * distribution(generator) - 20.0);
            velocity->set_z(130.0 * distribution(generator) - 20.0);
            base->set_allocated_velocity(velocity);

            // acceleration (-12 -- 10), based on Pkw-Pkw-Unfälle
            // https://doi.org/10.1007/978-3-8348-9974-3_12
            osi3::Vector3d* acceleration = new osi3::Vector3d();
            acceleration->set_x(22.0 * distribution(generator) - 12);
            acceleration->set_y(22.0 * distribution(generator) - 12);
            acceleration->set_z(22.0 * distribution(generator) - 12);
            base->set_allocated_acceleration(acceleration);

            mo->set_allocated_base(base);
        }
        stop = clock_get_ns();
        ts_gen[i] = stop - start;

        start = clock_get_ns();
        gt_ser.SerializeToString(&output);
        stop = clock_get_ns();
        ts_ser[i] = stop - start;

        start = clock_get_ns();
        gt_deser.ParseFromString(output);
        stop = clock_get_ns();
        ts_deser[i] = stop - start;
    }

    double min = std::numeric_limits<double>::max(), max = 0, mean = 0, variance = 0, stddev = 0;
    for(i = 0; i < num_iterations_max; i++)
    {
        min = (min > ts_gen[i]) ? ts_gen[i] : min;
        max = (max < ts_gen[i]) ? ts_gen[i] : max;
        mean += ts_gen[i];
        variance += ts_gen[i]*ts_gen[i];
    }
    mean /= num_iterations_max;
    variance = variance/num_iterations_max - mean*mean;
    stddev = sqrt( variance );
    std::cout << "Fill:" << std::endl << 
       "\tmin = " << min << " ns" << std::endl <<
       "\tmax = " << max << " ns" << std::endl <<
       "\tmean = " << mean << " ns" << std::endl << 
       "\tstandard deviation = " << stddev << " ns" << std::endl;

    min = std::numeric_limits<double>::max(), max = 0, mean=0, variance=0, stddev = 0;
    for(i=0; i < num_iterations_max; i++)
    {
        min = (min > ts_ser[i]) ? ts_ser[i] : min;
        max = (max < ts_ser[i]) ? ts_ser[i] : max;
        mean += ts_ser[i];
        variance += ts_ser[i]*ts_ser[i];
    }
    mean /= num_iterations_max;
    variance= variance/num_iterations_max - mean*mean;
    stddev = sqrt( variance );
    std::cout << "Serialize:" << std::endl << 
       "\tmin = " << min << " ns" << std::endl <<
       "\tmax = " << max << " ns" << std::endl <<
       "\tmean = " << mean << " ns" << std::endl << 
       "\tstandard deviation = " << stddev << " ns" << std::endl;
        
    min = std::numeric_limits<double>::max(), max = 0, mean = 0, variance = 0, stddev = 0;
    for(i = 0; i < num_iterations_max; i++)
    {
        min = (min > ts_deser[i]) ? ts_deser[i] : min;
        max = (max < ts_deser[i]) ? ts_deser[i] : max;
        mean += ts_deser[i];
        variance += ts_deser[i]*ts_deser[i];
    }
    mean /= num_iterations_max;
    variance = variance/num_iterations_max - mean*mean;
    stddev = sqrt( variance );
    std::cout << "Parse:" << std::endl << 
       "\tmin = " << min << " ns" << std::endl <<
       "\tmax = " << max << " ns" << std::endl <<
       "\tmean = " << mean << " ns" << std::endl << 
       "\tstandard deviation = " << stddev << " ns" << std::endl;

    delete [] ts_ser;
    delete [] ts_deser;
    delete [] ts_gen;
    return 0;
}
