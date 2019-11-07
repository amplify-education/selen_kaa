from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.options import DesiredCapabilities

from se_wrapper.browser_driver import BrowserDriver
from tests.setup import LOGS_SETUP, BROWSER_WIDTH, BROWSER_HEIGHT


class BrowserManager:

    def __init__(self, browser_type="chrome", use_grid=None, hub_uri=None, options=None):
        self.browser_type = browser_type
        self.hub_uri = hub_uri
        self.use_grid = use_grid
        self.options = options
        self._web_driver = None

    @property
    def web_driver(self):
        if self._web_driver is None:
            if self.use_grid:
                self._web_driver = BrowserDriver(self._get_remote_driver())
            else:
                if self.browser_type != "chrome":
                    raise NotImplementedError(f"Not implemented setup for {self.browser_type}")
                else:
                    self._web_driver = BrowserDriver(self._get_chrome_driver())
        return self._web_driver

    @staticmethod
    def _get_chrome_driver():
        cap = DesiredCapabilities.CHROME.copy()
        cap['loggingPrefs'] = LOGS_SETUP
        options = ChromeOptions()
        options.add_argument('--disable-translate')
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--verbose')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options, desired_capabilities=cap)
        driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
        return driver

    def _get_remote_driver(self):
        return webdriver.Remote(command_executor=self.hub_uri,
                                desired_capabilities=self.options)
