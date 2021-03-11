import os
import re

RE_USERNAME = re.compile("^[a-zA-Z0-9]{4,12}$")
RE_PASSWORD = re.compile(r"^[a-zA-Z0-9 !\"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]{12,32}$")
RE_CHARACTER_NAME = re.compile("^[a-zA-Z ]{1,40}$")
RE_CHARACTER_ANIME = re.compile("^[a-zA-Z-+!?: ]{1,100}$")
STORAGE_PATH = os.environ.get("STORAGE_PATH", "storage")
API_TOKEN = os.environ.get("API_TOKEN")
