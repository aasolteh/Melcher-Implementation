import wx
import sys
import time

import GazeParser.Configuration
from GazeParser.TrackingTools import getController
from psychopy import visual, event, gui, core

import datetime
import random

CAL_WINDOW_WIDTH  = 1920
CAL_WINDOW_HEIGHT = 1080

time.clock = time.perf_counter

class Logger:
    def __init__(self, name):
        try:
            self.fd = open(name, "w")
        except:
            print(f"failed to open/create file: {name}")
    
    def log(self, item):
        self.fd.write(f"{datetime.datetime.now()}: {item}")
    
    def close(self):
        self.fd.close();


class Controller:
    def __init__(self):
        self.tracker = getController(backend='PsychoPy', configFile='./Config/TrackerSettings.cfg')
        self.logger = Logger(".\controller.log")
        self.logger.log(f"Initialized controller\n")
        self.win = visual.Window(size=(CAL_WINDOW_WIDTH, CAL_WINDOW_HEIGHT),units='pix')
    
    def log(self, name):
        self.logger.log(name)

    def connect(self, ip, _portSend, _portRecv):
        self.log(f"Controller requesting connection to SimpleGazeTracker...\n")
        self.tracker.connect(ip, portSend=_portSend, portRecv=_portRecv)
        time.sleep(0.05)
        self.log(f"Controller connection established\n")

        conf = GazeParser.Configuration.Config("./config/GazeParser-BenQ.cfg")
        self.tracker.openDataFile('datafile.csv', config=conf)

    def calibrate(self):
        calarea = [-600,-500,600,500]
        calTargetPos = [[   0,   0],
                        [-500,-400],[-500,  0],[-500,400],
                        [   0,-400],[   0,  0],[   0,400],
                        [ 500,-400],[ 500,  0],[ 500,400]]

        self.tracker.setCalibrationScreen(self.win)
        self.tracker.setCalibrationTargetPositions(calarea, calTargetPos)

        self.log("starting calibration loop...\n")
        winOpen = True
        while winOpen:
            res = self.tracker.calibrationLoop()
            if res=='q':
                try:
                    self.win.close()
                    winOpen = False
                except:
                    self.log("Calibration loop failed with error\n")
            if self.tracker.isCalibrationFinished():
                self.log("Calibration loop completed successfully\n")
                break

    def close(self):
        self.tracker.closeDataFile()
        self.log("Closing controller\n")
        self.logger.close()
