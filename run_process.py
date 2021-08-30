# import requests module
import json
import warnings
warnings.filterwarnings("ignore")
from time import sleep
from bitbucket_resource import Bitbucket
from doc360_resource import Project_Api, Category, Article,Teams,Reader_Group

def run_process():
    """Required External Data"""
    workspace = "sample_workspace_id"
    repo_name = "sample_project"
    username = "bopod97869@fxseller.com"
    password = "P@ssword1"
    document360_token = "RKo/9SkC7rCD8/0Wfe1dts2OCgynxaVzF0/kU5Clg0qZTVSS0XkYoaDerbJdiYM6u0DxgYAU2mLM3HxX8pG7Z2wqBu5MALnsPprohmERARh3er7SCKwPdDNnJy04OkqAky/c4RzDJlifD3oPlvrCvw=="


    """Initiating objects of Document360 which will be needed"""
    project_360 = Project_Api(document360_token)
    category_360 = Category(document360_token)
    article_360 = Article(document360_token)
    teams_360 = Teams(document360_token)
    reader_group_360 = Reader_Group(document360_token)

    project_id_360 = project_360.get_project_id()
    user_id_360 = teams_360.primary_user_id()

    """Create Bitbucket Object"""
    bitbucket_obj = Bitbucket(workspace=workspace, repo_name=repo_name, username=username, password=password)


    """forming list of folders and files in repository"""
    repo_dict = bitbucket_obj.read_repository()
    folder_list, file_list = repo_dict["folders"], repo_dict["files"]



    """
    For Document360,
    Every folder will be treated as Category.
    Every sub-folder will be treated as sub-Category.
    Every file will be treated as article
    """


    """
    Since this is POC, we will keep process simple.
    Upon making changes to the Bitbucket repository, 
    the process will delete the existing categories and 
    recreate the categoies as per bitbucket repository
    """

    """To delete the categories, we execute the below code"""
    doc360_category_list = project_360.get_category_ID_list()
    if len(doc360_category_list.values()) > 0:
        for cat_id in list(doc360_category_list.values()):
            category_360.delete_category(cat_id)
            sleep(2)


    """Creating Files as Categories"""
    """Folder and File list"""
    repo_dict = bitbucket_obj.read_repository()
    folder_list, file_list = repo_dict["folders"], repo_dict["files"]

    """Read README file"""
    content_list = []
    for file_name in file_list:
        pub_content, prv_content = bitbucket_obj.read_file_direct(file_name=file_name, separator="DEVELOPER_SPECIFIC")
        content_list.append((pub_content, prv_content))

    """________________________________________________________________________________________________________________"""

    """Creating Category based on README.md file"""

    cat_file_params = [{
        "name": "Public_README",
        "project_version_id": project_id_360,
        "content": content_list[0][0],
        "category_type": 1,
        "user_id": user_id_360,
    },
        {
            "name": "Private_README",
            "project_version_id": project_id_360,
            "content": content_list[0][1],
            "category_type": 1,
            "user_id": user_id_360,
        }]

    for param in cat_file_params:
        category_360.post_add_category(parameters=param)
        sleep(2)

    """Forming Category List"""
    cat_list = project_360.get_category_ID_list()
    print(cat_list)

    """Public and Private Categories"""
    public_categories = [key for (key, value) in cat_list.items() if key.split("_")[0] == "Public"]
    private_categories = [key for (key, value) in cat_list.items() if key.split("_")[0] == "Private"]

    """Creating Reader Group"""
    # public

    param_1 = {
        "title": public_categories[0],
        # OPTIONAL_PARAMETER
        "description": "Docs for Public Viewing",
        "access_scope": {
            "access_level": 1,
            "categories": [cat_list[public_categories[0]]]
        },
    }

    # private

    param_2 = {
        "title": private_categories[0],
        # OPTIONAL_PARAMETER
        "description": "Docs for Private Viewing",
        "access_scope": {
            "access_level": 1,
            "categories": [cat_list[private_categories[0]]]
        },
    }

    for param in [param_1, param_2]:
        print(reader_group_360.post_add_group(parameters=param))
        sleep(2)



    # """Creating Categories in Document360 based on the folders in Bitbucket repository."""
    # for folder in folder_list:
    #     params = {"name":folder, "project_version_id":project_id_360}
    #     category_360.post_add_category(parameters=params)
    #     sleep(2)
    #
    #
    # """Creating Articles in their respective Categories in Document360 based on folder and files in Bitbucket"""
    # doc360_category_list = project_360.get_category_ID_list()
    # sleep(2)
    # for folder in folder_list:
    #     cat_id = doc360_category_list[folder]
    #     articles_in_cat = bitbucket_obj.category_content(folder)
    #     if len(articles_in_cat) > 0:
    #         for article in articles_in_cat:
    #             parameters = {
    #                 "title": article,
    #                 "category_id": cat_id,
    #                 "project_version_id": project_id_360,
    #                 "user_id": user_id_360,
    #                 "content": bitbucket_obj.read_file(folder, article),
    #             }
    #             article_360.post_add_article(parameters)
    #             sleep(2)
    #
    #
    # """Publishing the added Articles on Document360 website"""
    # article_list = project_360.get_article_ID_list()
    #
    # for folder in folder_list:
    #     cat_id = doc360_category_list[folder]
    #     articles_in_cat = bitbucket_obj.category_content(folder)
    #     if len(articles_in_cat) > 0:
    #         for article in articles_in_cat:
    #             parameters = {
    #                 "version_number": 1,
    #                 "user_id": user_id_360,
    #             }
    #             article_360.post_publish_article(id=article_list[article],parameters=parameters)
    #             sleep(2)
