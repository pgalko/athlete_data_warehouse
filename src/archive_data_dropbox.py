import dropbox
import os

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        #upload a file to Dropbox using API v2
        
        dbx = dropbox.Dropbox(self.access_token,timeout=None)

        with open(file_from, 'rb') as f:
            file_size = os.path.getsize(file_from)
            CHUNK_SIZE = 8 * 1024 * 1024

            if file_size <= CHUNK_SIZE:
                dbx.files_upload(f.read(), file_to)
            else:
                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,offset=f.tell())
                commit = dropbox.files.CommitInfo(path=file_to)

                while f.tell() <= file_size:
                    if ((file_size - f.tell()) <= CHUNK_SIZE):
                        dbx.files_upload_session_finish(f.read(CHUNK_SIZE),cursor,commit)
                        break
                    else:
                        dbx.files_upload_session_append_v2(f.read(CHUNK_SIZE),cursor)
                        cursor.offset = f.tell()
            f.close()

class CheckIfFileExists:
    def __init__(self, access_token):
        self.access_token = access_token

    def check_if_file_exists(self,path):
        #check if file exists in dropbox

        dbx = dropbox.Dropbox(self.access_token)

        try:
            dbx.files_get_metadata(path)
            return True
        except:
            return False


def check_if_file_exists_in_dbx(file_name,dbx_auth_token,folder):
    access_token = dbx_auth_token
    checkIfFileExists = CheckIfFileExists(access_token)
    file_name_to = file_name
    file_path_to = '/'+folder+'/'+file_name_to

    file_exists = checkIfFileExists.check_if_file_exists(file_path_to)

    return file_exists


def download_files_to_dbx(file_path_from,file_name,dbx_auth_token,folder):
    access_token = dbx_auth_token
    transferData = TransferData(access_token)
    file_name_to = file_name
    file_path_to = '/'+folder+'/'+file_name_to

    file_from = file_path_from
    file_to = file_path_to

    transferData.upload_file(file_from, file_to)
