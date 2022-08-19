# by katznboyz
# my links:
# - twitter.com/terrible_at_seo
# - artstation.com/katznboyz
# - youtube.com/c/katznboyz
# report issues to the repo https://github.com/katznboyz1/blender-multi-instance-rendering
# you may make changes to this and redistribute it, just don't sell it

print('[GPUINSTANCERENDER] STARTING SETUP')

from os.path import exists
import time, os, bpy

TMP_PATH_FOR_DATA = '/tmp/running-renders-blender-multi-instance-rendering.txt'
IS_MASTER_PROGRAM = False
PROCESS_ID = time.time()
NUMBER_OF_PROCESSES_TO_SPAWN = 0
DESIRED_GPU_TYPE = bpy.context.preferences.addons['cycles'].preferences.compute_device_type

# check if the tmp file exists
# if it doesnt, then initialize it
# if this was the program to initialize it, then it is the master program
IS_MASTER_PROGRAM = not exists(TMP_PATH_FOR_DATA)

if (IS_MASTER_PROGRAM): print('[GPUINSTANCERENDER] MASTER PROGRAM IDENTIFIED')

if (IS_MASTER_PROGRAM):
    tmpTrackerFile = open(TMP_PATH_FOR_DATA, 'w')
    tmpTrackerFile.write('\n')
    tmpTrackerFile.close()
    
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        if (device.use and device.type == DESIRED_GPU_TYPE):
            NUMBER_OF_PROCESSES_TO_SPAWN += 1
            print('[GPUINSTANCERENDER] FOUND MATCHING DEVICE {} TOTAL DEVICES {}'.format(device.id, NUMBER_OF_PROCESSES_TO_SPAWN))
    
    for process in range(NUMBER_OF_PROCESSES_TO_SPAWN):
        os.system('cd "{}"'.format(bpy.app.binary_path.replace('blender.exe', '')))
        os.system('start blender.exe -b "{}" -a --python spawner.py'.format(bpy.data.filepath))
    
else:
    print('[GPUINSTANCERENDER] SUB PROGRAM IDENTIFIED')
    tmpTrackerFileContents = str(open(TMP_PATH_FOR_DATA, 'r').read())
    tmpTrackerFile = open(TMP_PATH_FOR_DATA, 'a')
    tmpTrackerFile.write('{}\n'.format(PROCESS_ID))
    tmpTrackerFile.close()
    time.sleep(1)
    PROCESS_INDEX = tmpTrackerFileContents.count('.')
    
    print('[GPUINSTANCERENDER] SUB PROGRAM STARTING WITH INDEX {}'.format(PROCESS_INDEX))
    deviceIndex = 0
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        if (device.use and device.type == DESIRED_GPU_TYPE):
            if (deviceIndex == PROCESS_INDEX): 
                device.use = True
                print('[GPUINSTANCERENDER] INSTANCE {} ENABLING GPU ID {}'.format(PROCESS_INDEX, deviceIndex))
            else: 
                device.use = False
                print('[GPUINSTANCERENDER] INSTANCE {} DISABLING GPU ID {}'.format(PROCESS_INDEX, deviceIndex))
            deviceIndex += 1
    ctx = bpy.context
    ctx.scene.render.use_overwrite = False
    ctx.scene.render.use_placeholder = True
    bpy.ops.render.render()
    
    print('[GPUINSTANCERENDER] SUB PROGRAM UNREGISTERING')
    deviceIndex = 0
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        if (device.type == DESIRED_GPU_TYPE):
            device.use = True
            print('[GPUINSTANCERENDER] INSTANCE {} RE-ENABLING GPU ID {}'.format(PROCESS_INDEX, deviceIndex))
            deviceIndex += 1
    tmpTrackerFileContents = str(open(TMP_PATH_FOR_DATA, 'r').read())
    tmpTrackerFile = open(TMP_PATH_FOR_DATA, 'w')
    tmpTrackerFile.write(tmpTrackerFileContents.replace('{}\n'.format(PROCESS_ID), ''))
    tmpTrackerFile.close()
    tmpTrackerFileContents = str(open(TMP_PATH_FOR_DATA, 'r').read())
    if (tmpTrackerFileContents.count('.') == 0): os.remove(TMP_PATH_FOR_DATA)
    
    print('[GPUINSTANCERENDER] SUB PROGRAM EXITED SUCCESSFULLY')