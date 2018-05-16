from source.core.manager import Manager

path = 'H:\OneDrive\Sync\Scripts\AutoHotKey'


def get_action():
    print('Please enter an action: ')
    action = input()


while True:
    print('**************************************************************************************\n')
    print('Initialize program')
    print('Initialize manager')

    manager = Manager()

    # path = input()

    manager.add_repository(path)

    script = manager.find_script('H:\OneDrive\Sync\Scripts\AutoHotKey\Programming\SQL\Select From.ahk')

    manager.add_profile('programming')
    manager.add_script_to_profile('programming', script)

    print(manager.profile_list[0].name)
    print(manager.profile_list[0].script_list[0].script_path)

    input()
