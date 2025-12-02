import discord
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from dotenv import load_dotenv
from pystray import Icon, MenuItem, Menu
from PIL import Image
from threading import Thread

load_dotenv()
# Using ENV files to make a layer of security
bot_token = os.getenv("bot_token")
GUILD_ID = int(os.getenv("guild_id"))
COMMANDS_CHANNEL = int(os.getenv("COMMANDS_CHANNEL"))
JOIN_LOG_CHANNEL_ID = int(os.getenv("JOIN_LOG_CHANNEL_ID"))
LEAVE_LOG_CHANNEL_ID = int(os.getenv("LEAVE_LOG_CHANNEL_ID"))
RULES_CHANNEL_ID = int(os.getenv("RULES_CHANNEL_ID"))
WARN_ROLE_ID = int(os.getenv("WARN_ROLE_ID"))
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))
MEMBER_ROLL_ID = int(os.getenv("MEMBER_ROLL_ID"))
ICON_PATH = os.getenv("ICON_PATH")

# Giving the bot discord permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/",intents=intents,case_insensitive=True)

"""                     Start of Command section                             """

# Command to send or replay using the bot
@bot.tree.command(name="send", description="Send a message in the same channel.")
@app_commands.describe(message="The message you want to send", message_id="put the message id you want to reply to")
async def send(interaction: discord.Interaction, message: str, message_id: str = None):
    await interaction.response.send_message("Sending the message now", ephemeral=True)
    
    if message_id:
        try:
            reference_msg = await interaction.channel.fetch_message(int(message_id))
            await interaction.channel.send(message, reference=reference_msg)
        except:
            await interaction.channel.send(message)
    else:
        await interaction.channel.send(message)
    embed = discord.Embed(
        title="Send command executed",
        description=f"Message sent: {message}",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Executed by {interaction.user.name}")
    embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
    log_channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)

# Command to annoy a user by moving him from the first voice channel to the last
@bot.tree.command(name="roller",description="Use and see.")
@app_commands.checks.cooldown(1, 10.0)
@app_commands.describe(member="chose a member")
async def roller(interaction: discord.Interaction,member: discord.Member):
    worked = False
    voice_channels = interaction.guild.voice_channels
    try:
        for channel in voice_channels:
            await member.move_to(channel)
            await asyncio.sleep(0.5)
            worked = True
    except Exception as e:
        await interaction.followup.send_message(f"Didn't work {e}",ephemeral=True)
        return
    if worked:
        await interaction.followup.send_message("roller done rolling",ephemeral=True)
        return

# Command to move a user to the AFK channel
@bot.tree.command(name="toafk", description="Move to AFK.")
@app_commands.describe(member="The member you want to move to AFK")
async def zbaleh(interaction: discord.Interaction, member: discord.Member):
    await member.move_to(interaction.guild.get_channel(1398436106176954379))
    await interaction.response.send_message(f"{member.mention} was moved to AFK channel")
    return

# Command to warn members
@bot.tree.command(name="warn", description="Warn a member in the server.")
@app_commands.describe(member="The member you want to warn")
async def warn(interaction: discord.Interaction, member: discord.Member):
    duration = timedelta(minutes=60)
    reason = f"Warned by {interaction.user.mention}"
    if interaction.user.roles and ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("بس يا ملقوف ما عندك صلاحيات للامر")
        return
    warn_role = interaction.guild.get_role(WARN_ROLE_ID)
    if warn_role is None:
        await interaction.response.send_message("❌ Warn role not found.", ephemeral=True)
        return
    if member.roles and warn_role in member.roles:
        await member.remove_roles(warn_role)
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f"✅ {member.mention} has been timed out for 1 hour.")
        return
    try:
        await member.add_roles(warn_role)
        await interaction.response.send_message(f"✅ {member.mention} has been warned.")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I do not have permission to warn this member.", ephemeral=True)

