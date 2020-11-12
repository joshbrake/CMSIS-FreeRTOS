# PlatformIO library build script (in combination with library.json)
# Author: Josh Brake
# Copyright (c) 2020

# Example platformio.ini
#   [env:genericSTM32F401RE]
#   platform = ststm32
#   board = genericSTM32F401RE
#   framework = cmsis
#   build_flags =
#     -D FREERTOS_HEAP_IMPLEMENTATION=heap_1.c
#     -D FREERTOS_MCU_FAMILY=ARM_CM4
#   lib_deps = https://github.com/joshbrake/CMSIS-FreeRTOS

# In addition, it is necessary to place FreeRTOSConfig.h and RTE_Components.h
# files in the project source directory.

import sys
from os.path import isdir, join, realpath

Import('env')

build_flags = env.ParseFlags(env['BUILD_FLAGS'])
defines = {item[0]: item[1] for item in build_flags.get("CPPDEFINES") if len(item)==2}

mcu_family = defines.get("FREERTOS_MCU_FAMILY")
if mcu_family is None:
    sys.stderr.write("Error: FREERTOS_MCU_FAMILY not defined. Please add it to your build_flags.\n"
                     "Example: build_flags = -D FREERTOS_MCU_FAMILY=ARM_CM4\n")
    env.Exit(1)

heap_implementation = defines.get("FREERTOS_HEAP_IMPLEMENTATION", "1")

global_env = DefaultEnvironment()
platform = global_env.PioPlatform()
CMSIS_FRAMEWORK = platform.get_package_dir("framework-cmsis")

env.Append(
    CPPPATH=[
        realpath(join("Source", "portable", "GCC", mcu_family)),
        realpath(join(CMSIS_FRAMEWORK, "CMSIS", "RTOS2", "Include")),
        join(env.get("PROJECTSRC_DIR")), # For FreeRTOSConfig.h
    ]
)

env.Append(
    SRC_FILTER=[
        "-<*>",
        "+<CMSIS/RTOS2/FreeRTOS/Source/*.c>",
        "+<Source/*.c>",
        "+<Source/portable/*.c>",
        "+<Source/portable/GCC/%s/*.c>" % mcu_family,
        "+<Source/portable/MemMang/heap_%s.c>" % heap_implementation,
    ]
)