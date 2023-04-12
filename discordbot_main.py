# This example requires the 'message_content' privileged intent to function.
#! windows venv futtatásához Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

import datetime
import discord

from discord.ui import button, TextInput
from discord.ext import tasks

# Saját importok
from UserManager import UsersManage
from NeptunAPI import Api
from Lesson import CalendarLesson, Lesson

class PersistentView(discord.ui.View):
    "Nézet az órarend választóhoz, gombok bot resi után is működjenek"
    def __init__(self):
        super().__init__(timeout=None)

    @button(label='Mai nap', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, _: discord.ui.Button):
        "Mai nap gomg kattintás"
        api_data = api.get_neptun_calendar(users.get_user(interaction.user.id)) # interacion user id
        calendars = CalendarLesson(api_data["calendarData"], api_data["eloadasShow"])
        mai = calendars.get_today_lesson()
        embed = self.embed_generator(mai, "Mai óráid")
        await interaction.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)

    @button(label='Következő óra', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, _: discord.ui.Button):
        "Következő óra gomb kattintás"
        api_data = api.get_neptun_calendar(users.get_user(interaction.user.id)) # interacion user id
        calendars = CalendarLesson(api_data["calendarData"], api_data["eloadasShow"])
        mai = calendars.get_next_lesson()
        embed = self.embed_generator(mai, "Következő órád")
        await interaction.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)

    @button(label='Holnap', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interaction: discord.Interaction, _: discord.ui.Button):
        "Holnap gomgra kattintás"
        api_data = api.get_neptun_calendar(users.get_user(interaction.user.id)) # interacion user id
        calendars = CalendarLesson(api_data["calendarData"], api_data["eloadasShow"])
        mai = calendars.get_tomorrow_lesson()
        embed = self.embed_generator(mai, "Holnapi óráid")
        await interaction.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)

    def embed_generator(self, orararend:list[Lesson], orarend_title: str):
        "vissza adja az órarend embeded"
        embed=discord.Embed(title=orarend_title, color=0x16df63)
        for ora in orararend:
            oraname = ora.title + " \n("+ ora.location +")"
            kiiras = ora.get_mettol_meddig()
            embed.add_field(name=oraname, value=kiiras, inline=False)
        idojaras = api.weather.get_current_weather_string()
        embed.set_footer(text=idojaras)
        return embed


users = UsersManage()
api = Api("https://swansi.hu/python_gyak_api/")

class MyClient(discord.Client):
    "Fő discord bot client"
    def __init__(self, *, intents_req: discord.Intents):
        super().__init__(intents=intents_req)
        self.tree = discord.app_commands.CommandTree(self)
        self._tick = 0

    async def setup_hook(self) -> None:
        await self.tree.sync()
        self.background_task.start() #TODO loop indítása
        # gombok működésre bírása, alapból bot reset után nem csinálna semmit
        self.add_view(PersistentView())

    async def on_member_join(self, member):
        "Member join to guild (dc server)"
        await on_join_reg(member)

    async def on_ready(self):
        "When bot is ready"
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        api_user = api.get_users() # list kell nekünk
        users.set_user(api_user)
        
    @tasks.loop(minutes=10)
    async def background_task(self):
        "óra kezdés előtt kb 1 órával notoficationt küld"
        self._tick += 1
        if self._tick  == 2:
            api.weather.update_weather()
            print("weather update success in TICK:", self._tick)
            self._tick = 0
        all_user = users.get_all_user()
        for user in all_user:
            user_calendar = api.get_neptun_calendar(users.get_user(user.dcid))
            calendar_data = user_calendar["calendarData"]
            next_lesson = CalendarLesson(calendar_data,user.eloadasShow).get_next_lesson()[0]
            lesson_start = next_lesson.get_start_datetime()
            print("==========================")
            print(next_lesson)
            print(lesson_start)
            diff = lesson_start - datetime.datetime.now() # óra kezdése kivonása a mostani időből
            print(diff)
            hours, remainder = divmod(diff.seconds, 3600)
            print("DIFF HOURS:", hours)
            minutes, _ = divmod(remainder, 60)
            print(minutes)
            if 50 <= minutes <= 59 and hours == 0: # ha 50
                print("Óra kezdéséig van még 50-60 perc")
                view = PersistentView()
                embed = view.embed_generator([next_lesson], "Hamarosan órád lesz!")
                current_user = self.get_user(int(user.dcid))
                if current_user is None:
                    return # ha nincs user nem tud üzit küldeni neki
                dm = await current_user.create_dm()
                await dm.send(embed=embed, view=view)
            print("==========================")

    @background_task.before_loop
    async def before_my_task(self):
        "Mielőtt elkezdődne a background task"
        await self.wait_until_ready()  # Ha ready a bot akkor induljon el a loop
        # Bár nem tudom miért nem az on_ready-ben indítom a loopot, de elvileg ez így jobb


