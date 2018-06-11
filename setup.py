#! python
# -*- coding: UTF-8 -*-

import os
import subprocess
import sys
from distutils.spawn import find_executable

from setuptools import setup, find_packages
from setuptools.command.install import install
import configparser

def convert_version_file():
    """ Convert OSI VERSION file python config (ini) file
    String '[VERSION]' is inseted as a first line
    """
    with open('VERSION','r') as f:
        with open('version.ini','w') as f2: 
            f2.write('[VERSION]\n')
            f2.write(f.read())

# Read OSI Version informations
convert_version_file()
config = configparser.ConfigParser()
config.read('version.ini')
version_major = config['VERSION']['VERSION_MAJOR']
version_minor = config['VERSION']['VERSION_MINOR']
version_patch = config['VERSION']['VERSION_PATCH']


# Define package name and package path
generated_dir_name = os.path.join(os.getcwd(),'osi3')

try:
    os.mkdir(generated_dir_name)
except Exception:
    pass

try:
    open(os.path.join(generated_dir_name, '__init__.py'), 'a').close()
except Exception:
    pass



# Modify write to osi_version.proto
with open("./osi3/osi_version.proto.in", "rt") as fin:
    with open("./osi3/osi_version.proto", "wt") as fout:
        for line in fin:
            lineConfigured = line.replace('@VERSION_MAJOR@',str(version_major))
            lineConfigured = lineConfigured.replace('@VERSION_MINOR@',str(version_minor))
            lineConfigured = lineConfigured.replace('@VERSION_PATCH@',str(version_patch))
            fout.write(lineConfigured)


class GenerateProtobuf(install):

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
                'Alternatively, you can point the PROTOC environment variable'
                'at a local version.')
            sys.exit(1)
        return protoc

    """ Generate Protobuf Messages """
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
        for source in self.osi_files:
            sys.stdout.write('Protobuf-compiling ' + source + '\n')
            subprocess.check_call([self.find_protoc(),
                                   '--proto_path=.',
                                   '--python_out=' + os.getcwd(),
                                   './osi3/' + source])
        install.run(self)

setup(
    name='open-simulation-interface',
    version=str(version_major)+'.'+str(version_minor)+'.'+str(version_patch),
    description='A generic interface for the environmental perception of'
    'automated driving functions in virtual scenarios.',
    author='Carlo van Driesten, Timo Hanke, Nils Hirsenkorn,'
    'Pilar Garcia-Ramos, Mark Schiementz, Sebastian Schneider',
    author_email='Carlo.van-Driesten@bmw.de, Timo.Hanke@bmw.de,'
    'Nils.Hirsenkorn@tum.de, Pilar.Garcia-Ramos@bmw.de,'
    'Mark.Schiementz@bmw.de, Sebastian.SB.Schneider@bmw.de',
    packages=find_packages(),
    install_requires=['protobuf'],
    cmdclass={
        'install': GenerateProtobuf,
    },
    url='https://github.com/OpenSimulationInterface/open-simulation-interface',
    license="MPL 2.0",
    classifiers=[
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    data_files=[
        ("",
         ["LICENSE"])])
