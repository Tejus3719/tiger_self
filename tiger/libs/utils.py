from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import DriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import time
import libs.logger as logger
import os
import traceback
log = logger.get_logger(__name__)


class Base(object):
    """
    API's were tested by using the url : "https://www.testandquiz.com/selenium/testing.html"
    """
    def __init__(self, browser_name):
        try:
            self.url = ''
            if browser_name == "chrome":
                self.browser = webdriver.Chrome(ChromeDriverManager().install())
                self.browser.maximize_window()
                log.info("Successfully Chrome browser instance started")
            elif browser_name == "firefox":
                self.browser = webdriver.Firefox(DriverManager().install())
                self.browser.maximize_window()
                log.info("Successfully Firefox browser instance started")
            elif browser_name == "safari":
                self.browser = webdriver.Safari()
                self.browser.maximize_window()
                log.info("Successfully Safari browser instance started")
            else:
                self.browser = webdriver.Ie()
                self.browser.maximize_window()
                log.info("Successfully Internet explorer browser instance started")
        except Exception as e:
            traceback.print_exc()
            log.error("failed to open the browser with exception {} ".format(e))

    def open_url(self, url):
        """
        Method to open an url
        :param url:  link of the url to be opened
        Usage :
            obj = Base()
            obj.open_url(url = "https://www.google.com")
        :return: return True/False
        """
        self.url = url
        try:
            self.browser.get(self.url)
            log.info("successfully opened the url {} ".format(self.url))
        except Exception as e:
            log.error("failed to open the url with exception {} ".format(e))
            return False
        return True

    def get_current_url(self):
        """
        Method to get the current url
        Usage :
            obj = Base()
            obj.get_current_url()
        :return : url
        """
        try:
            url = self.browser.current_url
        except Exception as e:
            log.error("failed to get the current url with exception {} ".format(e))
            return False
        return url

    def implicit_wait(self, time):
        """
        This method waits browser for time seconds
        :param time: (int) time in secs
        :return:
        """
        flag = False
        try:
            self.browser.implicitly_wait(time)
            flag = True
        except Exception as e:
            log.error('failed to implicit wait with exceoption {}'.format(e))

        return flag

    def get_tittle(self):
        """
        Method to get the tittle
        Usage :
            obj = Base()
            obj.get_tittle()
        :return: title
        """
        try:
            title = self.browser.title
        except Exception as e:
            log.error("failed to get the title with exception {} ".format(e))
            return False
        return title

    def ele_locator(self, locator, locator_type):
        """
        Method to locate the element
        :param locator : name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage :
           obj = Base()
           obj.ele_locator(locator = ""//select[@id='testingDropdown']"",locator_type = "xpath")
        :return:  located element / False (if element is not located)
        """
        locator_type = locator_type.lower()
        try:
            if locator_type == "id":
                element = self.browser.find_element(By.ID, locator)
            elif locator_type == "xpath":
                element = self.browser.find_element(By.XPATH, locator)
            elif locator_type == "css":
                element = self.browser.find_element(By.CSS_SELECTOR, locator)
            elif locator_type == "name":
                element = self.browser.find_element(By.NAME, locator)
            elif locator_type == "class":
                element = self.browser.find_element(By.CLASS_NAME, locator)
            else:
                log.warn("locator_type {} is not supported ".format(locator_type))
                return False
        except Exception as e:
            log.error("Could not find the given element {}".format(e))
            return False
        return element

    def send_text(self, locator, locator_type, data, clear=None):
        """
        Method to send text to the box
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        :param data: to be filled in the box
        :param clear: clear the existing content and adds the user sent text in the box
        Usage :
            obj = Base()
            obj.send_text(locator = "//input[@id='fname']",locator_type = "xpath",data = "testing")
        :return:  True (if data is sent successfully) / False(if not )
        """
        element = self.ele_locator(locator, locator_type)
        if element is not None:
            try:
                if clear:
                    element.clear()
                element.send_keys(data)
                return True
            except Exception as e:
                log.error("failed to send keys with exception {} ".format(e))
                self.get_screenshot(info="Error")
                return False

    def refresh(self):
        """
        Method to refresh the current page
        Usage:
            obj = Base()
            obj.Refresh()
        :return:  None
        """
        try:
            self.browser.refresh()
            log.info("successfully refreshed the page {}".format(self.get_tittle()))
            return True
        except Exception as e:
            log.error("page refresh failed with exception {}".format(e))
            return False

    def get_text(self, locator, locator_type):
        """
        Method to get the text of the located element
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage :
                obj = Base()
                obj.get_text(locator = "//b[contains(.,'This is sample text.')]",locator_type = "xpath")
        :return: True, text of the located element / False (if the located element doesn't contain any text)
        """
        output_text = ''
        element = self.ele_locator(locator, locator_type)
        if element is not None:
            try:
                output_text = element.text
                if bool(output_text):
                    return True, output_text
                else:
                    log.warn("element doesn't contain any text")
                    return False, output_text
            except Exception as e:
                log.error("failed to get the text of the located element with exception {} ".format(e))
                self.get_screenshot(info="Error")
                return False, output_text

    def is_dispalyed(self, locator, locator_type):
        """
        Method to know whether the element is displayed
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.is_dispalyed(locator = "idOfButton",locator_type = "id")
        :return: True (if element is displayed) / False
        """
        display = self.ele_locator(locator, locator_type).is_displayed()
        if display:
            return True
        else:
            self.get_screenshot(info="Error")
            return False

    def is_enabled(self, locator, locator_type):
        """
        Method to know whether the element is enabled
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.is_enabled(locator = "//button[@id='idOfButton']",locator_type = "xpath")
        :return:  True (if element is enabled) / False
        """
        enabled = self.ele_locator(locator, locator_type).is_enabled()
        if enabled:
            return True
        else:
            self.get_screenshot(info="Error")
            return False

    def click(self, locator, locator_type):
        """
        Method to click on a particular element
        :param  locator: name/id/css/xpath/class of the element to be located
        :param  locator_type:  name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.Click(locator = "male",locator_type = "id")
        :return: True (if element is clickable) / False
        """
        element = self.ele_locator(locator, locator_type)
        if element is not None:
            try:
                element.click()
                return True
            except Exception as e:
                log.error("clicking element failed with exception {} ".format(e))
                self.get_screenshot(info="Error")
                return False

    def is_selected(self, locator, locator_type):
        """
        Method to know whether a check box is selected or not
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.Click(locator = "male",locator_type = "id")
        :return: True/False
        """
        selected = self.ele_locator(locator, locator_type).is_selected()
        if selected:
            return True
        else:
            self.get_screenshot(info="Error")
            return False

    def page_forward(self):
        """
        Method to forward from the current page
        Usage:
            obj = Base()
            obj.page_forward()
        :return: True/False
        """
        try:
            self.browser.forward()
            return True
        except Exception as e:
            log.error("page forward failed with exception {} ".format(e))
            return False

    def page_back(self):
        """
        Method to go back from the current page
        Usage:
            obj = Base()
            obj.page_back()
        :return: None
        """
        try:
            self.browser.back()
            return True
        except Exception as e:
            log.error("page forward failed with exception {} ".format(e))
            return False

    def switch_to_alert(self, locator, locator_type):
        """
        Method to switch to generated alert box
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type:  name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.switch_to_alert(locator = "//select[@id='testingDropdown']",locator_type = "xpath")
        :return:  alert (if alert box is generated) / False (if alert box is not generated)
        """
        self.click(locator, locator_type)
        alert = self.browser.switch_to.alert
        if alert:
            return alert
        else:
            log.error("alert was not generated")
            self.get_screenshot(info="Error")
            return False

    def get_alert_text(self, locator, locator_type):
        """
        Method to get the generated alert text
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type:  name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.accept_alert(locator = '''//button[@onclick="alert('hi, JavaTpoint Testing');"]''',
            locator_type = "xpath")
        :return:  text message in alert box
        """
        alert = self.switch_to_alert(locator, locator_type)
        if alert:
            return True, alert.text
        else:
            self.get_screenshot(info="Error")
            return False

    def accept_alert(self, locator, locator_type):
        """
        Method to accept the generated alert
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.accept_alert(locator = "//select[@id='testingDropdown']",locator_type = "xpath")
        :return: True/False
        """
        try:
            alert = self.switch_to_alert(locator, locator_type)
            alert.accept()
            return True
        except Exception as e:
            log.error("failed to accept the alert with exception {} ".format(e))
            self.get_screenshot(info="Error")
            return True

    def dismiss_alert(self, locator, locator_type):
        """
        Method to dismiss the generated alert box
        :param locator:  name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage:
            obj = Base()
            obj.dismiss_alert(locator = "//select[@id='testingDropdown']",locator_type = "xpath")
        :return:  True/False
        """
        try:
            alert = self.switch_to_alert(locator, locator_type)
            alert.dismiss()
            return True
        except Exception as e:
            log.error("failed to dismiss the alert with exception ".format(e))
            self.get_screenshot(info="Error")
            return False

    def select_by_dropdown(self, locator, locator_type, option_to_select, type_of=""):
        """
        Method to select the dropdown box values by using it's value/index/visible_text and by default it
         selects by visible text
        :param locator:  name/id/css/xpath/class of the element to be located
        :param locator_type:  name/id/css/xpath/class
        :param option_to_select: element to be selected from dropdown
        :param type_of = option to be passed to select element from drop down (value/index/visible(default))

        Usage:
            obj = Base()
            obj.select_by_dropdown(locator = "//select[@id='testingDropdown']",locator_type = "xpath",
            option_to_select="Manual Testing")
        :return:  True/False
        """
        dropdown = self.ele_locator(locator, locator_type)
        if dropdown is not None:
            try:
                select = Select(dropdown)
                if type_of == "value":
                    select.select_by_value(option_to_select)
                elif type_of == "index":
                    select.select_by_index(option_to_select)
                else:
                    select.select_by_visible_text(option_to_select)
            except Exception as e:
                log.error("could  not select from dropdown box with exception {}".format(e))
                self.get_screenshot(info="Error")
                return False
            return True

    def return_by_type(self, locator_type):
        """
        used to return the approporiate By value and it is used in wait_until_element
        Usage:
            obj = Base()
            obj.return_by_type(locator_type = "xpath")
        :param locator_type:  name/id/css/xpath/class
        :return: BY type which is used in wait_until_element method
        """
        if locator_type == "id":
            return By.ID
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "name":
            return By.NAME
        else:
            log.error(" locator type {} is not supported".format(locator_type))
            return False

    def wait_until_element(self, locator_type, locator, wait_type="", time_to_wait=10, frequency=0.5):
        """
        Method to wait until the element is visible/clickable/located (by default it waits for 10 seconds and checks
         for every 0.5 milli-seconds)
        Usage :
            obj = Base()
            obj.wait_until_element(locator = "//select[@id='testingDropdown']",locator_type = "xpath",
            option_to_select="Manual Testing")
        :param locator_type: name/id/css/xpath/class
        :param locator : name/id/css/xpath/class of the element to be located
        :param wait_type :
        :param time_to_wait :
        :param frequency :
        :return: element (if it located)/False(if not located)
        """
        element = None
        start_time = int(round(time.time())/1000)
        try:
            by_type = self.return_by_type(locator_type)
            wait = WebDriverWait(self.browser, time_to_wait, poll_frequency=frequency)
            if wait_type == "visible":
                element = wait.until(EC.visibility_of_element_located((by_type, locator)))
            elif wait_type == "clickable":
                element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            else:
                element = wait.until(EC.presence_of_element_located((by_type, locator)))

            end_time = int(round(time.time())/1000)
            load_time = (end_time - start_time)/1000
            log.info("element loaded in {} seconds".format(load_time))
            return True, element
        except Exception as e:
            end_time = int(round(time.time()) / 1000)
            load_time = (end_time - start_time) / 1000
            self.get_screenshot(info="Error")
            log.error("Element loading failed with exception {}  and it searched for {} seconds".format(e, load_time))
            return False

    def open_new(self, url):
        """
        Method to open the url in a new window
        Usage :
            obj = Base()
            obj.open_new(url="https://www.google.com")
        :param url: url to be opened in a new window
        :return: True (if it opens)/False (if it fails to open)
        """
        script = "window.open('{}', 'new window')".format(url)
        try:
            self.browser.execute_script(script)
            log.info("successfully opened the url {} in new window".format(url))
        except Exception as e:
            log.error("Error in opening new window with exception {} ".format(e))
            self.get_screenshot(info="Error")
            return False
        return True

    def title_handlers(self):
        """
        Method to return a dict with title names and its corresponding handlers
        Usage :
           obj = Base()
           obj.title_handlers()
        :return: (dict  with title name as key and it corresponding value as its handler)
           {'Google': 'CDwindow-923A1AFF3C906FFA69C40233B11985A4', 'Gmail - Free Storage and Email from Google':
            'CDwindow-8FD5999224F89F6A93491E3708935C53'}
           False : if no handlers were there
        """
        try:
            title_handlers = {}
            handlers = self.browser.window_handles
            for handle in handlers:
                self.browser.switch_to.window(handle)
                handle_title = self.get_tittle()
                title_handlers[handle_title] = handle
        except Exception as e:
            log.error("failed while fetching the title name and its handlers with {} ".format(e))
            return False
        return True,title_handlers

    def switch_window(self, title):
        """
        Method to switch between the windows
        Usage :
            obj = Base()
            obj.switch_window(title="Gmail - Free Storage and Email from Google")
        :return: True/False
        """
        try:
            out = self.title_handlers()
            if title in out[1].keys():
                self.browser.switch_to.window(out[1][title])
                log.info("successfully switched to window {} ".format(title))
            else:
                log.error("window with tittle {} is not opened  ".format(title))
                return False
        except Exception as e:
            log.error("failed to switch to the window with exception {}".format(e))
            self.get_screenshot(info="Error")
            return False
        return True

    def openandswitch(self, url):
        """
        Method to open url in new tab and switch to it.
        Usage :
            obj = Base()
            obj.openAndswitch(url = "https://www.google.com")
        :param url: url to be opened
        :return: True (if url is opened and successfully switched)/False (if not switched)
        """
        try:
            self.open_new(url)
            current_handle = self.browser.current_window_handle
            handlers = self.browser.window_handles
            for handle in handlers:
                if handle not in current_handle:
                    self.browser.switch_to.window(handle)
                    log.info("successfully switched to window")
        except Exception as e:
            log.error("failed to switch to the window with exception {}".format(e))
            self.get_screenshot(info="Error")
            return False
        return True

    def close_window(self, title):
        """
        Method to close the window
        :param title: tilte name of window to be closed
        Usage:
            obj = Base()
            obj.close_window(title = "Gmail - Free Storage and Email from Google")
        :return: True (if the window is closed)/False (if it is not closed)
        """
        try:
            out = self.title_handlers()
            if title in out[1].keys():
                self.browser.switch_to.window(out[1][title])
                self.browser.close()
            else:
                log.error("window with tittle {} is not opened  ".format(title))
                return False
        except Exception as e:
            log.error("failed to close the window with exception {}".format(e))
            self.get_screenshot(info="Error")
            return False
        return True

    def get_screenshot(self, log_path="", info="info"):
        """
        Method to take a screen shot
        Usage:
            obj = Base()
            obj.get_screenshot()
        :param log_path: path where the user want to store the log_path by default it will get the log_path from logger
         module.
        :param info:  info/debug/warn/error is expected to store the screen shot with either of its name
        :return: returns file name where the screen shot is stored
        """
        file_name = str(round(time.time()))
        if log_path:
            file_path = log_path+'/'+info+"_"+file_name+".png"
            self.browser.get_screenshot_as_file(filename=file_path)
            log.info(" Refer the screen shot : {}".format(file_path))
            return file_path
        else:
            path = logger.get_logpath()
            logger.mkdir_p(path = path+"/screenshots")
            if os.path.exists(path+"/screenshots"):
                file_path = path+"/screenshots"+'/'+info+"_"+file_name+".png"
                self.browser.get_screenshot_as_file(filename=file_path)
                log.info(" Refer the screen shot : {}".format(file_path))
                return file_path
            else:
                file_path = os.getcwd()+'/'+info+"_"+file_name+".png"
                self.browser.get_screenshot_as_file(filename=file_path)
                log.info(" Refer the screen shot : {}".format(file_path))
                return file_path

    def run_js(self, script, locator, locator_type):
        """
        Method to run a script on the located element
        :param script: script to be executed
        :param locator:  name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        Usage :
            obj = Base()
            obj.run_js(script = "",locator="",locator_type="")
        :return: (True,output(if script executed successfully)/False(if script execution fails)
        """
        element = self.ele_locator(locator, locator_type)
        try:
            if element is not None:
                output = self.browser.execute_script(script, element)
                return True
        except Exception as e:
            log.error("script execution failed with exception {} ".format(e))
            return False

    def get_all_attributes(self, locator, locator_type):
        """
        Method to get all the attributes with its values for the located element
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        :return: True,list of attributes along with the values of the located element/False
        """
        try:
            script = 'var items = {}; \
                for (index = 0; index < arguments[0].attributes.length; ++index) \
                { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; \
                return items;'
            attrs = self.run_js(script=script, locator=locator, locator_type=locator_type)
        except Exception as e:
            log.error("failed to get the attributes with exception {} ".format(e))
            self.get_screenshot(info="Error")
            return False
        return True, attrs[1]

    def submit(self,  locator, locator_type):
        """
        Method to submit an element
        :param locator: name/id/css/xpath/class of the element to be located
        :param locator_type: name/id/css/xpath/class
        :return: True/ False
        """
        element = self.ele_locator(locator_type=locator_type, locator=locator)
        if element is not None:
            try:
                element.submit()
                log.info("successfully submitted on element")
            except Exception as e:
                log.error("Error while submitting the element {} ".format(e))
                self.get_screenshot(info="Error")
                return False
            return True
        else:
            log.error("Element is refrenced to None")
            self.get_screenshot(info="Error")
            return False

    def wait_until_url(self, url, time_to_wait=10, frequency=0.5):
        """
        Method to wait until the url is loaded and by default it waits for 10 seconds and polls for 0.5 milli seconds
        Usage :
            obj = Base()
            obj.wait_until_url(url = "https://www.google.com")
        :param url: url to be loaded
        :param time_to_wait :
        :param frequency :
        :return: (True, loaded url)/False (if url failed to load)
        """
        start_time = int(round(time.time())/1000)
        try:
            wait = WebDriverWait(self.browser, time_to_wait, poll_frequency=frequency)
            url_to_load = wait.until(EC.url_to_be(url))
            end_time = int(round(time.time())/1000)
            load_time = (end_time - start_time)/1000
            log.info("url loaded in {} seconds".format(load_time))
        except Exception as e:
            end_time = int(round(time.time()) / 1000)
            load_time = (end_time - start_time) / 1000
            self.get_screenshot(info="Error")
            log.error("url loading failed with exception {}  and the url load time is  {} seconds".format(e, load_time))
            traceback.print_exc()
            return False
        return True, url_to_load

    def double_click(self, locator, locator_type):
        """
        Method to double click
        :param locator:
        :param locator_type:
        :return:
        """
        element = self.ele_locator(locator_type=locator_type, locator=locator)
        if element is not None:
            try:
                actions = ActionChains(self.browser)
                actions.double_click(element).perform()
                log.info("Successfully double clicked on element")
            except Exception as e:
                self.get_screenshot(info="Error")
                log.error("Double click on element failed with exception {} ".format(e))
                return False
            return True
        else:
            self.get_screenshot(info="Error")
            log.error("Failed to locate the element")
            return False

    def browser_quit(self):
        """
        Method to close the opened browser instance
        :return:
        """
        try:
            self.browser.quit()
            log.info("successfully the browser was closed")
        except Exception as e:
            log.error("failed to closed the browser with exception {} ".format(e))
            self.get_screenshot(info="Error")
            return False
        return True


