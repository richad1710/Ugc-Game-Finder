try:
    try:
        import requests
        import os
        from rgbprint import gradient_print, color, Color
        import webbrowser
        import json
    except ModuleNotFoundError as errora:
        import os
        print(f'{errora} Installing Now')
        os.system('pip install requests')
        os.system('pip install rgbprint')
        quit()
except ModuleNotFoundError as error:
    import os
    print(f'{error} Installing Now')
    os.system('pip install requests')
    os.system('pip install rgbprint')
    quit()

j = open('config.json')
data = json.load(j)

logo = ("""
  d8,                                          ,d8888b  d8,                d8b                 
 `8P                                           88P'    `8P                 88P                 
                                            d888888P                      d88                  
  88b d888b8b   d8888b   88bd88b .d888b,      ?88'      88b  88bd88b  d888888   d8888b  88bd88b
  88Pd8P' ?88  d8P' ?88  88P'  ` ?8b,         88P       88P  88P' ?8bd8P' ?88  d8b_,dP  88P'  `
 d88 88b  ,88b 88b  d88 d88        `?8b      d88       d88  d88   88P88b  ,88b 88b     d88     
d88' `?88P'`88b`?8888P'd88'     `?888P'     d88'      d88' d88'   88b`?88P'`88b`?888P'd88'     
            )88                                                                                
           ,88P                                                                                
       `?8888P                                                                                 
""")

gradient_print(logo, start_color=(69, 140, 255), end_color=(135, 181, 255))
gradient_print("What Is The Item Id?", start_color=(69, 140, 255), end_color=(135, 181, 255))
ids = input(f"{Color((69, 140, 255))}>{Color.white} ")

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = (data)["account"]['cookie']

def rbx_request(method, url, **kwargs):
    request = session.request(method, url, **kwargs)
    method = method.lower()
    if (method == "post") or (method == "put") or (method == "patch") or (method == "delete"):
        if "X-CSRF-TOKEN" in request.headers:
            session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
            if request.status_code == 403:
                request = session.request(method, url, **kwargs)
    return request


req = rbx_request("GET", f"https://economy.roblox.com/v2/assets/{ids}/details")

if req.status_code == 400:
    print("Not a Valid Id")
    os.system("pause")
    quit()

if (req.json())["SaleLocation"] is None or len((req.json())["SaleLocation"].get("UniverseIds", [])) == 0:
    print("Put Ur Roblox Cookie Or This Item Doesn't Have An Id")
    os.system("pause")
    quit()

universe_ids = (req.json())['SaleLocation'].get('UniverseIds', [])

req2 = rbx_request("GET", (f"https://games.roblox.com/v1/games?universeIds={','.join(map(str, universe_ids))}"))

game_list = []
for current in (req2.json())["data"]:
    game_list.append(current['rootPlaceId'])

req3 = rbx_request("GET", (f"https://www.roblox.com/games/{','.join(map(str, game_list))}"))
print(str(req3.url))
if data['game']['auto-join'] == True:
    webbrowser.open(f'roblox://experiences/start?placeId={",".join(map(str, game_list))}')
    print('Opened Browser')
else:
    print('Auto-join Disabled')

os.system("pause")
