import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
import iconGenerator as ig

def main():
    print("\nStarting Icon Generator")
    ig.parseArgs()
    ig.importObject()
    ig.setupCamera()
    #render is then handled from process information by the blender api

try:
    main()
except Exception as e:
    print(e)