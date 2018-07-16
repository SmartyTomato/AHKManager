from core.model.app_model import AppModel
from core.model.singleton import Singleton
from core.service.library_service import LibraryService
from core.service.profile_service import ProfileService


class AppService(Singleton):

    library_service: LibraryService = LibraryService()
    profile_service: ProfileService = ProfileService()

    def __init__(self):
        self.app_model: AppModel = AppModel()
        self.profile_selected_events: 'Method' = []
        self.library_selected_events: 'Method' = []

    def update_lists(self):
        self.update_library_list()
        self.update_profile_list()

    def update_library_list(self):
        self.app_model.libray_list = self.library_service.repository.library_list
        if self.app_model.selected_library:
            self.on_library_selected(self.app_model.selected_library.identifier())

    def update_profile_list(self):
        self.app_model.profile_list = self.profile_service.repository.profile_list
        if self.app_model.selected_profile:
            self.on_profile_selected(self.app_model.selected_profile.identifier())

    def on_profile_selected(self, identifier: str):
        profile = self.profile_service.find(identifier)
        if not profile:
            self.app_model.selected_profile = None
            self.app_model.profile_scripts = []
        else:
            self.app_model.selected_profile = profile
            self.app_model.profile_scripts = self.profile_service.get_profile_scripts(identifier)

        self.exec_events(self.profile_selected_events)

    def on_library_selected(self, identifier: str):
        library = self.library_service.find(identifier)
        if not library:
            self.app_model.selected_library = None
            self.app_model.library_scripts = []
        else:
            self.app_model.selected_library = library
            self.app_model.library_scripts = library.script_list

        self.exec_events(self.library_selected_events)

    def exec_events(self, events):
        for method in events:
            try:
                method()
            except Exception as error:
                print(error)
