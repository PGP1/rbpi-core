"""
module that contains raspberrypi controller, to reset device logic.
"""
import os

def reset_device():
    os.system('sudo reboot')
