#!/usr/local/env python3
# -*- coding: UTF-8 -*-

import os
import subprocess
import sys
import re
from distutils.spawn import find_executable

from setuptools import setup
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py

# protoc
from protoc import PROTOC_EXE

# configure the version number
VERSION_MAJOR = None
VERSION_MINOR = None
VERSION_PATCH = None
VERSION_SUFFIX = None
with open("VERSION", "rt") as versionin:
    for line in versionin:
        if line.startswith("VERSION_MAJOR"):
            VERSION_MAJOR = int(line.split("=")[1].strip())
        if line.startswith("VERSION_MINOR"):
            VERSION_MINOR = int(line.split("=")[1].strip())
        if line.startswith("VERSION_PATCH"):
            VERSION_PATCH = int(line.split("=")[1].strip())
        if line.startswith("VERSION_SUFFIX"):
            VERSION_SUFFIX = line.split("=")[1].strip()

package_name = "osi3"
package_path = os.path.join(os.getcwd(), package_name)


class ProtobufGenerator:
    @staticmethod
    def find_protoc():
        """Locates protoc executable"""

        if os.path.exists(PROTOC_EXE):
            protoc = PROTOC_EXE
        elif "PROTOC" in os.environ and os.path.exists(os.environ["PROTOC"]):
            protoc = os.environ["PROTOC"]
        else:
            protoc = find_executable("protoc")

        if protoc is None:
            sys.stderr.write(
                "protoc not found. Is protobuf-compiler installed? \n"
                "Alternatively, you can point the PROTOC environment variable "
                "to a local version."
            )
            sys.exit(1)
        return protoc

    osi_files = (
        "osi_common.proto",
        "osi_datarecording.proto",
        "osi_detectedlane.proto",
        "osi_detectedobject.proto",
        "osi_detectedoccupant.proto",
        "osi_detectedroadmarking.proto",
        "osi_detectedtrafficlight.proto",
        "osi_detectedtrafficsign.proto",
        "osi_environment.proto",
        "osi_featuredata.proto",
        "osi_groundtruth.proto",
        "osi_hostvehicledata.proto",
        "osi_lane.proto",
        "osi_logicaldetectiondata.proto",
        "osi_logicallane.proto",
        "osi_motionrequest.proto",
        "osi_object.proto",
        "osi_occupant.proto",
        "osi_referenceline.proto",
        "osi_roadmarking.proto",
        "osi_route.proto",
        "osi_sensordata.proto",
        "osi_sensorspecific.proto",
        "osi_sensorview.proto",
        "osi_sensorviewconfiguration.proto",
        "osi_streamingupdate.proto",
        "osi_trafficcommand.proto",
        "osi_trafficcommandupdate.proto",
        "osi_trafficlight.proto",
        "osi_trafficsign.proto",
        "osi_trafficupdate.proto",
        "osi_version.proto",
    )

    """ Generate Protobuf Messages """

    def generate(self):
        sys.stdout.write("Generating Protobuf Version Message\n")
        with open("osi_version.proto.in", "rt") as fin:
            with open("osi_version.proto", "wt") as fout:
                for line in fin:
                    lineConfigured = line.replace("@VERSION_MAJOR@", str(VERSION_MAJOR))
                    lineConfigured = lineConfigured.replace(
                        "@VERSION_MINOR@", str(VERSION_MINOR)
                    )
                    lineConfigured = lineConfigured.replace(
                        "@VERSION_PATCH@", str(VERSION_PATCH)
                    )
                    fout.write(lineConfigured)
        pattern = re.compile('^import "osi_')
        for source in self.osi_files:
            with open(source) as src_file:
                with open(os.path.join(package_path, source), "w") as dst_file:
                    for line in src_file:
                        dst_file.write(
                            pattern.sub('import "' + package_name + "/osi_", line)
                        )
        for source in self.osi_files:
            sys.stdout.write("Protobuf-compiling " + source + "\n")
            source_path = os.path.join(package_name, source)
            subprocess.check_call([self.find_protoc(), "--python_out=.", "--pyi_out=.", source_path])

    def maybe_generate(self):
        if os.path.exists("osi_version.proto.in"):
            self.generate()


class CustomBuildPyCommand(build_py):
    def run(self):
        ProtobufGenerator().maybe_generate()
        build_py.run(self)


class CustomSDistCommand(sdist):
    def run(self):
        ProtobufGenerator().generate()
        sdist.run(self)


try:
    os.mkdir(package_path)
except Exception:
    pass

try:
    with open(os.path.join(package_path, "__init__.py"), "wt") as init_file:
        init_file.write(
            f"__version__ = '{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}{VERSION_SUFFIX or ''}'\n"
        )
except Exception:
    pass

setup(
    version=str(VERSION_MAJOR)
    + "."
    + str(VERSION_MINOR)
    + "."
    + str(VERSION_PATCH)
    + (VERSION_SUFFIX or ""),
    packages=[package_name, "osi3trace"],
    cmdclass={
        "sdist": CustomSDistCommand,
        "build_py": CustomBuildPyCommand,
    },
)
