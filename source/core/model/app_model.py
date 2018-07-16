from typing import List

from core.model.library import Library
from core.model.profile import Profile
from core.model.script import Script
from core.service.library_service import LibraryService


class AppModel(object):

    library_service = LibraryService()

    def __init__(self):
        self.profile_list: List[Profile] = []
        self.libray_list: List[Library] = []
        self.selected_profile: Profile = None
        self.selected_library: Library = None
        self.profile_scripts: List[Script] = []
        self.library_scripts: List[Script] = []
