"""Fő discord bot file"""
#! windows venv futtatásához Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

import datetime
import discord

from discord import ButtonStyle
from discord.ui import button, TextInput
from discord.ext import tasks

# Saját importok
from UserManager import UsersManage
from NeptunAPI import Api
from Lesson import CalendarLesson, Lesson
from config import Config

config = Config()
if config.is_error is True:
    raise FileNotFoundError("File nem található")
class PersistentView(discord.ui.View):
    "Nézet az órarend választóhoz, gombok bot resi után is működjenek"
    def __init__(self):
        super().__init__(timeout=None)

    @button(label='Mai nap', style=ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interact: discord.Interaction, _: discord.ui.Button):
        "Mai nap gomg kattintás"
        api_data = api.get_neptun_calendar(users.get_user(interact.user.id))
        if api_data["ErrorMessage"] is None: # ha megváltoztatta a jelszavát pl
            calendars = CalendarLesson(api_data["calendarData"], api_data["eloadasShow"])
            mai = calendars.get_today_lesson()
            embed = self.embed_generator(mai, "Mai óráid")
            await interact.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)
        else:
            embed = client.get_reg_error_embed(api_data["ErrorMessage"])
            await interact.response.send_message(embed=embed)

    @button(label='Következő óra', style=ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interact: discord.Interaction, _: discord.ui.Button):
        "Következő óra gomb kattintás"
        api_data = api.get_neptun_calendar(users.get_user(interact.user.id))
        if api_data["ErrorMessage"] is None:
            calendars = CalendarLesson(api_data["calendarData"], api_data["eloadasShow"])
            mai = calendars.get_next_lesson()
            embed = self.embed_generator(mai, "Következő órád")
            await interact.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)
        else:
            embed = client.get_reg_error_embed(api_data["ErrorMessage"])
            await interact.response.send_message(embed=embed)

    @button(label='Holnap', style=ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interact: discord.Interaction, _: discord.ui.Button):
        "Holnap gomgra kattintás"
        api_data = api.get_neptun_calendar(users.get_user(interact.user.id))
        if api_data["ErrorMessage"] is None:
            calendars = CalendarLesson(api_data["calendarData"], api_data["eloadasShow"])
            mai = calendars.get_tomorrow_lesson()
            embed = self.embed_generator(mai, "Holnapi óráid")
            await interact.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)
        else:
            embed = client.get_reg_error_embed(api_data["ErrorMessage"])
            await interact.response.send_message(embed=embed)

    @button(label='Kövezkező vizsga', style=ButtonStyle.primary, custom_id='persistent_view:vizsga')
    async def vizsga(self, interact: discord.Interaction, _: discord.ui.Button):
        "Vizsga gomgra kattintás"
        api_data = api.get_neptun_calendar(users.get_user(interact.user.id))
        if api_data["ErrorMessage"] is None:
            calendars = CalendarLesson(api_data["calendarData"], api_data["eloadasShow"])
            mai = calendars.get_exam()
            embed = self.embed_generator(mai, "Következő vizsgáid")
            await interact.response.send_message(embed=embed, view=PersistentView(), ephemeral=True)
        else:
            embed = client.get_reg_error_embed(api_data["ErrorMessage"])
            await interact.response.send_message(embed=embed)

    def embed_generator(self, orararend:list[Lesson], orarend_title: str):
        "vissza adja az órarend embeded"
        embed=discord.Embed(title=orarend_title, color=0x16df63)
        for ora in orararend:
            oraname = ora.title + " \n("+ ora.location +")"
            kiiras = ora.get_mettol_meddig()
            embed.add_field(name=oraname, value=kiiras, inline=False)
        if len(orararend) == 0:
            embed_value = "Lehet lazítani vagy tanülni a kövi zhra 😉"
            embed.add_field(name="Nincs órád", value=embed_value,inline=False)
        idojaras = api.weather.get_current_weather_string()
        embed.set_footer(text=idojaras)
        return embed

users = UsersManage()
api = Api(config.users_api,config.neptun_api,config.weather_api,config.weather_status_codes)

