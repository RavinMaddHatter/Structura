from PIL import Image
import json 
import boto3
import os
import boto3
import decimal 
from botocore.exceptions import ClientError
import shutil
import sys
from structura_core import structura
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import requests
import jwt
import time
import shutil
app_id=os.environ.get('app_id')
discord_url = "https://discord.com/api/v10/applications/{}/commands".format(app_id)
discord_secret=os.environ.get('secret')
bucket=os.environ.get('bucket')
channel=os.environ.get('channel')
cpm=float(os.environ.get('cpm'))
corsHeaders={'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
                }
channelpref=os.environ.get('channelpref')

PUBLIC_KEY = os.environ.get('discord_key')
def update_stats(success=True,tick = 0):
    data={}
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  
    table = dynamodb.Table('Structura')
    if success:
        stat="packsCreated"
    else:
        stat="failures"
    used=time.time()-tick
    response = table.update_item(                                                             
        Key={'Statistic': "monthlyUse"},
        UpdateExpression= f"set {stat} = {stat} + :inc, runTime = runTime + :used",
        ExpressionAttributeValues={':inc': decimal.Decimal(1),
                                    ':used': decimal.Decimal(used)},
        ReturnValues="ALL_NEW")
    data["monthlyUse"]=response['Attributes']
    response = table.update_item(                                                             
        Key={'Statistic': "historicalTotal"},
        UpdateExpression= f"set {stat} = {stat} + :inc, runTime = runTime + :used",
        ExpressionAttributeValues={':inc': decimal.Decimal(1),
                                    ':used': decimal.Decimal(used)},
        ReturnValues="ALL_NEW")
    data["historicalTotal"]=response['Attributes']
    return data

    
def lambda_handler(event, context):
    try:
        return tempLambda(event, context)
    except:
        return errorResponse(200,"test top level")
def tempLambda(event, context):
    global tick
    tick=time.time()
    print("starting lambda handler")
    if "token" in event['headers'].keys():
        try:
            token = event['headers']["token"]
            decoded = verifyCognitoToken(token)
            if decoded["auth"]:
                try:
                    response = makeStructuraLabPack(event['headers'],decoded["json"])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    
                    print(exc_type, fname, exc_tb.tb_lineno)
                    data={'content': "failed due to error processing file. Error {}, in file {}, line number {} ".format(str(e), fname, exc_tb.tb_lineno)}
                    response = errorResponse(200,data)
            else:
                response = errorResponse(401,"Failed Authentication!")
    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            
            print(exc_type, fname, exc_tb.tb_lineno)
            data={'content': "failed due to error processing file. Error {}, in file {}, line number {} ".format(str(e), fname, exc_tb.tb_lineno)}
            response = errorResponse(200,data)
        return response
    else:
        try:
            body = json.loads(event['body'])
    
    
            
            signature = event['headers']['x-signature-ed25519']
            timestamp = event['headers']['x-signature-timestamp']
    
            # validate the interaction
    
            verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
            body2 = event['body']
        
            try:
                verify_key.verify(f'{timestamp}{body2}'.encode(), bytes.fromhex(signature))
            except BadSignatureError as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                raise Exception("Authentication error")
                
        
            # handle the interaction
            if body['channel']['id'] in channel :
                
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
            else:
                initial_callback(body, ephemeral=True)
                data={'content':f"Converstion in this channel are disallowed. Please use <#{channelpref}> to convert files","flags":64}
                send_repsonse(body,data)
        except Exception as e:
            print ("ERROR HANDLING")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            
            print(exc_type, fname, exc_tb.tb_lineno)
            if "name" in event.keys():
                return add_command(event)
            else:
                print(exc_type, fname, exc_tb.tb_lineno)
                print(body)
                print(event["body"])
                print(body.keys())
                update_stats(False, tick)
                try:
                    body = json.loads(event['body'])
                    #body = json.loads(event['body'], object_hook=ascii_encode_dict)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(body)
                    print(body.keys())
                    data={'content': "failed due to error processing file. Error {}, in file {}, line number {} ".format(str(e), fname, exc_tb.tb_lineno)}
                    send_repsonse(body,data)
                    raise
                except:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    raise
                
