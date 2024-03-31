import requests
from zipfile import ZipFile
import os


def update(url,structura_version, lookup_verison):
    initial_check = requests.get(url,headers={"structuraVersion": structura_version,"lookupVersion":lookup_verison}).json()
    print(initial_check)
    updated=False
    print(initial_check)
    if initial_check["info"] == 'Update Availible':
        print('Update Availible')
        print(initial_check["url"])
        response = requests.get(initial_check["url"], allow_redirects=True,stream=True)
        if response.headers.get('content-type') == "application/xml":
            print(response.content)
        else:
            with open("lookup_temp.zip","wb") as file:
                file.write(response.content)
            print("download completed")
            with ZipFile("lookup_temp.zip", 'r') as zObject:
                zObject.extractall(path="")
            os.remove("lookup_temp.zip")
            print("update complete")
            updated=True
    else:
        print("up to date")
    return updated
if __name__ =="__main__":
    update("https://update.structuralab.com/structuraUpdate",
           "Structura1-6",
           "none")
    