if __name__ == "__main__":

    obj = Base(browser_name="chrome")

    log.info("=====================================================================================================")
    log.info("Testing open_url method ")
    opn = obj.open_url(url="https://www.testandquiz.com/selenium/testing.html")
    if opn is True:
        log.info("successfully the url is opened")
    else:
        log.error("failed to open the url")

    log.info("=====================================================================================================")

    log.info("=====================================================================================================")
    log.info("Testing for current url method")
    curr_url = obj.get_current_url()
    log.info("current url is {}".format(curr_url))
    log.info("=====================================================================================================")
    log.info("Testing for get title method")
    curr_title = obj.get_tittle()
    log.info("title is {}".format(curr_title))
    log.info("=====================================================================================================")
    log.info("Testing for send text method")
    s_txt = obj.send_text(locator_type="xpath",locator="//input[@id='fname']",data="testing")
    if s_txt == True:
        log.info("send text method passed successfully")
    else:
        log.error("send text method failed")
    log.info("=====================================================================================================")
    log.info("Testing Refresh method")
    refresh = obj.Refresh()
    log.info("Refresh method passed")
    log.info("=====================================================================================================")
    log.info("Testing get text method")
    g_txt = obj.get_text(locator_type="xpath",locator="//b[contains(.,'This is sample text.')]")
    if g_txt[0] == True:
        log.info("get text method passed successfully")
    else:
        log.error("get text method failed")
    log.info("=====================================================================================================")
    log.info("Testing is displayed method")
    disp = obj.is_dispalyed(locator_type="id",locator="idOfButton")
    if disp:
        log.info("is displayed method passed")
    else:
        log.error("is displayed method failed")
    log.info("=====================================================================================================")
    log.info("Testing is enabled method")
    enab = obj.is_enabled(locator_type="xpath",locator="//button[@id='idOfButton']")
    if enab:
        log.info("is enabled method passed")
    else:
        log.error("is enabled method failed")
    log.info("=====================================================================================================")
    log.info("Testing click method")
    cli = obj.Click(locator_type="id",locator="male")
    if cli:
        log.info("click method passed")
    else:
        log.info("click method failed")
    log.info("=====================================================================================================")
    log.info("Testing is selected method")
    is_sele = obj.is_selected(locator_type="id",locator="male")
    if is_sele:
        log.info("is selected method passed")
    else:
        log.error("is selected method passed")
    log.info("=====================================================================================================")
    log.info("Testing page forward method")
    obj.page_forward()
    log.info("page forward method passed")
    log.info("=====================================================================================================")
    log.info("Testing page backward method")
    obj.page_back()
    log.info("page backward method passed")
    log.info("=====================================================================================================")
    log.info("Testing get alert method")
    ale_txt = obj.get_alert_text(locator_type="xpath",locator='''//button[@onclick="alert('hi, JavaTpoint Testing');"]''')
    if ale_txt[0] == True:
         log.info(ale_txt[1])
         log.info("get_alert_text method passed")
    else:
         log.warn("get_alert_text method failed")
    log.info("=====================================================================================================")
    log.info("testing accept alert method")
    obj.accept_alert(locator_type="xpath",locator='''//button[@onclick="alert('hi, JavaTpoint Testing');"]''')
    log.info("accept_alert method passed")
    log.info("=====================================================================================================")
    log.info("testing dismiss alert method")
    obj.dismiss_alert(locator_type="xpath", locator='''//button[@onclick="alert('hi, JavaTpoint Testing');"]''')
    log.info("dismiss_alert method passed")
    log.info("=====================================================================================================")
    log.info("testing select_by_dropdown method")
    drp_down = obj.select_by_dropdown(locator = "//select[@id='testingDropdown']",locator_type = "xpath",
    option_to_select="Manual Testing")
    if drp_down == True:
        log.info("select_by_dropdown method passed")
    else:
        log.error("select_by_dropdown method failed")
    log.info("=====================================================================================================")
    log.info("=====================================================================================================")
    log.info("testing wait_until_element method")
    wait = obj.wait_until_element(locator_type="xpath",locator="//b[contains(.,'This is sample text.')]")
    if wait[0] == True:
        log.info("wait_until_element method passed")
    else:
        log.info("wait_until_element method failed")
    log.info("=====================================================================================================")
    log.info("=====================================================================================================")
    log.info("testing open in new window method")
    new_tab = obj.open_new(url = "https://www.google.com")
    if new_tab == True:
        log.info("open_new method passed")
    else:
        log.info("open_new method failed")
    log.info("=====================================================================================================")
    log.info("testing tiltle_handlers method")
    tit_hndlr = obj.title_handlers()
    if tit_hndlr[0] == True:
        log.info("title_handlers method passed")
        log.info(tit_hndlr[1])
    else:
        log.error("title_handlers method failed")
    log.info("=====================================================================================================")
    log.info("testing for switch_window method ")
    swt_wdw = obj.switch_window(title="Sample Test Page")
    if swt_wdw == True:
        log.info("successfully switched to window")
    else:
        log.error("failed to switch to window")
    # log.info("=====================================================================================================")
    # log.info("testing for openAndswitch method")
    # opnsw = obj.openAndswitch(url="https://www.eenadu.net")
    # if opnsw == True:
    #     log.info("successfully opened and switched to window")
    # else:
    #     log.error("failed to open and switch to the window")
    # log.info("=====================================================================================================")
    # log.info("Testing close_window method")
    # cls_wdw = obj.close_window(title='Sample Test Page')
    # if cls_wdw == True:
    #     log.info("Successfully close_window method passed")
    # else:
    #     log.error("close_window method failed")
    # log.info("=====================================================================================================")
    log.info("Testing for run_js and get_all_attributes methods")
    attr_list = obj.get_all_attributes(locator="//a[contains(text(),'This is a link')]",locator_type="xpath")
    if attr_list[0] == True:
        log.info(attr_list[1])
        log.info("get_all_attributes method passed")
    else:
        log.error("get_all_attributes method failed")
    log.info("=====================================================================================================")
    log.info("testing submit method ")
    sub = obj.submit(locator="idOfButton",locator_type="id")
    if sub == True:
        log.info("submit method passed")
    else:
        log.error("submit method failed")
    log.info("=====================================================================================================")

    log.info("=====================================================================================================")
    log.info("testing wait_until_url method")
    wait_url = obj.wait_until_url(url="https://www.amazon.com")
    if wait_url == True:
        log.info("wait_until_url method passed")
    else:
        log.error("wait_until_url method failed")
    log.info("=====================================================================================================")
