#Get Mouse Position
import pyautogui
position = pyautogui.position()

print(position)

#Move Mouse
pyautogui.moveTo(500, 300, duration=2)

#Relative Mouse Movement
pyautogui.moveRel(100, 50, duration=1)

#Mouse Click
pyautogui.click(600, 400)

#Mouse Double Click
pyautogui.doubleClick(600, 400)

#mouse Right Click
pyautogui.rightClick(600, 400)

#Mouse Drag
pyautogui.dragTo(700, 500, duration=2)

# Keyboard Automation
pyautogui.write("Python Automation", interval=0.2)

# Multiple Keys
pyautogui.press(["tab", "tab", "enter"])

pyautogui.hotkey("ctrl", "c")