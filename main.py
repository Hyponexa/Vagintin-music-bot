import os
import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Синхронизировано {len(synced)} команд.")
    except Exception as e:
        print(f"Ошибка при синхронизации команд: {e}")

@bot.tree.command(name="play", description="Проиграть музыку по ссылке YouTube")
@app_commands.describe(url="Ссылка на видео")
async def play(interaction: discord.Interaction, url: str):
    voice_channel = interaction.user.voice.channel if interaction.user.voice else None
    if not voice_channel:
        await interaction.response.send_message("❌ Ты не в голосовом канале!", ephemeral=True)
        return

    vc = await voice_channel.connect()
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False,
        'outtmpl': 'song.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title', 'Трек')

    vc.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print(f'Ошибка: {e}' if e else '🎵 Воспроизведение завершено'))

    await interaction.response.send_message(f"▶️ Сейчас играет: **{title}**")

bot.run(TOKEN)
