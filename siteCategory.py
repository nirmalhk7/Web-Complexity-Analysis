from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getCategory(url,driver):
    category="Unclassified"
    try:
        print("{}: Querying Category ".format(url.split('www.')[1]))
        driver.get('https://sitereview.bluecoat.com/#/lookup-result/'+url)
        driver.implicitly_wait(5)
        category= driver.find_elements_by_class_name('clickable-category')[0].get_attribute("textContent")
    except Exception as e:
        print("siteCategory",e,url)
    return category

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('ignore-certificate-errors')
    # options.add_argument("--proxy-server={}".format(proxy.proxy))
    driver = webdriver.Chrome(chrome_options=options)
    print(getCategory('www.biolink777.com',driver))
    driver.quit()
    pass