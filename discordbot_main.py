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
    
    def getUsers(self):
        "Vissza adja az összes Users az APIból"
        full_url = self._get_url
        req = requests.get(url = full_url)
        data = req.json()
        print(data)
        return data
    
    def getUser(self, user: discord.Interaction):
        "Vissza adja a megadott Usert -> discord.Interaction-t vár és abból kéri ki az id-t ami alapján azonosítja az userst"
        full_url = self._get_url
        params = {"dcid": str(user.user.id)}
        req = requests.get(url = full_url,params=params)
        data = req.json()
        return data
    
    def registerUser(self, username, passwd, eloadas,dcid):
        "User mentése az adatbázisba"
        full_url = self._get_url
        params = {"name": username, "dcid":dcid, "password":passwd, "eloadasShow": eloadas} # TODO eloadás Igen/Nem convert to 0/1
        req = requests.get(url = full_url,params=params)
        data = req.json() # TODO vissza adott jsont bele kell appendolni a _users-be
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
        return data
        
        
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
                return user
        # return {}

    def set_user(self, users):
        "Összes user beállítása"
        self._users = users
    
    def add_user(self,user):
        "Új user regisztrálása"
        self._users.append(user) #TODO biztos append? xd
        

class CalendarLesson():
    "Órarend kezelése"
    def __init__(self, orak: dict) -> None:
        self._orak = orak
        self._currentTime = datetime.datetime.now()
    
    def _updateTime(self):
        "up-to-date legyen a dátum"
        self._currentTime = datetime.datetime.now()
        
    def getNextLesson(self):
        "Következő óra visszaadása"
        self._updateTime()
        today = datetime.date.today()
        return self._getLessonFromDate(today)[0] # TODo nem jó mert meg kell nézni a mostani időt és az alapján hogy mi a next
    
    def getTodayLessen(self):
        "Összes mai óra lekérése"
        self._updateTime()
        today = datetime.date.today()
        return self._getLessonFromDate(today)
    
    def getTommorrowLesson(self):
        "Összes holnapi óra lekérése"
        self._updateTime()
        tommorrow = datetime.date.today() + datetime.timedelta(days=1)
        return self._getLessonFromDate(tommorrow)
    
    def _getLessonFromDate(self,date: datetime.date):
        "Órák visszaadása egy adott napra, csak egy helper def"
        todayLessons = []
        currentDate = date
        for lesson in self._orak:
            less = self._lessonFormater(lesson)
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
    global users
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Mai nap', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        apiData = api.getNeptunCalendar("281840031738626058") # TODO saját dcid
        calendars = CalendarLesson(apiData["calendarData"])
        mai = calendars.getTodayLessen()
        embed=discord.Embed(title="Mai órarend", color=0x16df63)
        for ora in mai:
            oraname = ora["title"] + "("+ ora["location"] +")"
            mettol = datetime.datetime.fromtimestamp(int(ora["start"])/1000.0)
            meddig = datetime.datetime.fromtimestamp(int(ora["end"])/1000.0)
            
            kiiras = mettol.strftime("%Y-%m-%d %H:%M") + " - " + meddig.strftime("%H:%M")
            embed.add_field(name=oraname, value=kiiras, inline=False)
        embed.set_footer(text="Ide majd hogy kell-e esőrnyő meg ilyenek")
        await interaction.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)

    @discord.ui.button(label='Következő óra', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Következő óra', ephemeral=True)

    @discord.ui.button(label='Holnap', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Holnap', ephemeral=True)


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
        self.sendNotification.start() # loop indítása
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
        
    @tasks.loop(seconds=10)
    async def sendNotification(self):
        pass # TODO sync a notofication kiküldéséhez. Minden fél órában
    
    @sendNotification.before_loop
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
    """Regisztráció megkezdése"""
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
        # TODo reg api request, előtte meg neptup api check, hogy jó a jelszó 
        registered = api.registerUser(self.username, self.passwd, self.eloadasBejar,interaction.user.id)
        if(len(registered) == 1):
            print("sikeres regisztráció") # sikeres reg + hozzá kell adni az usersnek a listájához!!
            users.set_user(registered[0])
        await interaction.response.send_message(f'Thanks for your response, {self.name}! {self.name} \n {self.passwd}', ephemeral=True)


@client.tree.command(name="teszt")
async def teszt(interaction: discord.Interaction):
    # await client.tree.sync()

    currentUser = api.getUser(interaction)
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
    # TODO  api lekérés ha már van regisztrálva az apiba akkor csak üdvözölje max
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