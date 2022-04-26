from OS.interface import VolumeChangerInterface
from time import time
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

        self.old_volume = self.get_current_device_volume()
        self.last_changed = time()

    def vol_switched(self, new_value: int):
        self.logger.info('=======>  light changed: {x}'.format(x=new_value))
        # since both vol_switched and vol_changed are triggered when sliding a value (but not when switching)
        # there is a timeout mechanism
        if time() - self.last_changed > 0.3:
            if new_value == 0:
                # Get current volume and store in a val, so we can recreate it later
                self.old_volume = self.get_current_device_volume()
                self.vol_changed(0)
            else:
                self.vol_changed(self.old_volume)

    def vol_changed(self, new_value: int):
        self.logger.info('=======>  light switched: {x}'.format(x=new_value))
        self.last_changed = time()
        self.set_current_volume(new_value)
