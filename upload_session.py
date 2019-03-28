import requests
import json
from datetime import datetime
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

class UploadSession:
    def __init__(self,access_token,resource,content_bytes,chunksize=10):
        chunksize = chunksize * 1048576
        divisor = 327680 # set by microsoft
        if((chunksize % divisor) == 0):
            self.chunksize = chunksize
        self.access_token = access_token
        self.resource = resource
        self.content_bytes = content_bytes
        self.content_length = len(content_bytes)
        self._init_session()

    def start(self):
        return self._upload()

    def _gen_headers(self):
        return {
            "authorization" : "Bearer " + self.access_token
        }

    def _init_session(self):
        headers = self._gen_headers()
        url = "https://graph.microsoft.com/v1.0" + self.resource
        response = requests.request("POST",url,headers=headers)
        json_res = json.loads(response.text)
        ## Set The Params ##
        with open("./session.json",'w') as t:
            t.write(json.dumps(json_res))

        self.upload_url = json_res["uploadUrl"]
        self.expiration_str = json_res["expirationDateTime"]
        dummy_exp = self.expiration_str.replace("Z","")
        self.exp_date = datetime.fromisoformat(dummy_exp)

    def _upload_chunk(self,start_index,end_index):
        headers = self._gen_headers()
        headers["Content-Range"] = "bytes " + str(start_index) + "-" + str(end_index - 1) + "/" + str(self.content_length)
        data = self.content_bytes[start_index:end_index]
        response = requests.request("PUT",self.upload_url,data=data,headers=headers)
        return response

    def _upload(self):
        self.current_byte = 0 #This is the first byte count
        self.b_start = True
        self.b_complete = False
        while(self.b_complete == False):
            self.end_byte = self.current_byte + self.chunksize
            if(self.end_byte > self.content_length):
                self.end_byte = self.content_length
            response = self._upload_chunk(self.current_byte,self.end_byte)
            if(response.status_code == 202):
                self.current_byte = self.end_byte
            elif((response.status_code == 200) or (response.status_code == 201)):
                self.b_complete = True
                return response.text
            else:
                return response.text

class UploadDriveItemSession(UploadSession):
    def __init__(self,accessToken,drive_id,driveitem_id,content_bytes):
        resource = "/drives/" + drive_id + "/items/" + driveitem_id + "/createUploadSession/"
        UploadSession.__init__(self,accessToken,resource,content_bytes)
