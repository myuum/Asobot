from discord import ui
from typing import Optional
from discord.ext.ui import ViewTracker, Message, PaginationView, MessageProvider, PageView
import discord
from tabulate import tabulate
from db import birthday_sheet
import config.config as config
from view.asobu_pagination import AsobuPagination
from view.recycle_provider import RecycleProvider

limit = config.list_limit


class Page(PageView):
    def __init__(self, guild: discord.Guild, page_num):
        super(Page, self).__init__()
        self.guild = guild
        self.page_num = page_num

    async def body(self, _paginator: PaginationView):
        text = self.get_data()
        return Message(f"```shell\n{text}\n```")
    def get_data(self):
        d =birthday_sheet.get_page(self.page_num, limit)
        data = []
        for id, date in d:
            m = self.guild.get_member(id)
            if(m == None): continue
            data.append((m.display_name , date))
        print(data)
        return tabulate(data,headers=['ユーザー', '誕生日'],colalign=('left','right'))
        
    async def on_appear(self, paginator: PaginationView) -> None:
        now_max = paginator.max_page
        target = birthday_sheet.page_count(limit)
        if(now_max + 1 < target):
            for i in range(now_max + 1, target):
                paginator._views.append(Page(self.guild,i,limit))
                paginator.max_page = len(paginator._views) - 1
        print(f"appeared page: {paginator.page}")
async def create(guild: discord.Guild, ch: discord.TextChannel, message: Optional[discord.Message] = None):
    view = AsobuPagination(create_page(guild))
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(ch))

async def recycle(guild: discord.Guild, message: discord.Message):
    view = AsobuPagination(create_page(guild))
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(RecycleProvider(message))

def create_page(guild: discord.Guild):
    pages = []
    for i in range(birthday_sheet.page_count(limit)):
        pages.append(Page(guild,i))
    return pages
