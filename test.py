from upload_session import *

def upload_file(file_path,drive_id,driveitem_id,access_token):
    with open(file_path,'rb') as target:
        content_bytes = target.read()
    new_session = UploadDriveItemSession(access_token,drive_id,driveitem_id,content_bytes)
    session_response = new_session.start()
    print("upload complete response: ", session_response)

def main():
    ##################################
    # Replace These With Your Values#
    ###############################
    filepath = "path to file you would like to upload"
    drive_id = "ID of drive on Microsoft graph"
    driveitem_id = "Driveitem ID on microsoft graph"
    access_token = "Access Token For the Graph"
    upload_file(filepath,drive_id,driveitem_id,access_token)

if __name__ == '__main__':
    main()
