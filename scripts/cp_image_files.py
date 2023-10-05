# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Copy BRK Image Files
--------------------------------------------------------------------------
Copyright 2021, Octavo Systems, LLC. All rights reserved.

License:
Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its 
contributors may be used to endorse or promote products derived from 
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Copy all necessary image files for BRK to be used by Cube Programmer:

Pre-requisities:
  - Build BRK image using instructions at 
    https://github.com/octavosystems/meta-octavo-osd32mp1

Usage:
  -b <Path to build directory>
  -d <Path to destination directory>
  -p <Platform> defaults to brk.

"""
import sys
import os
import getopt
import shutil

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
image_dir = "tmp-glibc/deploy/images/osd32mp1-brk"
image_dir_brk = "tmp-glibc/deploy/images/osd32mp1-brk"
image_dir_red_v1_2 = "tmp-glibc/deploy/images/osd32mp1-red-v1_2"

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
# Files to copy
#   (<sub-directory relative to image_dir>, <file name>)
files = [
    ("flashlayout_octavo-image-weston/trusted", None,                   "FlashLayout_sdcard_stm32mp157c-osd32mp1-brk-trusted.tsv"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "tf-a-stm32mp157c-osd32mp1-brk-usb.stm32"),
    ("fip",                                     "fip",                  "fip-stm32mp157c-osd32mp1-brk-trusted.bin"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "tf-a-stm32mp157c-osd32mp1-brk-sdcard.stm32"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "metadata.bin"),
    ("fip",                                     "fip",                  "fip-stm32mp157c-osd32mp1-brk-trusted.bin"),
    (None,                                      None,                   "st-image-bootfs-openstlinux-weston-osd32mp1-brk.ext4"),
    (None,                                      None,                   "st-image-vendorfs-openstlinux-weston-osd32mp1-brk.ext4"),
    (None,                                      None,                   "octavo-image-weston-openstlinux-weston-osd32mp1-brk.ext4"),
    (None,                                      None,                   "st-image-userfs-openstlinux-weston-osd32mp1-brk.ext4")
]


# Files to copy
#   (<sub-directory relative to image_dir>, <file name>)
files_brk = [
    ("flashlayout_octavo-image-weston/trusted", None,                   "FlashLayout_sdcard_stm32mp157c-osd32mp1-brk-trusted.tsv"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "tf-a-stm32mp157c-osd32mp1-brk-usb.stm32"),
    ("fip",                                     "fip",                  "fip-stm32mp157c-osd32mp1-brk-trusted.bin"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "tf-a-stm32mp157c-osd32mp1-brk-sdcard.stm32"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "metadata.bin"),
    ("fip",                                     "fip",                  "fip-stm32mp157c-osd32mp1-brk-trusted.bin"),
    (None,                                      None,                   "st-image-bootfs-openstlinux-weston-osd32mp1-brk.ext4"),
    (None,                                      None,                   "st-image-vendorfs-openstlinux-weston-osd32mp1-brk.ext4"),
    (None,                                      None,                   "octavo-image-weston-openstlinux-weston-osd32mp1-brk.ext4"),
    (None,                                      None,                   "st-image-userfs-openstlinux-weston-osd32mp1-brk.ext4")
]
# Files to copy
#   (<sub-directory relative to image_dir>, <file name>)
files_red_v1_2 = [
    ("flashlayout_octavo-image-weston/trusted", None,                   "FlashLayout_sdcard_stm32mp157c-osd32mp1-red-v1_2-trusted.tsv"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "tf-a-stm32mp157c-osd32mp1-red-v1_2-usb.stm32"),
    ("fip",                                     "fip",                  "fip-stm32mp157c-osd32mp1-red-v1_2-trusted.bin"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "tf-a-stm32mp157c-osd32mp1-red-v1_2-sdcard.stm32"),
    ("arm-trusted-firmware",                    "arm-trusted-firmware", "metadata.bin"),
    ("fip",                                     "fip",                  "fip-stm32mp157c-osd32mp1-red-v1_2-trusted.bin"),
    (None,                                      None,                   "st-image-bootfs-openstlinux-weston-osd32mp1-red-v1_2.ext4"),
    (None,                                      None,                   "st-image-vendorfs-openstlinux-weston-osd32mp1-red-v1_2.ext4"),
    (None,                                      None,                   "octavo-image-weston-openstlinux-weston-osd32mp1-red-v1_2.ext4"),
    (None,                                      None,                   "st-image-userfs-openstlinux-weston-osd32mp1-red-v1_2.ext4")
]




# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def usage():
    """ Print usage information. """

    print("cp_image_files.py")
    print("  -b <path to build directory>")
    print("  -d <path to destination directory>")

# End def



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hb:d:p:", ["help", "build=", "dest=", "plat="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        sys.exit(2)

    build_dir = None
    dest_dir  = None
    platform  = None
    for o, a in opts:
        if   o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-b", "--build"):
            build_dir = a
        elif o in ("-d", "--dest"):
            dest_dir  = a
        elif o in ("-p", "--plat"):
            platform  = a
        else:
            assert False, "unhandled option"

    if (build_dir == None) or (dest_dir == None):
        usage()
        sys.exit()

    if (platform == None):
        platform = "brk"

    if (platform == "brk"):
        image_dir = image_dir_brk
        files = files_brk
    elif (platform == "red-v1_2"):
        image_dir = image_dir_red_v1_2
        files = files_red_v1_2

    if not os.path.isdir(build_dir):
        print("Build directory does not exist: {0}".format(build_dir))
        sys.exit()

    if not os.path.isdir(dest_dir):
        print("Destination directory does not exist: {0}".format(dest_dir))
        sys.exit()

    try:
        print("Copying image files from:")
        print("    Build       Directory = {0}".format(build_dir))
        print("    Destination Directory = {0}".format(dest_dir))

        source_dir = build_dir + "/" + image_dir

        for file in files:
            if file[0] is None:
                file_to_copy = source_dir + "/" + file[2]
            else:
                file_to_copy = source_dir + "/" + file[0] + "/" + file[2]

            if file[1] is None:
                dest_to_copy = dest_dir
            else:
                dest_to_copy = dest_dir + "/" + file[1]

            if not os.path.isdir(dest_to_copy):
                os.makedirs(dest_to_copy)

            shutil.copy2(file_to_copy, dest_to_copy)

            print("cp {0} {1}".format(file_to_copy, dest_to_copy))

    except Exception as e:
        print("ERROR:  {0}".format(e))


