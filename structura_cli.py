import argparse
import structura

parser = argparse.ArgumentParser(description='structura - hologram generator')
parser.add_argument('-p', '--pack', action='store', default='', help="pack name")
parser.add_argument('-n', '--name', action='store', default='', help="entity name")
parser.add_argument('-f', '--file', action='store', default='', help="structure file")
parser.add_argument('-l', '--list', action='store', default='false', help="make material list")

args = parser.parse_args()

if args.list == "false":
    mlist = False
elif args.list == "true":
    mlist = True

modFile=["{}".format(args.file)]
modName=["{}".format(args.name)]
models={}
offsets={}
ind=0
for i in range(len(modName)):
    models[modName[i]]={}
    print(modName[i])
    
    models[modName[i]]["structure"]="test_structures\{}.mcstructure".format(modFile[i])
    models[modName[i]]["offsets"]=[8,0,7]
    models[modName[i]]["opacity"] = 0.8
ind+=1
structura.generate_pack("{}".format(args.pack),models_object=models,makeMaterialsList=mlist)