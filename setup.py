#!/usr/local/env python3
# -*- coding: UTF-8 -*-

import os
import subprocess
import sys
import re
from distutils.spawn import find_executable

from setuptools import setup
from setuptools.command.build_py import build_py

# configure the version number
from shutil import copyfile
copyfile('VERSION', 'version.py')
from version import *
with open("osi_version.proto.in", "rt") as fin:
    with open("osi_version.proto", "wt") as fout:
        for line in fin:
            lineConfigured = line.replace('@VERSION_MAJOR@',str(VERSION_MAJOR))
            lineConfigured = lineConfigured.replace('@VERSION_MINOR@',str(VERSION_MINOR))
            lineConfigured = lineConfigured.replace('@VERSION_PATCH@',str(VERSION_PATCH))
            fout.write(lineConfigured)

package_name = 'osi3'
package_path = os.path.join(os.getcwd(), package_name)

class GenerateProtobufCommand(build_py):

    @staticmethod
    def find_protoc():
        """Locates protoc executable"""

        if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
            protoc = os.environ['PROTOC']
        else:
            protoc = find_executable('protoc')

        if protoc is None:
            sys.stderr.write(
                'protoc not found. Is protobuf-compiler installed? \n'
                'Alternatively, you can point the PROTOC environment variable '
                'to a local version.')
            sys.exit(1)
        return protoc

    osi_files = (
        'osi_version.proto',
        'osi_common.proto',
        'osi_datarecording.proto',
        'osi_detectedtrafficsign.proto',
        'osi_detectedtrafficlight.proto',
        'osi_detectedroadmarking.proto',
        'osi_detectedobject.proto',
        'osi_detectedoccupant.proto',
        'osi_detectedlane.proto',
        'osi_environment.proto',
        'osi_groundtruth.proto',
        'osi_hostvehicledata.proto',
        'osi_trafficsign.proto',
        'osi_trafficlight.proto',
        'osi_trafficupdate.proto',
        'osi_roadmarking.proto',
        'osi_featuredata.proto',
        'osi_object.proto',
        'osi_occupant.proto',
        'osi_lane.proto',
        'osi_sensordata.proto',
        'osi_sensorviewconfiguration.proto',
        'osi_sensorspecific.proto',
        'osi_sensorview.proto')

    """ Generate Protobuf Messages """

    def run(self):
        pattern = re.compile('^import "osi_')
        for source in self.osi_files:
            with open(source) as src_file:
                with open(os.path.join(package_path, source),"w") as dst_file:
                    for line in src_file:
                        dst_file.write(pattern.sub('import "' + package_name + '/osi_',line))
        for source in self.osi_files:
            sys.stdout.write('Protobuf-compiling ' + source + '\n')
            source_path = os.path.join(package_name, source)
            subprocess.check_call([self.find_protoc(),
                                   '--python_out=.',
                                   source_path])

        build_py.run(self)

try:
    os.mkdir(package_path)
except Exception:
    pass

try:
    open(os.path.join(package_path, '__init__.py'), 'a').close()
except Exception:
    pass

setup(
    name='open-simulation-interface',
    version=str(VERSION_MAJOR)+'.'+str(VERSION_MINOR)+'.'+str(VERSION_PATCH),
    description='A generic interface for the environmental perception of'
    'automated driving functions in virtual scenarios.',
    author='Carlo van Driesten, Timo Hanke, Nils Hirsenkorn,'
    'Pilar Garcia-Ramos, Mark Schiementz, Sebastian Schneider',
    author_email='Carlo.van-Driesten@bmw.de, Timo.Hanke@bmw.de,'
    'Nils.Hirsenkorn@tum.de, Pilar.Garcia-Ramos@bmw.de,'
    'Mark.Schiementz@bmw.de, Sebastian.SB.Schneider@bmw.de',
    packages=[package_name],
    install_requires=['protobuf'],
    cmdclass={
        'build_py': GenerateProtobufCommand,
    },
    url='https://github.com/OpenSimulationInterface/open-simulation-interface',
    license="MPL 2.0",
    classifiers=[
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    data_files=[
        ("",
         ["LICENSE"])])
