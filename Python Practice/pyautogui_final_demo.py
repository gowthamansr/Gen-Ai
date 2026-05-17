import pyautogui
import time

pyautogui.FAILSAFE = True

print("Automation starts in 5 seconds...")
time.sleep(5)

# Open Chrome
pyautogui.hotkey('win', 'r')
time.sleep(1)

pyautogui.write('chrome')
pyautogui.press('enter')

time.sleep(3)

# Search Google
pyautogui.hotkey('ctrl', 'l')

pyautogui.write('yesterday IPL match score')

pyautogui.press('enter')

time.sleep(5)

# Open first result
pyautogui.press('tab', presses=5)

pyautogui.press('enter')

print("Done")