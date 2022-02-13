import discord
from discord.ext.ui import View, ViewTracker, Message, PaginationView, MessageProvider, PageView
from typing import Union

class AsobuPagination(PaginationView):
    def change_page(self, interaction: discord.Interaction, page: int):
        if self.check is not None and not self.check(interaction): return
        if(page < 0): self.page = 0
        elif(self.max_page < page): self.page = self.max_page
        else : self.page = page