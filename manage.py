import sys, os, subprocess, dotenv
from models import *

dotenv.load_dotenv()

TORTOISE_ORM = {
    'connections': {
        'test_1': os.getenv("SQL_URL_TEST_1"),
        'test_2': os.getenv("SQL_URL_TEST_2"), 
    },
    'apps': {
        'app_test_1': {
            'models': ['manage', 'aerich.models'],
            'default_connection': 'test_1',
        },
        'app_test_2': {
            'models': ['manage'],
            'default_connection': 'test_2',
        }, 
    }
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        if "migrations" not in os.listdir():
            subprocess.run(["aerich", "init", "-t", "manage.TORTOISE_ORM"])
            subprocess.run(["aerich", "init-db"])
        else:
            subprocess.run(["aerich", "migrate", "--name", "first"])
            subprocess.run(["aerich", "upgrade"])