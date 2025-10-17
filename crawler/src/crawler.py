from __future__ import annotations

import os
import time
import random
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--disable-ipc-flooding-protection")
    
    # Proxy configuration
    if config.PROXY_ENABLED and config.PROXY_SERVER:
        options.add_argument(f"--proxy-server={config.PROXY_SERVER}")
        if config.PROXY_USERNAME and config.PROXY_PASSWORD:
            options.add_argument(f"--proxy-auth={config.PROXY_USERNAME}:{config.PROXY_PASSWORD}")
    
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


def simulate_human_mouse_movement(driver: WebDriver) -> None:
    """Simulate human-like mouse movements"""
    try:
        actions = ActionChains(driver)
        # Random mouse movements
        for _ in range(random.randint(2, 4)):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-50, 50)
            actions.move_by_offset(x_offset, y_offset)
            actions.pause(random.uniform(0.1, 0.3))
        actions.perform()
        time.sleep(random.uniform(0.5, 1.5))
    except Exception:
        # If mouse simulation fails, continue silently
        pass


def simulate_human_scrolling(driver: WebDriver) -> None:
    """Simulate human-like progressive scrolling"""
    try:
        # Get page height
        page_height = driver.execute_script("return document.body.scrollHeight")
        current_scroll = 0
        scroll_increment = random.randint(200, 500)
        
        while current_scroll < page_height:
            # Random scroll amount
            scroll_amount = random.randint(scroll_increment // 2, scroll_increment)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            current_scroll += scroll_amount
            
            # Random pause between scrolls
            time.sleep(random.uniform(0.8, 2.5))
            
            # Occasionally scroll back up slightly (human behavior)
            if random.random() < 0.2:
                back_scroll = random.randint(50, 150)
                driver.execute_script(f"window.scrollBy(0, -{back_scroll});")
                time.sleep(random.uniform(0.3, 0.8))
        
        # Scroll to top at the end
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.0, 2.0))
        
    except Exception:
        # Fallback to simple scrolling if advanced scrolling fails
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.8)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1.0)


def apply_additional_stealth_cdp(driver: WebDriver) -> None:
    """Apply additional stealth via Chrome DevTools Protocol"""
    try:
        # These CDP commands help bypass detection
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                window.chrome = { runtime: {} };
            '''
        })
        
        # Set realistic viewport
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'width': random.choice([1920, 1366, 1536, 1440]),
            'height': random.choice([1080, 768, 864, 900]),
            'deviceScaleFactor': 1,
            'mobile': False
        })
        
        # Set timezone
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {
            'timezoneId': 'America/New_York'
        })
        
        # Set locale
        driver.execute_cdp_cmd('Emulation.setLocaleOverride', {
            'locale': 'en-US'
        })
        
    except Exception:
        # If CDP commands fail, continue without them
        pass


def run() -> int:
    os.makedirs("/app/data", exist_ok=True)
    driver = connect_remote_driver()
    try:
        # Apply additional CDP-based stealth if not using proxy
        if not config.PROXY_ENABLED:
            apply_additional_stealth_cdp(driver)

        if config.STEALTH_TEST:
            print("Running stealth test...")
            driver.get("https://bot.sannysoft.com/")
            wait_for_idle(driver, config.PAGE_IDLE_MS)
            
            # Apply stealth masks after page loads
            apply_stealth_masks(driver)
            
            # Human-like behavior on test page
            simulate_human_mouse_movement(driver)
            simulate_human_scrolling(driver)
            
            driver.save_screenshot("/app/data/stealth_test.png")
            print("Stealth test completed - check stealth_test.png")

        print(f"Navigating to: {config.TARGET_URL}")
        driver.get(config.TARGET_URL)
        
        # Wait for page to load completely
        wait_for_idle(driver, config.PAGE_IDLE_MS)
        
        # Apply stealth masks after page loads to avoid timing issues
        apply_stealth_masks(driver)
        
        # Add human-like delay before interaction
        time.sleep(random.uniform(2.0, 5.0))
        
        # Simulate human mouse movements
        simulate_human_mouse_movement(driver)
        
        # Simulate human scrolling behavior
        simulate_human_scrolling(driver)
        
        # Additional random delay before capture
        time.sleep(random.uniform(1.0, 3.0))

        # Capture page content
        html = driver.page_source
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_html = f"/app/data/messari_bitcoin_{ts}.html"
        out_png = f"/app/data/page_{ts}.png"

        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html)
        driver.save_screenshot(out_png)
        print(f"Saved HTML to {out_html} and screenshot to {out_png}")
        
        # Verify content was captured correctly
        if "Example Domain" in html:
            print("WARNING: Detected example.com content - stealth may have failed")
            return 1
        elif config.TARGET_URL.split('/')[-1].lower() in html.lower():
            print("SUCCESS: Target content detected in captured HTML")
            return 0
        else:
            print("INFO: Content captured but target verification unclear")
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


