class VolumeChangerInterface:
    last_changed = 0
    old_volume = 0

    def __init__(self, logger=None):
        if logger is None:
            import logging
            self.logger = logging.getLogger()
        else:
            self.logger = logger

    # todo find out type and adjust
    def vol_switched(self, new_value):
        """Callback function for when the 'Sound' is switched on or off"""
        pass

    def vol_changed(self, new_value):
        """Callback function for when the numerical value for 'Volume' changes"""
        pass
