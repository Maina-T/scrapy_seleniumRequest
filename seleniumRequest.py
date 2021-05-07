import scrapy
from shutil import which
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class JumiaSpider(scrapy.Spider):
    name = 'jumia_test2'

    custom_settings = {
        'SELENIUM_DRIVER_NAME' : 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH' : which('chromedriver'),
        'SELENIUM_DRIVER_ARGUMENTS' : ['--headless'],
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy_selenium.SeleniumMiddleware': 800,
        },
        # '' : '',
        # '' : '',
    }


    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://www.jumia.co.ke/',
            wait_time = 3,
            screenshot = True,
            wait_until= EC.presence_of_element_located((By.XPATH, '//div[@class="sub"]')), # wait for element to occur
            callback = self.parse
        )

    def parse(self, response):
        # print(response.text)
        # img = response.meta['screenshot']
        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)


        
        # Handle pagination with scrapy-selenium
        next_page = response.xpath('//a[@aria-label="Next Page"]/@href').get() # next page url
            print(next_page)
            if next_page:
                absolute_url = f"https://www.jumia.co.ke{next_page}" # create next page absolute url
                yield SeleniumRequest(
                    url = absolute_url,
                    wait_time = 3,
                    callback = self.parse
                )