# To test the welcome message
@bot.tree.command(name="welcome_test",description="Test the welcome message.")
async def welcome_test(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"{interaction.user.name}",
        description=f"Hey {interaction.user.mention}, Welcome to the server!",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
    embed.add_field(name="━━━━⊱⊰━━━━", value=" ", inline=False)
    embed.add_field(name=f"➤ check out the rules here {interaction.guild.get_channel(RULES_CHANNEL_ID).mention}", value=" ", inline=False)
    embed.set_image(url="Example") # (width = 600,hight = 240, frame rate = 150)
    embed.set_footer(text=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await interaction.response.send_message(embed=embed)

# Command to send an embedded message about the server status
@bot.tree.command(name="status", description="Displays the server's current status")
async def status(interaction: discord.Interaction):
    guild = interaction.guild
    total_members = guild.member_count
    bot_count = sum(1 for member in guild.members if member.bot)
    human_count = total_members - bot_count

    embed = discord.Embed(
        title=f"📊 Server Status: {guild.name}",
        color=discord.Color.dark_gray()
    )
    embed.add_field(name="👥 Total Members", value=total_members, inline=True)
    embed.add_field(name="🤖 Bots", value=bot_count, inline=True)
    embed.add_field(name="🧑 Humans", value=human_count, inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.set_footer(text=f"Requested by {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

# Command to display a user avatar
@bot.tree.command(name="avatar", description="Fetch and display the avatar of a specified server member.")
@app_commands.describe(member="The member whose avatar you want to view")
async def avatar(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(
        title=f"{member.name}'s avatar"
    )
    embed.set_image(url=member.avatar.url)
    embed.set_footer(text=f"Requested by {interaction.user.name}")

    await interaction.response.send_message(embed=embed)

# command to fast convert currency
@bot.tree.command(name="convert", description="Let you convert a currency to Saudi Riyals.")
@app_commands.describe(amount="The amount to convert", currency="The currency to convert from")
async def convert(interaction: discord.Interaction, amount: float, currency: str):
    if currency == "USD":
        SAR = 3.75 * amount
    elif currency == "ARS":
        SAR = 335.45 * amount
    else:
        await interaction.response.send_message("❌ Unsupported currency.")
        return

    await interaction.response.send_message(f"{amount} {currency} = {SAR:.2f} SAR")

#Command to easily move all voice channel members to another channel
@bot.tree.command(name="move", description="Move all member from your current voice channel to another chosen one.")
@app_commands.describe(channel="the channel you want to move all members to")
async def move(interaction: discord.Interaction, channel: discord.VoiceChannel):
    if interaction.user.id != 542041823812648982:
        await interaction.response.send_message("You don't have permissions to use this command", ephemeral=True)
        return
        
    user = interaction.user
    if not user.voice or not user.voice.channel:
        await interaction.response.send_message("You are not in a voice channel.", ephemeral=True)
        return

    source_channel = user.voice.channel
    moved_members = []
    
    for member in source_channel.members:
        try:
            await member.move_to(channel)
            moved_members.append(member.display_name)
        except Exception as e:
            print(f"Could not move {member.display_name}: {e}")

    await interaction.response.send_message(f"Moved {len(moved_members)} members to **{channel}**.")

@bot.tree.command(name="banner",description="Fetch and display the banner of a specified server member.")
@app_commands.describe(member="The member whose banner you want to view")
async def banner(interaction:discord.Interaction,member: discord.Member):
    user = await bot.fetch_user(member.id)
    if user.banner is None:
        await interaction.response.send_message(
            f"{member.name} has no banner set.",
            ephemeral=True
        )
        return
    embed = discord.Embed(
        title=f"{member.name}'s banner"
    )
    embed.set_image(url=user.banner.url)
    embed.set_footer(text=f"Requested by {interaction.user.name}")
    await interaction.response.send_message(embed=embed)

"""                     End of Command section                             """


"""                     Start of Log/events section                             """

@bot.event
async def on_member_join(member):
    if member.bot:
        return
    role = member.guild.get_role(MEMBER_ROLL_ID)
    if role and role not in member.roles:
        await member.add_roles(role)
    embed = discord.Embed(
        title="Welcome!",
        description=f"Hey {member.mention}, welcome to the server",
        color=discord.Color.green()
            )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text="We're glad to have you here!")
    channel = bot.get_channel(JOIN_LOG_CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_ready():
    channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    print(f" Logged in as {bot.user}")
    embed = discord.Embed(
        title="Bot Started",
        description=f"{bot.user} is now online and operational.",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    await bot.change_presence(activity=discord.Activity(name="Monitoring"))
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="🚪 Member Left",
            description=f"{member.mention} has left the server.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"User ID: {member.id}")
        await log_channel.send(embed=embed)

@bot.event
async def on_member_ban(guild,user):
    channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    embed = discord.Embed(
        title="Member Banned",
        description=f"{user.mention} has been banned from the server.",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    guild = bot.get_guild(GUILD_ID)
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_ban):
            embed.add_field(
                name="Banned By",
                value=f"{entry.user.mention} (`{entry.user.id}`)",
                inline=False
            )
            break
    except discord.Forbidden:
        embed.add_field(
            name="Banned By",
            value="Unable to fetch audit logs (missing permission)",
            inline=False
        )
    await channel.send(embed=embed)

@bot.event
async def on_member_unban(guild, user):
    channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    embed = discord.Embed(
        title="Member Unbanned",
        description=f"{user.mention} has been unbanned from the server.",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_unban):
            embed.add_field(
                name="Unbanned By",
                value=f"{entry.user.mention} (`{entry.user.id}`)",
                inline=False
            )
            break
    except discord.Forbidden:
        embed.add_field(
            name="Unbanned By",
            value="Unable to fetch audit logs (missing permission)",
            inline=False
        )
    await channel.send(embed=embed)

@bot.event
async def on_soundboard_sound_delete(sound):
    channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    embed = discord.Embed(
        title="Sound deleted ",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name=f" ",value=f'{sound.name} {sound.emoji}',inline=True)
    guild = bot.get_guild(GUILD_ID)
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.soundboard_sound_delete):
                embed.add_field(
                    name="Deleted By",
                    value=f"{entry.user.mention} (`{entry.user.id}`)",
                    inline=False
                    )
                break
    except discord.Forbidden:
        embed.add_field(
            name="Deleted By",
            value="Unable to fetch audit logs (missing permission)",
            inline=False
        )
    await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    embed = discord.Embed(
        title=f"{message.author.mention} Message was Deleted",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Content", value=message.content, inline=False)
    embed.add_field(name="Channel", value=message.channel.mention, inline=False)
    if message.embeds:
        msg_type = "Embed"
    elif message.stickers:
        msg_type = "Sticker"
    elif message.attachments:
        msg_type = "Attachment"
    elif message.content:
        msg_type = "Text"
    else:
        msg_type = "Unknown"
    embed.add_field(name="Message type", value=msg_type, inline=False)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
    guild = bot.get_guild(GUILD_ID)
    await asyncio.sleep(1)
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                if entry.target == message.author:
                    embed.add_field(name="Deleted By", value=f"{entry.user.mention} (`{entry.user.id}`)", inline=False)
                break
    except discord.Forbidden:
        embed.add_field(name="Deleted By", value="Unable to fetch audit logs (missing permission)", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_bulk_message_delete(messages):
    guild = messages[0].guild
    channel = messages[0].channel
    log_channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)

    embed = discord.Embed(
        title="Bulk Messages Deleted",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    await asyncio.sleep(1)
    try:
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.message_bulk_delete):
            if entry.target == channel and (datetime.utcnow() - entry.created_at).total_seconds() < 10:
                if entry.user:
                    embed.set_author(
                        name=entry.user.name,
                        icon_url=entry.user.display_avatar.url
                    )
                    embed.add_field(
                        name="Deleted By",
                        value=f"{entry.user.mention} (`{entry.user.id}`)",
                        inline=False
                    )
                else:
                    embed.set_author(
                        name="Unknown",
                        icon_url="https://cdn.discordapp.com/embed/avatars/0.png"
                    )
                    embed.add_field(name="Deleted By", value="Unknown", inline=False)
                break
    except discord.Forbidden:
        embed.add_field(
            name="Deleted By",
            value="Unable to fetch audit logs (missing permission)",
            inline=False
        )

    embed.add_field(name="Channel", value=channel.mention, inline=False)
    embed.add_field(name="Number of Messages", value=len(messages), inline=False)

    await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before,after):
    if before.author.bot:
        return
    if before.content == after.content:
        return
    channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    embed = discord.Embed(
            title="Message Edited",
            color=discord.Color.dark_grey(),
            timestamp=datetime.now())
    embed.add_field(name="Before", value=before.content, inline=False)
    embed.add_field(name="After", value=after.content, inline=False)
    embed.set_author(name=before.author.name, icon_url=before.author.avatar.url if before.author.avatar else before.author.default_avatar.url)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id == LEAVE_LOG_CHANNEL_ID:
        await message.delete()
        return

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    
    if before.channel != after.channel:
        embed = discord.Embed(
        title="Member moved",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
        if member.id == 542041823812648982 and after.channel.id == 1414602727828492289:
            await member.move_to(before.channel)
        embed.add_field(name="Member Moved", value=f"{member.mention} moved from {before.channel.name} to {after.channel.name}", inline=False)
        guild = member.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_move):
                embed.add_field(name="Moved By", value=f"{entry.user.mention} (`{entry.user.id}`)", inline=False)
                break
        await log_channel.send(embed=embed)

    elif before.channel is not None and after.channel is None:
        channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
        embed = discord.Embed(
            title="Member disconnected from Voice Channel",
            description=f"{member.mention} has been disconnected from the voice channel.",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        guild = member.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_disconnect):
            if entry.target.id == member.id:
                embed.add_field(
                    name="Disconnected By",
                    value=f"{entry.user.mention} (`{entry.user.id}`)",
                    inline=False
                )
                break
        await channel.send(embed=embed)

    elif before.mute != after.mute:
        embed = discord.Embed(
        title="Voice State Update",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
        if after.mute:
        
            embed.add_field(
            name="Server Mute",
            value=f"{member.mention} was muted by the server",
            inline=False
        )
        else:
            embed.add_field(
            name="Server Unmute",
            value=f"{member.mention} was unmuted by the server",
            inline=False
        )

        guild = member.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
            if entry.target and entry.target.id == member.id:
                embed.add_field(
                name="Action By",
                value=f"{entry.user.mention} (`{entry.user.id}`)",
                inline=False
            )
            await log_channel.send(embed=embed)
            break

    elif before.deaf != after.deaf:
        embed = discord.Embed(
        title="Voice State Update",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
        if after.deaf:
            embed.add_field(
            name="Server Deaf",
            value=f"{member.mention} was deafened by the server",
            inline=False
        )
        else:
            embed.add_field(
            name="Server Undeaf",
            value=f"{member.mention} was undeafened by the server",
            inline=False
        )
    
        guild = member.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
            if entry.target and entry.target.id == member.id:
                embed.add_field(
                name="Action By",
                value=f"{entry.user.mention} (`{entry.user.id}`)",
                inline=False
            )
            await log_channel.send(embed=embed)
            break

"""                     End of Log/events section                             """

# To start the bot
def run_bot():
    bot.run(bot_token)


# Using Thread to give the bot an icon and adding it to System tray arrow in the task bar
Thread(target=run_bot,daemon=True).start()
image = Image.open(ICON_PATH)
menu = Menu(MenuItem("Exit",lambda icon, item: icon.stop()))
icon = Icon("Bot", image, "Bot", menu)
icon.run()

''' elif before.channel and not after.channel:
        embed.add_field(name="Member Left", value=f"{member.mention} left {before.channel.name}", inline=False)

    elif not before.channel and after.channel:
        embed.add_field(name="Member Joined", value=f"{member.mention} joined {after.channel.name}", inline=False)
            

    elif before.self_mute != after.self_mute:
        if after.self_mute:
            embed.add_field(name="Self Mute", value=f"{member.mention} muted themselves", inline=False)
        else:
            embed.add_field(name="Self Unmute", value=f"{member.mention} unmuted themselves", inline=False)

    elif before.self_deaf != after.self_deaf:
        if after.self_deaf:
            embed.add_field(name="Self Deaf", value=f"{member.mention} deafened themselves", inline=False)
        else:
            embed.add_field(name="Self Undeaf", value=f"{member.mention} undeafened themselves", inline=False)

    elif before.self_stream != after.self_stream:
        if after.self_stream:
            embed.add_field(name="Stream Started", value=f"{member.mention} started streaming", inline=False)
        else:
            embed.add_field(name="Stream Stopped", value=f"{member.mention} stopped streaming", inline=False)

    elif before.self_video != after.self_video:
        if after.self_video:
            embed.add_field(name="Camera On", value=f"{member.mention} turned on their camera", inline=False)
        else:
            embed.add_field(name="Camera Off", value=f"{member.mention} turned off their camera", inline=False)'''