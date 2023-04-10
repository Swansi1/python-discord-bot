# This example requires the 'message_content' privileged intent to function.

import json
from discord.ext import commands
import discord
from discord.ui import Button, View, TextInput
from discord import app_commands
from discord import ui, Member
from discord.ext.commands import Bot, Context
from discord.ext import tasks
import requests
import calendar, datetime



class Api():
    """"Kommunikáció az API-val"""
    global users
    def __init__(self,api_url) -> None:
        self._api_url = api_url
        self._get_url = self._api_url + "getUsers.php"
        self._reg_url = self._api_url + "registerUser.php"
        self.weather = weatherApi()
    
    def getUsers(self):
        "Vissza adja az összes Users az APIból"
        full_url = self._get_url
        req = requests.get(url = full_url)
        data = req.json()
        print(data)
        return data
    
    def getUser(self, dcid):
        "Vissza adja a megadott Usert -> dcid-t vár és abból kéri ki az id-t ami alapján azonosítja az userst"
        full_url = self._get_url
        params = {"dcid": str(dcid)}
        req = requests.get(url = full_url,params=params)
        data = req.json()
        return data
    
    def registerUser(self, username, passwd, eloadas,dcid):
        "User mentése az adatbázisba"
        full_url = self._reg_url
        data = {"username": username, "dcid": dcid, "password":passwd, "eloadasShow": eloadas} # TODO eloadás Igen/Nem convert to 0/1
        req = requests.post(url = full_url,data=data)
        data = req.json() # TODO vissza adott jsont bele kell appendolni a _users-be
        print("SIKERES REG?")
        print(data)
        return data

    def getNeptunCalendar(self, cuser):
        "Lekérdezi az usernek az órarendjét 8 napot kér le, cuser = DCID"
        current = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        end = current + datetime.timedelta(days=8)
        time_start = int(current.timestamp()) * 1000
        time_end = int(end.timestamp()) * 1000

        user = users.get_user(cuser)
        url = "http://swansi.hu:8000/neptun/naptar"
        payload={'username': user["username"], 'password': user["password"], 'timestamp_start': time_start, 'timestamp_end':time_end}
        req = requests.post(url, data=payload)
        data = req.json() # ez a szar API valamiért vissza adja a jelszót is...
        eloadas = {"eloadasShow": user["eloadasShow"]}
        data.update(eloadas) # adja hozzá hogy bejáre az EA-ra 
        return data
        
        
