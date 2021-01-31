
import sys
from database_ini_parser import config
import os

path_params = config(filename="encrypted_settings.ini", section="path")
LOGS_DIR = path_params.get("logs_dir")

class StdoutRedirection:
    """Standard output redirection context manager"""

    def __init__(self, username):
        file_name = str(username)+'_stdout.txt'
        self._path = os.path.join('static','stdout',file_name)

    def __enter__(self):    
        sys.stdout = open(self._path, mode="w+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__



class ErrorStdoutRedirection:
    """Custom Error log output redirection """

    def __init__(self, username):
        file_name = str(username)+"_error.log"
        self._path = os.path.join(LOGS_DIR,file_name)

    def __enter__(self):    
        sys.stdout = open(self._path, mode="a+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__


class ProgressStdoutRedirection:
    """Custom Progress log output redirection """

    def __init__(self, username):
        file_name = str(username)+"_progress.log"
        self._path = os.path.join(LOGS_DIR,file_name)

    def __enter__(self):    
        sys.stdout = open(self._path, mode="a+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__


class ConsolidatedProgressStdoutRedirection:
    """Custom Consolidated Progress log output redirection """

    def __init__(self):
        file_name = "consolidated_progress.log"
        self._path = os.path.join(LOGS_DIR,file_name)

    def __enter__(self):    
        sys.stdout = open(self._path, mode="a+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__
