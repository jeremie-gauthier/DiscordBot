import discord
from discord.ext import commands
from discord.utils import get
import random
import metadata

DEV_NAME	=	"Heimdalh#0989"

class dev_Heimdalh(commands.Cog):

	def	__init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		await self.client.change_presence(
			status=discord.Status.dnd,
			activity=discord.Game("Controlling your server")
		)
		print("dev.py is ready.")

	def	_identify_author(self, ctx):
		name = ctx.message.author.name
		discriminator = ctx.message.author.discriminator
		author = name + "#" + discriminator
		return (author)

	@commands.command(pass_context=True, aliases=["deco", "dc", "deconnexion"])
	async def disconnect(self, ctx):
		if metadata.current_status != "offline":
			voice = get(self.client.voice_clients, guild=ctx.guild)
			if voice and voice.is_connected():
				await voice.disconnect()
			metadata.current_status = "offline"
			await self.client.change_presence(status=discord.Status.offline)

	@commands.command(pass_context=True, aliases=["co", "connexion"])
	async def connect(self, ctx):
		if metadata.current_status == "offline":
			metadata.current_status = "online"
			await self.client.change_presence(
				status=discord.Status.dnd,
				activity=discord.Game("Controlling your server")
			)

	@commands.command(aliases=["logout"])
	async def close(self, ctx):
		author = self._identify_author(ctx)
		if (author == DEV_NAME):
			await self.client.close()

	@commands.command()
	async def load(self, ctx, extension):
		"""[dev only] Load cog"""
		author = self._identify_author(ctx)
		if (author == DEV_NAME):
			self.client.load_extension(f"cogs.{extension}")

	@commands.command()
	async def unload(self, ctx, extension):
		"""[dev only] Unload cog"""
		author = self._identify_author(ctx)
		if (author == DEV_NAME):
			self.client.unload_extension(f"cogs.{extension}")

	@commands.command(aliases=["r"])
	async def reload(self, ctx, extension):
		"""[dev only] Reload cog"""
		self.client.unload_extension(f"cogs.{extension}")
		self.client.load_extension(f"cogs.{extension}")

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if metadata.current_status == "online":
			if isinstance(error, commands.CommandNotFound):
				await ctx.send("Invalid command used.")

def	setup(client):
	client.add_cog(dev_Heimdalh(client))
