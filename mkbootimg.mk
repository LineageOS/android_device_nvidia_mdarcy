#
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

LOCAL_PATH := $(call my-dir)

INSTALLED_DTBIMAGE_TARGET_mdarcy_recovery := $(PRODUCT_OUT)/mdarcy_recovery.dtb.img
$(INSTALLED_DTBIMAGE_TARGET_mdarcy_recovery): $(INSTALLED_KERNEL_TARGET) | mkdtimg
	echo -e ${CL_GRN}"Building mdarcy recovery DTImage"${CL_RST}
	$(HOST_OUT_EXECUTABLES)/mkdtimg create $@ \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-darcy-p2894-0050-a08-00.dtb --id=2894 --rev=0x0a8 --custom0=0x28  \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-darcy-p2894-2551-b00-00.dtb --id=2894 --rev=0xb00 --custom0=2551  \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-darcy-p2894-3551-b03-00.dtb --id=2894 --rev=0xb03 --custom0=3551  \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a01.dtb      --id=3425 --rev=0xa1  --custom0=0x140 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a02.dtb      --id=3425 --rev=0xa2  --custom0=0x140 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a04.dtb      --id=3425 --rev=0xa3  --custom0=0x140 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a04.dtb      --id=3425 --rev=0xa4  --custom0=0x140

$(INSTALLED_BOOTIMAGE_TARGET): $(MKBOOTIMG) $(INTERNAL_BOOTIMAGE_FILES) $(BOOTIMAGE_EXTRA_DEPS)
	$(call pretty,"Target boot image: $@")
	$(hide) $(MKBOOTIMG) $(INTERNAL_BOOTIMAGE_ARGS) $(INTERNAL_MKBOOTIMG_VERSION_ARGS) $(BOARD_MKBOOTIMG_ARGS) --output $@
	$(hide) $(call assert-max-image-size,$@,$(BOARD_BOOTIMAGE_PARTITION_SIZE))

INTERNAL_RECOVERYIMAGE_ARGS += --recovery_dtbo $(INSTALLED_DTBIMAGE_TARGET_mdarcy_recovery)
$(INSTALLED_RECOVERYIMAGE_TARGET): $(recoveryimage-deps) $(RECOVERYIMAGE_EXTRA_DEPS) $(INSTALLED_DTBIMAGE_TARGET_mdarcy_recovery)
	$(call build-recoveryimage-target, $@, $(recovery_kernel))
