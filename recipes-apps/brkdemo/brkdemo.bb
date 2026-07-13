DESCRIPTION = "Webserver LED demo application"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://brkLed.py \
	   file://ledTemplate.html \
	   file://LEDWebServer.py"

S = "${WORKDIR}"

PACKAGES += "${PN}-userfs"

RDEPENDS:${PN} += "${PN}-userfs"
RDEPENDS:${PN}-userfs += "python3-core"

do_install () {
	install -d ${D}${prefix}/local/demo/LEDWebDemo
	install -m 0755 ${S}/brkLed.py ${D}${prefix}/local/demo/LEDWebDemo/brkLed.py
	install -m 0644 ${S}/ledTemplate.html ${D}${prefix}/local/demo/LEDWebDemo/ledTemplate.html
	install -m 0755 ${S}/LEDWebServer.py ${D}${prefix}/local/demo/LEDWebDemo/LEDWebServer.py
}

FILES:${PN}-userfs += "${prefix}/local/demo/LEDWebDemo/brkLed.py \
		       ${prefix}/local/demo/LEDWebDemo/ledTemplate.html \
		       ${prefix}/local/demo/LEDWebDemo/LEDWebServer.py"