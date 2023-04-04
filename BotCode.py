import os
import discord
from discord.ext import tasks

client = discord.Client(intents=discord.Intents.all())



os.environ['DISCORD_TOKEN'] = 
TOKEN = os.getenv('DISCORD_TOKEN')


os.environ['CHANNEL_ID'] = 

# Set the channel ID to count posts in
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Initialize the post counter
post_count = {}

# Define a function to update the post count
def update_post_count(message):
    global post_count
    if message.channel.id == CHANNEL_ID:
        author_id = message.author.id
        if author_id not in post_count:
            post_count[author_id] = 0
        post_count[author_id] += 1

# Define a function to send the post count message
async def send_post_count():
    global post_count
    message = "Post counts in the last 3 minutes:\n"
    for author_id, count in post_count.items():
        user = client.get_user(author_id)
        message += f"{user.name}: {count}\n"
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)
    post_count = {}

# Schedule the send_post_count function to run every 3 minutes
@tasks.loop(minutes=3)
async def post_count_loop():
    await send_post_count()

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    post_count_loop.start()

# Event listener for when a message is sent
@client.event
async def on_message(message):
    update_post_count(message)

# Run the bot
client.run(TOKEN)
