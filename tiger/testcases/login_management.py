import json
import pytest
import time
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
from libs import logger
from libs.tiger import Tiger

log = logger.get_logger(__name__)

with open('framework_mapping.json') as json_file:
    fwk_mapping = json.load(json_file)
    storage_url = fwk_mapping['url']['login_url'] + 'volume'

@pytest.fixture()
def setup():
    """
    This method does pre setup before running each testcase
    :return: (obj) tiger api obj
    """
    username = fwk_mapping['username']
    password = fwk_mapping['password']

    browser_name = fwk_mapping['login_mgmt']['browser']

    tiger_obj = Tiger(browser_name=browser_name)
    tiger_obj.login(username=username, password=password)

    running_flag = False

    log.info('waiting 60s for fetching tiger os status')
    curr_time = time.time()
    while not running_flag and time.time() <= curr_time + 60:
        running_flag = tiger_obj.tiger_running_status()

    if not running_flag:
        log.error('tiger os is not running .. starting tiger os')
        tiger_obj.start_tiger()

        log.info('waiting 60s for fetching tiger os status')
        curr_time = time.time()
        while not running_flag and time.time() <= curr_time + 60:
            running_flag = tiger_obj.tiger_running_status()
        if not running_flag:
            log.error('tiger os is not running .. quiting current instance')
            tiger_obj.browser_obj.browser_quit()
            assert False
        else:
            log.info('tiger os is running fine')
    else:
        log.info('tiger os is running fine')

    yield tiger_obj

    assert tiger_obj.browser_obj.browser_quit()

    return tiger_obj


def test_m19bqj_236(setup):
    """
    This method automated testcase M19BQJ-236
    :param setup: (obj) tiger class object
    :return:
    """
    tiger_obj = Tiger(browser_name=browser_name)
    tiger_obj.login(username=username, password=password)
