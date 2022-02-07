from discord.ext.ui import View, ViewTracker, Message, PaginationView, MessageProvider, PageView
import discord
from tabulate import tabulate
from . import birthday_sheet

class Page(PageView):
    def __init__(self, guild: discord.Guild, page_num, limit):
        super(Page, self).__init__()
        self.guild = guild
        self.page_num = page_num
        self.limit = limit

    async def body(self, _paginator: PaginationView):
        text = self.get_data()
        return Message(f"```shell\n{text}\n```")
    def get_data(self):
        d =birthday_sheet.get_page(self.page_num, self.limit)
        data = []
        for id, date in d:
            print(f"id= {id}")
            m = self.guild.get_member(id)
            print(f"n= {m}")
            if(m == None): continue
            data.append((m.display_name , date))
        print(data)

        return tabulate(data,headers=['ユーザー', '誕生日'],colalign=('left','right'))
        
    async def on_appear(self, paginator: PaginationView) -> None:
        print(f"appeared page: {paginator.page}")
async def create(guild: discord.Guild, ch: discord.TextChannel):
    pages = []
    limit = 10
    for i in range(birthday_sheet.page_count(limit)):
        pages.append(Page(guild,i,limit))
    view = PaginationView(pages)
    tracker = ViewTracker(view, timeout=None)
    await tracker.track(MessageProvider(ch))