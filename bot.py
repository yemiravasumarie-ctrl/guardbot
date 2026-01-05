import discord
from discord.ext import commands
import time

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# SPAM AYARLARI
MESSAGE_LIMIT = 5      # neçə mesaj
TIME_WINDOW = 7        # neçə saniyədə
user_messages = {}

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    now = time.time()
    user_id = message.author.id

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(now)

    # köhnə mesajları sil
    user_messages[user_id] = [
        t for t in user_messages[user_id]
        if now - t <= TIME_WINDOW
    ]

    # SPAM TUTULDU
    if len(user_messages[user_id]) > MESSAGE_LIMIT:
        try:
            await message.delete()
            await message.channel.send(
                f"⚠️ {message.author.mention} spam etmə!",
                delete_after=5
            )
        except:
            pass
        return

    await bot.process_commands(message)

bot.run("YOUR_TOKEN_HERE")
