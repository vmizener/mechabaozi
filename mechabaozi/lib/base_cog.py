import logging

from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger(f"mechabaozi.{self.qualified_name}")
