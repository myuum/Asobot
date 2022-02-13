from typing import Optional
import discord
from discord.ext.ui import MessageProvider
from discord import ui

class RecycleProvider(MessageProvider):
    def __init__( self,  message: Optional[discord.Message] = None ):
        self.message = message
        
    async def send_message(self, content: Optional[str], embeds, view: ui.View) -> discord.Message:
        if(self.message == None):
            self.message = await self.channel.send(content, embeds=embeds, view=view)
        else : 
            await self.edit_message(content, embeds=embeds, view=view)
        return self.message