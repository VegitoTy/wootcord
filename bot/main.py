import asyncio
import config
import discord

from discord.ext import commands
from handlers import dispatcher 
from tasks import queue

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

@queue.task(name=config.task_name, bind=True)
def queue_handler(self, data):
    try:
        loop = bot.loop
        asyncio.run_coroutine_threadsafe(dispatcher.dispatch(data), loop).result()
    except Exception as e:
        print(f"({self.request.retries}/{self.max_retries}) An error occured while passing data to bot: {e}")
        raise self.retry(exc=e, countdown=2**self.request.retries, max_retries=3)

def run_celery_worker():
    print("Celery worker thread is starting...")
    argv = [
        'worker',
        '-P', 'threads',
        #'--loglevel=info'
    ]
    queue.worker_main(argv)

async def main():
    loop = asyncio.get_running_loop()
    celery_worker = loop.run_in_executor(None, run_celery_worker)

    async with bot:
        print("Starting the bot...")
        await bot.start(config.bot_token)

    await celery_worker

if __name__ == '__main__':
    asyncio.run(main())
