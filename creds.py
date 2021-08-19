from os import getenv

from dotenv import load_dotenv

load_dotenv()

SSH_HOST = getenv("SSH_HOST")
SSH_PORT = getenv("SSH_PORT")
SSH_USERNAME = getenv("SSH_USERNAME")
SSH_PASSWORD = getenv("SSH_PASSWORD")
