import sys
import camera_func
import os

if __name__ == '__main__':  # the main of the program
    os.startfile("C:\\Program Files (x86)\\OceanTech\\OceanTechSideScanSonarPro\\x86\\OceanTechSideScanSonarPro.exe")
    sys.setswitchinterval(0.001)
    P = camera_func.Camera()
    P.opencamera.join()
    P.video.join()
