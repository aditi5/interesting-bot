import os

from app import app

if __name__ == "__main__":
	DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
	app.run(DISCORD_TOKEN)
