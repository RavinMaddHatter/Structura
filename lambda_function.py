from PIL import Image
import json
import boto3
import uuid
import os
import boto3
from botocore.exceptions import ClientError
import shutil
from structura_core import structura
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import requests
import uuid
app_id=os.environ.get('app_id')
discord_url = "https://discord.com/api/v10/applications/{}/commands".format(app_id)
discord_secret=os.environ.get('secret')
bucket=os.environ.get('bucket')

PUBLIC_KEY = os.environ.get('discord_key')
def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        signature = event['headers']['x-signature-ed25519']
        timestamp = event['headers']['x-signature-timestamp']

        # validate the interaction

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        message = timestamp + json.dumps(body, separators=(',', ':'))
    
        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return {
                'statusCode': 401,
                'body': json.dumps('invalid request signature')
                }
    
        # handle the interaction

        t = body['type']

        if t == 1:
            return {
                'statusCode': 200,
                'body': json.dumps({
                'type': 1
                })
            }
        elif t == 2:
            return command_handler(body)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('unhandled request type')
                }
    except:
        if "name" in event.keys():
            return add_command(event)
        else:
            raise

def command_handler(body):
    initial_callback(body)
    command = body['data']['name']
    
    if command == 'help':
        return help_command(body)
            
    elif command == 'convert':
        return convert_command(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('unhandled command')
            
        }
def add_command(body):
    headers = {
        "Authorization": "Bot {}".format(discord_secret)
    }
    r = requests.post(discord_url, headers=headers, json=body)
    return {
            'statusCode': 200,
            'body': r.text
            
        }
def initial_callback(body):
    data={
        'type': 5
        }
    interaction_id=body['id']
    interaction_token=body['token']
    url = "https://discord.com/api/v10/interactions/{}/{}/callback".format(interaction_id,interaction_token)
    r = requests.post(url, json=data)
    
def send_repsonse(body,data):
    interaction_id=body['id']
    interaction_token=body['token']
    url = "https://discord.com/api/v10/webhooks/{}/{}/messages/@original".format(app_id,interaction_token)
    r = requests.patch(url, json=data)

def help_command(body):
    data={
#            'type': 4,
#            'data':{
                'content': """This bot is a privlage not a right, it is provided by MadHatter and is paid for by him. Please use this as if it is costing your a small amount of money, as hosting it does cost money. If it becomes too expensive I will be shut down.
    /convert [upload file] : this command creates a structura pack from a valid structure file. If the file is not valid it will not work.
    """
#                }
            }
    send_repsonse(body,data)
    return {
            'statusCode': 200,
            'body': "success"
                
            }
def convert_command(body):
    try:

        
        data={
                'content': "working on conversion"
            }
        error=""

        for key in body["data"]["resolved"]["attachments"]:
            attach=body["data"]["resolved"]["attachments"][key]
            if attach["filename"].endswith(".mcstructure"):
                if attach["size"]>0:
                    file_url=attach["url"]
                    file_name=attach["filename"]
                    data["content"]=file_url
                    error=""
                    break
                else:
                    error="is empty"
                    data["content"]=error
            else:
                error="not a structure file"
                data["content"]=error
        
        if error=="":
            #shutil.rmtree("/tmp/input")
            response = requests.get(file_url)
            name=file_name.split(".mcstructure")[0]

            os.makedirs("/tmp/input", exist_ok=True)

            file_dir = f"/tmp/input/{file_name}"
            open(file_dir, "wb").write(response.content)
            data["content"]="Processing, if this hangs it is because the file is too big. retrying will not fix it"
            
            send_repsonse(body,data)
            created_file = make_pack("/tmp/"+name,file_dir)
            data["content"]=f"sending file to server {name}.mcpack"
            send_repsonse(body,data)
            s3_client = boto3.client('s3')
            folder=uuid.uuid4()
            s3_key=f"{folder}/{name}.mcpack"
            response = s3_client.upload_file(created_file, bucket, s3_key)
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': s3_key},
                ExpiresIn=3600)
            data["content"]=f"Your file has been created, it will be saved for 1 hour then deleted, here is the url {signed_url}"
            send_repsonse(body,data)
    except Exception as e:
        data={'content': "failed due to error processing file. "+str(e)}
        send_repsonse(body,data)
        raise
    return {
            'statusCode': 200,
            'body': "file created"
            }
def make_pack(name,file_dir):
    try:
        
        structura_base=structura(name)
        structura_base.set_opacity(20)
        structura_base.add_model("",file_dir)
        structura_base.set_model_offset("",[0,0,0])
        structura_base.generate_nametag_file()
        structura_base.generate_with_nametags()
        return structura_base.compile_pack()
    except Exception as e:
            data={'content': "failed due to error processing file. "+str(e)}
    return data
  
