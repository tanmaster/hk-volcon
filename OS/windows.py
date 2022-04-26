from time import time

from ctypes import cast, POINTER
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, EDataFlow, ERole, CLSID_MMDeviceEnumerator, \
    IMMDeviceEnumerator
import pythoncom

from OS.interface import VolumeChangerInterface

last_changed = time()
pythoncom.CoInitialize()


class MyAudioUtilities(AudioUtilities):
    @staticmethod
    def get_device_enumerator():
        return comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER)


class WindowsVolumeChanger(VolumeChangerInterface):

    def __int__(self, logger=None):
        super.__init__(logger)
        self.old_volume = self.get_current_device_volume().GetMasterVolumeLevelScalar() * 100
        self.last_changed = time()

    @staticmethod
    def get_current_device_volume():
        pythoncom.CoInitialize()
        device_enumerator = MyAudioUtilities.get_device_enumerator()
        devices = device_enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, ERole.eMultimedia.value)
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))

    def vol_switched(self, new_value):
        self.logger.info('=======>  light switched: {x}'.format(x=new_value))
        if time() - self.last_changed > 0.1:
            if new_value == 0:
                # Get current volume and store in a val, so we can recreate it later
                self.old_volume = self.get_current_device_volume().GetMasterVolumeLevelScalar() * 100
                self.vol_changed(0)
            else:
                self.vol_changed(self.old_volume)

    def vol_changed(self, new_value):
        self.logger.info('=======>  light changed: {x}'.format(x=new_value))
        self.last_changed = time()

        # Get default audio device using PyCAW
        # Get current volume
        self.get_current_device_volume().SetMasterVolumeLevelScalar(new_value / 100, None)
