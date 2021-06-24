#!/usr/bin/env python3

#
# Copyright 2018 Joachim Lusiardi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import logging
import os.path
from ctypes import cast, POINTER
from time import time
import comtypes
from comtypes import CLSCTX_ALL
from homekit import AccessoryServer
from homekit.model import Accessory
from homekit.model.characteristics import BrightnessCharacteristic
from homekit.model.services import LightBulbService
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, EDataFlow, ERole, CLSID_MMDeviceEnumerator, \
    IMMDeviceEnumerator

import pythoncom
pythoncom.CoInitialize()

# setup logger
logger = logging.getLogger('accessory')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(filename)s:%(lineno)04d %(levelname)s %(message)s'))
logger.addHandler(ch)
logger.info('starting')

last_changed = time()


class MyAudioUtilities(AudioUtilities):
    @staticmethod
    def GetDeviceEnumerator():
        return comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER)


def get_current_device_volume():
    pythoncom.CoInitialize()
    deviceEnumerator = MyAudioUtilities.GetDeviceEnumerator()
    devices = deviceEnumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, ERole.eMultimedia.value)
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


oldValue = get_current_device_volume().GetMasterVolumeLevelScalar() * 100


def vol_switched(new_value):
    global oldValue, last_changed
    logger.info('=======>  light switched: {x}'.format(x=new_value))
    if time() - last_changed > 0.1:
        if new_value == 0:
            # Get current volume and store in a val, so we can recreate it later
            oldValue = get_current_device_volume().GetMasterVolumeLevelScalar() * 100
            vol_changed(0)
        else:
            vol_changed(oldValue)


def vol_changed(new_value):
    global last_changed
    logger.info('=======>  light changed: {x}'.format(x=new_value))
    last_changed = time()
    # Get default audio device using PyCAW
    # Get current volume
    get_current_device_volume().SetMasterVolumeLevelScalar(new_value / 100, None)


def setup_args_parser():
    parser = argparse.ArgumentParser(description='HomeKit demo server')
    parser.add_argument('-f', action='store', required=False, dest='file',
                        default='./demoserver.json',
                        help='File with the config data (defaults to ./demoserver.json)')
    return parser.parse_args()


if __name__ == '__main__':
    args = setup_args_parser()

    config_file = "{}//{}".format(os.path.dirname(os.path.realpath(__file__)), args.file)

    # create a server and an accessory an run it unless ctrl+c was hit
    try:
        httpd = AccessoryServer(config_file, logger)

        # fill in whatever you like
        accessory = Accessory('PC Volume', 'tanmaster', 'PC', '0001', '0.1')
        lightBulbService = LightBulbService()

        lightBulbService.set_on_set_callback(vol_switched)
        bchar = BrightnessCharacteristic(1)
        bchar.set_set_value_callback(vol_changed)

        lightBulbService.append_characteristic(bchar)

        accessory.services.append(lightBulbService)
        httpd.add_accessory(accessory)

        httpd.publish_device()

        logger.info('published device and start serving')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    # unpublish the device and shut down
    logger.info('unpublish device')
    httpd.unpublish_device()
    httpd.shutdown()
