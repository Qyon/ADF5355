# coding=utf-8
__author__ = 'Qyon'


if __name__ == '__main__':
    from adf5355 import adf5355
    import spidev
    from time import sleep
    spi = spidev.SpiDev()
    spi.open(1, 0)
    spi.max_speed_hz = 1000000
    d = adf5355(spi, mute_till_lock_detect_en=True, ref_doubler_en=False, clkin=26000000, outb_en=True, outa_en=False, outb_power=3)
    f0 = 10368900000
    x = 10
    xdir = 1
    while True:
        x += xdir
        if x < 0:
            x = 1
            xdir = 1
        elif x > 10:
            x = 10
            xdir = -1
        d.set_freq(f0 + x * 100, 1)
        sleep(0.05)
