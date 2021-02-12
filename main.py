import discord
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv


load_dotenv()

bot = commands.Bot(command_prefix="/")
bot.voice_client = None
bot.playlist =[]
TOKEN = os.getenv('TOKEN')
bot.paused = False
bot.playlist_counter = 0
bot.playlist_max = 0
bot.continuous = False
print(TOKEN)


@bot.command()
async def join(ctx, voice):
    channel = discord.utils.get(ctx.guild.channels, name=voice)
    print(channel.id)
    await channel.connect()
    bot.voice_client = bot.voice_clients[0]


@bot.command()
async def play(ctx, filename = ""):
    bot.paused = False
    looper.cancel()
    bot.voice_client.stop()
    await asyncio.sleep(1)
    if filename == "":
        bot.playlist_counter = 0
        bot.continuous = True
        looper.start()
    elif filename.isnumeric() and bot.playlist_max != []:
        bot.playlist_counter = int(filename)-1
        if bot.continuous == True:
            looper.start()
        else:
            source = await discord.FFmpegOpusAudio.from_probe(bot.playlist[bot.playlist_counter])
            bot.voice_client.play(source)
    else:
        source = await discord.FFmpegOpusAudio.from_probe(filename)
        bot.voice_client.play(source)


@bot.command()
async def next(ctx):
    bot.paused = False
    bot.voice_client.stop()
    looper.cancel()
    bot.playlist_counter+=1
    await asyncio.sleep(1)
    looper.start()

@bot.command()
async def back(ctx):
    bot.paused = False
    bot.voice_client.stop()
    looper.cancel()
    bot.playlist_counter-=1
    await asyncio.sleep(10)
    looper.start()


@bot.command()
async def playlist(ctx, filelist, continuous = "n"):
    f = open(filelist, "r")
    f1 = f.readlines()
    for i in f1:
        bot.playlist.append(i.rstrip())
    for i in bot.playlist:
        print(i)
    bot.playlist_max = len(bot.playlist)
    if continuous == "c":
        bot.continous = True
    else:
        bot.continous = False

@bot.command()
async def clean(ctx):
    bot.playlist =[]
    bot.playlist_max = 0
    bot.playlist_counter = 0


@bot.command()
async def toggle(ctx):
    bot.continuous = not bot.continuous



@bot.command()
async def stop(ctx):
    bot.voice_client.stop()
    looper.cancel()


@bot.command()
async def pause(ctx):
    bot.voice_client.pause()
    bot.paused = True


@bot.command()
async def resume(ctx):
    bot.voice_client.resume()
    bot.paused = False

@bot.command()
async def name(ctx):
    line = "Now playing: "+ bot.playlist[bot.playlist_counter].split("/")[-1]
    await ctx.send(line)

@bot.command()
async def show(ctx):
    line = "The Playlist:\n"
    for i in range(bot.playlist_max):
        line = line + str(i+1)+" "+bot.playlist[i].split("/")[-1] +"\n"
    await ctx.send(line)

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@tasks.loop(seconds=30)
async def looper():
    print("looped")
    if bot.playlist_counter<bot.playlist_max:
        print("playlist not finished")
        if bot.voice_client.is_playing() == False:
            print("Not playing")
            if bot.paused == False:
                print("Not on pause")
                name = bot.playlist[bot.playlist_counter]
                print(name)
                source = await discord.FFmpegOpusAudio.from_probe(name)
                bot.voice_client.play(source)
                print("playing")
                bot.playlist_counter+=1
    else:
        looper.cancel()




bot.run(TOKEN)
