from os import stat
from controller import Controller
from psychopy import visual, event, gui, core
from psychopy.hardware import keyboard
import time
import numpy as np
import neuro_constants as const
import random

PI = np.pi
CAL_WINDOW_WIDTH  = 1200
CAL_WINDOW_HEIGHT = 1000
iter = 90
deg  = [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]
degrees = int(iter / len(deg)) * deg
adaptor_orientation = int(iter / 2) * [0, 0]
random.shuffle(degrees)
random.shuffle(adaptor_orientation)


def eval_distance(point1, point2):
    diff = np.array(point1) - np.array(point2)
    return np.linalg.norm(diff)

def fixated(gaze_pos, stim_pos):
    p1 = np.array(gaze_pos)
    p2 = np.array(stim_pos)
    if(eval_distance(p1-p2, [0, 0]) < const.MAX_DEVIATION):
        return True
    else:
        return False

def wait_for_space():
    waitkeypress = True
    while waitkeypress:
        if 'space' in event.getKeys():
            waitkeypress = False

def wait_for_key(sub_data):
    waitkeypress = True
    while waitkeypress:
        key = event.getKeys()
        if 'right' in key:
            waitkeypress = False
            sub_data.append('r')
        elif 'left' in key:
            waitkeypress = False
            sub_data.append('l')

        

def get_state(time_s):
    time_ms         = time_s * 1000
    adapter         = const.ADAPTER
    first_fixation  = const.FIRST_FIXATION
    second_fixation = const.SECOND_FIXATION
    test            = const.TEST

    if(time_ms <= adapter):
        return "adapter"
    elif(time_ms <= adapter + first_fixation):
        return "first_fixation"
    elif(time_ms <= adapter + first_fixation + second_fixation):
        return "second_fixation"
    elif(time_ms <= adapter + first_fixation + second_fixation + test):
        return "test"
    # elif(time_ms <= adapter + first_fixation + second_fixation + test + 20):
    #     return "choose"
    else:
        return "none"
        
def gabor_position():
    rand = random.randrange(2)
    if rand == 0:
        xPos = 1800 * np.tan(5 * PI / 180)
    else:
        xPos = -1800 * np.tan(5 * PI / 180)
    
    rand = random.randrange(5)
    if   rand == 0:
        yPos  =  0
    elif rand == 1:
        yPos  =  1800 * np.tan(4 * PI / 180)
    elif rand == 2:
        yPos  =  1800 * np.tan(7 * PI / 180)
    elif rand == 3:
        yPos  = -1800 * np.tan(4 * PI / 180)
    elif rand == 4:
        yPos  = -1800 * np.tan(7 * PI / 180)
    
    return xPos, yPos
    
def set_orientation():
    rand = random.randrange(2)
    if rand == 1:
        return 20
    else:
        return -20

def test_orientation():
    rand = random.randrange(5)
    if   rand == 0:
        return -2
    elif rand == 1:
        return -1
    elif rand == 2:
        return  1
    elif rand == 3:
        return  2
    elif rand == 4:
        return  0
    
def run_neuro(iterations):
    # window               = visual.Window       (size = (CAL_WINDOW_WIDTH, CAL_WINDOW_HEIGHT))
    gaborStim            = visual.GratingStim  (controller.win, tex  = "sin", mask = "gauss", size = (200, 200), units = 'pix', phase = (1, 1))
    testStim             = visual.GratingStim  (controller.win, tex  = "sin", mask = "gauss", size = (200, 200), units = 'pix', phase = (1, 1))
    messageStim          = visual.TextStim     (controller.win, alignHoriz = 'left', pos = (-150, -150), height = 20, text = 'Enter left or right arrow', units = 'pix') 
    firstFixationCircle  = visual.Polygon      (controller.win, size = 10, edges=32, fillColor=(-1,-1,-1), lineColor=(-1,-1,-1), units = 'pix')
    secondFixationCircle = visual.Polygon      (controller.win, size = 10, edges=32, fillColor=(-1,-1,-1), lineColor=(-1,-1,-1), units = 'pix')
    continueMessage      = visual.TextStim     (controller.win, alignHoriz = 'left', pos = (-150, -150), height = 20, text = 'Please press space to continue the task', units = 'pix')
    gaborStim.sf = 5.0 / 100.0
    testStim.sf  = 5.0 / 100.0

    trialClock = core.Clock()

    subjectName  = input("Please enter your name:")
    fp = open(subjectName + "_task.csv",'w')
    subject_data = []
    correct_data = []
    orientations = []
    adaptor      = []
    controller.tracker.startRecording(message='starting task')

    controller.win.flip()
    continueMessage.draw()
    controller.win.flip()
    wait_for_space()
    for run in range(iterations):
        resetTimer = True

        #### Initializations:

        xPos, yPos               = gabor_position()
        firstFixationCircle.pos  = (xPos, 0)
        secondFixationCircle.pos = (xPos, 0)
        gaborStim.setPos           ((xPos, 0))
        gaborStim.ori            = adaptor_orientation.pop()
        testStim.ori             = degrees.pop()

        if (testStim.ori < 0):
            correct_data.append('l')
        else:
            correct_data.append('r')

        orientations.append(testStim.ori)
        adaptor.append(gaborStim.ori)
        rand = random.randrange(2)
        if rand == 1:
            testStim.setPos((xPos, 0))
        else:
            testStim.setPos((xPos, 0))
        
        #### Starting Task:

        # controller.win.flip()
        # continueMessage.draw()
        # controller.win.flip()
        # wait_for_space()
        state = const.ADAPTER_STATE
        while state != "none":
            try:
                gaze_pos = controller.tracker.getEyePosition()
            except:
                continue

            if(not fixated(gaze_pos, [xPos, 0])):
                resetTimer = True
                firstFixationCircle.draw()
                controller.win.flip()
                print("Try focusing on fixation point")
                continue

            if(resetTimer):
                    initTime = trialClock.getTime()
                    resetTimer = False
            
            currentTime = trialClock.getTime()
            state       = get_state(currentTime - initTime)
            controller.win.flip()
            if(state == const.ADAPTER_STATE):
                gaborStim.draw()
                firstFixationCircle.draw()
                continue
                
            elif(state == const.FIRST_FIXATION_STATE):
                firstFixationCircle.draw()
                continue
                
            elif(state == const.SECOND_FIXATION_STATE):
                secondFixationCircle.draw()
                continue
                
            elif(state == const.TEST_STATE):
                testStim.draw()
                secondFixationCircle.draw()
                continue

            # elif(state == const.CHOOSE_STATE):
            #     # window.flip()
            #     messageStim.draw()
            #     controller.win.flip()
            #     key = wait_for_key()
            #     if key == False:
            #         subject_data.append('l')
            #     elif key == True:
            #         subject_data.append('r')

            elif(state == "none"):
                messageStim.draw()
                controller.win.flip()
                wait_for_key(subject_data)
                # controller.win.flip()
                continue
            # else:
            #     break
        
    fp.write('SubjectAns,CorrectAns,Orientation,AdaptorOrientation\n')
    for i in range(len(correct_data)):
        fp.write(subject_data[i]+','+correct_data[i]+','+str(orientations[i])+','+str(adaptor[i])+'\n')
    fp.flush()

if __name__ == "__main__":
    controller = Controller()
    controller.connect("127.0.0.1", 10003, 10004)
    controller.calibrate()
    run_neuro(iter)
    core.quit()