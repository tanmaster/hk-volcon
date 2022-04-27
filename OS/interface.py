from time import time


class VolumeChangerInterface:
    """
    Do not instantiate this class, inherit from it an implement the two static methods for your system.
    """
    last_changed = 0
    old_volume = 0

    @staticmethod
    def get_current_device_volume():
        """This function needs to be implemented by the inheriting class to provide a volume getter for the
        current System."""
        pass

    @staticmethod
    def set_current_volume(target: int):
        """This function needs to be implemented by the inheriting class to provide a volume setter for the
        current System."""
        pass

    def __init__(self, logger=None):
        if logger is None:
            import logging
            self.logger = logging.getLogger()
        else:
            self.logger = logger
        self.old_volume = self.get_current_device_volume()
        self.last_changed = time()

    def vol_switched(self, new_value: int):
        """Callback function for when the 'Sound' is switched on or off"""
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
        """Callback function for when the numerical value for 'Volume' changes"""
        self.logger.info('=======>  light switched: {x}'.format(x=new_value))
        self.last_changed = time()
        self.set_current_volume(new_value)
