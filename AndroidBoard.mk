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

-include device/nvidia/foster/AndroidBoard.mk

INSTALLED_DTBIMAGE_TARGET_mdarcy := $(PRODUCT_OUT)/install/mdarcy.dtb.img
$(INSTALLED_DTBIMAGE_TARGET_mdarcy): $(INSTALLED_KERNEL_TARGET) | mkdtimg
	echo -e ${CL_GRN}"Building mdarcy DTImage"${CL_RST}
	@mkdir -p $(PRODUCT_OUT)/install
	$(HOST_OUT_EXECUTABLES)/mkdtimg create $@ --id=2894 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-darcy-p2894-0050-a08-00.dtb --rev=0x0a8 --custom0=0x28 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-darcy-p2894-2551-b00-00.dtb --rev=0xb00 --custom0=2551 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-darcy-p2894-3551-b03-00.dtb --rev=0xb03 --custom0=3551

INSTALLED_DTBIMAGE_TARGET_sif    := $(PRODUCT_OUT)/install/sif.dtb.img
$(INSTALLED_DTBIMAGE_TARGET_sif): $(INSTALLED_KERNEL_TARGET) | mkdtimg
	echo -e ${CL_GRN}"Building sif DTImage"${CL_RST}
	@mkdir -p $(PRODUCT_OUT)/install
	$(HOST_OUT_EXECUTABLES)/mkdtimg create $@ --id=3425 --custom0=0x140 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a01.dtb --rev=0xa1 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a02.dtb --rev=0xa2 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a04.dtb --rev=0xa3 \
		$(KERNEL_OUT)/arch/arm64/boot/dts/tegra210b01-sif-p3425-0500-a04.dtb --rev=0xa4

ALL_DEFAULT_INSTALLED_MODULES += $(INSTALLED_DTBIMAGE_TARGET_mdarcy) $(INSTALLED_DTBIMAGE_TARGET_sif)

AVBTOOL_HOST := $(HOST_OUT_EXECUTABLES)/avbtool
INSTALLED_VBMETA_SKIP_TARGET := $(PRODUCT_OUT)/install/vbmeta_skip.img
$(INSTALLED_VBMETA_SKIP_TARGET): $(AVBTOOL_HOST)
	@$(AVBTOOL_HOST) make_vbmeta_image --flags 2 --padding_size 256 --output $@

ALL_DEFAULT_INSTALLED_MODULES += $(INSTALLED_VBMETA_SKIP_TARGET)
