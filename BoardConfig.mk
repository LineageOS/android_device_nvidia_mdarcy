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

include device/nvidia/foster/BoardConfig.mk

BOARD_RECOVERYIMAGE_PARTITION_SIZE := 28835840
BOARD_SYSTEMIMAGE_PARTITION_SIZE   := 1616904192
BOARD_VENDORIMAGE_PARTITION_SIZE   := 268435456

# Assert
TARGET_OTA_ASSERT_DEVICE := mdarcy,sif

# Bootloader versions
TARGET_BOARD_INFO_FILE := device/nvidia/mdarcy/board-info.txt

# Boot image
BOARD_CUSTOM_BOOTIMG    := true
BOARD_CUSTOM_BOOTIMG_MK := device/nvidia/mdarcy/mkbootimg.mk
BOARD_MKBOOTIMG_ARGS    := --header_version 1
