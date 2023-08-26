import requests
from zipfile import ZipFile


def update(url,structura_version, lookup_verison):
    initial_check = requests.get(url,headers={"structuraVersion": structura_version,"lookupVersion":lookup_verison}).json()
    if initial_check["info"] == 'Update Availible':
        print('Update Availible')
        response = requests.get(initial_check["url"], allow_redirects=True,stream=True)
        if response.headers.get('content-type') == "application/xml":
            print(response.content)
        else:
            with open("lookup_temp.zip","wb") as file:
                file.write(response.content)
            print("download completed")
            with ZipFile("lookup_temp.zip", 'r') as zObject:
                zObject.extractall(path="")
    else:
        print("up to date")
if __name__ =="__main__":
    update("https://smgafwso25.execute-api.us-east-2.amazonaws.com/default/structuraUpdate",
           "Structura1-6",
           "None")
    
