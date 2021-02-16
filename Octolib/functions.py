import requests
import git
import json
import os
import sys
import zipfile
import shutil

class octo_login:
    def __init__(self, username, token):
        self.username = username
        self.token = token
   
    def auth(self):
        git_session = requests.Session()
        git_session.auth = (self.username, self.token)
    

class octo_search:
    
    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        
    def search_user(self, user):
        url = "https://api.github.com/users/{}".format(self.user)
        
        r = requests.get(url)
        rop = json.loads(r.text)
        with open ('Database/JSON/gh_user_data.json', 'w') as gh_user_outfile:
            json.dump(rop, gh_user_outfile)
    
    def search_repo(self, repo):
        url = "https://api.github.com/repos/{}".format(self.repo)
        rop = json.loads(requests.get(url).text)
        with open('Database/JSON/gh_repo_data.json', 'w') as gh_repo_outfile:
            json.dump(rop, gh_repo_outfile)

class octo_download:
    
    def __init__(self, repo):
        self.repo = repo
       
    def download_repo(self):
        repo = "https://github.com/{}".format(self.repo)
        repo_json = "https://api.github.com/repos/{}".format(self.repo)
        
        r = requests.get(repo_json)
        rop = json.loads(r.text)
        with open('Database/JSON/gh_repo_data.json', 'w') as gh_repo_data:
            json.dump(rop, gh_repo_data)
        branch_js = str(rop['default_branch'])
        download_dir = 'Database/REPOSITORY'
        branch = [branch_js]
        
        
        if sys.platform == "win32":
            cmd = "rmdir " + download_dir + "/s /q"
        else:
            cmd = "rm -rf " + download_dir
            
        if os.path.exists(download_dir):
            os.system(cmd)
        os.makedirs(download_dir)
        
        for i in branch:
            new_dir = download_dir + '/' + i
            repo_git = git.Repo.clone_from(repo, new_dir, branch=i)
        with open('Database/JSON/gh_repo_data.json', 'r') as gh_repo_data:
            js = json.load(gh_repo_data)
            
        zip_name = "{}".format(js['name'])
        if os.path.exists(zip_name + ".zip"):
            os.remove(zip_name + ".zip")
            
        zfile = zipfile.ZipFile(zip_name + ".zip", 'w')
        for directory, subdirectory, files in os.walk(download_dir):
            for file in files:
                zfile.write(os.path.join(directory, file), os.path.relpath(os.path.join(directory, file), download_dir), compress_type=zipfile.ZIP_DEFLATED)
        zfile.close()
        shutil.rmtree(download_dir, True)
        os.system(cmd)
        
        