def makeStructuraLabPack(headder,userInfo):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('StructuraWebsite')
    guid = headder["guid"]
    response = table.get_item(Key={'GUID': guid})
    itemData = response["Item"]
    if userInfo["username"] == itemData["Creator"]:
        s3_client = boto3.client('s3')
        response = s3_client.list_objects_v2(Bucket="structuralab.com", Prefix=f"{guid}/")
        filesToConvert = {}
        try:
            shutil.rmtree(f"/tmp/{guid}")
        except:
            pass
        workingDir=f"/tmp/{guid}"
        os.mkdir(workingDir)
        
        name=headder["name"]
        structuraFolder=f"{workingDir}/{name}"
        structura_base=structura(structuraFolder)
        structura_base.set_opacity(20)
        if "Contents" in response.keys():
            for object in response['Contents']:
                if object["Key"].endswith(".mcstructure"):
                    fileName = object["Key"].split("/")[-1]
                    filesToConvert[fileName]=f"{workingDir}/{fileName}"
                    s3_client.download_file("structuralab.com", object["Key"], filesToConvert[fileName])
        if len(list(filesToConvert.keys()))==0:
            return errorResponse(200,f"No Files Found in {guid}")
        
        elif len(list(filesToConvert.keys()))==1:
            structura_base.add_model("",filesToConvert[list(filesToConvert.keys())[0]])
            structura_base.set_model_offset("",[0,0,0])
        else:
            for fileName in list(filesToConvert.keys()):
                nameTag=fileName.split(".mcstructure")[0]
                structura_base.add_model(nameTag,filesToConvert[fileName])
                structura_base.set_model_offset(nameTag,[0,0,0])
                
        structura_base.generate_nametag_file()
        structura_base.generate_with_nametags()
        created_file = structura_base.compile_pack()
        material_lists =  structura_base.make_nametag_block_lists()
        itemsList={}
        for _junk, structureReads in structura_base.structure_files.items():
            structureList=structureReads["block_list"]
            for item, count in structureList.items():
                if item in itemsList.keys():
                    itemsList[item]+=count
                else:
                    itemsList[item]=count
        s3_client.upload_file(created_file, "structuralab.com", f"{guid}/{name}.mcpack")
        response = table.get_item(Key={'GUID': guid})
        itemData = response["Item"]
        itemData["MaterialsList"] = itemsList
        itemData["StructuraFile"] = f"https://s3.us-east-2.amazonaws.com/structuralab.com/{guid}/{name}.mcpack"
        table.put_item(Item=itemData)
        return errorResponse(200,"Structrua pack made successfully!")
    else:
        return errorResponse(401,"Authentication Failed!")
def verifyCognitoToken(token):
    kidUrl="https://cognito-idp.us-east-2.amazonaws.com/us-east-2_F8JCwtZAa/.well-known/jwks.json" 
    response = requests.get(kidUrl)
    
    keys = json.loads(response.content)["keys"]
    
    jwtheaders=jwt.get_unverified_header(token)
    alg=jwtheaders["alg"]
    unverified=jwt.decode(token,options={"verify_signature":False})
    for key in keys:
        if key['kid'] == jwtheaders["kid"]:
            jwkValue=key
    print(json.dumps(jwkValue))
    publicKey = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwkValue))
    try:
        decoded=jwt.decode(token,publicKey,algorithms=[alg])
        retVal={"json":decoded,"auth":True}
    except:
        retVal={"json":{},"auth":False}
    return retVal
def errorResponse(errorCode,event):

    resp = {
        'statusCode': errorCode,
        'headers':corsHeaders,
        'body': json.dumps(event)}
    return resp
def command_handler(body):
    command = body['data']['name']
    if command == 'help':
        initial_callback(body, ephemeral=False)
        return help_command(body)
    elif command == 'convert':
        initial_callback(body, ephemeral=True)
        return convert_command(body,tick)
    elif command == 'convertpublic':
        initial_callback(body, ephemeral=False)
        return convert_command(body,tick)
    elif command == 'stats':
        initial_callback(body, ephemeral=False)
        return stats_command(body)
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
def initial_callback(body,ephemeral=False):
    data={
        'type': 5,
        'data':{
            "flags":0
            }
        }
    if ephemeral:
        data["data"]["flags"]=64
    interaction_id=body['id']
    interaction_token=body['token']
    url = "https://discord.com/api/v10/interactions/{}/{}/callback".format(interaction_id,interaction_token)
    r = requests.post(url, json=data)
    
