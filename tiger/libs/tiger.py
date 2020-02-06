from libs import utils
import json
from libs import logger
from selenium.webdriver.common.action_chains import ActionChains

log = logger.get_logger(__name__)


class Tiger:

    def __init__(self, browser_name):

        with open('framework_mapping.json') as json_file:
            self.fwk_mapping = json.load(json_file)
            self.login_url=self.fwk_mapping['url']['login_url']+'login'

            with open('page_layouts/login.json') as json_file:
                self.login_mapping = json.load(json_file)

            self.browser_obj = utils.Base(browser_name=browser_name)

    def login(self, username, password):
        """
        This method authenticates login mechanism
        :param username: (String) username of account
        :param password: (String) password of account
        :return: (boolean) login_status
        """
        try:
            login_url = self.fwk_mapping['url']['login_url']
            username_locator = self.login_mapping['username']['locator']
            username_type = self.login_mapping['username']['type']
            password_locator = self.login_mapping['password']['locator']
            password_type = self.login_mapping['password']['type']
            login_button_locator = self.login_mapping['login_button']['locator']
            login_button_type = self.login_mapping['login_button']['type']
            # close_button_locator = self.home_mapping['close-pop-up']['locator']
            # close_button_type = self.home_mapping['close-pop-up']['type']
        except Exception as e:
            log.error('locator xpath not found with error {}'.format(e))
            return False

        log.info('launching dashboard application')
        url_flag = self.browser_obj.open_url(login_url)
        if url_flag:
            log.info('Application launched successfully')
        else:
            log.error('Application launch failed')

        log.info('entering username')
        user_flag = self.browser_obj.send_text(locator=username_locator, locator_type=username_type, data=username)
        if user_flag:
            log.info('username entered correctly')
        else:
            log.error('username entered incorrectly')

        log.info('entering password')
        pass_flag = self.browser_obj.send_text(locator=password_locator, locator_type=password_type, data=password)
        if pass_flag:
            log.info('password entered correctly')
        else:
            log.error('password entered incorrectly')

        log.info('clicking on login button')
        login_button_flag = self.browser_obj.click(locator=login_button_locator, locator_type=login_button_type)
        if login_button_flag:
            log.info('login button clicked successfully')
        else:
            log.error('login button click failed')
        current_url = self.browser_obj.get_current_url()

            # if current_url == self.home_url:
            #     log.info('login successful')
            #     login_flag = True
            # else:
            #     log.error('login unsuccessful')
            #     login_flag = False

        return self.browser_obj


if __name__ == '__main__':

    pass

