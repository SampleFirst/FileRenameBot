import logging
import logging.config
from pyrogram import Client 
from config import APP_ID, API_HASH, TOKEN, FORCE_SUB, PORT
from aiohttp import web
from plugins.web import web_server


logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=150,
        )

    async def start(self):
       await super().start()
       me = await self.get_me()
       self.mention = me.mention
       self.username = me.username 
       self.force_channel = FORCE_SUB
       if FORCE_SUB:
         try:
            link = await self.export_chat_invite_link(FORCE_SUB)                  
            self.invitelink = link
         except Exception as e:
            logging.warning(e)
            logging.warning("Make Sure Bot admin in force sub channel")             
            self.force_channel = None
       app = web.AppRunner(await web_server())
       await app.setup()
       bind_address = "0.0.0.0"
       await web.TCPSite(app, bind_address, PORT).start()
       logging.info(f"{me.first_name} STARTED 👿👿👿")
      

    async def stop(self, *args):
      await super().stop()      
      logging.info("Bot Stopped")
        
bot = Bot()
bot.run()
