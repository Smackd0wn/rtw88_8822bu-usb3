# rtw88_8822bu-usb3
Switch RTL88x2BU to USB 3.0 because the Linux in-tree rtw88 driver does not
---
Realtek RTL88x2bu uses "[smart switching](https://store.rokland.com/blogs/news/76663941-understanding-mode-switching-in-realtek-rtl8812au-802-11ac-windows-drivers)" which means it always initializes in USB 2.0 mode when powered on. The Realtek 88x2bu driver can let the device switch to USB 3.0 mode (or back to 2.0) by [writing some registers](https://github.com/morrownr/88x2bu-20210702/blob/cd2b6cbd9c8fbfebee8a1f28fab8e4434450456c/hal/halmac/halmac_88xx/halmac_usb_88xx.c#L425-L472). However, the Linux kernel in-tree rtw88 driver does not support USB mode switching (yet), so the device will stay in USB 2.0. Fortunately, the rtw88 driver seems to work just fine with a device that is already in USB 3.0 mode.

This is a (crude) userspace program that tells the 88x2bu to switch to USB 3.0 mode. It depends on [pyusb](https://github.com/pyusb/pyusb).

Change VID:PID if yours is not 0bda:b812. The program **should** exit with an I/O error, because the device will "disconnect" (hence the I/O error) and reappear as a USB 3.0 device.
