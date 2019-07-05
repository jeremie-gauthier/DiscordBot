import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import metadata

PUNCTUATION	=	"?!.:»"
PAGES_LOAD	=	5

class Fun(commands.Cog):

	def __init__(self, client):
		self.client = client
		self._web_parser()

	@commands.Cog.listener()
	async def on_ready(self):
		print("fun.py is ready.")

	def	_web_parser(self):
		self.jokes = []
		for i in range(1, PAGES_LOAD):
			print(i, "/", PAGES_LOAD)
			r = requests.get("https://blague-humour.com/meilleures-blagues-droles/page/" + str(i))
			soup = BeautifulSoup(r.text, "html.parser")
			l = soup.findAll("div", attrs={"class": "entry-content"})
			if l is not None:
				l = list(filter(lambda s: "toto" not in s.getText().lower(), l))
				for s in l:
					self.jokes.append(s.getText())

	def	_format_joke(self, joke):
		words = joke.split()
		for i in range(len(words)):
			for p in PUNCTUATION:
				if p in words[i]:
					tmp = words[i].find(p) + 1
					if tmp < len(words[i]):
						if words[i][tmp] != ' ':
							words[i] = words[i][:tmp] + "\n" + words[i][tmp:]
		return (" ".join(words))

	@commands.command(aliases=['jokes'])
	async def joke(self, ctx):
		if metadata.current_status == "offline":
			return

		if not hasattr(self, "jokes"):
			self._web_parser()
		joke = random.choice(self.jokes)
		proper_joke = self._format_joke(joke)
		await ctx.send(f"{proper_joke}")

	@commands.command(aliases=['astre'])
	async def astres(self, ctx, *, question):
		if metadata.current_status == "offline":
			return

		responses = [
			"Oui",
			"Peut-etre",
			"Non"
		]
		await ctx.send(f"Question: {question}\nReponse: {random.choice(responses)}")

def	setup(client):
	client.add_cog(Fun(client))
