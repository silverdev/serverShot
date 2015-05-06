import sys
import termios

import usb.core
import usb.util

import platform
import time

# Protocol command bytes
DOWN = 0x01
UP = 0x02
LEFT = 0x04
RIGHT = 0x08
FIRE = 0x10
STOP = 0x20

DEVICE = None


def usage():
    print ""
    print "Commands:"
    print "  W          - move up"
    print "  S          - move down"
    print "  D          - move right"
    print "  A          - move left"
    print "  Space      - stop"
    print "  F          - fire"
    print "  R          - reset to center position"
    print "  K          - kill program"
    print ""


def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    global DEVICE
    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        raise ValueError('Missile device not found')

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception as e:
            pass  # already unregistered

    DEVICE.set_configuration()


def send_cmd(cmd):
    DEVICE.ctrl_transfer(
        0x21, 0x09, 0, 0, [
            0x02, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def move_turret(x):
    if DEVICE:
        if x == 'w':
            send_cmd(UP)
        if x == 'a':
            send_cmd(LEFT)
        if x == 's':
            send_cmd(DOWN)
        if x == 'd':
            send_cmd(RIGHT)
        if x == ' ':
            send_cmd(STOP)
        if x == 'f':
            send_cmd(FIRE)
            time.sleep(5)
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        if x == 'r':
            send_cmd(LEFT)
            time.sleep(6)
            send_cmd(DOWN)
            time.sleep(1)
            send_cmd(RIGHT)
            time.sleep(3)
            send_cmd(UP)
            time.sleep(.5)
            send_cmd(STOP)
