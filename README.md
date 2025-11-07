This is made for [this 3.5"toucschreen from AliExpress](https://nl.aliexpress.com/item/1005002346325383.html) on a Raspberry Pi running Trixie 64-bit Lite.

No need to install any additional drivers!

Install custom overlay from this repo:
- copy spi-ili9486.dtbo into /boot/firmware/overlays/

Edit config.txt:
- dtoverlay=vc4-fkms-v3d
- dtparam=spi=on
- dtoverlay=spi-ili9486,speed=64000000
- dtoverlay=ads7846,penirq=17,speed=3000000,penirq_pull=down,keep_vref_on=1,ti,x-plate-ohms=60

Install:
- libegl-dev
- python3-pygame
- python3-evdev

