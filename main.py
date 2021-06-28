from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from time import sleep

url = 'https://xxx.com/category/80/svet/'
file_import = 'svet.txt'
profile_refs = {'profile.default_content_setting_values': {'cookies': 2,
                                                           'images': 2,
                                                           'plugins': 2,
                                                           'popups': 2,
                                                           'geolocation': 2,
                                                           'notifications': 2,
                                                           'auto_select_certificate': 2,
                                                           'fullscreen': 2,
                                                           'mouselock': 2,
                                                           'mixed_script': 2,
                                                           'media_stream': 2,
                                                           'media_stream_mic': 2,
                                                           'media_stream_camera': 2,
                                                           'protocol_handlers': 2,
                                                           'ppapi_broker': 2,
                                                           'automatic_downloads': 2,
                                                           'midi_sysex': 2,
                                                           'push_messaging': 2,
                                                           'ssl_cert_decisions': 2,
                                                           'metro_switch_to_desktop': 2,
                                                           'protected_media_identifier': 2,
                                                           'app_banner': 2,
                                                           'site_engagement': 2,
                                                           'durable_storage': 2}}


class SeleniumScraper:
    """ Скрапер динамически подгружаемого контента """

    def __init__(self):
        """ Инициализируем браузер """

        opts = Options()
        opts.headless = False
        opts.add_experimental_option('profile_refs', profile_refs)
        opts.add_argument("start-maximized")
        opts.add_argument("disable-infobars")
        opts.add_argument("--disable-extensions")

        self.browser = Chrome('/Users/xxx/Desktop/Work/scraper/xxx/chromedriver', options=opts)

        self.browser.get(url)
        sleep(4)
        self.load_more()
        self.get_items()

    def load_more(self):
        print('Load items on page...')
        enabled = self.browser.find_element_by_xpath("//div[@class='more-items-wrapper']/a").is_displayed()
        while enabled:
            try:
                self.browser.find_element_by_xpath("//div[@class='more-items-wrapper']/a").click()
                sleep(2)
            except NoSuchElementException:
                print('NSEE')
                break
            except ElementNotInteractableException:
                print('ENIE')
                break

    def get_items(self):
        # Get hrefs from main(!loaded) items page.
        hrefs = [e.get_attribute('href') for e in self.browser.find_elements_by_xpath("//div[@class='products-list"
                                                                                      "-item-image']/a")]
        print('Get items')
        print(len(hrefs))
        # Go to item and take an info.
        items = []
        for href in hrefs:
            try:
                self.browser.get(href)
                sleep(1)
                item_name = self.browser.find_element_by_xpath("//div[@class='product-info']/h1").text
                item_cost = self.browser.find_element_by_xpath("//div[@class='product-price']").text
                item_desc = self.browser.find_element_by_xpath("//div[@class='typical']").text
                item_img = self.browser.find_element_by_xpath("//li[@class='product-page"
                                                              "-gallery-item']/img").get_attribute('src')

                item_info = f"{item_name}\t{item_cost}\t{item_desc}\t{item_img}\n"
                items.append(item_info)
            except NoSuchElementException:
                print('Cant find some Elements')
                continue

        with open(file_import, "w") as file:
            for item in items:
                file.write(item)
        file.close()
        self.browser.quit()


if __name__ == '__main__':
    data_scrapping = SeleniumScraper()
