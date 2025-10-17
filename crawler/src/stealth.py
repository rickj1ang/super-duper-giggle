from __future__ import annotations

from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver


def apply_stealth_masks(driver: WebDriver) -> None:
    _mask_webdriver_property(driver)
    _mask_chrome_runtime(driver)
    _mask_plugins_languages(driver)
    _mask_canvas(driver)
    _mask_webgl(driver)


def _mask_webdriver_property(driver: WebDriver) -> None:
    # navigator.webdriver -> undefined
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
    )


def _mask_chrome_runtime(driver: WebDriver) -> None:
    # navigator.chrome runtime stub
    driver.execute_script(
        """
        Object.defineProperty(navigator, 'chrome', {
          get: () => ({ runtime: {} })
        });
        """
    )


def _mask_plugins_languages(driver: WebDriver) -> None:
    # plugins and languages
    driver.execute_script(
        """
        Object.defineProperty(navigator, 'plugins', {
          get: () => [1,2,3,4,5]
        });
        Object.defineProperty(navigator, 'languages', {
          get: () => ['en-US', 'en']
        });
        """
    )


def _mask_canvas(driver: WebDriver) -> None:
    # Slight noise for canvas operations
    driver.execute_script(
        """
        const origGetContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function() {
          const ctx = origGetContext.apply(this, arguments);
          if (!ctx) return ctx;
          if (arguments[0] === '2d') {
            const origFillText = ctx.fillText;
            ctx.fillText = function() {
              if (arguments.length >= 4 && typeof arguments[3] === 'number') {
                arguments[3] = arguments[3] + Math.random() * 0.001;
              }
              return origFillText.apply(this, arguments);
            };
          }
          return ctx;
        };
        """
    )


def _mask_webgl(driver: WebDriver) -> None:
    # Vendor/renderer
    driver.execute_script(
        """
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
          if (parameter === 37445) { // UNMASKED_VENDOR_WEBGL
            return 'Intel Inc.';
          }
          if (parameter === 37446) { // UNMASKED_RENDERER_WEBGL
            return 'Intel Iris OpenGL Engine';
          }
          return getParameter.call(this, parameter);
        };
        """
    )


