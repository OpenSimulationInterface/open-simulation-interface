// \file clock.h
// \brief Platform independent time stamp
//
// \author    Georg Seifert  <Georg.Seifert@carissma.eu>
// \version   0.1
// \date      2021
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, you can obtain one at http://mozilla.org/MPL/2.0/
//

#ifndef HIGH_PRECITION_CLOCK_H
#define HIGH_PRECITION_CLOCK_H

#ifdef __unix__ 
    #include <time.h>
    #include <stdint.h>
#elif _WIN32
    #include <windows.h>
    #include <stdint.h>
#else
    #error "OS not supported!"
#endif

// \brief Time stamp with nanoseconds resolution
//
// \return monotonic time stamp
//
static inline uint64_t clock_get_ns()
{
#ifdef __unix__ 
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ((uint64_t)(ts.tv_sec * 1000000000)) + (uint64_t)ts.tv_nsec;
#elif _WIN32
    LARGE_INTEGER ts, freq;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&ts);
    return ((uint64_t)(ts.QuadPart * 1000000000)) / (uint64_t)freq.QuadPart;
#else
    #error "OS not supported!"
#endif
}

#endif  // HIGH_PRECITION_CLOCK_H
