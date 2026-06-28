FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://0002-Add-OSD32MP1-BRK-board-DT.patch \
            file://0003-Enable-fdtfile-environement-variable-generation.patch \
            file://0004-Add-DT-support-for-OSD32MP1-RED.patch \
            "