intents = discord.Intents.all()
client = MyClient(intents_req=intents)

@client.tree.command(name="sync")
async def sync(interaction: discord.Interaction):
    "sync command just for test"
    await client.tree.sync()
    client.add_view(PersistentView())
    # néha ledobja a 'láncot' és vissza kell rá rakni a view-et de ha nem jó a loopba be kell rakni
    await interaction.response.send_message("success", ephemeral=True)

# @app_commands.describe()
@client.tree.command(name="orarend")
async def orarend(interaction: discord.Interaction):
    """Órarend parancsok"""
    embed=discord.Embed(title="Órarend műveletek", color=0x2b31e3)
    name_field = "Kérlek válassz az alábbi műveletek közül!"
    embed.add_field(name=name_field, value="Kattints a gombokra", inline=False)
    await interaction.response.send_message(embed=embed, view=PersistentView())


class Register(discord.ui.Modal, title='Regisztráció'):
    "Regisztrációs nézet"
    username = TextInput(label='Neptun kód', placeholder="Neptun kód", required=True)
    passwd = TextInput(label='Jelszó', placeholder="Password", required=True)
    eloadas = TextInput(label="Bejársz előadásokra?", placeholder="Igen/Nem",default="Nem", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        "reg api request, előtte meg neptup api check, hogy jó a jelszó"
        try:
            if self.eloadas.value.upper() == "IGEN": # kell neki egy .value, hogy str-be adja vissza
                self.eloadas = 1
            else:
                self.eloadas = 0
        except Exception:
            self.eloadas = 1 # ezért legyen valami értéke
        registered = api.register_user(self.username, self.passwd, self.eloadas,interaction.user.id)
        if len(registered) == 1:
            print("sikeres regisztráció") # sikeres reg + hozzá kell adni az usersnek a listájához!!
            users.add_user(registered)
        # TODO message kicserélése a /orarend parancsba lévő cuccra
        await interaction.response.send_message("Köszi batyi a reget", ephemeral=True)



async def on_join_reg(ctx: discord.Member):
    "Ha nincs regisztrálva regisztrálja, amúgy órarendválasztó"
    #  api lekérés ha már van regisztrálva az apiba akkor csak üdvözölje max
    user = api.get_user(ctx.id)
    if len(user) == 0:
        # Ha nincs user DO registration
        button_reg = discord.ui.Button(label="Regisztráció", style=discord.ButtonStyle.green)
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(Register())
        button_reg.callback = button_callback
        view = discord.ui.View()
        view.add_item(button_reg)
        # print(ctx.author.name)
        # user = bot.get_user(ctx.author.id)
        dm = await ctx.create_dm()
        dm_text = "Szia uram, ha szeretnéd használni az órarendet akkor kérlek regisztrálj be!"
        await dm.send(dm_text, view=view)
    else:
        dm = await ctx.create_dm()
        embed=discord.Embed(title="Órarend műveletek", color=0x2b31e3)
        field_name = "Kérlek válassz az alábbi műveletek közül!"
        embed.add_field(name=field_name, value="Kattints a gombokra", inline=False)
        await dm.send(embed=embed, view=PersistentView())

client.run('MTA5MTMwOTY4NDk4MTUxNDI3MA.GfEBla.IO-j6pnGx34p4fX3ipYlg0lKvpcpZmm9fT0uXA')
# TODO CONFIG FILE + COmmitnél kiszedni


#! tesz része
# api_user = api.get_users() # list kell nekünk
# users.set_user(api_user) # be vannak á


# teszttt = api.get_neptun_calendar("281840031738626058")
# calendars = CalendarLesson(teszttt["calendarData"])
# print("/=======")
# print(calendars.get_today_lesson())




# orarend["calendarData"][0]["start"]
# orarend["calendarData"][0]["end"]
# orarend["calendarData"][0]["title"]
# orarend["calendarData"][0]["location"]


#? neptun adatok lekérdezése https://github.com/RuzsaGergely/Atlantisz
