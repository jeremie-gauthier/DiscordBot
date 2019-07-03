import discord
from discord.ext import commands
import random

class dev_Heimdalh(commands.Cog):

	def	__init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game("Controlling your server"))
		print("dev.py is ready.")

	@commands.command(aliases=["logout"])
	async def close(self, ctx):
		await self.client.change_presence(status=discord.Status.offline)
		await self.client.close()

	@commands.command()
	async def load(self, ctx, extension):
		"""[dev only] Load cog"""
		self.client.load_extension(f"cogs.{extension}")

	@commands.command()
	async def unload(self, ctx, extension):
		"""[dev only] Unload cog"""
		self.client.unload_extension(f"cogs.{extension}")

	@commands.command(aliases=["r"])
	async def reload(self, ctx, extension):
		"""[dev only] Reload cog"""
		self.client.unload_extension(f"cogs.{extension}")
		self.client.load_extension(f"cogs.{extension}")

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send("Invalid command used.")

def	setup(client):
	client.add_cog(dev_Heimdalh(client))
