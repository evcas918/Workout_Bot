import discord
from discord.ext import commands

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable this to read message content in guilds

# Initialize the bot with the correct prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory storage for workout logs
workout_logs = {}

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

# Command: Log a workout
@bot.command()
async def log(ctx, muscle: str = None, duration: int = None):
    print(f"Received command: {ctx.message.content}")
    if muscle is None or duration is None:
        await ctx.send("Please specify the muscle group and duration. Example: `!log chest 30`")
        return

    user = ctx.author.name
    if user not in workout_logs:
        workout_logs[user] = []
    workout_logs[user].append((muscle, duration))
    total_duration = sum(d for _, d in workout_logs[user])
    await ctx.send(f'{user} logged {muscle} workout for {duration} minutes! Total time: {total_duration} minutes.')

# Command: Display the leaderboard
@bot.command()
async def leaderboard(ctx):
    leaderboard = sorted(workout_logs.items(), key=lambda x: sum(d for _, d in x[1]), reverse=True)
    message = "**Leaderboard**\n"
    for rank, (user, logs) in enumerate(leaderboard, 1):
        total_time = sum(d for _, d in logs)
        message += f'{rank}. {user} - {total_time} minutes\n'
    await ctx.send(message)

# Run the bot
bot.run('DISCORD_BOT_TOKEN')