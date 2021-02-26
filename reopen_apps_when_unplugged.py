import subprocess
import yaml
import time

# SETTINGS
MAIN_DISPLAY_NAME = 'Color LCD'  # name of the laptop screen
SLEEP_TIME = 2  # sleep time between checks 
APPS_TO_REOPEN = ['Telegram', 'Messages', 'Pycharm']  # list of apps that you want to reopen


def open_app(app_name: str):
    """
    Function to open an app

    :param app_name: name of the app you want to open
    """
    subprocess.Popen(["open", "-n", f'/System/Applications/{app_name}.app'], stdout=subprocess.PIPE)
    subprocess.Popen(["open", "-n", f'/Applications/{app_name}.app'], stdout=subprocess.PIPE)


def close_app(app_name: str):
    """
    Function to close an app

    :param app_name: name of the app you want to close
    """
    subprocess.call(['osascript', '-e', f'tell application "{app_name}" to quit'])


def check_if_app_is_running(app_name: str) -> bool:
    """
    Function utilizing Apple script to check if app is running or not.
    When running for the first time you might be prompted to grant access to System Events to Terminal.app

    :param app_name: name of the app you want to check
    :return:
    """
    count = int(subprocess.check_output(["osascript",
                                         "-e", "tell application \"System Events\"",
                                         "-e", "count (every process whose name is \"" + app_name + "\")",
                                         "-e", "end tell"]).strip())
    return count > 0


def reopen_app(app_name: str):
    if check_if_app_is_running(app_name) is True:
        print(f'Reopening {app_name}')
        close_app(app_name)
        open_app(app_name)


def reopen_apps_list(list_of_apps: list):
    for app in list_of_apps:
        reopen_app(app)


def check_if_main_only() -> bool:
    """
    Function utilizes system profiler and checks connected displays among GPUs

    """
    displays_yaml = subprocess.run(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE).stdout
    displays_yaml = yaml.safe_load(displays_yaml)

    graphics = displays_yaml['Graphics/Displays'].keys()

    for card in graphics:
        if 'Displays' in displays_yaml['Graphics/Displays'][card].keys():

            displays = displays_yaml['Graphics/Displays'][card]['Displays']
            amount_of_displays = len(displays_yaml['Graphics/Displays'][card]['Displays'])

            if amount_of_displays == 1 and MAIN_DISPLAY_NAME in displays.keys():
                return True
            else:
                return False


def do_if_unplugged():
    """
    what to do when unplugged
    """
    print('doing if unplugged')
    reopen_apps_list(APPS_TO_REOPEN)


def do_if_plugged():
    """
    what to do when plugged
    """
    print('doing if plugged')


current_state = check_if_main_only()

if __name__ == '__main__':
    while True:
        new_state = check_if_main_only()
        if new_state != current_state:

            if new_state is True:
                do_if_unplugged()
            else:
                do_if_plugged()

            current_state = new_state

        time.sleep(SLEEP_TIME)
