# coding=utf-8
__author__ = 'Qyon'


if __name__ == '__main__':
    from adf5355 import adf5355
    import spidev
    from time import sleep
    spi = spidev.SpiDev()
    spi.open(1, 0)
    spi.max_speed_hz = 4000000
    d = adf5355(spi, mute_till_lock_detect_en=True, ref_doubler_en=False, clkin=26000000, outb_en=True, outa_en=False, outb_power=3)
    f0 = 10368900000
    x = 0
    xmax = 10
    xdir = 1
    fstep = 200
    sleep_time = 0.5
    sleep_time_step = -0.1
    while True:
        x += xdir
        if x < 0:
            x = 1
            xdir = 1
            sleep_time += sleep_time_step
            if sleep_time <= 0:
                sleep_time = 0.5
        elif x > xmax:
            x = xmax
            xdir = -1
        d.set_freq(f0 + x * fstep, 1)
        sleep(sleep_time)
