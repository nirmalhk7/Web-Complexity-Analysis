from browsermobproxy import Server
from selenium import webdriver
import json


class CreateHar(object):
    """create HTTP archive file"""

    def __init__(self, mob_path):
        """initial setup"""
        self.browser_mob = mob_path
        self.server = self.driver = self.proxy = None

    @staticmethod
    def __store_into_file(title, result):
        """store result"""
        har_file = open(title + '.har', 'w')
        har_file.write(str(result))
        har_file.close()

    def __start_server(self):
        """prepare and start server"""
        server_port=8090
        self.server = Server(self.browser_mob,options={'port':server_port})
        self.server.start()
        self.proxy = self.server.create_proxy()
        print("browsermob-proxy active on {}".format(server_port))

    def __start_driver(self):
        """prepare and start driver"""
        profile = webdriver.Chrome()
        # profile = webdriver.FirefoxProfile()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        options.add_argument("--proxy-server={}".format(self.proxy.selenium_proxy))
        # profile.set_proxy(self.proxy.selenium_proxy())
        self.driver = webdriver.Chrome(options=options)

    def start_all(self):
        """start server and driver"""
        self.__start_server()
        self.__start_driver()

    def create_har(self, title, url):
        """start request and parse response"""
        print("Requesting and parsing",url)
        self.proxy.new_har(title)
        self.driver.get(url)
        result = json.dumps(self.proxy.har, ensure_ascii=False)
        self.__store_into_file(title, result)

    def stop_all(self):
        """stop server and driver"""
        self.server.stop()
        self.driver.quit()