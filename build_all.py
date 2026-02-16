from shutil import copyfile
import shutil
import json
from zipfile import ZIP_DEFLATED, ZipFile
import os
from datetime import datetime
import shutil
try:
    shutil.rmtree("temp/")
except:
    pass
import PyInstaller.__main__
import os

# Define the path to your main script
script_path = 'structura.py' 

# Define the output directory (optional)
output_dir = 'dist' 

# Define the name for your executable (optional)
app_name = 'Structura'

# Construct the list of PyInstaller arguments
# This example creates a one-file, windowed executable with a custom name
pyinstaller_args = [
    script_path,
    '--onefile',
    '--windowed',
    f'--name={app_name}',
    f'--distpath={output_dir}' # Specify the output directory
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print(f"PyInstaller finished. Check the '{output_dir}' directory for your executable.")



currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
update_package_name=f'update_package_{currentDay}-{currentMonth}-{currentYear}'
with open("lookups/lookup_version.json","r") as file:
    old_update=json.load(file)
old_update["version"]=update_package_name
old_update["notes"]="NOTE: a new version of structura will need to be manually downloaded. This is to address lag issues. No further updates for 1.6 will be issued. https://github.com/RavinMaddHatter/Structura/releases"
with open("lookups/lookup_version.json","w+") as file:
    json.dump(old_update,file,indent=2)
try:
    os.mkdir("temp")
except:
    print("folder exists")
shutil.copytree("lookups", f"temp/lookups")
shutil.copytree("Vanilla_Resource_Pack", "temp/Vanilla_Resource_Pack")
shutil.make_archive("temp", 'zip', "temp")
if os.path.exists(update_package_name+".zip"):
    os.remove(update_package_name+".zip")
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
copyfile("log_config.py", "temp/log_config.py")
shutil.make_archive("temp", 'zip', "temp")
shutil.rmtree("temp")
print(update_package_name)
if os.path.exists(update_package_name+".zip"):
    try:
        os.remove(f'lambda_package_{currentDay}-{currentMonth}-{currentYear}.zip')
    except:
        print(f'lambda_package_{currentDay}-{currentMonth}-{currentYear}.zip doesnt exist')
os.rename(f'temp.zip',f'lambda_package_{currentDay}-{currentMonth}-{currentYear}.zip')
shutil.move(update_package_name+".zip",os.path.join("dist",update_package_name+".zip"))
shutil.move(f'lambda_package_{currentDay}-{currentMonth}-{currentYear}.zip',os.path.join("dist",f'lambda_package_{currentDay}-{currentMonth}-{currentYear}.zip'))
