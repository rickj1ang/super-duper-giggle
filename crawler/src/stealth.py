from __future__ import annotations

from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver


def apply_stealth_masks(driver: WebDriver) -> None:
    _mask_webdriver_property(driver)
    _mask_chrome_runtime(driver)
    _mask_plugins_languages(driver)
    _mask_canvas(driver)
    _mask_webgl(driver)
    _mask_permissions_api(driver)
    _mask_battery_api(driver)
    _mask_connection_api(driver)
    _mask_hardware_properties(driver)
    _mask_screen_properties(driver)
    _mask_media_devices(driver)
    _mask_notification_permissions(driver)
    _mask_webgl_vendor_renderer(driver)
    _mask_timezone_offset(driver)


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


def _mask_permissions_api(driver: WebDriver) -> None:
    # Mock permissions API with realistic states
    driver.execute_script(
        """
        const originalQuery = navigator.permissions.query;
        navigator.permissions.query = function(permission) {
          return Promise.resolve({
            state: permission.name === 'notifications' ? 'default' : 'granted',
            onchange: null
          });
        };
        """
    )


def _mask_battery_api(driver: WebDriver) -> None:
    # Mock battery API with realistic values
    driver.execute_script(
        """
        Object.defineProperty(navigator, 'getBattery', {
          get: () => () => Promise.resolve({
            charging: Math.random() > 0.3,
            chargingTime: Math.floor(Math.random() * 7200),
            dischargingTime: Math.floor(Math.random() * 28800),
            level: 0.7 + Math.random() * 0.3
          })
        });
        """
    )


def _mask_connection_api(driver: WebDriver) -> None:
    # Mock network connection API
    driver.execute_script(
        """
        Object.defineProperty(navigator, 'connection', {
          get: () => ({
            effectiveType: '4g',
            downlink: 10 + Math.random() * 5,
            rtt: 50 + Math.random() * 100,
            saveData: false
          })
        });
        """
    )


def _mask_hardware_properties(driver: WebDriver) -> None:
    # Mock hardware properties
    driver.execute_script(
        """
        Object.defineProperty(navigator, 'hardwareConcurrency', {
          get: () => 8
        });
        Object.defineProperty(navigator, 'deviceMemory', {
          get: () => 8
        });
        Object.defineProperty(navigator, 'maxTouchPoints', {
          get: () => 0
        });
        """
    )


def _mask_screen_properties(driver: WebDriver) -> None:
    # Mock screen properties
    driver.execute_script(
        """
        Object.defineProperty(screen, 'colorDepth', {
          get: () => 24
        });
        Object.defineProperty(screen, 'pixelDepth', {
          get: () => 24
        });
        """
    )


def _mask_media_devices(driver: WebDriver) -> None:
    # Mock media devices enumeration
    driver.execute_script(
        """
        Object.defineProperty(navigator.mediaDevices, 'enumerateDevices', {
          value: () => Promise.resolve([
            { deviceId: 'default', kind: 'audioinput', label: 'Default - Microphone' },
            { deviceId: 'default', kind: 'audiooutput', label: 'Default - Speaker' }
          ])
        });
        """
    )


def _mask_notification_permissions(driver: WebDriver) -> None:
    # Mock notification permission
    driver.execute_script(
        """
        Object.defineProperty(Notification, 'permission', {
          get: () => 'default'
        });
        """
    )


def _mask_webgl_vendor_renderer(driver: WebDriver) -> None:
    # Enhanced WebGL vendor/renderer masking
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
        
        const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(parameter) {
          if (parameter === 37445) { // UNMASKED_VENDOR_WEBGL
            return 'Intel Inc.';
          }
          if (parameter === 37446) { // UNMASKED_RENDERER_WEBGL
            return 'Intel Iris OpenGL Engine';
          }
          return getParameter2.call(this, parameter);
        };
        """
    )


def _mask_timezone_offset(driver: WebDriver) -> None:
    # Mock timezone offset to appear more natural
    driver.execute_script(
        """
        const originalGetTimezoneOffset = Date.prototype.getTimezoneOffset;
        Date.prototype.getTimezoneOffset = function() {
          return -300; // EST/EDT offset
        };
        """
    )


