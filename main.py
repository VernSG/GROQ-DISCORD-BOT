import discord
from discord.ext import commands
import os
import random
import asyncio
from groq import AsyncGroq

# Inisialisasi intents Discord
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

# Token bot Discord
BOT_TOKEN = 'BOT TOKEN KALIAN'

# Inisialisasi bot Discord
bot = commands.Bot(command_prefix='!', intents=intents)

# Ambil GROQ_API_KEY dari environment variable
groq_api_key = 'GROQ_API KALIAN'

# Inisialisasi client Groq async dengan API key
client = AsyncGroq(api_key=groq_api_key)

# Daftar pesan untuk auto-reply (dalam bahasa Indonesia)
auto_replies = [
    "Hai beb!", "Manggil aja, udah belajar belom?", "Kenapa nichh?",
    "Ada masalah kawan?", "Hai aku disini aja kok!", "Ya?", "Apa kabar?",
    "Ada yang bisa dibantu?", "Senang melihatmu!", "Butuh bantuan?",
    "Halo! Ada yang bisa aku lakukan?", "Bagaimana harimu?",
    "Apa yang sedang kamu kerjakan?", "Ada yang menarik?",
    "Hai! Ada kabar apa?", "Butuh bantuan belajar?", "Ada yang ingin dibahas?",
    "Halo! Apa kabar?", "Selamat datang!", "Hai! Semoga harimu menyenangkan!"
]

# Channel ID tempat bot akan otomatis menjawab
allowed_channel_id = 1256208812105400442  # Ganti dengan ID channel yang diizinkan

# Channel ID for announcements
announcement_channel_id = 1258044623805480970  # Ganti dengan ID channel announcement

# Channel mention
channel_mention = f'<#{announcement_channel_id}>'

# Function to send new post announcements
async def send_new_post_announcement(channel, title, description, author):
    embed = discord.Embed(title="Post Baru di Forum", description="Hai! Akademikus ada post baru nih teman teman.", color=discord.Color.blue())
    embed.add_field(name="Judul Post", value=title, inline=False)
    embed.add_field(name="Deskripsi Post", value=description, inline=False)
    embed.add_field(name="Author", value=author, inline=False)
    embed.add_field(name="Status", value="Sedang Aktif😏", inline=False)
    embed.add_field(name="Tags", value="Article", inline=False)
    # If you have an image URL, set it here
    embed.set_image(url="https://res.cloudinary.com/djsdnb4td/image/upload/v1720010920/images_mixsv3.jpg")  # Ganti dengan URL gambar yang sesuai
    
    await channel.send(embed=embed)

# Command to announce a new post
@bot.command(name='newpost')
async def new_post(ctx, title: str, description: str, author: str):
    channel = bot.get_channel(announcement_channel_id)
    if channel:
        await send_new_post_announcement(channel, title, description, author)
        await ctx.send(f"New post announcement sent to {channel_mention}")
    else:
        await ctx.send("Announcement channel not found.")

# Event handler untuk bot siap
@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name='Jangan Lupa Sholat'))

    # Event handler untuk pesan baru
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        # Cek apakah pesan masuk dari channel yang diizinkan
        if message.channel.id == allowed_channel_id:
            try:
                chat_completion = await client.chat.completions.create(
                    messages=[{
                        "role": "system",
                        "content": "you are a helpful assistant."
                    }, {
                        "role": "user",
                        "content": message.content
                    }],
                    model="llama3-8b-8192",
                    temperature=0.5,
                    max_tokens=1024,
                    top_p=1,
                    stop=None,
                    stream=False)

                response_content = chat_completion.choices[0].message.content

                # Check if response_content exceeds Discord's message length limit
                if len(response_content) > 2000:
                    response_content = response_content[:1997] + "..."  # Truncate to fit within limit

                await asyncio.sleep(2)  # Delay selama 2 detik sebelum mengirim balasan
                await message.channel.send(response_content)

            except Exception as e:
                print(f"Error processing Groq API: {e}")
                await message.channel.send("Oops! Something went wrong while processing your request.")

        else:
            # Jika pesan masuk dari channel lain, bot perlu di-mention untuk merespons
            if bot.user.mentioned_in(message):
                reply = random.choice(auto_replies)
                await asyncio.sleep(2)  # Delay selama 2 detik sebelum mengirim balasan
                await message.channel.send(reply)

        await bot.process_commands(message)


@bot.command(name='say')
async def say(ctx, *, text):
    # Sends the user's input message to the channel where the message was received
    await ctx.send(text)
# Menjalankan bot dengan token bot Discord Anda 
bot.run(BOT_TOKEN)