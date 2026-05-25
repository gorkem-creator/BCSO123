import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync() # Komutları Discord'a işler
    print(f"{bot.user} hazır!")

@bot.tree.command(name="panel_kur", description="BCSO Mesai panelini gönderir")
async def panel_kur(interaction: discord.Interaction):
    embed = discord.Embed(title="BCSO Mesai Paneli", description="Aşağıdaki butonları kullan.", color=discord.Color.blue())
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="Mesai Giriş (10-41)", style=discord.ButtonStyle.green, custom_id="giris"))
    view.add_item(discord.ui.Button(label="Mesai Çıkış (10-42)", style=discord.ButtonStyle.red, custom_id="cikis"))
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data['custom_id'] == "giris":
            await interaction.response.send_message("✅ Mesaiye giriş yaptın!", ephemeral=True)
        elif interaction.data['custom_id'] == "cikis":
            await interaction.response.send_message("❌ Mesaiyi bitirdin!", ephemeral=True)

bot.run(os.environ['TOKEN'])
