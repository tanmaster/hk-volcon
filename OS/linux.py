import alsaaudio
from OS.interface import VolumeChangerInterface


class LinuxVolumeChanger(VolumeChangerInterface):
    @staticmethod
    def get_current_device_volume():
        print(alsaaudio.mixers())
        print(alsaaudio.PCM(alsaaudio.PCM_PLAYBACK))
        print(alsaaudio.Mixer().mixerid())
        m = alsaaudio.Mixer()
        return m.getvolume()[0]

    @staticmethod
    def set_current_volume(target: int):
        m = alsaaudio.Mixer()
        m.setvolume(target)

    def __int__(self, logger=None):
        super.__init__(logger)
