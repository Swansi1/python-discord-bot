import asyncio
import discord
from discord import ui
from discord.ui import Button, View, TextInput
from discord.ext import commands
from discord.ext.commands import Bot, Context
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

# intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True
# # tree = discord.app_commands.CommandTree(bot)


class Register(ui.Modal, title='Regisztráció'):
    name = ui.TextInput(label='Neptun kód', placeholder="Neptun kód", required=True)
    answer = ui.TextInput(label='Jelszó', placeholder="Password", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        # TODo reg api request, előtte meg neptup api check, hogy jó a jelszó 
        await interaction.response.send_message(f'Thanks for your response, {self.name}! {self.name} \n {self.answer}', ephemeral=True)


async def teszt(ctx: Context):
    button = Button(label="Regisztráció", style=discord.ButtonStyle.green)
    
    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(Register())
        
    button.callback = button_callback
    view = View()
    view.add_item(button)
    
    # print(ctx.author.name)
    # user = bot.get_user(ctx.author.id)
    dm = await ctx.author.create_dm()
    
    await dm.send("Szia uram", view=view)






intents = discord.Intents.all()


# client = MyClient(intents=intents)
client = commands.Bot(command_prefix='/', description=description, intents=intents)
# client = discord.Client(intents=intents)
# tree = discord.app_commands.CommandTree(client)

@client.command(name = "teszt", description = "My first application Command") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(ctx: commands.context.Context):
    await teszt(ctx)


@client.event
async def on_ready():
    # await c.sync(guild=discord.Object(id=1091308819482689548))
    print("Ready!")
    
@client.event
async def on_member_join(member):
    print("Új tag joinolt ")
    teszt()



client.run('MTA5MTMwOTY4NDk4MTUxNDI3MA.GfEBla.IO-j6pnGx34p4fX3ipYlg0lKvpcpZmm9fT0uXA')