class weatherApi():
    "Időjárás API"
    def __init__(self) -> None:
        self._statusCodes = [{'status': 1000, 'text': 'Napos idő'}, {'status': 1003, 'text': 'Részben felhős'}, {'status': 1006, 'text': 'Felhős'}, {'status': 1009, 'text': 'Borús'}, {'status': 1030, 'text': 'Gyenge köd'}, {'status': 1063, 'text': 'A közelben eső'}, {'status': 1066, 'text': 'A közelben foltokban havazás'}, {'status': 1069, 'text': 'A közelben foltokban dara'}, {'status': 1072, 'text': 'A közelben foltokban szemerkélő fagyos eső'}, {'status': 1087, 'text': 'A közelben hirtelen vihar'}, {'status': 1114, 'text': 'Hófúvás'}, {'status': 1117, 'text': 'Hóvihar'}, {'status': 1135, 'text': 'Köd'}, {'status': 1147, 'text': 'Jeges köd'}, {'status': 1150, 'text': 'Foltokban enyhe szemerkélő eső'}, {'status': 1153, 'text': 'Enyhe szemerkélő eső'}, {'status': 1168, 'text': 'Fagyos szemerkélő eső'}, {'status': 1171, 'text': 'Heves szemerkélő fagyos eső'}, {'status': 1180, 'text': 'Foltokban enyhe eső'}, {'status': 1183, 'text': 'Enyhe eső'}, {'status': 1186, 'text': 'Időnként mérsékelt eső'}, {'status': 1189, 'text': 'Mérsékelt eső'}, {'status': 1192, 'text': 'Időnként heves eső'}, {'status': 1195, 'text': 'Heves eső'}, {'status': 1198, 'text': 'Enyhe fagyos eső'}, {'status': 1201, 'text': 'Mérsékelt, vagy heves fagyos eső'}, {'status': 1204, 'text': 'Enyhe ólmos eső'}, {'status': 1207, 'text': 'Mérsékelt, vagy heves ólmos eső'}, {'status': 1210, 'text': 'Foltokban enyhe havazás'}, {'status': 1213, 'text': 'Enyhe havazás'}, {'status': 1216, 'text': 'Foltokban mérsékelt havazás'}, {'status': 1219, 'text': 'Mérsékelt havazás'}, {'status': 1222, 'text': 'Foltokban heves havazás'}, {'status': 1225, 'text': 'Heves havazás'}, {'status': 1237, 'text': 'Apró szemű jégeső'}, {'status': 1240, 'text': 'Enyhe eső, zápor'}, {'status': 1243, 'text': 'Mérsékelt, vagy heves felhőszakadás'}, {'status': 1246, 'text': 'Viharos felhőszakadás'}, {'status': 1249, 'text': 'Enyhe ólmos záporeső'}, {'status': 1252, 'text': 'Mérsékelt, vagy heves ólmos záporeső'}, {'status': 1255, 'text': 'Enyhe hózápor'}, {'status': 1258, 'text': 'Mérsékelt, vagy heves hózápor'}, {'status': 1261, 'text': 'Enyhe apró szemű jégeső'}, {'status': 1264, 'text': 'Mérsékelt, vagy heves apró szemű jégeső'}, {'status': 1273, 'text': 'Foltokban enyhe eső mennydörgéssel, villámlással'}, {'status': 1276, 'text': 'A területen foltokban enyhe eső mennydörgéssel, villámlással'}, {'status': 1279, 'text': 'A területen foltokban enyhe havazás mennydörgéssel, villámlással'}, {'status': 1282, 'text': 'Mérsékelt, vagy heves hózápor mennydörgéssel, villámlással'}] 
        self._url = "http://api.weatherapi.com/v1/current.json?key=0704db3dc77744e9b38171403231004&q=Szeged&aqi=no"
        self.currentWeather = {}
        
    def getCurrentWeather(self):
        "lekéri a jelenlegi időjárást"
        if len(self.currentWeather) == 0:
            self.updateWeather()
        return self.currentWeather

    def getCurrentWeatherToString(self):
        idojaras = self.getCurrentWeather()
        return "Időjárás("+ idojaras["name"] +"): Hőmérséklet: " + str(idojaras["temp"]) +"C \n" + idojaras["condition"] + "\nUtolsó frissítés: " + idojaras["last_update"]

    def updateWeather(self):
        "jelenlegi időjárás frissítése" 
        # TODO majd a taskba frissítse pl 10 percenként
        req = requests.get(self._url)
        data = req.json()
        print("IDŐJÁRÁS API JSON")
        print(data)
        getHunText = self._statusToText(data["current"]["condition"]["code"])
        dictReturn = {"name": data["location"]["name"], "condition": getHunText, "temp": data["current"]["temp_c"], "last_update": data["current"]["last_updated"]}
        self.currentWeather = dictReturn
        return dictReturn
    
    def _statusToText(self, statusCode):
        "Status codebeból magyar text mert alapból angol."
        text = "-"
        for status in self._statusCodes:
            if status["status"] == statusCode:
                text = status["text"]
                return text
        return text
        
        
class Users():
    "Regisztrált felhasználók kezelése"
    global api
    def __init__(self, users = []) -> None:
        self._users = users
    
    def get_user(self, dcid) -> list:
        "DCid alapján vissza adja az users, HA van regisztrálva"
        print(type(self._users))
        for user in self._users:
            if user["dcid"] == str(dcid):
                print("MEGTALÁLTA AZ USERST")
                print(user)
                return user
        # return {}

    def set_user(self, users):
        "Összes user beállítása"
        self._users = users
    
    def add_user(self,user):
        "Új user regisztrálása"
        print("HOZZÁADÁS LELŐTTT")
        print(self._users)
        self._users.append(user) #TODO biztos append? xd
        print(self._users) 
        

