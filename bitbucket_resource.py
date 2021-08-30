# import requests module
import requests
from requests.auth import HTTPBasicAuth


class Bitbucket:
    def __init__(self, workspace, repo_name, username, password):
        self.workspace = workspace
        self.repo_name = repo_name
        self.username = username
        self.password = password
        self.base_url = "https://api.bitbucket.org/2.0/"


    @staticmethod
    def is_folder(var_name):
        if "." in var_name:
            return False
        elif var_name == "README":
            return False
        else:
            return True


    def read_repository(self):
        """returns dictionary of folders and files in repository"""
        response = requests.get(url=self.base_url + f"repositories/{self.workspace}/{self.repo_name}/src/master/",
                                auth=HTTPBasicAuth(self.username, self.password))

        response_data = response.json()

        num_repo_content = len(response_data["values"])

        repo_files = [response_data["values"][i]["path"] for i in range(num_repo_content)]

        folder_list = []
        file_list = []

        for element in repo_files:
            if Bitbucket.is_folder(element):
                folder_list.append(element)
            else:
                file_list.append(element)

        return {"folders": folder_list,
                "files": file_list}

    def category_content(self, folder_name):
        """returns list of files/sub-folders in the given folder"""
        response = requests.get(url=self.base_url + f"repositories/{self.workspace}/{self.repo_name}/src/master/{folder_name}/",
                                       auth=HTTPBasicAuth(self.username, self.password))

        response_data = response.json()

        num_folder_content = len(response_data["values"])

        folder_content = [response_data["values"][i]["path"].split("/")[1] for i in range(num_folder_content)]

        return folder_content



    def read_file(self, folder_name, file_name):
        """reads the content of the file in folder"""
        response = requests.get(
            url=self.base_url + f"repositories/{self.workspace}/{self.repo_name}/src/master/{folder_name}/{file_name}",
            auth=HTTPBasicAuth(self.username, self.password))

        return response.text

    def read_file_direct(self, file_name, separator):
        """reads the content of the file in repository.
        it returns Public part and Private part of file based on the separator"""
        response = requests.get(
            url=self.base_url + f"repositories/{self.workspace}/{self.repo_name}/src/master/{file_name}",
            auth=HTTPBasicAuth(self.username, self.password))

        return response.text.split(separator)
