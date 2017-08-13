# coding=utf-8
__author__ = 'Qyon'
"""
SRC: https://github.com/analogdevicesinc/linux/blob/xcomm_zynq/drivers/iio/frequency/adf5355.c
Licensed under the GPL-2.
"""

from math import ceil
import time
from regs import *
from fractions import gcd


def DIV_ROUND_UP(x, y):
    return int(ceil(x / y))


def clamp(tmp, param, param1):
    return max(min(tmp, param1), param)

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(int(value >> (i * 8) & 0xff))
    result.reverse()
    return result

class adf5355(object):
    class adf5355_state:
        clkin = 0
        fpfd = 0
        min_vco_freq = ADF4355_MIN_VCO_FREQ
        min_out_freq = ADF4355_MIN_OUT_FREQ
        max_out_freq = ADF4355_MAX_OUT_FREQ
        freq_req_chan = 0
        integer = 0
        fract1 = 0
        fract2 = 0
        mod2 = 0
        rf_div_sel = 0
        delay_us = 0
        regs = [0 for i in range(0, ADF5355_REG_NUM)]
        clock_shift = 0
        all_synced = 0
        is_5355 = True

    """
    
    """

    def __init__(self, spi, ref_div_factor=0, ref_doubler_en=False, ref_div2_en=False, cp_curr_uA=900,
                 mux_out_sel=ADF5355_MUXOUT_DIGITAL_LOCK_DETECT, ref_diff_en=True, mux_out_3V3_en=True,
                 phase_detector_polarity_neg=False, clkin=26000000, cp_gated_bleed_en=False, cp_neg_bleed_en=True,
                 mute_till_lock_detect_en=True, outa_en=True, outb_en=True, outa_power=0, outb_power=0
                 ):
        self.spi = spi
        self.cp_gated_bleed_en = cp_gated_bleed_en
        self.cp_neg_bleed_en = cp_neg_bleed_en
        self.mute_till_lock_detect_en = mute_till_lock_detect_en
        self.outb_en = outb_en
        self.outa_en = outa_en
        self.outa_power = outa_power
        self.outb_power = outb_power
        self.mux_out_sel = mux_out_sel
        self.ref_diff_en = ref_diff_en
        self.mux_out_3V3_en = mux_out_3V3_en
        self.phase_detector_polarity_neg = phase_detector_polarity_neg
        self.cp_curr_uA = cp_curr_uA
        self.ref_div2_en = ref_div2_en
        self.ref_doubler_en = ref_doubler_en
        self.ref_div_factor = ref_div_factor
        self.st = self.adf5355_state()
        self.st.clkin = clkin
        self.setup()

    def spi_write(self, value):
        bytes_to_send = int_to_bytes(value, 4)
        #print "0x%08x" % value, value, bytes_to_send
        self.spi.writebytes(bytes_to_send)

    def pll_fract_n_compute(self, vco, pfd):

        tmp = vco % pfd
        vco /= pfd
        tmp = tmp * ADF5355_MODULUS1
        fract2 = tmp % pfd
        tmp /= pfd
        integer = vco
        fract1 = tmp
        mod2 = pfd

        while mod2 > ADF5355_MAX_MODUS2:
            mod2 >>= 1
            fract2 >>= 1

        gcd_div = gcd(fract2, mod2)
        mod2 /= gcd_div
        fract2 /= gcd_div

        return integer, fract1, fract2, mod2

    def pll_fract_n_get_rate(self, channel):
        # val = (((u64)
        # st->integer * ADF5355_MODULUS1) + st->fract1) *st->fpfd;
        val = ((self.st.integer * ADF5355_MODULUS1) + self.st.fract1) + self.st.fpfd
        # tmp = (u64)
        # st->fract2 * st->fpfd;
        tmp = self.st.fract2 * self.st.fpfd
        # do_div(tmp, st->mod2);
        tmp /= self.st.mod2
        # val += tmp + ADF5355_MODULUS1 / 2;
        val += tmp + ADF5355_MODULUS1 / 2
        # do_div(val, ADF5355_MODULUS1 *
        #        (1 << (channel == 1 ? 0: st->rf_div_sel)));
        val /= (ADF5355_MODULUS1 * (1 << (0 if channel == 1 else self.st.rf_div_sel)))
        # if (channel == 1)
        #     val <<= 1;
        if channel == 1:
            val <<= 1
        return val

    def setup(self):
        ref_div_factor = self.ref_div_factor

        while True:
            # ref_div_factor + +;
            ref_div_factor += 1
            # st->fpfd = (st->clkin * (pdata->ref_doubler_en ? 2: 1)) / (ref_div_factor * (pdata->ref_div2_en ? 2: 1));
            self.st.fpfd = (self.st.clkin * (2 if self.ref_doubler_en else 1)) / (
                ref_div_factor * (2 if self.ref_div2_en else 1))
            if self.st.fpfd <= ADF5355_MAX_FREQ_PFD:
                break

        # tmp = DIV_ROUND_CLOSEST(pdata->cp_curr_uA - 315, 315U);
        tmp = int(round((self.cp_curr_uA - 315) / 315))
        # tmp = clamp(tmp, 0U, 15U);
        tmp = max(min(tmp, 15), 0)
        self.st.regs[ADF5355_REG4] = ADF5355_REG4_COUNTER_RESET_EN(0) | \
                                     ADF5355_REG4_CP_THREESTATE_EN(0) | \
                                     ADF5355_REG4_POWER_DOWN_EN(0) | \
                                     ADF5355_REG4_PD_POLARITY_POS(int(not self.phase_detector_polarity_neg)) | \
                                     ADF5355_REG4_MUX_LOGIC(int(self.mux_out_3V3_en)) | \
                                     ADF5355_REG4_REFIN_MODE_DIFF(int(self.ref_diff_en)) | \
                                     ADF5355_REG4_CHARGE_PUMP_CURR(tmp) | \
                                     ADF5355_REG4_DOUBLE_BUFF_EN(1) | \
                                     ADF5355_REG4_10BIT_R_CNT(ref_div_factor) | \
                                     ADF5355_REG4_RDIV2_EN(int(self.ref_div2_en)) | \
                                     ADF5355_REG4_RMULT2_EN(int(self.ref_doubler_en)) | \
                                     ADF5355_REG4_MUXOUT(self.mux_out_sel)

        self.st.regs[ADF5355_REG5] = ADF5355_REG5_DEFAULT

        self.st.regs[ADF5355_REG7] = ADF5355_REG7_LD_MODE_INT_N_EN(0) | \
                                     ADF5355_REG7_FACT_N_LD_PRECISION(3) | \
                                     ADF5355_REG7_LOL_MODE_EN(0) | \
                                     ADF5355_REG7_LD_CYCLE_CNT(0) | \
                                     ADF5355_REG7_LE_SYNCED_REFIN_EN(1) | \
                                     ADF5355_REG7_DEFAULT

        self.st.regs[ADF5355_REG8] = ADF5355_REG8_DEFAULT

        # tmp = DIV_ROUND_UP(st->fpfd, 20000U * 30U);
        tmp = DIV_ROUND_UP(self.st.fpfd, 2000 * 30)
        # tmp = clamp(tmp, 1U, 1023U);
        tmp = clamp(tmp, 1, 1023)

        self.st.regs[ADF5355_REG9] = ADF5355_REG9_TIMEOUT(tmp) | \
                                     ADF5355_REG9_SYNTH_LOCK_TIMEOUT(DIV_ROUND_UP(self.st.fpfd * 2, 100000 * tmp)) | \
                                     ADF5355_REG9_ALC_TIMEOUT(DIV_ROUND_UP(self.st.fpfd * 5, 100000 * tmp)) | \
                                     ADF5355_REG9_VCO_BAND_DIV(DIV_ROUND_UP(self.st.fpfd, 2400000))

        tmp = DIV_ROUND_UP(self.st.fpfd / 100000 - 2, 4)
        tmp = clamp(tmp, 1, 255)

        # /* Delay > 16 ADC_CLK cycles */
        self.st.delay_us = DIV_ROUND_UP(16000000, self.st.fpfd / (4 * tmp + 2))

        self.st.regs[ADF5355_REG10] = ADF5355_REG10_ADC_EN(1) | \
                                      ADF5355_REG10_ADC_CONV_EN(1) | \
                                      ADF5355_REG10_ADC_CLK_DIV(tmp) | \
                                      ADF5355_REG10_DEFAULT

        self.st.regs[ADF5355_REG11] = ADF5355_REG11_DEFAULT

        self.st.regs[ADF5355_REG12] = ADF5355_REG12_PHASE_RESYNC_CLK_DIV(0) | ADF5355_REG12_DEFAULT

        self.st.all_synced = False

    def set_freq(self, freq, channel):
        if channel == 0:
            if freq > self.st.max_out_freq or freq < self.st.min_out_freq:
                raise Exception('Invalid frequency!')
            self.st.rf_div_sel = 0
            while freq < self.st.min_vco_freq:
                freq <<= 1
                self.st.rf_div_sel += 1
        else:
            # /* ADF5355 RFoutB 6800...13600 MHz */
            if freq > ADF5355_MAX_OUTB_FREQ or freq < ADF5355_MIN_OUTB_FREQ:
                raise Exception('Invalid frequency!')
            freq >>= 1

        self.st.integer, self.st.fract1, self.st.fract2, self.st.mod2 = self.pll_fract_n_compute(freq, self.st.fpfd)
        #print "self.st.integer %u, self.st.fract1 %u, self.st.fract2 %u, self.st.mod2 %u, freq %u, self.st.fpfd %u, rf_div_sel %u" % (self.st.integer, self.st.fract1, self.st.fract2, self.st.mod2, freq, self.st.fpfd, self.st.rf_div_sel)
        prescaler = (self.st.integer >= ADF5355_MIN_INT_PRESCALER_89)

        """
            /* Tests have shown that the optimal bleed set is the following:
             * 4/N < IBLEED/ICP < 10/N
             */
        """
        cp_bleed = DIV_ROUND_UP(400 * self.cp_curr_uA, self.st.integer * 375)
        cp_bleed = clamp(cp_bleed, 1, 255)

        self.st.regs[ADF5355_REG0] = ADF5355_REG0_INT(self.st.integer) | \
                                     ADF5355_REG0_PRESCALER(prescaler) | ADF5355_REG0_AUTOCAL(1)
        self.st.regs[ADF5355_REG1] = ADF5355_REG1_FRACT(self.st.fract1)
        self.st.regs[ADF5355_REG2] = ADF5355_REG2_MOD2(self.st.mod2) | ADF5355_REG2_FRAC2(self.st.fract2)

        self.st.regs[ADF5355_REG6] = ADF5355_REG6_OUTPUT_PWR(self.outa_power) | \
                                     ADF5355_REG6_RF_OUT_EN(int(self.outa_en)) | \
                                     (ADF5355_REG6_RF_OUTB_EN(
                                         int(self.outb_en)) if self.st.is_5355 else ADF4355_REG6_OUTPUTB_PWR( self.outb_power) | ADF4355_REG6_RF_OUTB_EN(int(self.outb_en))) | \
                                     ADF5355_REG6_MUTE_TILL_LOCK_EN(int(self.mute_till_lock_detect_en)) | \
                                     ADF5355_REG6_CP_BLEED_CURR(cp_bleed) | \
                                     ADF5355_REG6_RF_DIV_SEL(self.st.rf_div_sel) | \
                                     ADF5355_REG6_FEEDBACK_FUND(1) | \
                                     ADF5355_REG6_NEG_BLEED_EN(int(self.cp_neg_bleed_en)) | \
                                     ADF5355_REG6_GATED_BLEED_EN(int(self.cp_gated_bleed_en)) | \
                                     ADF5355_REG6_DEFAULT

        self.st.freq_req = freq
        self.st.freq_req_chan = channel

        return self.sync_config(False)

    def sync_config(self, sync_all):
        if sync_all or not self.st.all_synced:
            for i in  range(ADF5355_REG_NUM -1, ADF5355_REG0 - 1, -1):
                self.spi_write(self.st.regs[i] | i)
            self.st.all_synced = True
        else:
            self.spi_write(self.st.regs[ADF5355_REG6] | ADF5355_REG6)
            self.spi_write(self.st.regs[ADF5355_REG4] | ADF5355_REG4 | ADF5355_REG4_COUNTER_RESET_EN(1))
            self.spi_write(self.st.regs[ADF5355_REG2] | ADF5355_REG2)
            self.spi_write(self.st.regs[ADF5355_REG1] | ADF5355_REG1)
            self.spi_write(self.st.regs[ADF5355_REG0] & ~ADF5355_REG0_AUTOCAL(1))
            self.spi_write(self.st.regs[ADF5355_REG4] | ADF5355_REG4)
            time.sleep(self.st.delay_us / 1000000)
            self.spi_write(self.st.regs[ADF5355_REG0])

    def disable(self):
        self.st.regs[ADF5355_REG4] |= ADF5355_REG4_POWER_DOWN_EN(1)
        self.sync_config(True)

if __name__ == '__main__':
    d = adf5355()
    d.set_freq(1100000000, 0)
