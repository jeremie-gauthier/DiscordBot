import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import random
import metadata

class MusicMP3(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("music_mp3.py is ready.")

	@commands.command(pass_context=True)
	async def join(self, ctx):
		"""Let the bot join your current channel"""
		if metadata.current_status == "offline":
			return

		channel = ctx.message.author.voice.channel
		self.voice = get(self.client.voice_clients, guild=ctx.guild)

		if self.voice and self.voice.is_connected():
			await self.voice.move_to(channel)
		else:
			self.voice = await channel.connect()

		print(f"The bot has connected to {channel}\n")
		await ctx.send(f"Joined {channel}")

	@commands.command(pass_context=True, aliases=["l", "lea"])
	async def leave(self, ctx):
		"""Disconnect the bot from the current channel"""
		if metadata.current_status == "offline":
			return
		channel = ctx.message.author.voice.channel
		self.voice = get(self.client.voice_clients, guild=ctx.guild)

		if self.voice and self.voice.is_connected():
			await self.voice.disconnect()
			print(f"The bot has left {channel}")
			await ctx.send(f"Left {channel}")
		else:
			print("Bot was told to leave voice channel, but was not in one")
			await ctx.send("Not in a voice channel")

	@commands.command(pass_context=True, aliases=["p"])
	async def play(self, ctx, url : str):
		"""Play song from YouTube"""
		if metadata.current_status == "offline":
			return

		song_there = os.path.isfile("song.mp3")
		try:
			if song_there:
				os.remove("song.mp3")
				print("Supposed to removed old song file")
		except PermissionError:
			print("Trying to delete song file, but it's being played")
			await ctx.send("ERROR: Music playing")
			return

		await ctx.send("Getting everything ready now")
		self.voice = get(self.client.voice_clients, guild=ctx.guild)
		ydl_opts = {
			'format': "bestaudio/best",
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192'
			}]
		}

		url = url.split("&")[0]
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print("Downloading audio now\n")
			ydl.download([url])

		for file in os.listdir("./"):
			if file.endswith(".mp3"):
				name = file
				print(f"Renamed File: {file}\n")
				os.rename(file, "song.mp3")

		self.voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
		self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
		self.voice.source.volume = 0.07

		nname = name.rsplit("-", 2)
		await ctx.send(f"Playing: {nname[0]}")
		print("Playing\n")

	
	@commands.command(pass_context=True)
	async def chiantos(self, ctx):
		"""Play a random song from Naheulbeuk"""
		if metadata.current_status == "offline":
			return
		prefix = "./chiantos/"
		songs = os.listdir("./chiantos/")
		chosen = prefix + random.choice(songs)
		self.voice = get(self.client.voice_clients, guild=ctx.guild)
		self.voice.play(discord.FFmpegPCMAudio(chosen), after=lambda e: print(f"{chosen} has finished playing"))
		self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
		self.voice.source.volume = 0.07


def	setup(client):
	client.add_cog(MusicMP3(client))