class CalendarLesson():
    "Órarend kezelése"
    def __init__(self, orak: dict,eloadas=0) -> None:
        self._orak = orak
        self._isEloadas = int(eloadas) # TODO must 0 / 1 | 0 = Nem jár be az előadásra és úgy adja vissza
        self._currentTime = datetime.datetime.now()
        self._today = datetime.date.today()
    
    def _updateTime(self,_TESZT=1): # nem kell paramétert megadni a teszt csak hogy hány nappal tolja el
        "up-to-date legyen a dátum"
        self._currentTime = datetime.datetime.now() + datetime.timedelta(days=_TESZT) #! CSAK TESZT MIATT!!!!
        self._today = datetime.date.today() + datetime.timedelta(days=_TESZT)
        
    def getNextLesson(self):
        "Következő óra visszaadása"
        self._updateTime()

        # list-be adja vissza a dictet... ne csak 1 dictet
        koviOra = [] # dictet insertelünk bele azazh egy órát
        for i in range(0,8):  
            for ora in self._getLessonFromDate(self._today + datetime.timedelta(days=i)): # hozzá ad mindig 1 napot mert lehet nem ma van a kövi óra
                oraKezdes = datetime.datetime.fromtimestamp(int(ora["start"]) / 1000.0)
                if  oraKezdes > self._currentTime: # dátum szerint vannak a list-ben szóval az első találat a kapó
                    # kezdés > mint a mostani 
                    koviOra.append(ora)
                    return koviOra 
        return koviOra 
    
    def getTodayLessen(self):
        "Összes mai óra lekérése"
        self._updateTime()
        return self._getLessonFromDate(self._today)
    
    def getTommorrowLesson(self):
        "Összes holnapi óra lekérése"
        self._updateTime()
        tommorrow = self._today + datetime.timedelta(days=1)
        return self._getLessonFromDate(tommorrow)
    
    def _getLessonFromDate(self,date: datetime.date) -> dict:
        "Órák visszaadása egy adott napra, csak egy helper def"
        todayLessons = []
        currentDate = date
        for lesson in self._orak:
            less = self._lessonFormater(lesson)
            try:
                if less == "EA": # ha ea hagyja ki az iterációt
                    continue
            except:
                pass
            if currentDate == datetime.date.fromtimestamp(int(less["start"]) / 1000.0):
                todayLessons.append(less)
        return todayLessons
        
        
    def _lessonFormater(self,lesson):
        "Sok hülyeség kiszedése, timestampok fixálása, óra neve rövidítése"
        # print(lesson)
        # title syntax
        # syntax = '[Órarend Szünnap]    -Tavaszi tanítási szünet (Spring school break)'
        # syntax = "[Óra] Hardware és software rendszerek verifikációja (IBK615G)  - IB615G-1   Minden hét (Gombás Éva Dr.) (IR-223-3 - Irinyi 223 PC-terem(IR-223-3))"
        newLesson = {}
        startTimeStamp = lesson["start"].split("(")[1].split(")")[0]
        # startDateTime = datetime.datetime.fromtimestamp(int(startTimeStamp)/1000.0)

        endTimeStamp =lesson["end"].split("(")[1].split(")")[0]
        # endDateTime = datetime.datetime.fromtimestamp(int(endTimeStamp)/1000.0)
        newTitle = lesson["title"]
        try:
            if self._isEloadas == 0: # nem jár be az eakra..
                print("NEM jár be az órákra")
                if 'e)' in newTitle or 'E)' in newTitle:
                    return "EA"
            else:
                print("Stréber a tag és bejár az összes órára")
            if '[Óra]' in newTitle: # Todo több iffel bővíteni (nem tudom hogy írja a vizsgákat) VIZSGA: [Vizsga]
                newTitle = newTitle.split("]")[1].split("-")[0].strip()
        except Exception as e:
            pass
        newLesson["start"] = startTimeStamp
        newLesson["end"] = endTimeStamp
        newLesson["title"] = newTitle
        newLesson["location"] = lesson["location"]
        return newLesson




