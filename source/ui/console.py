from core.model.global_variable import GlobalVariable
from core.utility.configuration import Configuration

path = 'Z:\OneDrive\Scripts\AutoHotKey'


def get_action():
    print('Please enter an action: ')
    action = input()

# while True:
#     print('**************************************************************************************\n')
#     print('Initialize program')
#     print('Initialize manager')

#     # path = input()
#     repo_manager.add_library(path)
#     print(configs.save_repository(repo_manager.repository))
#     script = repo_manager.find_script(
#         'Z:\OneDrive\Scripts\AutoHotKey\Startup\Duplicate Line.ahk')
#     script2 = repo_manager.find_script(
#         'Z:\OneDrive\Scripts\AutoHotKey\Common\Select Line.ahk')

#     script.start()
#     script2.start()
#     # manager.add_profile('programming')
#     # manager.add_script_to_profile('programming', script)
#     print('Current running script')
#     for s in repo_manager.find_all_running_scripts():
#         print(s.to_string())

#     # print(manager.profile_list[0].name)
#     # print(manager.profile_list[0].script_list[0].script_path)
#     # print()

#     # for str in manager.to_string():
#     #     print(str)
#     input()

#     script.stop()
#     for s in repo_manager.find_all_running_scripts():
#         print(s.to_string())

#     input()

repo_manager = GlobalVariable.get_repo_manager()
repo_manager.add_library(path)
repo_manager.add_profile('programming')
repo_manager.add_profile('gaming')
# repo_manager = RepoManager.from_json(configs.load_repository())
repo_manager.refresh()
script = repo_manager.find_script('Z:\OneDrive\Scripts\AutoHotKey\Startup\Duplicate Line.ahk')
script2 = repo_manager.find_script(
    'Z:\OneDrive\Scripts\AutoHotKey\Common\Select Line.ahk')
repo_manager.add_script_to_profile('programming', script)
repo_manager.add_script_to_profile('gaming', script2)
gaming = repo_manager.find_profile('gaming')
programming = repo_manager.find_profile('programming')
gaming.start()
programming.start()
programming.stop()
input()
Configuration.get().save_repository(repo_manager)
