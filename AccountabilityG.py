import os
import discord
from discord.ext import tasks

client = discord.Client(intents=discord.Intents.all())


# Set the Discord API token
os.environ['DISCORD_TOKEN'] = ''

# Get the token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')


# Set the channel ID to count posts in
os.environ['CHANNEL_ID'] = '700160552437153835'

# Get the channel ID from the environment variable
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Set the thread name and message archive duration
THREAD_NAME = "Test Template for Accountability G (1)"
MESSAGE_ARCHIVE_DURATION = 1440  # 24 hours * 60 minutes


# Get the channel and thread objects for logging
channel = None
thread = None

# Event listener for when the bot is ready
@client.event
async def on_ready():
    global channel, thread
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(CHANNEL_ID)
    thread = discord.utils.get(await channel.threads(), name=THREAD_NAME)
    if thread is None:
        print(f"Thread '{THREAD_NAME}' not found. Please check the thread name.")
        return
    await thread.send("Accountability G now active, taking count of all users posts in the accountability channel")
    post_count_loop.start()

# Initialize the post counters for the channel and the thread
post_count_channel = {}
post_count_thread = {}

# Define a function to update the post counts for the channel and the thread separately
def update_post_count(message):
    global post_count_channel, post_count_thread
    if message.channel.id == CHANNEL_ID:
        if  '✅' in message.content:
            author_id = message.author.id
            if author_id not in post_count_channel:
                post_count_channel[author_id] = 0
            post_count_channel[author_id] += 1
    elif message.channel.id == thread.id:
        if  '✅' in message.content:
            author_id = message.author.id
            if author_id not in post_count_thread:
                post_count_thread[author_id] = 0
            post_count_thread[author_id] += 1

# Define a function to send the post counts for the channel and the thread separately
async def send_post_count():
    global post_count_channel, post_count_thread
    message_channel = "Weekly Checkup, Here are all the champs who kept up with their accountability:\n"
    for author_id, count in post_count_channel.items():
        user = client.get_user(author_id)
        message_channel += f"{user.name}: {count}\n"
    await channel.send(message_channel)
    post_count_channel = {}

    message_thread = "Weekly Checkup, Here are all the champs who kept up with their accountability:\n"
    for author_id, count in post_count_thread.items():
        user = client.get_user(author_id)
        message_thread += f"{user.name}: {count}\n"
    await thread.send(message_thread)
    post_count_thread = {}

# Schedule the send_post_count function to run every 7 days
@tasks.loop( hours = 168 )
async def post_count_loop():
    await send_post_count()

# Event listener for when a message is sent
@client.event
async def on_message(message):
    update_post_count(message)

# Run the bot
client.run(TOKEN)