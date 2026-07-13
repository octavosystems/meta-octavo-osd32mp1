
do_install:stm32mp1common() {
    install -d ${D}${nonarch_base_libdir}/firmware/brcm/

    # ---- 43430-----
    # Install calibration file
    install -m 0644 ${WORKDIR}/nvram-murata/cyfmac43430-sdio.1DX.txt ${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.txt
    # disable Wakeup on WLAN
    sed -i "s/muxenab=\(.*\)$/#muxenab=\1/g" ${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.txt

    # Take newest murata firmware
    install -m 0644 ${WORKDIR}/murata/cyfmac43430-sdio.bin ${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.bin
    install -m 0644 ${WORKDIR}/murata/cyfmac43430-sdio.1DX.clm_blob ${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.clm_blob

    # Add symlinks for newest kernel compatibility
    cd ${D}${nonarch_base_libdir}/firmware/brcm/
    ln -sf brcmfmac43430-sdio.bin brcmfmac43430-sdio.st,stm32mp157c-osd32mp1-red.bin
    ln -sf brcmfmac43430-sdio.txt brcmfmac43430-sdio.st,stm32mp157c-osd32mp1-red.txt

    # 43430
    install -m 644 ${S}/BCM43430A1_001.002.009.0159.0528.1DX.hcd ${D}${nonarch_base_libdir}/firmware/brcm/BCM43430A1.hcd
    install -m 644 ${S}/LICENCE.cypress ${D}${nonarch_base_libdir}/firmware/LICENCE.cypress_bcm4343
    cd ${D}${nonarch_base_libdir}/firmware/brcm/
    ln -sf BCM43430A1.hcd BCM.st,stm32mp157c-osd32mp1-red.hcd
}
