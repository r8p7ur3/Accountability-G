import os
import discord
from discord.ext import tasks

client = discord.Client(intents=discord.Intents.all())


os.environ['DISCORD_TOKEN'] = 'CC'
TOKEN = os.getenv('DISCORD_TOKEN')

# TRIBE threads
os.environ['THREAD_ID'] = "TRIBE"
THREAD_ID = int(os.getenv('THREAD_ID'))

# Initialize the post counter
post_count = {}

# Define a function to update the post count
def update_post_count(message):
    global post_count
    if message.channel.id == THREAD_ID and message.author != client.user:
        content = message.content.lower()
        if 'a' in content or '✅' in content:
            author_id = message.author.id
            if author_id not in post_count:
                post_count[author_id] = 0
            post_count[author_id] += 1

# Define a function to send the post count message
async def send_post_count():
    global post_count
    message = "Post count for users who posted messages containing the letter 'a' or the ✅ emoji within the last 360 minutes\n"
    for author_id, count in post_count.items():
        user = client.get_user(author_id)
        message += f"{user.name}: {count}\n"
    thread = client.get_channel(THREAD_ID)
    await thread.send(message)
    post_count = {}

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    thread = client.get_channel(THREAD_ID)
    await thread.send('I am online now. Taking logs of users and posts that have the letter \'a\' as well as the emoji :white_check_mark:')
    post_count_loop.start()

# Event listener for when a message is sent
@client.event
async def on_message(message):
    update_post_count(message)

# Schedule the send_post_count function to run every 6 hours
@tasks.loop(minutes=360)
async def post_count_loop():
    await send_post_count()

# Run the bot
client.run(TOKEN)