def send_repsonse(body,data):
    interaction_id=body['id']
    interaction_token=body['token']
    url = "https://discord.com/api/v10/webhooks/{}/{}/messages/@original".format(app_id,interaction_token)
    r = requests.patch(url, json=data)
def send_url_buttons(body,labels,urls,text="pack creation complete"):
    interaction_id=body['id']
    interaction_token=body['token']
    data={
            "content":text,
            "components": [
                {
                "type": 1,
                "components": [
                    ]
                }
            ]
        }
    for i in range(len(labels)):
        button={
                    "type": 2,
                    "label": labels[i],
                    "style": 5,
                    "url": urls[i]
                    }
        data["components"][0]["components"].append(button)   
    url = "https://discord.com/api/v10/webhooks/{}/{}/messages/@original".format(app_id,interaction_token)
    r = requests.patch(url, json=data)
def help_command(body):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  
    table = dynamodb.Table('Structura')
    response = table.get_item(Key={'Statistic': "historicalTotal"})
    pack_creation_time=float(response["Item"]['runTime'])/float(response["Item"]['packsCreated'])
    packsCreated=float(response["Item"]['packsCreated'])
    packs_per_view = pack_per_youtube_View(pack_creation_time)
    help_text=f"This bot is a privlage not a right, To keep it funded do check out a few videos. Each video you watch pays for {packs_per_view:0.1f} conversions \n"
    help_text+="Note: on may 20 2023 i changed the name of the file upload in the command. This may be cached on your device if you are an long time user fully close the app or restart your device to see if that fixes it.\n\r"
    help_text+="/convert [file1] [file2-file6 optional]: this command creates a structura pack from a valid structure file. If the file is not valid it will not work. If you select more than 1 file the name tag will be the file name. this one is private so we dont see what is going on\n\r"
    help_text+="/convertpublic [file1] [file2-file6 optional] : this command creates a structura pack from a valid structure file. If the file is not valid it will not work.If you select more than 1 file the name tag will be the file name. This one is public so we can see what is going on\n\n"
    help_text+="if you are having trouble check <#1129115788972929095> for more information on how to use the bot.\n\n"
    help_text+="If the Discord bot is giving you probelms consider using https://structuralab.com/ it has the same features as the bot... but a different User interface with wider compatiblity"   
    data={
#            'type': 4,
#            'data':{
                'content':help_text 
#                }
            }
    send_repsonse(body,data)
    return {
            'statusCode': 200,
            'body': "success"
                
            }
def stats_command(body):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  
    table = dynamodb.Table('Structura')
    response = table.get_item(Key={'Statistic': "historicalTotal"})
    pack_creation_time_total=float(response["Item"]['runTime'])
    packsCreated_total=float(response["Item"]['packsCreated'])
    failures_total=float(response["Item"]['failures'])
    response = table.get_item(Key={'Statistic': "monthlyUse"})
    execution_time_month = float(response["Item"]['runTime'])
    failures_month = float(response["Item"]['failures'])
    pack_creation_time_month=float(response["Item"]['runTime'])
    packsCreated_month=float(response["Item"]['packsCreated'])
    
    response = table.get_item(Key={'Statistic': "brokenBlocks"})
    in_github = 54
    
    most_failed_block="error"
    seen = len(response["Item"].keys())
    
    try:
        response["Item"].pop("Statistic")
        block_dict=response["Item"]
        block_dict=dict(zip(response["Item"], map(int, response["Item"].values())))
        most_failed_block=max(block_dict, key=block_dict.get)
        block_failures=block_dict[most_failed_block]
    except:
        most_failed_block="None"
        block_failures=0
        pass
        
    
    
    help_text="Here are some statistics for the bot. We had a ton:\n"
    help_text+=f"Packs Created                 \t: {packsCreated_total:0.0f} total,\t{packsCreated_month:0.0f} this month\n"
    help_text+=f"The bot has failed to create  \t: {failures_total:0.0f} total,\t{failures_month:0.0f} this month\n"
    help_text+=f"The bot has run for a total of\t: {pack_creation_time_total:0.2f}s total,\t{pack_creation_time_month:0.2f}s this month\n"
    help_text+=f"Broken Blocks                 \t: {in_github} reported,\t {seen} seen\n"
    help_text+=f"Most Used Failed Block          \t: {most_failed_block},\t {block_failures} times\n"
    data={
#            'type': 4,
#            'data':{
                'content':help_text 
#                }
            }
    send_repsonse(body,data)
    return {
            'statusCode': 200,
            'body': "success"
                
            }