class PersistentView(discord.ui.View):
    "Nézet az órarend választóhoz, gombok bot resi után is működjenek"
    global users, api
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Mai nap', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        apiData = api.getNeptunCalendar(interaction.user.id) # interacion user id
        calendars = CalendarLesson(apiData["calendarData"], apiData["eloadasShow"])
        mai = calendars.getTodayLessen()
        embed = self._embedGenerator(mai, "Mai óráid")
        await interaction.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)

    @discord.ui.button(label='Következő óra', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        apiData = api.getNeptunCalendar(interaction.user.id) # interacion user id
        calendars = CalendarLesson(apiData["calendarData"], apiData["eloadasShow"])
        mai = calendars.getNextLesson()
        embed = self._embedGenerator(mai, "Következő órád")
        await interaction.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)

    @discord.ui.button(label='Holnap', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        apiData = api.getNeptunCalendar(interaction.user.id) # interacion user id
        calendars = CalendarLesson(apiData["calendarData"], apiData["eloadasShow"])
        mai = calendars.getTommorrowLesson()
        embed = self._embedGenerator(mai, "Holnapi óráid")
        await interaction.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)
        
    def _embedGenerator(self, orararend, orarendTitle: str):
        "vissza adja az órarend embeded"
        embed=discord.Embed(title=orarendTitle, color=0x16df63)
        for ora in orararend:
            print("JELENLEGI ÓRA CHECK::")
            print(ora)
            print("======")
            oraname = ora["title"] + " \n("+ ora["location"] +")"
            mettol = datetime.datetime.fromtimestamp(int(ora["start"])/1000.0)
            meddig = datetime.datetime.fromtimestamp(int(ora["end"])/1000.0)
            
            kiiras = mettol.strftime("%Y-%m-%d %H:%M") + " - " + meddig.strftime("%H:%M")
            embed.add_field(name=oraname, value=kiiras, inline=False)
            
        idojaras = api.weather.getCurrentWeatherToString()
        # {"name": data["location"]["name"], "condition": getHunText, "temp": data["current"]["temp_c"], "last_update": data["current"]["last_updated"]}
        
        embed.set_footer(text=idojaras)
        return embed


users = Users()
api = Api("https://swansi.hu/python_gyak_api/")

class MyClient(discord.Client):
    "Fő discord bot client"
    global users, api
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        

    async def setup_hook(self) -> None:
        await self.tree.sync()
        # self.backgroundTask.start() #TODO loop indítása
        self.add_view(PersistentView()) # gombok működésre bírása, alapból bot reset után nem csinálna semmit

    async def on_member_join(self, member):
        print("Új tag joinolt ")
        await on_join_reg(member)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        api_user = api.getUsers() # list kell nekünk
        print(api_user)
        users.set_user(api_user) # be vannak állítva az userek apira nincs szükség mert ha regisztrál egy új akkor nem fetcheljük az apit, localba adjuk hozzá + api insert
        
    @tasks.loop(minutes=10)
    async def backgroundTask(self):
        api.weather.updateWeather()
        pass # TODO sync a notofication kiküldéséhez. Minden fél órában
    #TODO ha 1 óra és 50 perc van az órakezdésik akkor küld notit mert 15 perc lesz a tasks.loop ezért 1x küld csak notit 
    
    @backgroundTask.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # Ha ready a bot akkor induljon el a loop
        # Bár nem tudom miért nem az on_ready-ben indítom a loopot, de elvileg ez így jobb


intents = discord.Intents.all()
client = MyClient(intents=intents)

@client.tree.command(name="sync")
async def sync(Interaction: discord.Interaction):
    print("lefutott")
    await client.tree.sync()

