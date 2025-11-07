This is made for [this 3.5"toucschreen from ALiExpress](https://nl.aliexpress.com/item/1005002346325383.html) on a Raspberry Pi running Trixie 64-bit Lite

install custom overlay:
cp spi-ili9486.dtbo /boot/firmware/overlays/

config.txt:
dtoverlay=vc4-kms-v3d
max_framebuffers=2
disable_fw_kms_setup=1
dtparam=spi=on
dtoverlay=spi-ili9486,speed=32000000
dtoverlay=ads7846,penirq=17,speed=3000000,penirq_pull=down,keep_vref_on=1,ti,x-plate-ohms=60

install:
libegl-dev
python3-pygame
python3-evdev