def convert_command(body,tick):
    auth_time="{:.2f}".format(time.time()-tick)
    try:

        
        data={
                'content': "working on conversion",
                "flags":0
            }
        valid_files=[]
        for key in body["data"]["resolved"]["attachments"]:
            attach=body["data"]["resolved"]["attachments"][key]
            if attach["filename"].endswith(".mcstructure"):
                if attach["size"]>0:
                    valid_files.append([attach["url"],attach["filename"]])
        if len(valid_files)>1:
            file_url=valid_files[0][0]
            file_name=valid_files[0][1]
            make_pack_nametag(valid_files,body,tick)
        elif len(valid_files)==1:
            file_url=valid_files[0][0]
            file_name=valid_files[0][1]
            make_pack_single(file_url,file_name,body,tick)
        else: 
            raise Exception("No Valid Files were attached, Either File size is 0kb or no .mcstructure files were loaded")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        update_stats(False,tick)
        data={'content': "failed due to error processing file. Error {}, in file {}, line number {} ".format(str(e), fname, exc_tb.tb_lineno)}
        send_repsonse(body,data)
        raise
    return {
            'statusCode': 200,
            'body': "file created"
            }
def make_pack_nametag(valid_files,body,tick):
    data={
            'content': "working on conversion",
            "flags":0
        }
    os.makedirs("/tmp/input", exist_ok=True)
    names=[]
    file_dict={}
    for info in valid_files:
        file_url = info[0]
        file_name = info[1]
        response = requests.get(file_url)
        nm=file_name.split(".mcstructure")[0]
        names.append(nm)
        file_dir = f"/tmp/input/{file_name}"
        file_dict[nm]=file_dir
        open(file_dir, "wb").write(response.content)
    data["content"]="Processing, if this hangs it is because the file is too big. retrying will not fix it"
    send_repsonse(body,data)
    
    structura_base=structura("/tmp/"+names[0])
    structura_base.set_opacity(20)
    for name in names:
        structura_base.add_model(name,file_dict[name])
        structura_base.set_model_offset(name,[0,0,0])
    structura_base.generate_nametag_file()
    structura_base.generate_with_nametags()
    skipped = structura_base.get_skipped()
    update_skiped(skipped)
    created_file = structura_base.compile_pack()
    material_lists =  structura_base.make_nametag_block_lists() 
    s3_client = boto3.client('s3')
    folder="{:.2f}".format(time.time())
    s3_key=f"{folder}/{name}.mcpack"
    data["content"]=f"sending file to server {name}.mcpack {created_file}"
    send_repsonse(body,data)
    response = s3_client.upload_file(created_file, bucket, s3_key)
    labels=["Structura Pack"]
    urls=[f"https://{bucket}.s3.amazonaws.com/{s3_key}"]
    i=0
    for mat_list in material_lists:
        list_name=names[i][:15]+".txt"
        i+=1
        labels.append(f"Block_list {i}")
        s3_key=f"{folder}/{list_name}"
        response = s3_client.upload_file(mat_list, bucket, s3_key)
        urls.append(f"https://{bucket}.s3.amazonaws.com/{s3_key}")
    skipped_text=""
    if len(list(skipped.keys()))>1:
        skipped_text=", unsupported blocks were skipped. Consider sharing the structure file in <#801477108127891466>"
        labels.append("skipped")
        list_name=f"skipped_list{i}.txt"
        s3_key=f"{folder}/{list_name}"
        response = s3_client.upload_file(f"/tmp/{names[0]} skipped.txt", bucket, s3_key)
        urls.append(f"https://{bucket}.s3.amazonaws.com/{s3_key}")
        
    stats=update_stats(True,tick)
    pack_creation_time=float(stats['historicalTotal']['runTime'])/float(stats['historicalTotal']['packsCreated'])
    packsCreated=float(stats['historicalTotal']['packsCreated'])
    packs_per_view = pack_per_youtube_View(pack_creation_time) 
    text=f"Your File has been created. Bot Stats: Average Pack Creation Time = {pack_creation_time:0.2f}, total packs created= {packsCreated:0.0f}, Packs per Youtube View = {packs_per_view:0.2f}{skipped_text}"
    #text=str(file_dict[name]) 
    send_url_buttons(body,labels,urls,text=text)
