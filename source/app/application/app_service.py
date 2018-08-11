from typing import List

from core.model.app_model import AppModel
from core.model.singleton import Singleton
from core.model.library import Library
from core.model.profile import Profile
from core.model.script import Script
from core.service.library_service import LibraryService
from core.service.profile_service import ProfileService


class AppService(Singleton):

    library_service: LibraryService = LibraryService()
    profile_service: ProfileService = ProfileService()

    def __init__(self):
        self.app_model: AppModel = AppModel()
        self.profile_selected_events: 'Method' = []
        self.library_selected_events: 'Method' = []

    # region public methods

    def get_library_list(self) -> List[Library]:
        return self.library_service.repository.library_list

    def get_profile_list(self) -> List[Profile]:
        return self.profile_service.repository.profile_list

    def get_selected_library_scripts(self) -> List[Script]:
        if not self.app_model.selected_library_id:
            return []

        library = self.library_service.find(self.app_model.selected_library_id)
        return library.script_list if library else []

    def get_selected_profile_scripts(self) -> List[Library]:
        if not self.app_model.selected_profile_id:
            return []

        return self.profile_service.get_profile_scripts(
            self.app_model.selected_profile_id)

    # endregion public methods

    # region events

    def on_profile_selected(self, identifier: str):
        profile = self.profile_service.find(identifier)
        if not profile:
            self.app_model.selected_profile_id = None
        else:
            self.app_model.selected_profile_id = identifier

        self._exec_events(self.profile_selected_events)

    def on_library_selected(self, identifier: str):
        library = self.library_service.find(identifier)
        if not library:
            self.app_model.selected_library_id = None
        else:
            self.app_model.selected_library_id = identifier

        self._exec_events(self.library_selected_events)

    # endregion events

    # region private methods

    def _exec_events(self, events):
        for method in events:
            try:
                method()
            except Exception as error:
                print(error)

    # endregion private methods
