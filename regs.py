# coding=utf-8
__author__ = 'Qyon'
"""
SRC: https://github.com/analogdevicesinc/linux/blob/xcomm_zynq/drivers/iio/frequency/adf5355.c
Licensed under the GPL-2.
"""


# /* REG0 Bit Definitions */
def ADF5355_REG0_INT(x):
    return (((x) & 0xFFFF) << 4)


def ADF5355_REG0_PRESCALER(x):
    return ((x) << 20)


def ADF5355_REG0_AUTOCAL(x):
    return ((x) << 21)


# /* REG1 Bit Definitions */
def ADF5355_REG1_FRACT(x):
    return (((x) & 0xFFFFFF) << 4)


# /* REG2 Bit Definitions */
def ADF5355_REG2_MOD2(x):
    return (((x) & 0x3FFF) << 4)


def ADF5355_REG2_FRAC2(x):
    return (((x) & 0x3FFF) << 18)


# /* REG3 Bit Definitions */
def ADF5355_REG3_PHASE(x):
    return (((x) & 0xFFFFFF) << 4)


def ADF5355_REG3_PHASE_ADJUST(x):
    return ((x) << 28)


def ADF5355_REG3_PHASE_RESYNC(x):
    return ((x) << 29)


def ADF5355_REG3_EXACT_SDLOAD_RESET(x):
    return ((x) << 30)


# /* REG4 Bit Definitions */
def ADF5355_REG4_COUNTER_RESET_EN(x):
    return ((x) << 4)


def ADF5355_REG4_CP_THREESTATE_EN(x):
    return ((x) << 5)


def ADF5355_REG4_POWER_DOWN_EN(x):
    return ((x) << 6)


def ADF5355_REG4_PD_POLARITY_POS(x):
    return ((x) << 7)


def ADF5355_REG4_MUX_LOGIC(x):
    return ((x) << 8)


def ADF5355_REG4_REFIN_MODE_DIFF(x):
    return ((x) << 9)


def ADF5355_REG4_CHARGE_PUMP_CURR(x):
    return (((x) & 0xF) << 10)


def ADF5355_REG4_DOUBLE_BUFF_EN(x):
    return ((x) << 14)


def ADF5355_REG4_10BIT_R_CNT(x):
    return (((x) & 0x3FF) << 15)


def ADF5355_REG4_RDIV2_EN(x):
    return ((x) << 25)


def ADF5355_REG4_RMULT2_EN(x):
    return ((x) << 26)


def ADF5355_REG4_MUXOUT(x):
    return (((x) & 0x7) << 27)


ADF5355_MUXOUT_THREESTATE = 0
ADF5355_MUXOUT_DVDD = 1
ADF5355_MUXOUT_GND = 2
ADF5355_MUXOUT_R_DIV_OUT = 3
ADF5355_MUXOUT_N_DIV_OUT = 4
ADF5355_MUXOUT_ANALOG_LOCK_DETECT = 5
ADF5355_MUXOUT_DIGITAL_LOCK_DETECT = 6

# /* REG5 Bit Definitions */
ADF5355_REG5_DEFAULT = 0x00800025


# /* REG6 Bit Definitions */
def ADF4355_REG6_OUTPUTB_PWR(x):
    return (((x) & 0x7) << 4)


def ADF4355_REG6_RF_OUTB_EN(x):
    return ((x) << 9)


def ADF5355_REG6_OUTPUT_PWR(x):
    return (((x) & 0x3) << 4)


def ADF5355_REG6_RF_OUT_EN(x):
    return ((x) << 6)


def ADF5355_REG6_RF_OUTB_EN(x):
    return ((x) << 10)


def ADF5355_REG6_MUTE_TILL_LOCK_EN(x):
    return ((x) << 11)


def ADF5355_REG6_CP_BLEED_CURR(x):
    return (((x) & 0xFF) << 13)


def ADF5355_REG6_RF_DIV_SEL(x):
    return (((x) & 0x7) << 21)


def ADF5355_REG6_FEEDBACK_FUND(x):
    return ((x) << 24)


def ADF5355_REG6_NEG_BLEED_EN(x):
    return ((x) << 29)


def ADF5355_REG6_GATED_BLEED_EN(x):
    return ((x) << 30)


ADF5355_REG6_DEFAULT = 0x14000006


# /* REG7 Bit Definitions */
def ADF5355_REG7_LD_MODE_INT_N_EN(x):
    return ((x) << 4)


def ADF5355_REG7_FACT_N_LD_PRECISION(x):
    return (((x) & 0x3) << 5)


