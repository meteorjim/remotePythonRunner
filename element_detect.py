from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as excon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import logging
from time import sleep

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]\t[%(filename)s:%(lineno)d]: %(message)s')
# driver = webdriver.PhantomJS(executable_path='E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver = webdriver.PhantomJS(
    executable_path='/Users/jim/Downloads/phantomjs/bin/phantomjs')
# driver = webdriver.Chrome(executable_path='/Users/jim/Downloads/phantomjs/bin/chromedriver')
driver.set_window_size(1920, 1080)


def get_absolute_xpath(element):
    with open('xpath.js', 'r') as jsfile:
        xpath_script = jsfile.read()
    return driver.execute_script(xpath_script, element)


def high_light_element(element, background='yellow', border='green'):
    driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",
                          element, "background:%s ;border:4px solid %s;" % (background, border))


class AttributesElement(WebElement):
    def __init__(self, element, element_type='div'):
        self.element = element
        self.xpath = self._get_absolute_xpath()
        self.element_type = element_type
        self.element_id = self._get_element_id()
        self.element_class = self._get_element_class()

    def _get_absolute_xpath(self):
        with open('xpath.js', 'r') as jsfile:
            xpath_script = jsfile.read()
        return driver.execute_script(xpath_script, self.element)

    def _get_element_id(self):
        return driver.execute_script('return arguments[0].getAttribute("id")', self.element)

    def _get_element_class(self):
        return driver.execute_script('return arguments[0].getAttribute("class")', self.element)

    def get_parent(self):
        returnElement = driver.execute_script(
            'return arguments[0].parentElement', self.element)
        xpath_nodes = str.split(self.xpath, '/')
        return AttributesElement(returnElement, xpath_nodes[len(xpath_nodes)-2])

    def get_children(self):
        try:
            return driver.execute_script('return arguments[0].children', self.element)
        except Exception as ex:
            logging.error('no children found:%s', ex)
            return None

    def get_element(self):
        return self.element


if __name__ == '__main__':
    logging.info('start get address')
    driver.get('https://login.taobao.com/member/login.jhtml')
    aa = driver.find_elements_by_xpath('//a')
    bb = []
    for a in aa:
        b = AttributesElement(a, 'link')
        # print(b.get_parent().xpath)
        logging.info(b.get_parent().element_type)
        bb.append(b)
    driver.stop_client()
    driver.close()
