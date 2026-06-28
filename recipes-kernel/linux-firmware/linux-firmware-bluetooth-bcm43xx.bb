# Copyright (C) 2018, STMicroelectronics - All Rights Reserved

SUMMARY = "Bluetooth firmware for BCM4343"
HOMEPAGE = "https://github.com/murata-wireless/cyw-bt-patch"
LICENSE = "Firmware-cypress-bcm43"
LIC_FILES_CHKSUM = "file://LICENCE.cypress;md5=cbc5f665d04f741f1e006d2096236ba7"

NO_GENERIC_LICENSE[Firmware-cypress-bcm43] = "LICENCE.cypress"

inherit allarch

SRC_URI = "git://github.com/murata-wireless/cyw-bt-patch;protocol=https;branch=master"
SRCREV = "bbc63f8b15394023c4a2fd9f74565fbd0d76ae71"

PV = "6.0"

S = "${WORKDIR}/git"

PACKAGES =+ "${PN}-cypress-license"

do_install() {
}

do_install:append:stm32mp1common() {
    install -d ${D}${nonarch_base_libdir}/firmware/brcm/

    # 43430
    install -m 644 ${S}/BCM43430A1_001.002.009.0159.0528.1DX.hcd ${D}${nonarch_base_libdir}/firmware/brcm/BCM43430A1.hcd
    install -m 644 ${S}/LICENCE.cypress ${D}${nonarch_base_libdir}/firmware/LICENCE.cypress_bcm4343
    cd ${D}${nonarch_base_libdir}/firmware/brcm/
    ln -sf BCM43430A1.hcd BCM.st,stm32mp157f-dk2.hcd
    ln -sf BCM43430A1.hcd BCM.st,stm32mp135f-dk.hcd
}
do_install:append:stm32mp2common() {
    install -d ${D}${nonarch_base_libdir}/firmware/brcm/
    install -m 644 ${S}/LICENCE.cypress ${D}${nonarch_base_libdir}/firmware/LICENCE.cypress_bcm4343

    # 43439
    install -m 644 ${S}/CYW4343A2_001.003.016.0031.0000.1YN.hcd ${D}${nonarch_base_libdir}/firmware/brcm/BCM4343A2.hcd
    cd ${D}${nonarch_base_libdir}/firmware/brcm/
    ln -sf BCM4343A2.hcd BCM.st,stm32mp257f-dk.hcd
    ln -sf BCM4343A2.hcd BCM.st,stm32mp257f-dk-ca35tdcid-ostl.hcd
    ln -sf BCM4343A2.hcd BCM.st,stm32mp257f-dk-ca35tdcid-ostl-m33-examples.hcd
    ln -sf BCM4343A2.hcd BCM.st,stm32mp235f-dk.hcd

}
do_install:append:stm32mp21common() {
    install -d ${D}${nonarch_base_libdir}/firmware/brcm/

    # 4373
    install -m 644 ${S}/LICENCE.cypress ${D}${nonarch_base_libdir}/firmware/LICENCE.cypress_bcm4373
    install -m 644 ${S}/BCM4373A0_001.001.025.0103.0155.FCC.CE.2AE.hcd ${D}${nonarch_base_libdir}/firmware/brcm/BCM4373A0.hcd
    cd ${D}${nonarch_base_libdir}/firmware/brcm/
    ln -sf BCM4373A0.hcd BCM.st,stm32mp215f-dk.hcd
}

LICENSE:${PN} = "Firmware-cypress-bcm43"
LICENSE:${PN}-cypress-license = "Firmware-cypress-bcm43"

FILES:${PN}-cypress-license = "${nonarch_base_libdir}/firmware/LICENCE.cypress*"
FILES:${PN} = "${nonarch_base_libdir}/firmware/"

RDEPENDS:${PN} += "${PN}-cypress-license"

RRECOMMENDS:${PN}:append:stm32mpcommon = " ${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'bluetooth-suspend', '', d)} "

# Firmware files are generally not ran on the CPU, so they can be
# allarch despite being architecture specific
INSANE_SKIP = "arch"
