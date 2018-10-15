from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as excon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import logging

class AttributesElement:
    def __init__(self, element, driver, element_type='div',):
        self.element = element
        self.xpath = self._get_absolute_xpath()
        self.element_type = element_type
        self.driver = driver
        self.element_id = self._get_element_id()
        self.element_class = self._get_element_class()
        self.element_text = self.element.text

    def _get_absolute_xpath(self):
        with open('xpath.js', 'r') as jsfile:
            xpath_script = jsfile.read()
        return self.driver.execute_script(xpath_script, self.element)

    def _get_element_id(self):
        result = self.driver.execute_script('return arguments[0].getAttribute("id")', self.element)
        if result is None:
            return ''
        else:
            return result

    def send_keys(self, context):
        self.get_element().send_keys(context)

    def click(self):
        self.element.click()

    def _get_element_class(self):
        result = self.driver.execute_script('return arguments[0].getAttribute("class")', self.element)
        if result is None:
            return ''
        else:
            return result

    def _get_element_text(self):
        result = self.get_element().text
        if result is None:
            return ''
        else:
            return result

    def get_element_image_path(self):
        left = self.element.location['x']
        top = self.element.location['y']
        right = self.element.location['x'] + self.element.size['width']
        bottom = self.element.location['y'] + self.element.size['height']
        self.driver.save_screenshot('./temp_img/element.png')
        im = Image.open('./temp_img/element.png')
        im = im.crop((left, top, right, bottom))
        im.save('./temp_img/element.png')
        return './temp_img/element.png'

    def get_parent(self):
        returnElement = self.driver.execute_script('return arguments[0].parentElement', self.element)
        xpath_nodes = str.split(self.xpath, '/')
        return AttributesElement(returnElement, xpath_nodes[len(xpath_nodes)-2])

    def get_children(self):
        try:
            return self.driver.execute_script('return arguments[0].children', self.element)
        except Exception as ex:
            logging.error('no children found:%s', ex)
            return None

    def get_element(self):
        return self.element
