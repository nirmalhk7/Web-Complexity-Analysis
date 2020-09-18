from selenium import webdriver
import time

options = webdriver.ChromeOptions()

options.add_argument('headless')

options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(chrome_options=options)

driver.get('https://facebook.com')

driver.implicitly_wait(5)

email = driver.find_element_by_css_selector('input[type=text]')

password = driver.find_element_by_css_selector('input[type=password]')

login = driver.find_element_by_css_selector('#u_0_b')

email.send_keys('0123456789')

password.send_keys('0123456789')

driver.get_screenshot_as_file('main-page.png')

login.click()

driver.get('https://www.facebook.com/')

driver.get_screenshot_as_file('evan-profile.png')
