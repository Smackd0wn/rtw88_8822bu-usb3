# Userspace program that switchs RTL8812bu to USB 3.0 mode
# See https://github.com/morrownr/88x2bu-20210702/blob/cd2b6cbd9c8fbfebee8a1f28fab8e4434450456c/hal/halmac/halmac_88xx/halmac_usb_88xx.c#L425-L472
import usb.core
import time

dev = usb.core.find(idVendor=0x0bda, idProduct=0xb812)
if dev.is_kernel_driver_active(0): dev.detach_kernel_driver(0)

#define REG_SYS_CFG2 0x00FC
#cur_mode = (HALMAC_REG_R8(REG_SYS_CFG2 + 3) == 0x20) ? HALMAC_USB_MODE_U3 : HALMAC_USB_MODE_U2;
val = dev.ctrl_transfer(0xc0, 5, 0x00fc+3, 0, 1)
if val[0] == 0x20: raise RuntimeError('already in usb3 mode')

val = dev.ctrl_transfer(0xc0, 5, 0x00c4, 0, 4)
ctrl2 = int.from_bytes(val, 'little')

#define BIT_SHIFT_USB23_SW_MODE_V1 18
#define BIT_MASK_USB23_SW_MODE_V1 0x3
#define BIT_USB3_USB2_TRANSITION BIT(20)
if not ctrl2 & (1<<20): raise RuntimeError('not supported')

#usb_tmp &= ~(BIT_USB23_SW_MODE_V1(0x3));
#HALMAC_REG_W32(REG_PAD_CTRL2, usb_tmp | BIT_USB23_SW_MODE_V1(HALMAC_USB_MODE_U3) | BIT_RSM_EN_V1); 
ctrl2 &= ~(3<<18)
ctrl2 |= (2<<18) | (1<<16)
dev.ctrl_transfer(0x40, 5, 0x00c4, 0, ctrl2.to_bytes(4, 'little'))
#HALMAC_REG_W8(REG_PAD_CTRL2 + 1, 4); 
dev.ctrl_transfer(0x40, 5, 0x00c4+1, 0, (4).to_bytes(1, 'little'))

#define REG_SYS_PW_CTRL 0x0004
#define BIT_APFM_OFFMAC BIT(9)
#HALMAC_REG_W16_SET(REG_SYS_PW_CTRL, BIT_APFM_OFFMAC);
val = dev.ctrl_transfer(0xc0, 5, 0x0004, 0, 2)
reg = int.from_bytes(val, 'little')
reg |= 1<<9
dev.ctrl_transfer(0x40, 5, 0x0004, 0, reg.to_bytes(2, 'little'))

#define BIT_NO_PDN_CHIPOFF_V1 BIT(17)
#HALMAC_REG_W32_SET(REG_PAD_CTRL2, BIT_NO_PDN_CHIPOFF_V1);
val = dev.ctrl_transfer(0xc0, 5, 0x00c4, 0, 4)
time.sleep(0.001)
ctrl2 = int.from_bytes(val, 'little')
ctrl2 |= 1<<17
dev.ctrl_transfer(0x40, 5, 0x00c4, 0, ctrl2.to_bytes(4, 'little'))
