"""
Contains a manager to control and install new dependencies if they are
present in the new pulled version.
"""
import os
import subprocess

import asyncio

from custom_funcs import RequirementsSorted


class DependenciesManager:
    """
    A class to manage dependencies based on environment variables
    and requirements files.

    Attributes:
        env_file (str): Path to the environment file (e.g., .zshrc)
         to read and update environment variables.
        req_file (str): Path to the requirements file
         containing dependencies to be installed.
        env_name (str): Environment variable name to track the number
         of dependencies.
        command (str): Shell command to reload the environment variables
         after updating.
        sorter (type[RequirementsSorted]): Class type for sorting
         dependencies.
        env_content (str): Content read from the environment file.
    """

    # pylint: disable=R0913
    def __init__(
            self,
            env_file: str = '/home/vlf/.zshrc',
            reqs_file: str = './requirements.txt',
            env_name: str = 'DEPS_AMOUNT',
            command: str = 'zsh -c "source /home/vlf/.zshrc"',
            sorter: type[RequirementsSorted] = RequirementsSorted
            ) -> None:
        """
        Initialize the DependenciesManager with paths and configurations.

        :param env_file: Path to the environment file to read and update
         (default is '/home/flv/.zshrc').
        :param req_file: Path to the requirements file
         (default is './requirements.txt').
        :param env_name: Environment variable name to track the number
         of dependencies (default is 'DEPS_AMOUNT').
        :param command: Shell command to reload the environment
         variables (default is 'zsh -c "source /home/vlf/.zshrc"').
        :param sorter: Class type for sorting dependencies
         (default is RequirementsSorted).
        """
        self.env_file = env_file
        self.reqs_file = reqs_file
        self.env_name = env_name
        self.command = command
        self.sorter = sorter
        self.env_content = self.get_env_content()
        self.reqs_content = self.get_reqs_content()

    def sort_lines(self) -> None:
        """
        Sort the dependencies using the provided sorter class.

        This method runs the sorter asynchronously to sort
        the dependencies.
        """
        asyncio.run(self.sorter().sort_dependencies())

    def get_env_content(self) -> str:
        """
        Read the content of the environment file.

        :return: Content of the environment file as a string.
        """
        with open(self.env_file, 'r', encoding='utf-8') as file:
            env_content = file.read()
        return env_content

    def get_reqs_content(self) -> str:
        """
        Read the content of the requirements file.

        :return: Content of the requirements file as a string.
        """
        with open(self.reqs_file, 'r', encoding='utf-8') as file:
            reqs_content = file.read()
        return reqs_content

    def get_var(self) -> int:
        """
        Get the value of the environment variable, updating it
        if necessary.

        If the environment variable is not set, it calculates the number
        of dependencies
        and updates the environment file accordingly. It then reloads
        the environment.

        :return: Value of the environment variable as an integer.
        """
        value = os.getenv(self.env_name, '')
        if value == '':
            value = self.export_env_var()  # type: ignore
        value = int(value)  # type: ignore
        return value  # type: ignore

    def export_env_var(self) -> int:
        """
        Export a new environment variable by updating the environment
        file.

        This method appends the new environment variable to
        the environment file
        and sets it within the current process.

        :return: The number of dependencies as an integer.
        """
        deps_amount = len(self.reqs_content.split())
        with open(self.env_file, 'a', encoding='utf-8') as env_file:
            env_var = f'\nexport {self.env_name}={str(deps_amount)}'
            env_file.write(env_var)
        subprocess.run(self.command, shell=True, text=True, capture_output=True, check=True)
        value = len(self.reqs_content.split())
        os.environ[self.env_name] = str(value)
        return value

    @staticmethod
    def install_dependencies(dependencies: list[str]) -> None:
        """
        Install the list of dependencies using pip.

        :param dependencies: List of dependency strings to be installed.
        """
        for dep in dependencies:
            command = f'pip3 install {dep}'
            subprocess.run(command, shell=True, text=True, capture_output=True, check=True)

    def main(self) -> None:
        """
        Main method to handle dependency installation and sorting.

        It compares the current number of dependencies with
        the previously recorded amount,
        installs any new dependencies, and sorts the dependencies.
        """
        reqs_content_list = self.reqs_content.split()
        previous_amount = self.get_var()
        current_amount = len(reqs_content_list)
        if current_amount > previous_amount:
            diff = current_amount - previous_amount
            needed_deps = reqs_content_list[-1:-diff:-1]
            self.install_dependencies(needed_deps)

        self.sort_lines()


if __name__ == "__main__":
    DependenciesManager().main()
