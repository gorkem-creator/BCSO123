import discord
from discord.ext import commands
import sqlite3
import os

# --- AYARLAR ---
# Token'ı artık kodun içine değil, Render'daki Environment Variables kısmına yazacaksın.
TOKEN = os.environ.get('TOKEN')
MESAILOG_ID = 1507899796390936739  # Buraya log kanalının ID'sini gir
BASVURU_TAKIP_ID = 1507926143825612863 # Buraya başvuru takip kanalının ID'sini gir

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Veritabanı
conn = sqlite3.connect('mesai.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS mesai (user_id INTEGER PRIMARY KEY, dakika INTEGER)')
conn.commit()

@bot.event
async def on_ready():
    await bot.tree.sync() # Slash komutlarını aktif eder
    print(f"{bot.user} başarıyla giriş yaptı!")

# Panelleri Kurma Komutu
@bot.tree.command(name="panel_kur", description="BCSO Panellerini kurar")
@discord.app_commands.checks.has_permissions(administrator=True)
async def panel_kur(interaction: discord.Interaction):
    embed = discord.Embed(
        title="BCSO Mesai Paneli", 
        description="Mesaide değilken botu açık bırakmanız mesainizin sıfırlanması ve strike 1 yemenizle sonuçlanır.", 
        color=discord.Color.green()
    )
    embed.set_image(url="https://media.discordapp.net/attachments/1498313566015717446/1498797722365460683/image.png")
    
    view = discord.ui.View(timeout=None)
    # Butonlar eklenecek
    view.add_item(discord.ui.Button(label="Mesai Başlat", style=discord.ButtonStyle.green, custom_id="giris"))
    view.add_item(discord.ui.Button(label="Mesai Bitir", style=discord.ButtonStyle.red, custom_id="cikis"))
    
    await interaction.response.send_message("Panel gönderildi!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)

# Botu Çalıştır
if TOKEN:
    bot.run(TOKEN)
else:
    print("HATA: TOKEN bulunamadı! Render'da Environment Variables kısmına eklediğinden emin ol.")
