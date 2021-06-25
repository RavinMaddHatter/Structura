import structura
import os
modFile=["01-6xSingleItemSortes",
         "02-2xNonStackableItemFilter",
         "03-Autopusher1",
         "04-AutoPusher2",
         "05-2x1x4-AutoDroper",
         "06-4x1x3-AutoDropper",
         "07-3x3x1-AutoDropper",
         "08-4x4x1-AutoDroper",
         "09-2-5TickClock",
         "10-3-9TickClock",
         "11-ObserverClock",
         "12-HoperClock",
         "13-RisingEdgePulse",
         "14-2x4x1FallingEdgeMono",
         "15-2x3x2FallingEdgeMono",
         "16-3x4x1FallingEdgeMon",
         "17-AndGate",
         "18-OrGate",
         "19-NandGate",
         "20-NorGate",
         "21-XorGate",
         "22-2x1x5PulseExtender",
         "23-5x3x1-PulseExtender",
         "24-3x1x4-Tflipflop",
         "25-3x2x3-TFlipFlop",
         "26-2x3BarrelDoor",
         "27-2x3TrapDoorDoor",
         "28-2x4TrapDoorDoor",
         "29-multi sorter",
         "SnowFarm"]
modName=["SingleItemSorter",
         "Non-Stackable",
         "AutoPusher1",
         "AutoPusher2",
         "AutoDropper1",
         "AutoDropper2",
         "AutoDropper3",
         "AutoDropper4",
         "Clock1",
         "Clock2",
         "Clock3",
         "Clock4",
         "Pulse1",
         "Pulse2",
         "Pulse3",
         "Pulse4",
         "And",
         "Or",
         "Nand",
         "Nor",
         "Xor",
         "PulseExtender1",
         "PulseExtender2",
         "FlipFlop1",
         "FlipFlop2",
         "BarrelDoor",
         "2x3TrapDoor",
         "2x4TrapDoor",
         "MultiSorter",
         "ReLiC"]
models={}
offsets={}
ind=0
for i in range(len(modName)):
    print(i)
    print(i>=9)
    if len(models.keys())<=4:
        
        models[modName[i]]="test structures\{}.mcstructure".format(modFile[i])
        offsets[modName[i]]=[8,0,7]
    else:
        ind+=1
        #if os.path.isfile("{}-{}.mcpack".format("HattersToyBox",i)):
        #    os.remove("{}-{}".format("HattersToyBox",i))
        structura.generate_pack("{}-{}".format("HattersToyBox",ind),50,models,offsets,makeMaterialsList=True)
        models={}
        offsets={}
ind+=1
structura.generate_pack("{}-{}".format("HattersToyBox",ind),50,models,offsets,makeMaterialsList=True)
