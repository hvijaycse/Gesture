import pyautogui
import time


def mouseActions(mouseActionQueue: list, stop):

    last_action = ''
    sleep_time = 0.05
    while True:
        # print(mouseActionQueue)
        if stop():
            print("Killing the Thread")
            break


        if mouseActionQueue:

            action = mouseActionQueue.pop()

            if last_action == "LEFTMOUSEDOWN" and action[0]!= "LEFTMOUSEDOWN":
                pyautogui.mouseUp(button='left')


            if action[0] == "CURSOR":
                pyautogui.moveTo(action[1][0], action[1][1])

            elif action[0] == "LEFTMOUSEDOWN" :
                
                if last_action != action[0]:
                    pyautogui.mouseDown(button="left")

                pyautogui.moveTo(action[1][0], action[1][1])
            
            elif action[0] == "LEFTMOUSEDOUBLECLICK" and last_action != "LEFTMOUSEDOUBLECLICK":
                pyautogui.doubleClick()

            
            elif action[0] == "SCROLL":
                if last_action == action[0]:
                    Nx, Ny = action[1]
                    diff_x = Px - Nx
                    diff_y = Py - Ny


                    if abs(diff_x) < 10:
                        diff_x = 0
                    if abs(diff_y) < 10:
                        diff_y = 0

                    if abs(diff_x) > abs(diff_y):
                        pyautogui.hscroll(
                            clicks=int(diff_x)*5)
                    else:
                        pyautogui.scroll(
                            clicks=int(diff_y)*5)
                Px, Py = action[1]
                
            
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