from typing import List
from typing import Callable

from core.model.app_model import AppModel
from core.model.library import Library
from core.model.profile import Profile
from core.model.script import Script
from core.utility.configuration import Configuration
from core.service.library_service import library_service
from core.service.profile_service import ProfileService


class AppService:

    profile_service: ProfileService = ProfileService()
    configuration: Configuration = Configuration()

    app_model: AppModel = AppModel()
    profile_selected_events: List[Callable] = []
    library_selected_events: List[Callable] = []

    # region public methods

    def get_library_list(self) -> List[Library]:
        return library_service.repository.library_list

    def get_profile_list(self) -> List[Profile]:
        return self.profile_service.repository.profile_list

    def get_selected_library_scripts(self) -> List[Script]:
        if not self.app_model.selected_library_id:
            return []

        library = library_service.find(self.app_model.selected_library_id)
        return library.script_list if library else []

    def get_selected_profile_scripts(self) -> List[Library]:
        if not self.app_model.selected_profile_id:
            return []

        return self.profile_service.get_profile_scripts(
            self.app_model.selected_profile_id)

    def refresh(self):
        self.app_model.main_window.refresh()

    def save_configuration(self):
        self.configuration.save(self.profile_service.repository,
                                library_service.repository)

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
        library = library_service.find(identifier)
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
