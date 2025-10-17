from __future__ import annotations

import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import config
from .stealth import apply_stealth_masks


def build_options() -> ChromeOptions:
    width, height = config.choose_window_size()
    ua = config.choose_user_agent()

    options = ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument(f"--user-agent={ua}")
    options.add_argument(f"--lang={config.LANG}")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-translate")
    # Headful: do NOT set --headless
    return options


def connect_remote_driver() -> WebDriver:
    options = build_options()
    driver = webdriver.Remote(
        command_executor="http://chrome:4444/wd/hub",
        options=options,
    )
    driver.set_page_load_timeout(config.REQUEST_TIMEOUT_SECONDS)
    driver.set_script_timeout(config.SCRIPT_TIMEOUT_SECONDS)
    return driver


def wait_for_idle(driver: WebDriver, idle_ms: int) -> None:
    # crude network idle-ish: wait readyState complete and then sleep briefly
    WebDriverWait(driver, config.REQUEST_TIMEOUT_SECONDS).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(idle_ms / 1000.0)


def run() -> int:
    os.makedirs("/app/data", exist_ok=True)
    driver = connect_remote_driver()
    try:
        apply_stealth_masks(driver)

        if config.STEALTH_TEST:
            driver.get("https://bot.sannysoft.com/")
            wait_for_idle(driver, config.PAGE_IDLE_MS)
            driver.save_screenshot("/app/data/stealth_test.png")

        driver.get(config.TARGET_URL)
        wait_for_idle(driver, config.PAGE_IDLE_MS)

        # light human-like scroll
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.8)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1.0)

        html = driver.page_source
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_html = f"/app/data/messari_bitcoin_{ts}.html"
        out_png = f"/app/data/page_{ts}.png"

        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html)
        driver.save_screenshot(out_png)
        print(f"Saved HTML to {out_html} and screenshot to {out_png}")
        return 0
    except Exception as e:
        print(f"Crawler error: {e}")
        return 1
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(run())


