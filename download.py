import os
import requests
import oead
import json

boss_1 = "https://raw.githubusercontent.com/Sheldon10095/Splatfestival_StaffFiles/main/FestFiles/00000543"
boss_2 = "https://raw.githubusercontent.com/Sheldon10095/Splatfestival_StaffFiles/main/FestFiles/00000544"
boss_3 = "https://raw.githubusercontent.com/Sheldon10095/Splatfestival_StaffFiles/main/FestFiles/00000545"

def download_file(url, file_name):
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)

def download():
    
    os.mkdir('./temp')
    os.mkdir('./data')

    # download files

    def download_file(url, file_name):
        r = requests.get(url, allow_redirects=True)
        open(file_name, 'wb').write(r.content)

    download_file(boss_1, "temp/00000543")
    download_file(boss_2, "temp/00000544")
    download_file(boss_3, "temp/00000545")

    # handle 00000543

    os.system("BFRESExtractor_NoPause temp/00000543")
    os.remove('./temp/00000543')

    # handle 00000544

    os.rename("temp/00000544", "data/00000544.byml")

    # convert yaml to xml



    # handle 00000545

    os.system("BFRESExtractor_NoPause temp/00000545")
    os.remove('./temp/00000545')

    # move bfres files

    os.rename('./1_FTEX/', './temp/1_FTEX/')

    # remove non-gtx files

    for file in os.listdir('./temp/1_FTEX/'):
        if ".gtx" not in file:
            os.remove(f"./temp/1_FTEX/{file}")

    # convert gtx and cleanup

    for file in os.listdir('./temp/1_FTEX/'):
        os.system(f"tools\gtx\gtx_extract ./temp/1_FTEX/{file}")
        os.remove(f"./temp/1_FTEX/{file}")

    for file in os.listdir('./temp/1_FTEX/'):
        os.rename(f"./temp/1_FTEX/{file}", f"./temp/{file}")

    os.rmdir('./temp/1_FTEX/')

    # convert dds files to png

    for file in os.listdir('./temp/'):
        os.system(f"ffmpeg -i ./temp/{file} ./data/{file[:-4]}.png")
        os.remove(f"./temp/{file}")

    # remove temp folder

    os.rmdir('./temp/')

def fesdata():

    with open('./data/00000544.byml', 'rb') as f:
        f = bytearray(f.read())
        f[3] = 2
        info = oead.byml.from_binary(f)

    festivalId = str(info['FestivalId'])

    starttime = str(info['Time']['Start'])
    endtime = str(info['Time']['End'])

    rule = str(info['Rule'])
    stage_1 = str(info['Stages'][0]['MapID'])
    stage_2 = str(info['Stages'][1]['MapID'])
    stage_3 = str(info['Stages'][2]['MapID'])

    team_1_sname = str(info['Teams'][0]['ShortName']['EUen'])
    team_2_sname = str(info['Teams'][1]['ShortName']['EUen'])

    with open('./data/FesData.json', 'w') as f:
        json.dump({"FestivalId": festivalId, "TimeStart": starttime, "TimeEnd": endtime, "Rule": rule, "Stages": [stage_1, stage_2, stage_3],"Teams": [{"Name": team_1_sname}, {"Name": team_2_sname}]}, f)
    
    os.remove('./data/00000544.byml')

def gamedata(type:str, id:str):
    
    if type == "rule":
        match id:
            case "cPnt":
                return "Turf War"
            case "cVar":
                return "Splat Zones"
            case "cVlf":
                return "Tower Control"
            case "cVgl":
                return "Rainmaker"
            case _:
                exit("Invalid Rule ID")

    elif type == "stage":
        match id:
            case "0":
                return "Urchin Underpass"
            case "1":
                return "Walleye Warehouse"
            case "2":
                return "Saltspray Rig"
            case "3":
                return "Arowana Mall"
            case "4":
                return "Blackbelly Skatepark"
            case "5":
                return "Camp Triggerfish"
            case "6":
                return "Port Mackerel"
            case "7":
                return "Kelp Dome"
            case "8":
                return "Moray Towers"
            case "9":
                return "Bluefin Depot"
            case "10":
                return "Hammerhead Bridge"
            case "11":
                return "Flounder Heights"
            case "12":
                return "Museum D'Alfonsino"
            case "13":
                return "Ancho-V Games"
            case "14":
                return "Piranha Pit"
            case "15":
                return "Mahi-Mahi Resort"
            case _:
                exit("Invalid Stage ID")

if __name__ == "__main__":
    download()
    fesdata()