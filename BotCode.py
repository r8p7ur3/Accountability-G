import os
import discord
from discord.ext import tasks

client = discord.Client(intents=discord.Intents.all())

# Set the Discord API token
os.environ['DISCORD_TOKEN'] = ''

# Get the token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Set the channel IDs to count posts in
os.environ['CHANNEL_ID'] = '1107301390784663592' #gmt-3 progress
os.environ['CHANNEL_ID_2'] = '1107301968365490329' #gmt-2 progress
os.environ['CHANNEL_ID_3'] = '1107302033284943934' #gmt-5-6 progress

# Get the channel IDs from the environment variables
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
CHANNEL_ID_2 = int(os.getenv('CHANNEL_ID_2'))
CHANNEL_ID_3 = int(os.getenv('CHANNEL_ID_3'))

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
    await thread.send("Accountability G is now active, taking account of all users who posts accountability. Please only use the ✅ emoji when posting accountability (ONLY USE ✅ EMOJI ONCE A DAY) ")
    post_count_daily.start()
    post_count_weekly.start()

# Initialize the post counters for the channels and the thread
post_count_channel = {
    'channel_1': {},
    'channel_2': {},
    'channel_3': {}
}
post_count_thread = {}

# Define a function to update the post counts for the channels and the thread separately
def update_post_count(message, channel_id):
    global post_count_channel, post_count_thread
    if message.channel.id == channel_id:
        if '✅' in message.content:
            author_id = message.author.id
            if author_id not in post_count_channel[channel_id]:
                post_count_channel[channel_id][author_id] = 0
            post_count_channel[channel_id][author_id] += 1
    elif message.channel.id == thread.id:
        if '✅' in message.content:
            author_id = message.author.id
            if author_id not in post_count_thread:
                post_count_thread[author_id] = 0
            post_count_thread[author_id] += 1

# Define a function to send the daily post with the post counts for each channel
async def send_daily_post():
    global post_count_channel, post_count_thread
    message_channel_1 = "Daily Accountability Checkup - GMT 3:\n"
    for author_id, count in post_count_channel['channel_1'].items():
        user = client.get_user(author_id)
        message_channel_1 += f"{user.name}: {count}\n"
    await channel.send(message_channel_1)
    post_count_channel['channel_1'] = {}

    message_channel_2 = "Daily Accountability Checkup - GMT 2:\n"
    for author_id, count in post_count_channel['channel_2'].items():
        user = client.get_user(author_id)
        message_channel_2 += f"{user.name}: {count}\n"
    await channel.send(message_channel_2)
    post_count_channel['channel_2'] = {}

    message_channel_3 = "Daily Accountability Checkup - GMT 5-6:\n"
    for author_id, count in post_count_channel['channel_3'].items():
        user = client.get_user(author_id)
        message_channel_3 += f"{user.name}: {count}\n"
    await channel.send(message_channel_3)
    post_count_channel['channel_3'] = {}

# Define a function to send the weekly post with the post counts for each channel
async def send_weekly_post():
    global post_count_channel, post_count_thread
    message_channel_1 = "Weekly Accountability Checkup - GMT 3:\n"
    for author_id, count in post_count_channel['channel_1'].items():
        user = client.get_user(author_id)
        message_channel_1 += f"{user.name}: {count}\n"
    await channel.send(message_channel_1)
    post_count_channel['channel_1'] = {}

    message_channel_2 = "Weekly Accountability Checkup- GMT 2:\n"
    for author_id, count in post_count_channel['channel_2'].items():
        user = client.get_user(author_id)
        message_channel_2 += f"{user.name}: {count}\n"
    await channel.send(message_channel_2)
    post_count_channel['channel_2'] = {}

    message_channel_3 = "Weekly Accountability Checkup- GMT 5-6:\n"
    for author_id, count in post_count_channel['channel_3'].items():
        user = client.get_user(author_id)
        message_channel_3 += f"{user.name}: {count}\n"
    await channel.send(message_channel_3)
    post_count_channel['channel_3'] = {}

    message_thread = "Weekly Checkup - Thread:\n"
    for author_id, count in post_count_thread.items():
        user = client.get_user(author_id)
        message_thread += f"{user.name}: {count}\n"
    await thread.send(message_thread)
    post_count_thread = {}

# Schedule the send_daily_post function to run every 24 hours
@tasks.loop(hours=24)
async def post_count_daily():
    await send_daily_post()

# Schedule the send_weekly_post function to run every 7 days
@tasks.loop(hours=168)
async def post_count_weekly():
    await send_weekly_post()

# Event listener for when a message is sent
@client.event
async def on_message(message):
    update_post_count(message, CHANNEL_ID)
    update_post_count(message, CHANNEL_ID_2)
    update_post_count(message, CHANNEL_ID_3)

# Run the bot
client.run(TOKEN)
