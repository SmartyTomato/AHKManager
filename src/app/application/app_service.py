from typing import List
from typing import Callable

from src.core.model.app_model import AppModel
from src.core.model.library import Library
from src.core.model.profile import Profile
from src.core.model.script import Script
from src.core.utility.configuration import Configuration
from src.core.service.library_service import library_service
from src.core.service.profile_service import profile_service


class AppService:

    configuration: Configuration = Configuration()

    app_model: AppModel = AppModel()
    profile_selected_events: List[Callable] = []
    library_selected_events: List[Callable] = []

    # region public methods

    def get_library_list(self) -> List[Library]:
        return library_service.repository.library_list

    def get_profile_list(self) -> List[Profile]:
        return profile_service.repository.profile_list

    def get_selected_library_scripts(self) -> List[Script]:
        if not self.app_model.selected_library_id:
            return []

        library = library_service.find(self.app_model.selected_library_id)
        return library.script_list if library else []

    def get_selected_profile_scripts(self) -> List[Library]:
        if not self.app_model.selected_profile_id:
            return []

        return profile_service.get_profile_scripts(
            self.app_model.selected_profile_id)

    def refresh(self):
        self.app_model.main_window.refresh()

    def save_configuration(self):
        self.configuration.save(profile_service.repository,
                                library_service.repository)

    # endregion public methods

    # region events

    def on_profile_selected(self, identifier: str):
        profile = profile_service.find(identifier)
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
