import os
import dotenv

dotenv.load_dotenv()

webhook_secret = os.getenv('WEBHOOK_SECRET')
task_name = "wootcord.process_webhooks"
redis_password = os.getenv('REDIS_PASSWORD')
broker_url = f'redis://:{redis_password}@localhost:6379/0'

if not webhook_secret:
    raise ValueError("WEBHOOK_SECRET environment variable is not set.")

if not redis_password:
    raise ValueError("REDIS_PASSWORD environment variable is not set.")