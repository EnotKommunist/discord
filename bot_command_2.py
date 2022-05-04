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
bot = commands.Bot(command_prefix='?', intents=intents)
client = commands.Bot(command_prefix='p!')

list_of_bad_words = [
    'лох',
    "чмо",
    "гей",
    "четрила"
    'nigger',
    'nigga',
    'niger',
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


#unban
@client.command(name='unban')
@commands.has_permissions(administrator=True)
async def _unban(ctx, *, user_id: int):
    """Разбанить участника"""
    await ctx.message.delete()
    try:
        user = await client.fetch_user(user_id=user_id)
        await ctx.guild.unban(user)
        await ctx.send(f'Участник с ID {user_id} успешно разбанен.')
    except discord.DiscordException:
        await ctx.send(f'Участник с ID {user_id} не забанен, поэтому не может быть разбанен.')


#avatar
@client.command()
async def avatar(ctx, member : discord.Member = None):
    user = ctx.message.author if (member == None) else member
    embed = discord.Embed(title=f'Аватар пользователя {user}', color= 0x0c0c0c)
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def userinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Имя дискорда: {Member.name}\n\n"
		    f"Никнейм на сервере: {Member.nick}\n\n"
		    f"Статус: {Member.status}\n\n"
		    f"ID: {Member.id}\n\n"
		    f"Игрок присоединился к серверу: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
		    f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}",
		    color=0xff0000, timestamp=ctx.message.created_at)
    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help_command_admin(ctx):
    emb = discord.Embed(title='Навигация по командам для администрации')
    emb.add_field(name='{}clear'.format('p!'), value='Очистка чата')
    emb.add_field(name='{}ban @name'.format('p!'), value='Бан пользователя')
    emb.add_field(name='{}unban @name'.format('p!'), value='Бан пользователя снят')
    emb.add_field(name='{}kick @name'.format('p!'), value='Бан пользователя')
    emb.add_field(name='{}mute @name'.format('p!'), value='Замутать пользователя(не хочет работать)')
    await ctx.send(embed=emb)


@client.command(pass_context=True)
async def help_command_people(ctx):
    emb = discord.Embed(title='Навигация по командам для пользователя')
    emb.add_field(name='{}avatar @name'.format('p!'), value='выводит аватар любого пользователя')
    emb.add_field(name='{}userinfo @name'.format('p!'), value='выводит информацию о любом пользователя')
    emb.add_field(name='{}join'.format('p!'), value='Добавление бота в голосовой канал')
    emb.add_field(name='{}play #ссылка на ютубе#'.format('p!'), value='Воспроизведение песни')
    await ctx.send(embed=emb)


@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    for i in msg.split():
        if i in list_of_bad_words:
            await message.delete()

'''
@client.command(pass_context=True)
@commands.has_role('администратор')
async def mute(ctx, user: discord.Member):
    role = get(ctx.author.guild.roles, name="простой сметрный")
    await ctx.author.remove_roles(role)
    await ctx.send("{} has been muted from chat".format(user.name))
'''

#__________________________________________________#
#music

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
    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")


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
# __________________________________________________#

client.run(TOKEN)