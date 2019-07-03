import discord
from discord.ext import commands

class Moderation(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("moderation.py is ready.")

	@commands.command()
	async def ping(self, ctx):
		"""Show your ping"""
		await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

	@commands.command()
	async def clear(self, ctx, amount : int):
		"""Erase the most recents messages"""
		await ctx.channel.purge(limit=amount)

	@clear.error
	async def clear_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please specify an amount of messages to delete.")
		elif isinstance(error, commands.UserInputError):
			await ctx.send("```Usage: .clear <amount>\n\n<amount> should be an integer```")

def	setup(client):
	client.add_cog(Moderation(client))