class MyClient(discord.Client):
    "Fő discord bot client"
    def __init__(self, *, intents_req: discord.Intents):
        super().__init__(intents=intents_req)
        self.tree = discord.app_commands.CommandTree(self)
        self._tick = 0

    async def setup_hook(self) -> None:
        await self.tree.sync()
        self.background_task.start() # loop indítása
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
        print("loopStartAT", datetime.datetime.now())
        self._tick += 1
        if self._tick == 2:
            api.weather.update_weather()
            print("weather update success in TICK:", self._tick)
            self._tick = 0
        print("LOOPTICK", self._tick)
        all_user = users.get_all_user()
        print("ALLUSER",all_user)
        for user in all_user:
            user_calendar = api.get_neptun_calendar(users.get_user(user.dcid))
            print(user_calendar)
            if user_calendar["ErrorMessage"] is not None: # neptun api hiba
                if user.is_error_reported is False:
                    user.is_error_reported = True
                    embed = self.get_reg_error_embed(user_calendar["ErrorMessage"])
                    direct_message = await self.get_user(int(user.dcid)).create_dm()
                    await direct_message.send(embed=embed)
                continue
            calendar_data = user_calendar["calendarData"]
            next_lesson = CalendarLesson(calendar_data,user.eloadas_show).get_next_lesson()[0]
            lesson_start = next_lesson.get_start_datetime()
            print("==========================")
            print(next_lesson.title)
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
                # nem értem miért sír a pylint a 'dm' változóra discord.py-ba CREATE_DM() a def!!!!
                direct_message = await current_user.create_dm()
                await direct_message.send(embed=embed, view=view)
            print("==========================")

    @background_task.before_loop
    async def before_my_task(self):
        "Mielőtt elkezdődne a background task"
        await self.wait_until_ready()  # Ha ready a bot akkor induljon el a loop
        # Bár nem tudom miért nem az on_ready-ben indítom a loopot, de elvileg ez így jobb

    def get_orarend_valaszto_embed(self) -> discord.Embed:
        "Órarend választó embed visszadása"
        embed=discord.Embed(title="Órarend műveletek", color=0x2b31e3)
        name_field = "Kérlek válassz az alábbi műveletek közül!"
        embed.add_field(name=name_field, value="Kattints a gombokra", inline=False)
        return embed

    def get_reg_error_embed(self,error_msg) -> discord.Embed:
        "Órarend választó embed visszadása"
        embed=discord.Embed(title="Regisztráció", color=0xff0000)
        field_name = "Sikertelen regisztráció"
        embed.add_field(name=field_name, value=error_msg, inline=False)
        return embed

intents = discord.Intents.all()
client = MyClient(intents_req=intents)

@client.tree.command(name="sync")
async def sync(interaction: discord.Interaction):
    "sync command just for test"
    await client.tree.sync()
    client.add_view(PersistentView())
    # néha ledobja a 'láncot' és vissza kell rá rakni a view-et de ha nem jó a loopba be kell rakni
    await interaction.response.send_message("success", ephemeral=True)

@client.tree.command(name="register")
async def reg_command(interaction: discord.Interaction):
    "Regisztrációs parancs"
    await interaction.response.send_modal(Register())

@client.tree.command(name="orarend")
async def orarend(interaction: discord.Interaction):
    """Órarend parancsok"""
    embed = client.get_orarend_valaszto_embed()
    await interaction.response.send_message(embed=embed, view=PersistentView())
class Register(discord.ui.Modal, title='Regisztráció'):
    "Regisztrációs nézet"
    username = TextInput(label='Neptun kód', placeholder="Neptun kód", required=True)
    passwd = TextInput(label='Jelszó', placeholder="Password", required=True)
    ea = TextInput(label="Bejársz előadásokra?",placeholder="Igen/Nem",default="Nem",required=True)
    async def on_submit(self, interaction: discord.Interaction):
        "reg api request, előtte meg neptup api check, hogy jó a jelszó"
        eloadas_bejaras = 0
        try:
            if self.ea.value.upper() == "IGEN": # kell neki egy .value, hogy str-be adja vissza
                eloadas_bejaras = 1
            else:
                eloadas_bejaras = 0
        except Exception:
            eloadas_bejaras = 1 # ezért legyen valami értéke
        reg_teszt = api.get_neptun_reg_teszt(self.username,self.passwd)
        if reg_teszt["error"] is False: # jó minden
            reged = api.register_user(self.username, self.passwd, eloadas_bejaras,interaction.user.id)
            users.add_user(reged)
            embed = client.get_orarend_valaszto_embed()
            await interaction.response.send_message(embed=embed, view=PersistentView())
        else: # sikertelen reg
            embed = client.get_reg_error_embed(reg_teszt["msg"])
            await interaction.response.send_message(embed=embed)

async def on_join_reg(ctx: discord.Member):
    "Ha nincs regisztrálva regisztrálja, amúgy órarendválasztó"
    user = api.get_user(ctx.id)
    if len(user) == 0: # ha nincs regisztrálva
        # Ha nincs user DO registration
        button_reg = discord.ui.Button(label="Regisztráció", style=ButtonStyle.green)
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(Register())
        button_reg.callback = button_callback
        view = discord.ui.View()
        view.add_item(button_reg)
        direct_message = await ctx.create_dm()
        dm_text = "Szia uram, ha szeretnéd használni az órarendet akkor kérlek regisztrálj be!"
        await direct_message.send(dm_text, view=view)
    else: # ha regisztrálva van
        direct_message = await ctx.create_dm()
        embed = client.get_orarend_valaszto_embed()
        await direct_message.send(embed=embed, view=PersistentView())

client.run(config.bot_token)

# TODO update user account

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
