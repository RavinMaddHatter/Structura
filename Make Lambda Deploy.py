from shutil import copyfile
import shutil
import json
from zipfile import ZIP_DEFLATED, ZipFile
import os
from datetime import datetime

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
update_package_name=f'update_package_{currentDay}-{currentMonth}-{currentYear}'
with open("lookups/lookup_version.json","r") as file:
    old_update=json.load(file)
old_update["version"]=update_package_name
with open("lookups/lookup_version.json","w+") as file:
    json.dump(old_update,file,indent=2)
try:
    os.mkdir("temp")
except:
    print("folder exists")
shutil.copytree("lookups", f"temp/lookups")
shutil.copytree("Vanilla_Resource_Pack", "temp/Vanilla_Resource_Pack")
shutil.make_archive("temp", 'zip', "temp")
os.rename(f'temp.zip',update_package_name+".zip")

copyfile("animation_class.py", "temp/animation_class.py")
copyfile("armor_stand_class.py", "temp/armor_stand_class.py")
copyfile("armor_stand_geo_class.py", "temp/armor_stand_geo_class.py")
copyfile("big_render_controller.py", "temp/big_render_controller.py")
copyfile("lambda_function.py", "temp/lambda_function.py")
copyfile("manifest.py", "temp/manifest.py")
copyfile("render_controller_class.py", "temp/render_controller_class.py")
copyfile("structura.py", "temp/structura.py")
copyfile("structura_core.py", "temp/structura_core.py")
copyfile("structure_reader.py", "temp/structure_reader.py")
copyfile("updater.py", "temp/updater.py")
shutil.make_archive("temp", 'zip', "temp")
shutil.rmtree("temp")

os.rename(f'temp.zip',f'lambda_package_{currentDay}-{currentMonth}-{currentYear}.zip')
