from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from time import sleep

url = 'https://xxx.com/category/80/svet/'
chromedriver = '/Users/xxx/Desktop/Work/scraper/xxx/chromedriver'

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

XPATH_LOAD_MORE_ITEMS = "//div[@class='more-items-wrapper']/a"
XPATH_GET_LINKS_DICT = "//div[@class='products-list-item-image']/a"
XPATH_GET_PRODUCT_INFO = "//div[@class='product-info']/h1"
XPATH_GET_PRODUCT_PRICE = "//div[@class='product-price']"
XPATH_GET_PRODUCT_TYPICAL = "//div[@class='typical']"
XPATH_GET_PRODUCT_IMG_SRC = "//li[@class='product-page-gallery-item']/img"

file_import = 'svet.txt'


class SeleniumScraper:
    """ Скрапер динамически подгружаемого контента """

    def __init__(self):
        """ Инициализируем браузер, устанавливаем настройки """

        self.browser = Chrome(chromedriver, options=self.opts)
        self.opts = Options()
        self.opts.headless = False
        self.opts.add_experimental_option('profile_refs', profile_refs)
        self.opts.add_argument(["start-maximized", "disable-infobars", "--disable-extensions"])

    def start_scraping(self):
        """ Подключаемся к url, запускаем скрапер """

        self.browser.get(url)
        sleep(4)
        self.load_more()
        self.get_links_dict()
        self.get_items_data()
        self.write_to_file()

    def load_more(self):
        """ Прогружаем все товарные позиции на страницу """

        print('Load items on page...')
        enabled = self.browser.find_element_by_xpath(XPATH_LOAD_MORE_ITEMS).is_displayed()
        while enabled:
            try:
                self.browser.find_element_by_xpath(XPATH_LOAD_MORE_ITEMS).click()
                sleep(2)
            except NoSuchElementException as error:
                print('NSEE')
                raise error
            except ElementNotInteractableException as error:
                print('ENIE')
                raise error

    def get_links_dict(self):
        """ Получаем список ссылок товаров на полностью прогруженной странице """

        links_dict = [e.get_attribute('href') for e in self.browser.find_elements_by_xpath(XPATH_GET_LINKS_DICT)]

        return links_dict

    def get_items_data(self):
        """ Проходимся по ссылкам, забираем необходимые данные """

        links_dict = self.get_links_dict()
        items = []
        for href in links_dict:
            try:
                self.browser.get(href)
                sleep(1)
                item_name = self.browser.find_element_by_xpath(XPATH_GET_PRODUCT_INFO).text
                item_cost = self.browser.find_element_by_xpath(XPATH_GET_PRODUCT_PRICE).text
                item_desc = self.browser.find_element_by_xpath(XPATH_GET_PRODUCT_TYPICAL).text
                item_img = self.browser.find_element_by_xpath(XPATH_GET_PRODUCT_IMG_SRC).get_attribute('src')

                item_info = f"{item_name}\t{item_cost}\t{item_desc}\t{item_img}\n"
                items.append(item_info)
            except NoSuchElementException:
                print('Cant find some Elements')
                continue

        return items

    def write_to_file(self):
        """ Записываем в файл полученные данные по товарам """

        items = self.get_items_data()
        with open(file_import, "w") as file:
            for item in items:
                file.write(item)
        file.close()
        self.browser.quit()


if __name__ == '__main__':
    data_scrapping = SeleniumScraper()
    data_scrapping.start_scraping()
