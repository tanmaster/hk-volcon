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
        return comtypes.CoCreateInstance(CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, comtypes.CLSCTX_INPROC_SERVER)


class WindowsVolumeChanger(VolumeChangerInterface):

    def __int__(self, logger=None):
        super.__init__(logger)
        self.old_volume = self.get_current_device_volume().GetMasterVolumeLevelScalar() * 100
        self.last_changed = time()

    @staticmethod
    def set_current_volume(target: int):
        pythoncom.CoInitialize()
        device_enumerator = MyAudioUtilities.get_device_enumerator()
        devices = device_enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, ERole.eMultimedia.value)
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        cast(interface, POINTER(IAudioEndpointVolume)).SetMasterVolumeLevelScalar(target / 100, None)

    @staticmethod
    def get_current_device_volume():
        pythoncom.CoInitialize()
        device_enumerator = MyAudioUtilities.get_device_enumerator()
        devices = device_enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, ERole.eMultimedia.value)
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume)).GetMasterVolumeLevelScalar() * 100
