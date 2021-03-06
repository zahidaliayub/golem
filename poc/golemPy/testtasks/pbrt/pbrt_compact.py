import os
import glob
import cPickle as pickle
import zlib
import subprocess
import platform, psutil
import win32api, win32process

############################
def format_pbrt_cmd( renderer, startTask, endTask, totalTasks, numSubtasks, numCores, outfilebasename, scenefile ):
    return "{} --starttask {} --endtask {} --outresultbasename {} --totaltasks {} --ncores {} --subtasks {} {}".format( renderer, startTask, endTask, outfilebasename, totalTasks, numCores, numSubtasks, scenefile )

############################
def run_pbrt_task( pathRoot, startTask, endTask, totalTasks, numSubtasks, numCores, outfilebasename, sceneFile ):
    pbrt = os.path.join( resourcePath, "pbrt.exe" )

    outputFiles = os.path.join( tmpPath, outfilebasename )

    files = glob.glob( outputFiles + "*.exr" )

    for f in files:
        os.remove(f)

    cmd = format_pbrt_cmd( pbrt, startTask, endTask, totalTasks, numSubtasks, numCores, outputFiles, os.path.join( resourcePath, sceneFile ) )
    
    print cmd
   
    pc = subprocess.Popen( cmd )

    win32process.SetPriorityClass( pc._handle, win32process.IDLE_PRIORITY_CLASS )

    pc.wait()

    print outputFiles

    files = glob.glob( outputFiles + "*.exr" )

    print files

    res = []

    for f in files:
        fh = open( f, "rb" )
        fileData = fh.read()
        fileData = zlib.compress( fileData, 9 )
        #fileData = u"11111111111111111"
        res.append( pickle.dumps( ( os.path.basename( f ), fileData ) ) )
        fh.close()

    return res


output = run_pbrt_task( pathRoot, startTask, endTask, totalTasks, numSubtasks, numCores, outfilebasename, sceneFile )
        