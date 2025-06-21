import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

STAFF_CAN_MENTION = {
    "QuickDrops": 1381710625142735111,
    "Giveaways": 1381710624630898749, 
}

STAFF_ROLE_ID = 1381708265573842954 

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Sync error: {e}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Slash Mention (/mention) Command.
@bot.tree.command(name="mention", description="Mention a specific role with a custom message")
@app_commands.describe(role="Role to mention", message="The message to send")
async def mention(interaction: discord.Interaction, role: str, message: str):
    # Check if user has Staff role
    staff_role = discord.utils.get(interaction.user.roles, id=STAFF_ROLE_ID)
    if not staff_role and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("🚫 You don't have permission to use this command.", ephemeral=True)
        return

    # Normalize role key
    role_key = role.lower()
    if role_key not in STAFF_CAN_MENTION:
        await interaction.response.send_message("❌ You can only mention 'quickdrops' or 'giveaways' roles.", ephemeral=True)
        return

    role_id = STAFF_CAN_MENTION[role_key]
    role_obj = interaction.guild.get_role(role_id)
    if role_obj is None:
        await interaction.response.send_message("⚠️ That role doesn't exist in this server.", ephemeral=True)
        return

    # Format message with line breaks
    formatted_message = message.replace("\\n", "\n")

    # Defer response to hide original "User used a command" bubble
    await interaction.response.defer(ephemeral=True)

    # Send message in the same channel anonymously
    await interaction.channel.send(f"{role_obj.mention}\n{formatted_message}")

bot.run('MTM4NjAwNjIzNzk3MTQ4MDU4Ng.Go7X_Y.2NXSWmm7yZ2JuckBjOVZJPn9dKUogHyHkV9evg')
