# blender-multi-instance-rendering

### A script that allows you to render using multiple GPUs at once in Blender.

***Disclaimers:***

- This is NOT an addon. It is a script that has to be added to every file you want to use multi-GPU rendering for. I'll make it into an addon in the future.

- This does NOT need administrator privileges to run.

- The script is not tested on Eevee, and CUDA Cycles GPU rendering, only on OPTIX Cycles GPU rendering. It will probably work just fine, though.

- The script follows your user settings, and has no settings menu.

- The script will only spawn as many instances as you have GPUs, so 1 GPU = 1 instance. This is to avoid trampling over the other processes.

***Setup:***

- Add the script `spawner.py` to your .blend file through the Blender text editor.

***Usage:***

- To render using multiple GPUs, run the script using the run arrow on the top of the text editor. This will open command prompt windows where you can monitor the new blender instances.

***Reporting Issues/Adding Suggestions***:

To report an issue, or add a suggestion, raise an issue on the repo: https://github.com/katznboyz1/blender-multi-instance-rendering
