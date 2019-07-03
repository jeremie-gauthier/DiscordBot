import discord
from discord.ext import commands
import random

class Fun(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("fun.py is ready.")

	@commands.command(aliases=['astre'])
	async def astres(self, ctx, *, question):
		responses = [
			"Oui",
			"Peut-etre",
			"Non"
		]
		await ctx.send(f"Question: {question}\nReponse: {random.choice(responses)}")

def	setup(client):
	client.add_cog(Fun(client))
