""" Wrapper around Selenium WebDriver.
 Calls all methods on self._webdriver.
 Added some method for usability.

"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ActionChains

from se_wrapper import help_utils
from se_wrapper.web_driver_config import WebDriverConfig


TimeoutType = help_utils.TimeoutType


class BrowserDriver:

    def __init__(self, webdriver: WebDriver):
        self._webdriver: WebDriver = webdriver
        self.config = WebDriverConfig()


    def __getattr__(self, attr):
        """Calls method or properties on self._webdriver.
        Returns callable or attribute of WebDriver.
        :param attr: any attr of the WebDriver
        :return: Any

        """
        try:
            orig_attr = self._webdriver.__getattribute__(attr)
            if callable(orig_attr):
                def hooked(*args, **kwargs):
                    result = orig_attr(*args, **kwargs)
                    # prevent recursion
                    if result == self._webdriver:
                        return self
                    return result
                return hooked
            return orig_attr
        except AttributeError as exc:
            raise AttributeError(f"WebDriver has no attribute {attr}.\n{exc}")

    @property
    def action_chains(self):
        return ActionChains(self._webdriver)

    def init_web_element(self, selector: str, timeout: TimeoutType = None):
        """Init a new WrappedWebElement.
        Lazy initialization. Element would be called on the time of first interaction.
        :param selector: str as css selector or xpath
        :param timeout: time to wait until element appears
        :return: WrappedWebElement
        """
        if selector is None:
            raise Exception("Selector should be not empty.")
        timeout_ = timeout or self.config.DEFAULT_TIMEOUT
        return self.config.WrappedElementType(self._webdriver, selector, timeout_)

    def init_all_web_elements(self, selector: str, timeout: TimeoutType = None):
        """Init a list with references to WrappedWebElement.
        Lazy initialization. All elements would be called on the time of first interaction
        with any of the elements.
        :return: List of WrappedWebElements
        """
        timeout_ = timeout or self.config.DEFAULT_TIMEOUT
        WrappedElementType = self.config.WrappedElementType
        return self.config.WrappedElementArrayType(self._webdriver, selector, WrappedElementType, timeout_)
