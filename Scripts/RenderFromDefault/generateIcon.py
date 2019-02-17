import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
import iconGenerator as ig

def main():
    print("\nStarting Icon Generator")
    ig.resetSceneFromFactory()
    ig.parseArgs()
    ig.importObject()
    ig.setupRenderSettings()
    ig.setupCamera()
    #ig.setupLighting()
    #ig.setupPostprocessing()
    #ig.setupRender()
    #render is then handled from process information by the blender api

try:
    main()
except Exception as e:
    print(e)