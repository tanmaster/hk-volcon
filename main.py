#!/usr/bin/env python3

import argparse
import json
import logging
import os.path
import platform
import socket
from random import randint

from homekit import AccessoryServer
from homekit.model import Accessory
from homekit.model.characteristics import BrightnessCharacteristic
from homekit.model.services import LightBulbService

from OS.interface import VolumeChangerInterface

# setup logger
logger = logging.getLogger('accessory')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(filename)s:%(lineno)04d %(levelname)s %(message)s'))
logger.addHandler(ch)
logger.info('starting')


def setup_args_parser():
    parser = argparse.ArgumentParser(description='HomeKit volume control server')
    parser.add_argument('-f', action='store', required=False, dest='file', default='server.json',
                        help='File with the config data (defaults to ./server.json)')
    parser.add_argument('-n', action='store', required=False, dest='name',
                        default='hk-volcon', help='Display name of the server.')
    parser.add_argument('-p', action='store', required=False, dest='port',
                        default=56565, help='TCP port at which hk-volcon shall listen')
    parser.add_argument('-ip', action='store', required=False, dest='ip_address',
                        default=None, help='Override automatically detected IP address')
    return parser.parse_args()


def get_network_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def generate_mac():
    return "02:00:00:%02x:%02x:%02x" % (randint(0, 255), randint(0, 255), randint(0, 255))


def generate_pin():
    return '{:03d}-{:02d}-{:03d}'.format(randint(0, 999), randint(0, 99), randint(0, 999))


if __name__ == '__main__':
    args = setup_args_parser()

    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.file)
    if not os.path.exists(config_path):
        logger.info('Creating new server file at {}'.format(config_path))
        # set some config parameters and save it
        config_data = {
            'host_ip': get_network_ip() if args.ip_address is None else args.ip_address,
            'name': args.name,
            'accessory_pin': generate_pin(),
            'category': 'Lightbulb',
            'host_port': args.port,
            'accessory_pairing_id': generate_mac(),
            'c#': 0
        }
        logger.info('Your pin is {}'.format(config_data['accessory_pin']))
        json.dump(config_data, open(config_path, 'w'))

    # create a server and an accessory and run it until ctrl+c is hit
    try:
        httpd = AccessoryServer(config_path, logger)

        current_os = platform.system()
        # fill in whatever you like
        accessory = Accessory('PC Volume', 'tanmaster', current_os, '{:04d}'.format(randint(0, 9999)), '0.1')
        lightBulbService = LightBulbService()
        volume_changer: VolumeChangerInterface

        if current_os == 'Windows':
            from OS.windows import WindowsVolumeChanger
            volume_changer = WindowsVolumeChanger(logger)
        elif current_os == 'Linux':
            from OS.linux import LinuxVolumeChanger
            volume_changer = LinuxVolumeChanger(logger)
        elif current_os == 'Darwin':
            from OS.macos import MacintoshVolumeChanger
            volume_changer = MacintoshVolumeChanger(logger)
        else:
            logger.error('Unsupported OS')
            exit(-1)

        lightBulbService.set_on_set_callback(volume_changer.vol_switched)
        b_char = BrightnessCharacteristic(1)
        b_char.set_set_value_callback(volume_changer.vol_changed)

        lightBulbService.append_characteristic(b_char)
        accessory.services.append(lightBulbService)

        httpd.add_accessory(accessory)
        httpd.publish_device()
        logger.info('published device and start serving')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    logger.info('un-publish device')
    httpd.unpublish_device()
    httpd.shutdown()
