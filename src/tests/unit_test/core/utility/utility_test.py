import pytest
from unittest.mock import MagicMock

from core.utility.utility import Utility


class UtilityTest:
    @pytest.fixture
    def utility(self):
        return Utility()

    def get_file_name_no_extension_test(self, utility):
        expected_result = 'test'
        file_name = 'test.py'
        file_path = 'C:\\test.py'

        utility.get_file_name = MagicMock(
            return_value=file_name)
        result = utility.get_file_name_no_extension(file_path)

        assert expected_result == result

    def get_file_name_no_extension_test_invalid_path(self, utility):
        expected_result = ''
        file_name = ''
        file_path = 'C:invalid**path'

        utility.get_file_name = MagicMock(
            return_value=file_name)
        result = utility.get_file_name_no_extension(file_path)

        assert expected_result == result

    def get_file_extension_test(self, utility):
        expected_result = '.py'
        file_name = 'test.py'
        file_path = 'C:\\test.py'

        utility.get_file_name = MagicMock(
            return_value=file_name)
        result = utility.get_file_extension(file_path)

        assert expected_result == result

    def get_file_extension_test_file_no_extension(self, utility):
        expected_result = ''
        file_name = 'test'
        file_path = 'C:\\test'

        utility.get_file_name = MagicMock(
            return_value=file_name)
        result = utility.get_file_extension(file_path)

        assert expected_result == result

if __name__ == '__main__':
    pytest.main()
