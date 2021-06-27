import pyautogui
import time
from platform import  system

def mouseActions(
    mouseActionQueue: list, 
    stop,
    scroll_reverse = False):

    last_action = ''
    sleep_time = 0.1

    if system() == "Darwin":
        command_key = 'command'
    else:
        command_key = 'win'


    while True:
        # print(mouseActionQueue)
        if stop():
            print("Killing the Thread")
            break


        if mouseActionQueue:

            action = mouseActionQueue.pop()

            if last_action == "LEFTMOUSEDOWN" and  action[0]!= "LEFTMOUSEDOWN":
                    # print(action[0])
                    # print("Mouse Up")
                    # print("-"*20)
                    # print()
                    pyautogui.mouseUp(button='left')
            


            if action[0] == "CURSOR":
                pyautogui.moveTo(action[1][0], action[1][1])

            elif action[0] == "LEFTMOUSEDOWN" :

                if last_action != action[0]:
                    # print("-"*20)
                    pyautogui.mouseDown(button="left")
                else:
                    # print("MOUSE MOVE")
                    pyautogui.moveTo(action[1][0], action[1][1])
            
            elif action[0] == "LEFTMOUSEDOUBLECLICK" and last_action != "LEFTMOUSEDOUBLECLICK":
                pyautogui.doubleClick()

            
            elif action[0] == "SCROLL":
                if last_action == action[0]:
                    Nx_Scroll, Ny_Scroll = action[1]
                    diff_x_Scroll = Px_Scroll - Nx_Scroll
                    diff_y_Scroll = Py_Scroll - Ny_Scroll
                    
                    if not scroll_reverse:
                        diff_x_Scroll, diff_y_Scroll = -diff_x_Scroll, -diff_y_Scroll

                    if abs(diff_x_Scroll) > abs(diff_y_Scroll):
                        pyautogui.hscroll(
                            clicks=int(diff_x_Scroll)*10)
                    else:
                        pyautogui.scroll(
                            clicks=int(diff_y_Scroll)*15)
                Px_Scroll, Py_Scroll = action[1]

            elif action[0] == "TASKVIEW":
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
            if last_action == "CLICK":
                pyautogui.mouseUp(button='left')
            time.sleep(sleep_time)