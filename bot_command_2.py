from youtube_dl import YoutubeDL
import random, logging
from discord.utils import get
import discord
from discord.ext import commands
from token_2 import TOKEN


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
bot = commands.Bot(command_prefix='p!', intents=intents)
client = commands.Bot(command_prefix="?")

list_of_bad_words = [
    'лох',
    "чмо",
    "гей",
    "четрила"
    'nigger',
    'nigga',
    'негр',
    'naga',
    'ниггер',
    'нига',
    'нага',
    'faggot',
    'гомик'
    'хохол',
    'хач',
    'жид',
    'хиджаб',
    'даун',
    'аутист',
    'дебил',
    'retard',
    'virgin',
    'simp',
    'incel',
    'cимп',
    'cunt',
    'куколд'
]


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def user_mute(ctx, member: discord.Member):
    #mutedRole = discord.utils.get(ctx.guild.roles, name="mute")
    await member.remove_roles()
    await ctx.send(f'У {member.mention}, ограничение жизни наложено свыше')


#clear
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear( ctx, amount=100):
    await ctx.channel.purge(limit=amount + 1)


#kick
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'user {member.mention} больше не с нами')


#ban
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'user {member.mention} больше не с нами(навсегда)')


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help_command(ctx):
    emb = discord.Embed(title='Навигация по командам для администрации')
    emb.add_field(name='{}clear'.format('.'), value='Очистка чата')
    emb.add_field(name='{}ban @name'.format('.'), value='Бан пользователя')
    emb.add_field(name='{}kick @name'.format('.'), value='Бан пользователя')
    emb.add_field(name='{}mute @name'.format('.'), value='Замутать пользователя')

    await ctx.send(embed=emb)


@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    for i in msg.split():
        if i in list_of_bad_words:
            await message.delete()


@client.command(pass_context=True)
@commands.has_role('администратор')
async def mute(ctx, user: discord.Member):
    role = get(ctx.author.guild.roles, name="простой сметрный")
    await ctx.author.remove_roles(role)
    await ctx.send("{} has been muted from chat".format(user.name))


@client.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")


@client.command(brief="Plays a video, from a youtube URL")
async def play(ctx, url):
    await ctx.message.author.voice.channel.connect(reconnect=True)
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    print(voice)
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    voice.play(discord.FFmpegPCMAudio(executable="C:/Users/balab/PycharmProjects/discord/ffmpeg/ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
    voice.is_playing()



#bot.run(TOKEN)
client.run(TOKEN)