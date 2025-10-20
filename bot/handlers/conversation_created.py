import discord
from discord.ext import commands

from pydantic import ConfigDict, validate_call
from models import ConversationCreated

@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
async def handle(bot: commands.Bot, data: ConversationCreated):
    info = discord.Embed(
        title="Conversation Info",
        color=discord.Color.blue()
    )

    info.add_field(name="Conversation ID:", value=str(data.id), inline=False)
    info.add_field(name="Created By:", value=f"{data.meta.sender.id} - {data.meta.sender.name}", inline=False)
    info.add_field(name="Status:", value=data.status, inline=False)
    
    await bot.forum.create_thread(
        name = f"#{data.id} - {data.meta.sender.name}",
        embed=info
    )
    
