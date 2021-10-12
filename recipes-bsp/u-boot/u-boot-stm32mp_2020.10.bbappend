FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://0006-Add-OSD32MP1-BRK-board-support.patch \
	    file://0007-Fix-dts-include-file-for-OSD32MP1-BRK.patch \
	    file://0008-Fix-broken-label-reference-for-OSD32MP1-BRK.patch \
	    file://0009-Fix-broken-reference-to-i2c4-pins-for-OSD32MP1-BRK.patch"