def pack_per_youtube_View(creation_time):
    cost_compute=0.0000166667#per gb second
    ram_allocated_GB=0.5
    price_per_write_unit=1.25/1000000
    #cpm=5.97
    packs_per_view = cpm/((creation_time*ram_allocated_GB*cost_compute+4*price_per_write_unit)*1000)
    
    return packs_per_view
def update_skiped(skipped):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  
    table = dynamodb.Table('Structura')
    expression="ADD "
    vals={}
    for block,variants in skipped.items():
        for variant, count in variants.items():
            block=block.replace("minecraft:","").replace("-","").replace("+","")
            variant=variant.replace(":","").replace("-","").replace("+","")
            key=f"{block}_{variant}"
            expression+=f"{key} :{key}, "
            vals[f":{key}"]=1
    if expression != "ADD ":
        expression=expression[:-2]
        response = table.update_item(                                                             
            Key={'Statistic': "brokenBlocks"},
            UpdateExpression= expression,
            ExpressionAttributeValues=vals,
            ReturnValues="ALL_NEW")        
    
def make_pack_single(file_url,file_name,body,tick):
    data={
            'content': "working on conversion",
            "flags":0
        }
    response = requests.get(file_url)
    name = file_name.split(".mcstructure")[0]
    os.makedirs("/tmp/input", exist_ok=True)
    file_dir = f"/tmp/input/{file_name}"
    open(file_dir, "wb").write(response.content)

    data["content"]="Processing, if this hangs it is because the file is too big. retrying will not fix it"
    send_repsonse(body,data)
    
    structura_base=structura("/tmp/"+name)
    structura_base.set_opacity(20)
    structura_base.add_model("",file_dir)
    structura_base.set_model_offset("",[0,0,0])
    structura_base.generate_nametag_file()
    structura_base.generate_with_nametags()
    skipped = structura_base.get_skipped()
    update_skiped(skipped)
    
    created_file = structura_base.compile_pack()
    material_lists =  structura_base.make_nametag_block_lists() 
    s3_client = boto3.client('s3')
    folder="{:.2f}".format(time.time())
    s3_key=f"{folder}/{name}.mcpack"
    data["content"]=f"sending file to server {name}.mcpack {created_file}"
    send_repsonse(body,data)
    response = s3_client.upload_file(created_file, bucket, s3_key)
    labels=["Structura Pack"]
    urls=[f"https://{bucket}.s3.amazonaws.com/{s3_key}"]
    i=0
    for mat_list in material_lists:
        i+=1
        list_name=f"Block_list{i}.txt"
        
        labels.append(f"Block_list {i}")
        s3_key=f"{folder}/{list_name}"
        response = s3_client.upload_file(mat_list, bucket, s3_key)
        urls.append(f"https://{bucket}.s3.amazonaws.com/{s3_key}")
    skipped_text=""
    if len(list(skipped.keys()))>1:
        skipped_text=", unsupported blocks were skipped. Consider sharing the structure file in <#801477108127891466>"
        labels.append("skipped")
        list_name=f"skipped_list{i}.txt"
        s3_key=f"{folder}/{list_name}"
        response = s3_client.upload_file(f"/tmp/{name} skipped.txt", bucket, s3_key)
        urls.append(f"https://{bucket}.s3.amazonaws.com/{s3_key}")
    stats=update_stats(True,tick)
    pack_creation_time=float(stats['historicalTotal']['runTime'])/float(stats['historicalTotal']['packsCreated'])
    packsCreated=float(stats['historicalTotal']['packsCreated'])
    packs_per_view = pack_per_youtube_View(pack_creation_time)
    text=f"Your File has been created. Bot Stats: Average Pack Creation Time = {pack_creation_time:0.2f}, total packs created= {packsCreated:0.0f}, Packs per Youtube View = {packs_per_view:0.2f}{skipped_text}"
    send_url_buttons(body,labels,urls,text=text)

  
