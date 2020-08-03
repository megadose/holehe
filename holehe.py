from holehe import *
from tqdm import tqdm
import argparse
from termcolor import colored
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--email", help="Email of the target")
args = parser.parse_args()
websites=[adobe,ebay,facebook,instagram,tumblr,pastebin,github,twitter,pinterest,lastfm,spotify,firefox,office365,live]

infos =[]
description = colored("Email used","green")+","+colored(" Email not used","magenta")+","+colored(" Rate limit","red")+"\n"
for website in tqdm(websites):
    infos.append({str(website).split(" ")[1].split(" ")[0]:website(args.email)})
print("\033[H\033[J")
print("*"*25)
print(args.email)
print("*"*25+"\n")
for i in infos:
    key, value = next(iter(i.items()))
    i = value
    #print(i)
    if i["rateLimit"]==True:
        websiteprint=colored(key,"red")
    elif i["exists"]==False :
        websiteprint=colored(key,"magenta")
    else:
        toprint=""
        if i["emailrecovery"]!= None:
            toprint+=" "+i["emailrecovery"]
        if i["phoneNumber"]!= None:
            toprint+=" / "+i["phoneNumber"]
        if i["others"]!= None:
            toprint+=" / FullName "+i["others"]["FullName"]
            toprint+=" / profilePicture "+i["others"]["profilePicture"]

        websiteprint=colored(str(key)+toprint,"green")
    print(websiteprint)

print("\n"+description)
