#!/usr/bin/python

import time
import sys

# Default settings
otp_length = 4
start_range = 1001
speed = 1.0

def display_menu():
    print("\n--- Launcher Menu ---")
    print(f"1. Start brute force (current settings: OTP length = {otp_length}, Starting range = {start_range}, Speed = {speed} seconds)")
    print("2. Set OTP length (4 or 6)")
    print(f"3. Set starting range (current: {start_range})")
    print(f"4. Set entry speed (current: {speed} seconds)")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")

    if not choice.isdigit() or int(choice) not in range(1, 6):
        print("Invalid choice! Please enter a number between 1 and 5.")
        return display_menu()
    
    return int(choice)

def set_otp_length():
    global otp_length
    length = input(f"Enter OTP length (4 or 6, current: {otp_length}): ")
    if length not in ['4', '6']:
        print("Invalid OTP length! Please enter 4 or 6.")
    else:
        otp_length = int(length)

def set_starting_range():
    global start_range
    start_range_input = input(f"Enter starting range for OTP (e.g., 1001, current: {start_range}): ")
    if not start_range_input.isdigit():
        print("Invalid starting range! Please enter a numeric value.")
    else:
        start_range = int(start_range_input)

def set_speed():
    global speed
    speed_input = input(f"Enter delay between attempts in seconds (e.g., 0.5 for faster, 1 for normal, current: {speed}): ")
    try:
        speed = float(speed_input)
        if speed < 0:
            raise ValueError
    except ValueError:
        print("Invalid speed! Please enter a positive number.")

def brute_force_otp():
    print("Starting brute force in 5 seconds...")
    time.sleep(5)
    
    max_value = 10**otp_length - 1  # e.g., 9999 for 4-digit, 999999 for 6-digit
    
    for otp in range(start_range, max_value + 1):
        otp_str = str(otp).zfill(otp_length)  # Ensure the OTP has the correct length (e.g., 0001, 0023)
        
        # Simulate the OTP entry and submission (replace these with actual code to interact with the target system)
        print(f"Trying OTP: {otp_str}")
        # Here you would replace the print statement with the code to enter OTP and submit it

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
            print("Invalid option! Please select a valid option.")

if __name__ == "__main__":
    main()
