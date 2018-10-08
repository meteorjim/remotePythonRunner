from selenium import webdriver
from selenium.webdriver.support import expected_conditions as excon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import logging
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]\t[%(filename)s:%(lineno)d]: %(message)s')
driver = webdriver.PhantomJS(executable_path='/Users/jim/Downloads/phantomjs/bin/phantomjs')
# driver = webdriver.Chrome(executable_path='/Users/jim/Downloads/phantomjs/bin/chromedriver')
driver.set_window_size(1920,1080)


def get_absolute_xpath(element):
    with open('selenium_plus/xpath.js','r') as jsfile:
        xpath_script = jsfile.read()
    return driver.execute_script(xpath_script, element)


def high_light_element(element, background='yellow', border='green'):
    driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",element, "background:%s ;border:4px solid %s;" % (background, border))
    # driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",element, "border:1px solid %s;"%(border))


if __name__ == '__main__':
    logging.info('start get address')
    # driver.get('https://blog.csdn.net/zwq912318834/article/details/79262007')
    driver.get('https://login.taobao.com/member/login.jhtml')
    # driver.get('https://www.taobao.com/')
    logging.info('start getting xpath')
    all_elements = driver.find_elements_by_xpath("//a")
    all_elements.extend(driver.find_elements_by_xpath("//a/*"))
    # all_elements.extend(driver.find_elements_by_xpath("//input"))
    # all_elements.extend(driver.find_elements_by_xpath("//input/*"))
    # all_elements.extend(driver.find_elements_by_xpath("//button"))
    # all_elements.extend(driver.find_elements_by_xpath("//button/*"))
    # all_elements.extend(driver.find_elements_by_xpath("//img"))
    # all_elements.extend(driver.find_elements_by_xpath("//img/*"))
    # all_elements.extend(driver.find_elements_by_xpath("//image"))
    # all_elements.extend(driver.find_elements_by_xpath("//image/*"))
    displayed_elements = []
    logging.info('proccessing!!!!!')
    for element in all_elements :
        try:
            if element.is_displayed():
                # print(get_absolute_xpath(element))
                high_light_element(element)
                displayed_elements.append(element)
                # print(get_absolute_xpath(element))
        except Exception as exception:
            logging.error('this element has no longer exist:%s',element)
            continue
            # logging.error(exception)
    logging.info('\nall_element is %s\ninteractable element is %s',len(all_elements),len(displayed_elements))
    driver.save_screenshot('screeshot.png')
    logging.info('done')
    driver.stop_client()
    driver.close()
