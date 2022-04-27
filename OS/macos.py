from OS.interface import VolumeChangerInterface
import osascript


class MacintoshVolumeChanger(VolumeChangerInterface):

    @staticmethod
    def get_current_device_volume():
        result = osascript.osascript('get volume settings')
        vol_info = result[1].split(',')
        output_vol = vol_info[0].replace('output volume:', '')
        return int(output_vol)

    @staticmethod
    def set_current_volume(target: int):
        vol = "set volume output volume {}".format(target)
        osascript.osascript(vol)

    def __int__(self, logger=None):
        super.__init__(logger)
