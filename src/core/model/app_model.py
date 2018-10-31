from core.service.library_service import LibraryService


class AppModel():

    library_service = LibraryService()

    def __init__(self):
        self.application = None
        self.main_window = None

        self.selected_profile_id: str = None
        self.selected_library_id: str = None
