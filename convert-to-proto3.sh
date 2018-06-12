#!/bin/sh

# This shell script converts all proto files to proto3 syntax, which can
# then be used as a stand in for the proto2 syntax files. The resulting
# on-the-wire format should be compatible with the proto2-based formats
# in all respects.
#
# Call this script prior to building normally if you want/need to use
# proto3 syntax, e.g. for language bindings that do not support proto2,
# like C#.

test -f osi_version.proto && rm osi_version.proto

for f in osi_version.proto.in osi_*.proto
do
    mv $f $f.pb2 && sed -e 's/syntax *= *"proto2";/syntax = "proto3";/' -e 's/^\([ \t]*\)optional /\1/' $f.pb2 > $f
done

mv CMakeLists.txt CMakeLists.txt.pb2 && sed -e 's/find_package(Protobuf 2.6.1 REQUIRED)/find_package(Protobuf 3.0.0 REQUIRED)/' CMakeLists.txt.pb2 > CMakeLists.txt
