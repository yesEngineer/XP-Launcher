# Creation Date: 02/22/2024
# Creator ID: noEngineer/yesEngineer

import os
import time
import json
import webbrowser
import subprocess
from colorama import init, Fore, Style
import ctypes
import psutil

# Initialize colorama
init()

# Constants
DATA_FOLDER = os.path.join(os.getenv('APPDATA'), 'XP-Launcher', 'data')
PROFILES_FILE = os.path.join(DATA_FOLDER, 'profiles.json')
PROGRAM_TITLE = "XP-Launcher"

# Windows API constants
SW_SHOWNORMAL = 1
HWND_TOPMOST = 0
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040

class Profile:
    def __init__(self, name, paths, update_commands=None, start_gta=False, gta_path=None):
        self.name = name
        self.paths = paths
        self.update_commands = update_commands or []
        self.start_gta = start_gta
        self.gta_path = gta_path

    def open_profile(self):
        for path in self.paths:
            if path.startswith("http"):
                webbrowser.open(path)
            else:
                subprocess.Popen(path, shell=True)  # Start other programs

    def update(self):
        for command in self.update_commands:
            subprocess.run(command, shell=True)

    def start_gta_first(self):
        if self.start_gta and self.gta_path:
            if not self.is_gta_running():
                subprocess.Popen(self.gta_path, shell=True)  # Start GTA V
                print("Starting GTA V...")
                while not self.is_gta_running():
                    time.sleep(1)  # Check every 1 second if GTA V is running
                print("GTA V started successfully.")

    def is_gta_running(self):
        process_name = "GTA5.exe"
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.name() == process_name:
                return True
        return False



def create_profile():
    print_header("Create New Profile")
    name = input("Enter profile name: ")
    start_gta = input("Start GTA V with this profile? (y/n): ").lower() == 'y'
    gta_path = None
    if start_gta:
        gta_path = input("Enter the path to GTA V shortcut (Grand Theft Auto V.url): ")
    paths = input("Enter paths to files separated by commas: ").split(',')
    update_commands = input("Enter update commands separated by commas: ").split(',')
    profile = Profile(name, paths, update_commands, start_gta, gta_path)
    return profile

def load_profiles():
    profiles = []
    if os.path.isfile(PROFILES_FILE):
        with open(PROFILES_FILE, 'r') as f:
            for line in f:
                if line.strip():  # Check if line is not empty
                    profile_data = json.loads(line)
                    profile = Profile(profile_data['name'], profile_data['paths'], profile_data.get('update_commands', []), profile_data.get('start_gta', False), profile_data.get('gta_path'))
                    profiles.append(profile)
    return profiles

def save_profiles(profiles):
    with open(PROFILES_FILE, 'w') as f:
        for profile in profiles:
            profile_data = {'name': profile.name, 'paths': profile.paths, 'update_commands': profile.update_commands, 'start_gta': profile.start_gta, 'gta_path': profile.gta_path}
            json.dump(profile_data, f)
            f.write('\n')

def print_header(header_text):
    print("\n" + Fore.CYAN + Style.BRIGHT + f"== {header_text} ==" + Style.RESET_ALL)

def print_separator():
    print("-" * 40)

def center_window(hwnd):
    """Center the window on the screen."""
    user32 = ctypes.windll.user32
    screensize_x = user32.GetSystemMetrics(0)
    screensize_y = user32.GetSystemMetrics(1)
    window_rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(window_rect))
    window_width = window_rect.right - window_rect.left
    window_height = window_rect.bottom - window_rect.top
    new_x = screensize_x // 2 - window_width // 2
    new_y = screensize_y // 2 - window_height // 2
    user32.SetWindowPos(hwnd, HWND_TOPMOST, new_x, new_y, 0, 0, SWP_NOSIZE | SWP_SHOWWINDOW)

def main():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    profiles = load_profiles()

    # Set console window title
    ctypes.windll.kernel32.SetConsoleTitleW(PROGRAM_TITLE)

    # Center console window
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    center_window(hwnd)

    while True:
        os.system("cls")
        print_header(PROGRAM_TITLE)
        print_separator()
        print("Select an option:")
        print("1. Profiles")
        print("2. Create New Profile")
        print("3. Delete Profile")
        print("4. Exit")
        print_separator()

        choice = input("Enter your choice: ")

        if choice == "1":
            os.system("cls")
            if not profiles:
                print("No profiles created yet.")
            else:
                print_header("Profiles")
                print_separator()  # Added separator here
                for i, profile in enumerate(profiles, 1):
                    print(f"{i}. {profile.name}")
                print_separator()
                print("0. Go back")
                print_separator()

                profile_choice = input("Enter profile number: ")
                if profile_choice == "0":
                    continue
                try:
                    profile_index = int(profile_choice)
                    if 0 < profile_index <= len(profiles):
                        profile = profiles[profile_index - 1]
                        profile.start_gta_first()  # Start GTA V if necessary
                        print(f"Updating profile '{profile.name}'...")
                        profile.update()
                        print(f"Starting profile '{profile.name}'...")
                        profile.open_profile()
                    else:
                        print("Invalid profile number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == "2":
            os.system("cls")
            profile = create_profile()
            profiles.append(profile)
            save_profiles(profiles)
            print(f"Profile '{profile.name}' created successfully.")
        elif choice == "3":
            os.system("cls")
            if not profiles:
                print("No profiles to delete.")
            else:
                print_header("Delete Profile")
                print_separator()  # Added separator here
                for i, profile in enumerate(profiles, 1):
                    print(f"{i}. {profile.name}")
                print_separator()
                print("0. Go back")
                print_separator()

                delete_choice = input("Enter profile number to delete: ")
                if delete_choice == "0":
                    continue
                try:
                    delete_index = int(delete_choice)
                    if 0 < delete_index <= len(profiles):
                        deleted_profile = profiles.pop(delete_index - 1)
                        save_profiles(profiles)
                        print(f"Profile '{deleted_profile.name}' deleted successfully.")
                    else:
                        print("Invalid profile number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == "4":
            print("Exiting XP-Launcher...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