def ADF5355_REG7_LOL_MODE_EN(x):
    return ((x) << 7)


def ADF5355_REG7_LD_CYCLE_CNT(x):
    return (((x) & 0x3) << 8)


def ADF5355_REG7_LE_SYNCED_REFIN_EN(x):
    return ((x) << 25)


ADF5355_REG7_DEFAULT = 0x10000007

# /* REG8 Bit Definitions */
ADF5355_REG8_DEFAULT = 0x102D0428


# /* REG9 Bit Definitions */
def ADF5355_REG9_SYNTH_LOCK_TIMEOUT(x):
    return (((x) & 0x1F) << 4)


def ADF5355_REG9_ALC_TIMEOUT(x):
    return (((x) & 0x1F) << 9)


def ADF5355_REG9_TIMEOUT(x):
    return (((x) & 0x3FF) << 14)


def ADF5355_REG9_VCO_BAND_DIV(x):
    return (((x) & 0xFF) << 24)


# /* REG10 Bit Definitions */
def ADF5355_REG10_ADC_EN(x):
    return ((x) << 4)


def ADF5355_REG10_ADC_CONV_EN(x):
    return ((x) << 5)


def ADF5355_REG10_ADC_CLK_DIV(x):
    return (((x) & 0xFF) << 6)


ADF5355_REG10_DEFAULT = 0x00C0000A

# /* REG11 Bit Definitions */
ADF5355_REG11_DEFAULT = 0x0061300B


# /* REG12 Bit Definitions */
def ADF5355_REG12_PHASE_RESYNC_CLK_DIV(x):
    return (((x) & 0xFFFF) << 16)


ADF5355_REG12_DEFAULT = 0x0000041C

# /* Specifications */
ADF5355_MIN_VCO_FREQ = 3400000000  # /* Hz */
ADF5355_MAX_VCO_FREQ = 6800000000  # /* Hz */
ADF5355_MAX_OUT_FREQ = ADF5355_MAX_VCO_FREQ  # /* Hz */
ADF5355_MIN_OUT_FREQ = (ADF5355_MIN_VCO_FREQ / 64)  # /* Hz */
ADF5355_MAX_OUTB_FREQ = (ADF5355_MAX_VCO_FREQ * 2)  # /* Hz */
ADF5355_MIN_OUTB_FREQ = (ADF5355_MIN_VCO_FREQ * 2)  # /* Hz */

ADF4355_MIN_VCO_FREQ = 3400000000  # /* Hz */
ADF4355_MAX_VCO_FREQ = 6800000000  # /* Hz */
ADF4355_MAX_OUT_FREQ = ADF4355_MAX_VCO_FREQ  # /* Hz */
ADF4355_MIN_OUT_FREQ = (ADF4355_MIN_VCO_FREQ / 64)  # /* Hz */

ADF4355_3_MIN_VCO_FREQ = 3300000000  # /* Hz */
ADF4355_3_MAX_VCO_FREQ = 6600000000  # /* Hz */
ADF4355_3_MAX_OUT_FREQ = ADF4355_3_MAX_VCO_FREQ  # /* Hz */
ADF4355_3_MIN_OUT_FREQ = (ADF4355_3_MIN_VCO_FREQ / 64)  # /* Hz */

ADF4355_2_MIN_VCO_FREQ = 3400000000  # /* Hz */
ADF4355_2_MAX_VCO_FREQ = 6800000000  # /* Hz */
ADF4355_2_MAX_OUT_FREQ = 4400000000  # /* Hz */
ADF4355_2_MIN_OUT_FREQ = (ADF4355_2_MIN_VCO_FREQ / 64)  # /* Hz */

ADF5355_MAX_FREQ_PFD = 125000000  # /* Hz */
ADF5355_MAX_FREQ_REFIN = 600000000  # /* Hz */
ADF5355_MAX_MODUS2 = 16384
ADF5355_MAX_R_CNT = 1023

ADF5355_MODULUS1 = 16777216
ADF5355_MIN_INT_PRESCALER_89 = 75

ADF5355_REG0 = 0
ADF5355_REG1 = 1
ADF5355_REG2 = 2
ADF5355_REG3 = 3
ADF5355_REG4 = 4
ADF5355_REG5 = 5
ADF5355_REG6 = 6
ADF5355_REG7 = 7
ADF5355_REG8 = 8
ADF5355_REG9 = 9
ADF5355_REG10 = 10
ADF5355_REG11 = 11
ADF5355_REG12 = 12
ADF5355_REG_NUM = 13