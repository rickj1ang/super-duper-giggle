import os
import random


TARGET_URL = os.getenv("TARGET_URL", "https://messari.io/project/bitcoin")

STEALTH_TEST = os.getenv("STEALTH_TEST", "0") == "1"

REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "45"))
PAGE_IDLE_MS = int(os.getenv("PAGE_IDLE_MS", "1200"))
SCRIPT_TIMEOUT_SECONDS = int(os.getenv("SCRIPT_TIMEOUT_SECONDS", "30"))

LANG = os.getenv("LANG", "en-US")
TIMEZONE = os.getenv("TZ", "America/New_York")

WINDOW_SIZES = [
    (1920, 1080),
    (1366, 768),
    (1536, 864),
    (1440, 900),
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]


def choose_window_size() -> tuple[int, int]:
    return random.choice(WINDOW_SIZES)


def choose_user_agent() -> str:
    return random.choice(USER_AGENTS)


