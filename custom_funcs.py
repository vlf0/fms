"""Module responsible for storage feature-func."""
from builtins import Exception
import os
import aiofiles


class ExtensionError(Exception):
    """Custom exception for unsupported file extensions."""

    def __init__(self, ext: str) -> None:
        """
        Instantiate `ExtensionError` class object.

        :param ext: Extension name of considered file.
        """
        super().__init__(ext)
        self.message = self.__create_message(ext)

    @staticmethod
    def __create_message(ext: str) -> str:
        """
        Create the error message for the unsupported file extension.

        :param ext: str: The unsupported file extension.
        :return: str: The error message.
        """
        return (f"Can't create instance with the {ext} extension."
                f" Allowed extension is {ConfigFilesSorter.allowed_extensions}")

    def __str__(self) -> str:
        """
        Return the error message.

        :return: str: The error message.
        """
        return self.message


class ConfigFilesSorter:
    """A class to sort dependencies in a configuration  file."""

    allowed_extensions = {'ini', 'config', 'toml'}

    def __init__(self, req_file: str) -> None:
        """
        Instantiate the `ConfigFilesSorter` instance.

        :param req_file: str: The name of the configuration  file.
        """
        super().__init__()
        self.root_path: str = os.path.dirname(os.path.abspath(__file__))
        self.req_file = req_file
        self.full_path: str = self.__get_full_path()
        self.__check_file_extension(self.req_file)

    def __get_full_path(self) -> str:
        """
        Get the full path of the configuration file.

        :return: str: The full path of the configuration file.
        """
        return rf'{self.root_path}\{self.req_file}'

    def __check_file_extension(self, req_file: str) -> None:
        """
        Check if the file extension is allowed.

        :param req_file: str: The name of the configuration file.
        :raise ExtensionError: If the file extension is not allowed.
        """
        req_file_extension = req_file.split('.')[1]
        if req_file_extension not in self.allowed_extensions:
            raise ExtensionError(req_file_extension)

    async def get_file_content(self) -> str:
        """
        Read the content of the configuration file.

        :return: str: The content of the configuration file.
        """
        async with aiofiles.open(file=self.req_file, mode='r', encoding='utf-8') as file:
            content = await file.read()
        return content

    async def sort_dependencies(self) -> None:
        """
        Sort the dependencies in the configuration file.

        :return: None
        """
        content = await self.get_file_content()
        removed_literals = content.replace('\n', ' ')
        dependencies_list = removed_literals.split(' ')
        extensions = [dependence.lower() for dependence in dependencies_list]
        extensions.sort()
        sorted_dependencies = '\n'.join(extensions)

        await self.__rewrite_requirements_file(sorted_dependencies)

    async def __rewrite_requirements_file(self, content: str) -> None:
        """
        Write the sorted dependencies back to the configuration file.

        :param content: str: The sorted dependencies.
        :return: None
        """
        async with aiofiles.open(self.req_file, 'w', encoding='utf-8') as file:
            await file.write(content)


class RequirementsSorted(ConfigFilesSorter):
    """A class to sort dependencies in the requirements.txt file."""

    allowed_extensions = {'txt'}

    def __init__(self, req_file: str = 'requirements.txt') -> None:
        """
        Instantiate `RequirementsSorted` class.

        :param req_file: str: The name of the configuration file (defaults to 'requirements.txt').
        """
        super().__init__(req_file)
        self.req_file = req_file
