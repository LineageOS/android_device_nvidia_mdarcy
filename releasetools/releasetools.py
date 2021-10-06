# Copyright (C) 2021 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

""" Custom OTA commands for mdarcy devices """

import common
import re
import os

APP_PART     = '/dev/block/by-name/APP'
DTB_PART     = '/dev/block/by-name/DTB'
STAGING_PART = '/dev/block/by-name/USP'
VBMETA_PART  = '/dev/block/by-name/vbmeta'
VENDOR_PART  = '/dev/block/by-name/vendor'

PUBLIC_KEY_PATH     = '/sys/devices/7000f800.efuse/7000f800.efuse:efuse-burn/public_key'
FUSED_PATH          = '/sys/devices/7000f800.efuse/7000f800.efuse:efuse-burn/odm_production_mode'
DTSFILENAME_PATH    = '/proc/device-tree/nvidia,dtsfilename'

MODE_UNFUSED        = '0x00000000\n'
MODE_FUSED          = '0x00000001\n'

DARCY_PUBLIC_KEY    = '0x435a807e9187c53eae50e2dcab521e0ea41458a9b18d31db553ceb711c21fb52\n'
MDARCY_PUBLIC_KEY   = '0xc5ae4221f0f4f5113c0271b3519cac7f0bcb0cb860381a4648e9eee350e97f89\n'
SIF_PUBLIC_KEY      = '0x26646fe375375e39410853f75e59e2c4ca8440926fa37604a280b5c8a25a2c3e\n'
DARCY_BL_VERSION    = '32.00.2019.50-t210-79558a05'

def FullOTA_PostValidate(info):
  if 'INSTALL/bin/resize2fs_static' in info.input_zip.namelist():
    info.script.AppendExtra('run_program("/tmp/install/bin/resize2fs_static", "' + APP_PART + '");');
    info.script.AppendExtra('run_program("/tmp/install/bin/resize2fs_static", "' + VENDOR_PART + '");');

def FullOTA_Assertions(info):
  if 'RADIO/mdarcy.blob' in info.input_zip.namelist():
    CopyBlobs(info.input_zip, info.output_zip)
    AddBootloaderFlash(info, info.input_zip)
  else:
    AddBootloaderAssertion(info, info.input_zip)

def IncrementalOTA_Assertions(info):
  FullOTA_Assertions(info)

def CopyBlobs(input_zip, output_zip):
  for info in input_zip.infolist():
    f = info.filename
    if f.startswith("RADIO/") and (f.__len__() > len("RADIO/")):
      fn = f[6:]
      common.ZipWriteStr(output_zip, "firmware-update/" + fn, input_zip.read(f))

def AddBootloaderAssertion(info, input_zip):
  android_info = input_zip.read("OTA/android-info.txt").decode('utf-8')
  m = re.search(r"require\s+version-bootloader\s*=\s*(\S+)", android_info)
  if m:
    bootloaders = m.group(1).split("|")
    if "*" not in bootloaders:
      info.script.AssertSomeBootloader(*bootloaders)
    info.metadata["pre-bootloader"] = m.group(1)

