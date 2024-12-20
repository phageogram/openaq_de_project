from os import environ
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    class Config():
        env_prefix = ""