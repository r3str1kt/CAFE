# discord py libraries 

import asyncio
import discord
import os
from discord.ext import commands
from keep_alive import keep_alive

command_prefix="!"

# bot intents

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=discord.Intents.all(), command_prefix="!",description="S1mple Moderation Bot")

# bot events


@client.event
async def on_ready():
  print("client running with:")
  print("Username: ", client.user.name)
  await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.playing, name=f"{command_prefix}help | Moderating Over Server"))
  
# client commands
# help command
# moderation commands
# vc commands
# confess command
  

@client.command(aliases=['j'], help='Joins the vc')
async def join(ctx):
  channel = ctx.author.voice.channel
  await channel.connect()

@client.command(aliases=['l'], help='Leaves the vc')
async def leave(ctx):
  await ctx.voice_client.disconnect()

@client.command(aliases=['p'], name='ping', help='Returns the Latency')
async def ping(ctx):
  await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(aliases=['c'], help='To clear messages')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
  await ctx.channel.purge(limit=amount)
  await ctx.send(f"Purged : `{amount} messages`", delete_after= 10)

@client.command(aliases=['k'], help='Kicks the mentioned user')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
  await member.send(member.name +" have been kicked from the server, Because : " + reason)
  await ctx.send(member.name + " has been kicked from the server, Because : " +reason)
  await member.kick(reason=reason)

@client.command(aliases=['b'], help='Bans the mentioned user')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason):
  await member.send(member.name +" have been banned from the server, Because : " + reason)
  await ctx.send(member.name + " has been banned from server, Because : " +reason)
  await member.ban(reason=reason)

@client.command(aliases=['ub'], help='Unbans the mentioned user')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_disc = member.split('#')
  for banned_entry in banned_users:
    user = banned_entry.user
    if (user.name, user.discriminator) == (member_name, member_disc):
      await ctx.guild.unban(user)
      await ctx.send(member_name + " has been unbanned!")
      return
  await ctx.send(member + " was not found ")


@client.command(aliases=['m'], description="Mutes the specified user.",help='Mutes the mentioned user')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")
  if not mutedRole:
    mutedRole = await guild.create_role(name="Muted")
    for channel in guild.channels:
      await channel.set_permissions(mutedRole,speak=False,send_messages=False,read_message_history=False,read_messages=True)
  await member.add_roles(mutedRole, reason=reason)
  await ctx.send(f"Muted {member.mention} for reason {reason}")
  await member.send(f"You were muted in the server {guild.name} for {reason}")

@client.command(aliases=['um'], description="Unmutes a specified user.", help='Unmutes the mentioned user')
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
  embed.add_field(name="Join position", value=str(members.index(member) + 1))
  embed.add_field(name="Registered",value=member.created_at.strftime(date_format))
  if len(member.roles) > 1:
    role_string = ' '.join([r.mention for r in member.roles][1:])
    embed.add_field(name="Roles [{}]".format(len(member.roles) - 1), value=role_string, inline=False) 
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions
    if p[1]])
  embed.add_field(name="Guild permissions", value=perm_string, inline=False)
  embed.set_footer(text='ID: ' + str(member.id))
  return await ctx.send(embed=embed, delete_after= 10)


@client.command(aliases=['av'], help="Gives user's avatar")
async def avatar(ctx, *, avamember: discord.Member = None):
  if avamember == None:
    usavrl = ctx.author.avatar.url
    embed = discord.Embed(title=('{}\'s Avatar'.format(ctx.author.name)), colour=discord.Colour.random())
    embed.set_image(url='{}'.format(usavrl))
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.reply(embed=embed, mention_author=True, delete_after= 10)
  else:
    userAvatarUrl = avamember.avatar.url
    embed = discord.Embed(title=('{}\'s Avatar'.format(avamember.name)), colour=discord.Colour.random())
    embed.set_image(url='{}'.format(userAvatarUrl))
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.reply(embed=embed, mention_author=True, delete_after= 10)


snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await asyncio.sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@client.command(name = 'snipe')
async def snipe(ctx):
  channel = ctx.channel
  try: 
    em = discord.Embed(title= f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id], colour = discord.Colour.random())
    em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
    await ctx.send(embed = em)
  except KeyError: 
    await ctx.send(f"There are no recently deleted messages in #{channel.name}")

keep_alive()
token = os.environ.get("BOT_TOKEN")
client.run(token)
