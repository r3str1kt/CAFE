import discord
from discord.ext import commands, tasks
import os
import random
import logging
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=discord.Intents.all(), command_prefix = "$", description = "Watching ð˜¾ð˜¼ð™ð™€ ð˜¾ð™ð™Žð™ð™Šð™ˆð™€ð™ð™Ž")

@client.event
async def on_ready():
 print('We have logged in as {0.user}'.format(client))


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="New members"))
  #activity can be change to watching, streaming, idle, dnd and name="new members can be renamed!"
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
	    guild = client.get_guild(937280745737715742) #serverid
	    welcome_channel = guild.get_channel(937282799206031381) #channel id
	    embed= discord.Embed(title=f'**Welcome to {guild.name}.**', description=f" **Thank you  {member.mention} for joining** **{member.guild.name}!**  **Do take Roles from** <#937282792998449193> **,** <#937604561852567632> **&** <#1029394825079959563> . **Hope you have a good time here!**", color = discord.Colour.teal())
    #change the values <#937282792998449193> <#937604561852567632> with the channel_id of your server. 
	    embed.set_image(url='https://media.discordapp.net/attachments/1034370053208035338/1034370176449265714/ezgif.com-gif-maker.gif')
	    embed.set_thumbnail(url=member.avatar.url)
    # if you want can uncomment the above line (19)
	    embed.set_footer(text=f"{member.name} / {member.guild.name}", icon_url = member.avatar.url)
	    await welcome_channel.send(embed=embed)



#in url="" add url of the image or gif for example welcoming image or gif line(18)
# To add emote <:emote_name:emote_id> 
# Like this <:cute_shy:855711538610700289> 
# To mention channel <#channel_id>
# Like this <#834093087336693802> 
# To add animated emote <a:emote_name:emote_id> 
# Like this <a:mochi_dance:875026913922547712>


@client.command(aliases=['p'], name='ping', help='Returns the Latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(aliases=['c'], help='To clear messages')
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
  await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'], help='Kicks the mentioned user')
@commands.has_permissions(kick_members = True)
async def kick(ctx,member: discord.Member,*,reason="No reason provided"):
	await member.send(member.name +" have been kicked from the server, Because : "+reason)
	await ctx.send(member.name +" has been kicked from the server, Because : "+reason)
	await member.kick(reason=reason)

@client.command(aliases=['b'], help='Bans the mentioned user')
@commands.has_permissions(ban_members = True)
async def ban(ctx,member: discord.Member,*,reason):
	await member.send(member.name + " have been banned from the server, Because : "+reason)
	await ctx.send(member.name + " has been banned from server, Because : "+reason)
	await member.ban(reason=reason)

@client.command(aliases=['ub'], help='Unbans the mentioned user')
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
	banned_users = await ctx.guild.bans()
	member_name, member_disc = member.split('#')
	for banned_entry in banned_users:
		user = banned_entry.user
		if(user.name, user.discriminator)==(member_name,member_disc):
			await ctx.guild.unban(user)
			await ctx.send(member_name + " has been unbanned!")
			return
	await ctx.send(member + " was not found ")		

@client.command(aliases=['m'], description="Mutes the specified user.", help = 'Mutes the mentioned user')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=True)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@client.command(aliases=['um'], description="Unmutes a specified user.", help = 'Unmutes the mentioned user')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

@client.command(aliases=['i'], help='Gives user info')
async def userinfo(ctx, *, member: discord.Member):
    if member is None:
        member = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=000000, description=member.mention)
    embed.set_author(name=str(member), icon_url=member.avatar.url)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Joined", value=member.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(member)+1))
    embed.add_field(name="Registered", value=member.created_at.strftime(date_format))
    if len(member.roles) > 1:
        role_string = ' '.join([r.mention for r in member.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(member.id))
    return await ctx.send(embed=embed)

keep_alive()
token = os.environ.get("BOT_TOKEN")
# add in secrets with key = BOT_TOKEN & value = YOUR TOKEN ID
# D'ont add inverted commas just add the token :)
client.run(token)
