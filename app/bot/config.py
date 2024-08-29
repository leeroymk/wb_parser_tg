from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    token = os.getenv("API_TOKEN")
    return Config(tg_bot=TgBot(token=token))
