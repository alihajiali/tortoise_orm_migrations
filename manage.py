import sys, os, subprocess, dotenv, asyncio
from tortoise import Tortoise, run_async
from models import *

dotenv.load_dotenv()

TORTOISE_ORM = {
    'connections': {
        'test_2': os.getenv("SQL_URL_TEST_2"), 
        'test_1': os.getenv("SQL_URL_TEST_1"),
    },
    'apps': {
        'app_test_2': {
            'models': ['manage', 'aerich.models'],
            'default_connection': 'test_2',
        }, 
        'app_test_1': {
            'models': ['manage', 'aerich.models'],
            'default_connection': 'test_1',
        },
    }
}

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def main():
    await init()
    print((await Event1.all())[0].name)
    print((await Event2.all())[0].name)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        if "migrations" not in os.listdir():
            subprocess.run(["aerich", "init", "-t", "manage.TORTOISE_ORM"])
            subprocess.run(["aerich", "init-db"])
        else:
            subprocess.run(["aerich", "migrate", "--name", "first"])
            subprocess.run(["aerich", "upgrade"])
    else:
        asyncio.run(main())