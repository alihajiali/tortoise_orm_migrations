import sys, os, subprocess, dotenv, asyncio
from tortoise import Tortoise, run_async
from models import *

dotenv.load_dotenv()

TORTOISE_ORM = {
    'connections': {
        'test_1': os.getenv("SQL_URL_TEST_1"),
        'test_2': os.getenv("SQL_URL_TEST_2"), 
    },
    'apps': {
        # 'app_test_1': {
        #     'models': ['manage', 'aerich.models'],
        #     'default_connection': 'test_1',
        # },
        'app_test_2': {
            'models': ['manage', 'aerich.models'],
            'default_connection': 'test_2',
        }, 
    }
}

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def main():
    await init()
    print((await Event1.all()))
    print((await Event2.all()))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":

        if "migrations" not in os.listdir():
            subprocess.run(["aerich", "init", "-t", "manage.TORTOISE_ORM"])
            subprocess.run(["aerich", "init-db"])
        else:
            for app_name in TORTOISE_ORM["apps"]:
                print(f"Migrating {app_name}")
                if app_name not in os.listdir("migrations"):
                    subprocess.run(["aerich", "init-db"])
                subprocess.run(["aerich", "migrate", "--name", app_name])
                subprocess.run(["aerich", "upgrade"])
    else:
        asyncio.run(main())