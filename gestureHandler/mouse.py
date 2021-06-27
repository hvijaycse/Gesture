# Importing all the modules required

import pyautogui
import time
from platform import  system


def mouseActions(
    mouseActionQueue: list, 
    stop,
    scroll_reverse: bool = False
    ):

    '''
    This method is used with threading to perform
    mouse action getting input from mouseActionQueue

    args: 
    ----------------------------------------------------------------------  
    mouseActionQueue: list 

    "List of queue, to recive input from the main program, This is how
    main program communicate with the method thread."

    ----------------------------------------------------------------------

    stop: mehod

    "This method is used to stop the thread. If this method return True
    the tread will be stopped. 
    "

    ----------------------------------------------------------------------

    scroll_reverse: bool = True

    "
    This argument is used to reverse the scroll direction
    "
    
    '''

    # Setting variables
    last_action = ''
    sleep_time = 0.1

    # Setting command key based on OS.
    if system() == "Darwin":
        command_key = 'command'
    else:
        command_key = 'win'

    
    # Loop to read action from queue and perform
    # action based on them.

    while True:
        # Checking if thread needed to be stopped
        # or not 
        if stop():
            # Stopping the thread.
            break

        # Checking if there is any action that need to be performed.
        if mouseActionQueue:

            # Getting the action to be performred
            action = mouseActionQueue.pop()


            if last_action == "LEFTMOUSEDOWN" and  action[0]!= "LEFTMOUSEDOWN":
                    # Picking left mouse button up.
                    pyautogui.mouseUp(button='left')

            # perform action based upon input
            if action[0] == "CURSOR":
                # Moving the curosor
                pyautogui.moveTo(action[1][0], action[1][1])

            elif action[0] == "LEFTMOUSEDOWN" :
                # This will be used for drag and drop
                if last_action != action[0]:
                    # print("-"*20)
                    pyautogui.mouseDown(button="left")
                else:
                    # print("MOUSE MOVE")
                    pyautogui.moveTo(action[1][0], action[1][1])
            
            elif action[0] == "LEFTMOUSEDOUBLECLICK" and last_action != "LEFTMOUSEDOUBLECLICK":
                # Double click to open application
                # and directory in windows
                pyautogui.doubleClick()

            
            elif action[0] == "SCROLL":
                # This perform scrolling 
                if last_action == action[0]:
                    Nx_Scroll, Ny_Scroll = action[1]
                    diff_x_Scroll = Px_Scroll - Nx_Scroll
                    diff_y_Scroll = Py_Scroll - Ny_Scroll
                    
                    if not scroll_reverse:
                        diff_x_Scroll, diff_y_Scroll = -diff_x_Scroll, -diff_y_Scroll

                    if abs(diff_x_Scroll) > abs(diff_y_Scroll):
                        # Performing horizontal scroll
                        pyautogui.hscroll(
                            clicks=int(diff_x_Scroll)*10)
                    else:
                        # performing vertical scroll
                        pyautogui.scroll(
                            clicks=int(diff_y_Scroll)*15)
                
                # Storing the last coordinate.
                Px_Scroll, Py_Scroll = action[1]

            elif action[0] == "TASKVIEW":
                # This is used to open TaskView in windows
                if last_action != action[0]:
                    
                    pyautogui.hotkey(command_key, 'tab')
                  
                else:
                    time.sleep(sleep_time  * 2)
                
            
            elif action[0] == "ZOOM":
                # This does not work perfectly
                '''

                if last_action!= action[0]:

                    lastDis = action[1]
                
                diff = lastDis - action[1]

                lastDis = action[1]

                # print(diff, action[1])

                diff = diff*20

                if abs(diff) > 20 and abs(diff) < 50:
                    pyautogui.click()
                    pyautogui.keyDown('ctrl')

                    # if diff < 0:
                    #     button = '+'
                    # else:
                    #     button = '-'
                    # pyautogui.keyDown(button)
                    # pyautogui.keyUp(button)
                    pyautogui.scroll(-int(diff))
                    pyautogui.keyUp('ctrl')
                '''

                time.sleep(sleep_time)



            else:
                time.sleep(sleep_time)

            
            last_action = action[0]
            # print(action, last_action)
        else:
            if last_action == "LEFTMOUSEDOWN":
                pyautogui.mouseUp(button='left')
            time.sleep(sleep_time)


if __name__ == "__main__":
    print(
        '''
This program is used to perform mouse action.

It is required to be used with the Thread.

______________________________________________________________________
Method: mouseActions
----------------------------------------------------------------------
args:   
mouseActionQueue: list 

"List of queue, to recive input from the main program, This is how
main program communicate with the method thread."

----------------------------------------------------------------------

stop: mehod

"This method is used to stop the thread. If this method return True
the tread will be stopped. 
"

----------------------------------------------------------------------

scroll_reverse: bool = True

"
This argument is used to reverse the scroll direction
"
'''
    )