import logging
import os
from time import sleep

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as excon

from utility.image_recognition import img_varification_to_string


def get_absolute_xpath(element):
    with open('xpath.js', 'r') as jsfile:
        xpath_script = jsfile.read()
    return driver.execute_script(xpath_script, element)


def high_light_element(element, background='yellow', border='green'):
    driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",element, "background:%s ;border:4px solid %s;" % (background, border))


def get_element(attribute_element_list, target_label):
    for element in attribute_element_list:
        if target_label in element.element_text:
            return element
        elif target_label in element.element_id:
            return element
        elif target_label in element.element_class:
            return element
        elif target_label in element.get_parent().element_text:
            return element
        elif target_label in element.get_parent().element_id:
            return element
        elif target_label in element.get_parent().element_class:
            return element
        elif target_label in element.get_parent().get_parent().element_text:
            return element
        elif target_label in element.get_parent().get_parent().element_id:
            return element
        elif target_label in element.get_parent().get_parent().element_class:
            return element
    return None


def get_all_visible_attributes_elements(element_type, driver):
    all_elements = driver.find_elements_by_xpath(element_type)
    result = []
    for element in all_elements:
        if element.is_displayed():
            temp = AttributesElement(element, driver, element_type=element_type)
            result.append(temp)
    return result


class AttributesElement:
    def __init__(self, element, driver, element_type='div',):
        self.element = element
        self.xpath = self._get_absolute_xpath()
        self.element_type = element_type
        self.element_id = self._get_element_id()
        self.element_class = self._get_element_class()
        self.element_text = self.element.text

    def _get_absolute_xpath(self):
        with open('xpath.js', 'r') as jsfile:
            xpath_script = jsfile.read()
        return driver.execute_script(xpath_script, self.element)

    def _get_element_id(self):
        result = driver.execute_script('return arguments[0].getAttribute("id")', self.element)
        if result is None:
            return ''
        else:
            return result

    def send_keys(self, context):
        self.get_element().send_keys(context)

    def click(self):
        self.element.click()

    def _get_element_class(self):
        result = driver.execute_script('return arguments[0].getAttribute("class")', self.element)
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
        driver.save_screenshot('./temp_img/element.png')
        im = Image.open('./temp_img/element.png')
        im = im.crop((left, top, right, bottom))
        im.save('./temp_img/element.png')
        return './temp_img/element.png'

    def get_parent(self):
        returnElement = driver.execute_script('return arguments[0].parentElement', self.element)
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
    logging.basicConfig(level=logging.INFO,format='%(asctime)s [%(levelname)s]\t[%(filename)s:%(lineno)d]: %(message)s')
    driver = webdriver.PhantomJS(executable_path='/Users/jim/Downloads/phantomjs/bin/phantomjs')
    # driver = webdriver.Chrome(executable_path='/Users/jim/Downloads/phantomjs/bin/chromedriver')
    driver.set_window_size(1280, 1080)
    # driver.get('https://login.taobao.com/')
    driver.get('https://test.cmmat.com/mop')
    sleep(2)
    # 获取输入框
    all_elements = get_all_visible_attributes_elements('//input', driver)
    element = get_element(all_elements, '用户名')
    element.send_keys('18900001144')
    element = get_element(all_elements, '密码')
    element.send_keys('abcd1234')
    element = get_element(all_elements, '验证码')
    # 获取验证码图片
    all_elements = get_all_visible_attributes_elements('//img', driver)
    img_element = get_element(all_elements, '验证码')
    validate_str = img_varification_to_string(img_element.get_element_image_path(), 90)
    logging.info('varification is : %s',validate_str)
    element.send_keys(validate_str)
    all_elements = get_all_visible_attributes_elements('//button', driver)
    element = get_element(all_elements, '登 录')
    element.click()
    sleep(5)
    driver.save_screenshot('screeshot.png')
    driver.stop_client()
    driver.close()
