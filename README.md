# XP-Launcher

XP-Launcher is a console-based launcher tool written in Python that allows you to manage and launch various applications associated with Grand Theft Auto V (GTA V) cheats and mods. It provides a simple interface to start GTA V, open different cheat menus, and perform other related tasks.

## Features

- Launch GTA V
- Create and manage multiple profiles
- Specify update commands for files associated with profiles
- Delete existing profiles

## Installation

1. Clone this repository to your local machine:

   `git clone https://github.com/yesEngineer/XP-Launcher.git`

2. Install the required dependencies:

   `pip install -r requirements.txt`

## Usage

1. Run the app.py script:

   `python app.py`

2. Follow the on-screen prompts to select options from the menu.

3. To create a new profile, select the option "Create New Profile" and follow the prompts to enter profile details.

4. To delete an existing profile, select the option "Delete Profile" and follow the prompts to select the profile to delete.

5. To exit the XP-Launcher, select the option "Exit" from the main menu.

## Compiling to Executable

You can also compile the app.py script into a standalone executable using pyinstaller. Make sure you have pyinstaller installed, then run the following command:

   `pyinstaller --onefile --icon=icon.ico --name="XP-Launcher" app.py`

This will generate a single executable file named XP-Launcher.exe in the dist directory.

## Credits

XP-Launcher was created by yesEngineer.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