def AddBootloaderFlash(info, input_zip):
  """ If device is fused """
  info.script.AppendExtra('ifelse(')
  info.script.AppendExtra('  read_file("' + FUSED_PATH + '") == "' + MODE_FUSED + '",')
  info.script.AppendExtra('  (')

  """ Fused darcy """
  info.script.AppendExtra('    ifelse(')
  info.script.AppendExtra('      getprop("ro.hardware") == "darcy",')
  info.script.AppendExtra('      (')
  info.script.AppendExtra('        ifelse(')
  info.script.AppendExtra('          is_substring("tegra210b01", read_file("' + DTSFILENAME_PATH + '")),')
  """ mdarcy """
  info.script.AppendExtra('          (')
  info.script.AppendExtra('            ifelse(')
  info.script.AppendExtra('              getprop("ro.bootloader") == "' + DARCY_BL_VERSION + '",')
  info.script.AppendExtra('              (')
  info.script.AppendExtra('                ui_print("Correct bootloader already installed for fused mdarcy");')
  info.script.AppendExtra('              ),')
  info.script.AppendExtra('              (')
  info.script.AppendExtra('                ifelse(')
  info.script.AppendExtra('                  read_file("' + PUBLIC_KEY_PATH + '") == "' + MDARCY_PUBLIC_KEY + '",')
  info.script.AppendExtra('                  (')
  info.script.AppendExtra('                    ui_print("Flashing updated bootloader for fused mdarcy");')
  info.script.AppendExtra('                    package_extract_file("firmware-update/mdarcy.blob", "' + STAGING_PART + '");')
  info.script.AppendExtra('                  ),')
  info.script.AppendExtra('                  (')
  info.script.AppendExtra('                    ui_print("Unknown public key " + read_file("' + PUBLIC_KEY_PATH + '") + " for mdarcy detected.");')
  info.script.AppendExtra('                    ui_print("This is not supported. Please report to LineageOS Maintainer.");')
  info.script.AppendExtra('                    abort();')
  info.script.AppendExtra('                  )')
  info.script.AppendExtra('                );')
  info.script.AppendExtra('              )')
  info.script.AppendExtra('            );')
  info.script.AppendExtra('            package_extract_file("install/mdarcy.dtb.img", "' + DTB_PART + '");')
  info.script.AppendExtra('          ),')
  """ darcy """
  info.script.AppendExtra('          (')
  info.script.AppendExtra('            ui_print("Darcy is not supported in this build. Please install a `foster` build instead.");')
  info.script.AppendExtra('            abort();')
  info.script.AppendExtra('          )')
  info.script.AppendExtra('        )')
  info.script.AppendExtra('      )')
  info.script.AppendExtra('    );')

  """ Fused sif """
  info.script.AppendExtra('    ifelse(')
  info.script.AppendExtra('      getprop("ro.hardware") == "sif",')
  info.script.AppendExtra('      (')
  info.script.AppendExtra('        ifelse(')
  info.script.AppendExtra('          getprop("ro.bootloader") == "' + DARCY_BL_VERSION + '",')
  info.script.AppendExtra('          (')
  info.script.AppendExtra('            ui_print("Correct bootloader already installed for fused sif");')
  info.script.AppendExtra('          ),')
  info.script.AppendExtra('          ifelse(')
  info.script.AppendExtra('            read_file("' + PUBLIC_KEY_PATH + '") == "' + SIF_PUBLIC_KEY + '",')
  info.script.AppendExtra('            (')
  info.script.AppendExtra('              ui_print("Flashing updated bootloader for fused sif");')
  info.script.AppendExtra('              package_extract_file("firmware-update/sif.blob", "' + STAGING_PART + '");')
  info.script.AppendExtra('            ),')
  info.script.AppendExtra('            (')
  info.script.AppendExtra('              ui_print("Unknown public key " + read_file("' + PUBLIC_KEY_PATH + '") + " for sif detected.");')
  info.script.AppendExtra('              ui_print("This is not supported. Please report to LineageOS Maintainer.");')
  info.script.AppendExtra('              abort();')
  info.script.AppendExtra('            )')
  info.script.AppendExtra('          )')
  info.script.AppendExtra('        );')
  info.script.AppendExtra('        package_extract_file("install/sif.dtb.img", "' + DTB_PART + '");')
  info.script.AppendExtra('      )')
  info.script.AppendExtra('    );')

  info.script.AppendExtra('  ),')

  """ If not fused """
  info.script.AppendExtra('  (')

  """ Unfused darcy """
  info.script.AppendExtra('    ifelse(')
  info.script.AppendExtra('      getprop("ro.hardware") == "darcy",')
  info.script.AppendExtra('      (')
  info.script.AppendExtra('        ifelse(')
  info.script.AppendExtra('          is_substring("tegra210b01", read_file("' + DTSFILENAME_PATH + '")),')
  """ mdarcy """
  info.script.AppendExtra('          (')
  info.script.AppendExtra('            ifelse(')
  info.script.AppendExtra('              getprop("ro.bootloader") == "' + DARCY_BL_VERSION + '",')
  info.script.AppendExtra('              (')
  info.script.AppendExtra('                ui_print("Correct bootloader already installed for unfused mdarcy");')
  info.script.AppendExtra('              ),')
  info.script.AppendExtra('              (')
  info.script.AppendExtra('                ui_print("This is an unfused mdarcy.");')
  info.script.AppendExtra('                ui_print("This is not supported. Please report to LineageOS Maintainer.");')
  info.script.AppendExtra('                abort();')
  info.script.AppendExtra('              )')
  info.script.AppendExtra('            );')
  info.script.AppendExtra('            package_extract_file("install/mdarcy.dtb.img", "' + DTB_PART + '");')
  info.script.AppendExtra('          ),')
  """ darcy """
  info.script.AppendExtra('          (')
  info.script.AppendExtra('            ui_print("Darcy is not supported in this build. Please install a `foster` build instead.");')
  info.script.AppendExtra('            abort();')
  info.script.AppendExtra('          )')
  info.script.AppendExtra('        )')
  info.script.AppendExtra('      )')
  info.script.AppendExtra('    );')

  """ Unfused sif """
  info.script.AppendExtra('    ifelse(')
  info.script.AppendExtra('      getprop("ro.hardware") == "sif",')
  info.script.AppendExtra('      (')
  info.script.AppendExtra('        ifelse(')
  info.script.AppendExtra('          getprop("ro.bootloader") == "' + DARCY_BL_VERSION + '",')
  info.script.AppendExtra('          (')
  info.script.AppendExtra('            ui_print("Correct bootloader already installed for unfused sif");')
  info.script.AppendExtra('          ),')
  info.script.AppendExtra('          (')
  info.script.AppendExtra('            ui_print("This is an unfused sif.");')
  info.script.AppendExtra('            ui_print("This is not supported. Please report to LineageOS Maintainer.");')
  info.script.AppendExtra('            abort();')
  info.script.AppendExtra('          )')
  info.script.AppendExtra('        );')
  info.script.AppendExtra('        package_extract_file("install/sif.dtb.img", "' + DTB_PART + '");')
  info.script.AppendExtra('      )')
  info.script.AppendExtra('    );')

  info.script.AppendExtra('  )')
  info.script.AppendExtra(');')
  info.script.AppendExtra('package_extract_file("install/vbmeta_skip.img", "' + VBMETA_PART + '");')