# @app_commands.describe()
@client.tree.command(name="asd")
async def asd(interaction: discord.Interaction):
    """Órarend parancsok"""
    embed=discord.Embed(title="Órarend műveletek", color=0x2b31e3)
    embed.add_field(name="Kérlek válassz az alábbi műveletek közül!", value="Kattints a gombokra", inline=False)
    await interaction.response.send_message(embed=embed, view=PersistentView())


class Register(ui.Modal, title='Regisztráció'):
    "Regisztrációs nézet"
    global api,users
    username = ui.TextInput(label='Neptun kód', placeholder="Neptun kód", required=True)
    passwd = ui.TextInput(label='Jelszó', placeholder="Password", required=True)
    eloadasBejar = ui.TextInput(label="Bejársz előadásokra?", placeholder="Igen/Nem",default="Nem", required=True) 
    async def on_submit(self, interaction: discord.Interaction):
        #  reg api request, előtte meg neptup api check, hogy jó a jelszó 
        try:
            if self.eloadasBejar.upper() == "IGEN": # TODO ez valamiért nem jó
                self.eloadasBejar = 1
            else:
                self.eloadasBejar = 0
        except:
            self.eloadasBejar = 1 # ha hiba van akkor is járjon be sajnálom hogy nem tud beütni 3 betűs szót
        registered = api.registerUser(self.username, self.passwd, self.eloadasBejar,interaction.user.id)
        if(len(registered) == 1):
            print("sikeres regisztráció") # sikeres reg + hozzá kell adni az usersnek a listájához!!
            users.add_user(registered[0])
        await interaction.response.send_message(f'Thanks for your response, {self.username}! {self.username}', ephemeral=True)


@client.tree.command(name="teszt")
async def teszt(interaction: discord.Interaction):
    # await client.tree.sync()

    currentUser = api.getUser(interaction.user.id)
    if len(currentUser) == 1:
        # van már ilyen user
        embed=discord.Embed(title="Regisztráció", color=0xff0000)
        embed.add_field(name="Regisztráció sikertelen", value="Van már regisztrált felhasználód!", inline=False)
        embed.set_footer(text="Ha törölni szeretnéd az accountodat használd a /delete parancsot.")
        await interaction.response.send_message(embed=embed)
        return
    
    button = Button(label="Regisztráció", style=discord.ButtonStyle.green)
    
    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(Register())
        
    button.callback = button_callback
    view = View()
    view.add_item(button)
    
    
    await interaction.response.send_message("Szia uram", view=view)
    
async def on_join_reg(ctx: Member):
    "Ha nincs regisztrálva elküldi neki a regisztrációs embedet, ha már igen akkor az órarend választót"
    #  api lekérés ha már van regisztrálva az apiba akkor csak üdvözölje max
    user = api.getUser(ctx.id)
    if len(user) == 0:
        # Ha nincs user DO registration
        button = Button(label="Regisztráció", style=discord.ButtonStyle.green)
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(Register())
            
        button.callback = button_callback
        view = View()
        view.add_item(button)
        # print(ctx.author.name)
        # user = bot.get_user(ctx.author.id)
        dm = await ctx.create_dm()
        await dm.send("Szia uram, ha szeretnéd használni az órarendet akkor kérlek regisztrálj be!", view=view)
    else:
        pass # TODo send Preview vagy mi a rákot, órarend választót

client.run('') # TODO bot id kiszedése ha commitelünk



#! tesz része
# api_user = api.getUsers() # list kell nekünk
# users.set_user(api_user) # be vannak á


# teszttt = api.getNeptunCalendar("281840031738626058")
# calendars = CalendarLesson(teszttt["calendarData"])
# print("/=======")
# print(calendars.getTodayLessen())




# orarend["calendarData"][0]["start"]
# orarend["calendarData"][0]["end"]
# orarend["calendarData"][0]["title"]
# orarend["calendarData"][0]["location"]


#? neptun adatok lekérdezése https://github.com/RuzsaGergely/Atlantisz