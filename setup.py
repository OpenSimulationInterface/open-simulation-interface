#! python
# -*- coding: UTF-8 -*-

import os
import subprocess
import sys
from distutils.spawn import find_executable

from setuptools import setup
from setuptools.command.install import install

package_name = 'osi'
package_path = os.path.join(os.getcwd(), package_name)


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

    osi_files = (
        'common.proto',
        'detected_landmark.proto',
        'detected_lane.proto',
        'detected_object.proto',
        'detected_occupant.proto',
        'environment.proto',
        'ground_truth.proto',
        'landmark.proto',
        'lane.proto',
        'low_level_data.proto',
        'model_internal.proto',
        'object.proto',
        'occupant.proto',
        'sensor_data_for_recording.proto',
        'sensor_data.proto',
        'sensor_specific_object_data.proto')

    """ Generate Protobuf Messages """

    def run(self):
        for source in self.osi_files:
            sys.stdout.write('Protobuf-compiling ' + source + '\n')
            subprocess.check_call([self.find_protoc(),
                                   '--proto_path=.',
                                   '--python_out=' + package_path,
                                   './' + source])

        install.run(self)

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
    version='2.0.1',
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
