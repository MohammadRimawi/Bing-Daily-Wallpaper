import requests
import json
import shutil
import os
import datetime
import time


datetime.datetime.now()
path = os.getcwd()


log = open("./Bing Daily Wallpaper/code/log", "a")
log.write(str(datetime.datetime.now()) + " ")

state = { "loadConfig":0 ,"connected":0, "downloaded":0, "saved":0, "set":0 }

########### Start Load config.json ##########

message = " 1) Loading config.json"
print( message )

jsonPath = "./Bing Daily Wallpaper/code/config.json"

try:
    config = json.load(open(jsonPath))
except:
    error ="\n\t↳ ERROR: config.json was not loaded at [ " +  jsonPath + " ]\n \t\t↳ "+ str( state )
    log.write( error +"\n")
    print( error )
    exit()

state["loadConfig"]=1
message = "\t↳ Config.json successfuly loaded"
print( message )

############ End Load config.json ############

######### Start Request Bing Daily Image API #########

message = " 2) Requesting API"
print( message )

bingAPI = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=' + str(config["offset"])+'&n=1&mkt=en-' + config["country"]

try:
    response = requests.get(bingAPI)
    responseJSON = json.loads(response.text)
    # print(bingAPI)
except:
    error ="\n\t↳ ERROR: Faild to connect to Bing Servers\n\t↳ Using [ " + bingAPI + " ]\n \t\t↳ " + str( state )  
    log.write( error +"\n")
    print( error )
    exit()

state["connected"]=1
message = "\t↳ Connected successfuly to Bing Servers"
print( message )


########## End Request Bing Daily Image API ##########

############### Start Downloading Image ###############

message = " 3) Downloading Image"
print( message )

imageURL = "https://www.bing.com" + responseJSON["images"][0]["url"]

try:
    imageResponse = requests.get(imageURL,stream = True)
except:
    error ="\n\t↳ ERROR: Faild to download the image\n\t↳ Using [ " + imageURL + " ]\n \t\t↳ " + str( state )  
    log.write( error +"\n")
    print( error )
    exit()
# print(imageURL)
state["downloaded"]=1
message = "\t↳ The Image was Downloaded successfuly"
print( message )

################ End Downloading Image ################


############### Start Saving Image ###############

message = " 4) Saving Image"
print( message )
# print(responseJSON["images"][0]["copyright"])


if config["history"] == True or config["defaultName"]=="": 
    imageName = str(responseJSON["images"][0]["copyright"])
else:
    imageName = config["defaultName"]

if not os.path.isdir(path+"/"+config["filename"]): 
    os.mkdir(path+"/"+config["filename"])

temp = ""
for i in range(len(imageName.split('/'))-1):
    temp += imageName.split('/')[i]+"\\"+imageName.split('/')[i+1]


imageName = temp

filename =  config["filename"] + imageName#.split('(')[0].strip()

        
try:
    imageResponse.raw.decode_content = True
    
    with open(filename,"wb") as img:
        shutil.copyfileobj(imageResponse.raw, img)
        
except:
    error ="\n\t↳ ERROR: Faild to save the image\n\t↳ At [ " + filename + " ]\n \t\t↳ " + str( state )  
    log.write( error +"\n")
    print( error )
    exit()

state["saved"]=1
message = "\t↳ The Image was Saved successfuly"
print( message )

################ End Saving Image ################

############### Start Setting Image ###############

message = " 5) Setting Image"
print( message )


command = '/usr/bin/gsettings set org.gnome.desktop.background picture-uri "'+ str(path) +'/'+ filename +'"'


if not os.system( command )==0:
    error ="\n\t↳ ERROR: Faild to set the image\n\t↳ Using [ " + command + " ]\n \t\t↳ " + str( state )  
    log.write( error +"\n")
    print( error )
    exit()

state["set"]=1
message = "\t↳ The Image was Set successfuly"
print( message )

################ End Setting Image ################


log.write( str( state ) + '\n')
print(state)
log.close()

