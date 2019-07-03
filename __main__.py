import sys
import os
import discord
from discord.ext import commands

PATH_COGS	=	"./cogs"

def get_token(pathname):
	try:
		fd = open(pathname, "r")
	except (IsADirectoryError, FileNotFoundError, PermissionError):
		return (-1)
	tok = fd.readline().strip('\n')
	fd.close()
	return (tok)

def load_cogs():
	for filename in os.listdir(PATH_COGS):
		if filename.endswith(".py"):
			client.load_extension(f"cogs.{filename[:-3]}")

if __name__ == '__main__':
	if len(sys.argv) == 2:
		TOKEN = get_token(sys.argv[1])
		if TOKEN == -1:
			print(f"ERROR: \"{sys.argv[1]}\" is not a valid file.")
			sys.exit(-1)

		client = commands.Bot(command_prefix = '.')
		load_cogs()
		try:
			client.run(TOKEN)
		except discord.errors.LoginFailure:
			print("ERROR: wrong data sent.")
			sys.exit(-1)
	else:
		print("Usage: python3 bot.py <path/to/your/token>")
		sys.exit(-1)
