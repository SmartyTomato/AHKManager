import os

from src.core.service.library_service import library_service
from src.core.service.message_service import MessageService
from src.core.service.profile_service import ProfileService
from src.core.utility.configuration import Configuration

path = os.getcwd() + '\\test_data\\AutoHotKey'

message_service = MessageService()
profile_service = ProfileService()
configuration = Configuration()
configuration.load()

library_service.add(path)
profile_service.add('programming')
profile_service.add('gaming')
# repo_manager = RepoManager.from_json(configs.load_repository())
library_service.refresh()
script = library_service.find_script(
    os.getcwd() + '\\test_data\\AutoHotKey\\Startup\\Duplicate Line.ahk')
script2 = library_service.find_script(
    os.getcwd() + '\\test_data\\AutoHotKey\\Common\\Select Line.ahk')
profile_service.add_script('programming', script)
profile_service.add_script('gaming', script2)
gaming = profile_service.find('gaming')
programming = profile_service.find('programming')

profile_service.start('gaming')
for msg in message_service.messages:
    print(msg)

profile_service.start('programming')
profile_service.stop('programming')
input()
