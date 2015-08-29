from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

__all__ = ['PageFactory', 'HomePage', 'VideoAddPage']


def find_by(*args):
    """
    Wrapper function for driver.find_element()
    :param by: selenium.webdriver.common.by.By
    :param value: string
    :returns: property object of WebElement
    """
    def decorated(obj):
        return obj._driver.find_element(*args)
    return property(decorated)


class PageFactory(object):
    """
    Creates a page object using a webdriver object
    :param driver: WebDriver object
    :param page: Page class
    :returns: Page object
    """
    @staticmethod
    def init(driver, page):
        obj = page()
        obj._driver = driver
        return obj


class HomePage(object):
    """
    PageObject class for Login Page
    """
    url = 'http://qm-homework.wikia.com/'
    ajax_login_anchor = find_by(By.CSS_SELECTOR, 'a[data-id].ajaxLogin')
    login_dropdown_div = find_by(
        By.CSS_SELECTOR, 'div#UserLoginDropdown.UserLoginDropdown')
    username_input = find_by(
        By.CSS_SELECTOR,
        'div.UserLoginDropdown input[name=username]#usernameInput')
    password_input = find_by(
        By.CSS_SELECTOR,
        'div.UserLoginDropdown input[name=password]#passwordInput')
    submit_input = find_by(By.CSS_SELECTOR, 'input[type=submit].login-button')
    contribute_dropdown_nav = find_by(
        By.CSS_SELECTOR, 'nav.wikia-menu-button.contribute')
    add_video_menuitem_anchor = find_by(
        By.CSS_SELECTOR, 'li > a[data-id=wikiavideoadd]')

    def open_login_dropdown(self):
        try:
            ajax_login_anchor = WebDriverWait(self._driver, 10) \
                .until(EC.visibility_of(self.ajax_login_anchor))
            ActionChains(self._driver) \
                .move_to_element(ajax_login_anchor) \
                .perform()
            login_dropdown_div = WebDriverWait(self._driver, 10) \
                .until(EC.visibility_of(self.login_dropdown_div))
        except TimeoutException:
            return False
        else:
            return login_dropdown_div.is_displayed()

    def submit_login_info(self, username, password):
        WebDriverWait(self._driver, 10) \
            .until(EC.visibility_of(self.username_input)).send_keys(username)
        WebDriverWait(self._driver, 10) \
            .until(EC.visibility_of(self.password_input)).send_keys(password)
        WebDriverWait(self._driver, 10) \
            .until(EC.visibility_of(self.submit_input)).submit()


class VideoAddPage(object):
    """
    PageObject class for Video Add Page
    """
    url = 'http://qm-homework.wikia.com/wiki/Special:WikiaVideoAdd'
    video_add_url_input = find_by(
        By.CSS_SELECTOR,
        ('form[name=quickaddform] '
         'input[name=wpWikiaVideoAddUrl]#wpWikiaVideoAddUrl'))
    add_submit = find_by(
        By.CSS_SELECTOR, 'form[name=quickaddform] input[type=submit]')
    confirm_msg_div = find_by(
        By.CSS_SELECTOR, 'div.banner-notification.confirm > div.msg')
    confirm_msg_anchor = find_by(
        By.CSS_SELECTOR, 'div.banner-notification.confirm > div.msg > a')
