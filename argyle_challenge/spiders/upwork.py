import os
import json
import math
import shutil
from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from argyle_challenge import config as cf
import time


class UpworkSpider(Spider):
    name = 'upwork'
    allowed_domains = ['upwork.com']
    login_url = 'https://www.upwork.com/ab/account-security/login'
    api_url = 'https://www.upwork.com/ab/find-work/api/feeds/search?user_location_match=1'
    headers: dict = None
    item_count: int = None
    max_item_count: int = 100
    driver = webdriver.Chrome('../chromedriver')
    secret_header_text = "Let's make sure it's you"
    recaptcha_header = "Please verify you are a human"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        # shutil.rmtree('../info/errors', ignore_errors=True)

    def start_requests(self):
        """
        Handles the login portion of the spider
        :return: request to the upwork api
        """

        # create selenium driver and get login page
        self.driver.get(self.login_url)

        # login - reCaptcha
        if self.check_text_equals('//*[@class="page-title"]/h1/text()', self.recaptcha_header):
            input('''
            PAUSING SPIDER FOR RECAPTCHA...
              - complete the recaptha
              - once complete, press enter in the terminal to continue the spider
              
              ''')

        # login - username page
        username_input_box = '//*[@id="login_username"]'
        username_continue_btn = '//*[@id="login_password_continue"]'
        self.check_html_element_exists(username_input_box, 15, 'Timeout exception when getting the login page')
        self.form_input_and_click_btn(username_input_box, cf.arg_username, username_continue_btn)

        # login - password page
        password_input_box = '//*[@id="login_password"]'
        password_continue_btn = '//*[@id="login_control_continue"]'
        self.check_html_element_exists(password_input_box, 15, 'Timeout exception when getting the password page')
        self.form_input_and_click_btn(password_input_box, cf.arg_password, password_continue_btn)

        # login - secret answer page
        if self.check_text_equals('//h1/descendant::*/text()', self.secret_header_text):
            secret_input_box = '//*[@id="login_deviceAuthorization_answer"]'
            secret_continue_btn = '//*[@id="login_control_continue"]'
            self.check_html_element_exists(secret_input_box, 15, 'Timeout exception when getting the password page')
            self.form_input_and_click_btn(secret_input_box, cf.arg_secret_answer, secret_continue_btn)

        # logged in - list view page
        thumbs_down_btn = '//*[@class="job-feedback"]'
        self.check_html_element_exists(thumbs_down_btn, 15, 'Timeout exception when getting the list view page')
        cookies_string = '; '.join(
            [f"{cookie.get('name')}={cookie.get('value')}" for cookie in self.driver.get_cookies()]
        )
        self.headers = {
            'x-requested-with': 'XMLHttpRequest',
            'cookie': cookies_string
        }
        self.driver.quit()
        yield Request(url=self.api_url, headers=self.headers)

    def parse(self, response):
        # get pagination data from api
        data = json.loads(response.body)
        # TODO check api has the expected keys
        item_count = data.get('paging').get('total')
        number_of_pages = math.ceil(item_count / self.max_item_count)
        for page_number in range(number_of_pages):
            request = f"https://www.upwork.com/ab/find-work/api/feeds/search?paging={page_number};{item_count}&user_location_match=1"
            yield Request(url=request, headers=self.headers, callback=self.get_data_from_api)

    def get_data_from_api(self, response):
        data = json.loads(response.body)
        items = data.get('results')
        for item in items:
            print(item)

    # class helper functions ===========================================================================================
    def form_input_and_click_btn(self, input_xpath: str, input_value: str, continue_btn_xpath: str):
        self.driver.find_element_by_xpath(input_xpath).click()
        self.driver.find_element_by_xpath(input_xpath).send_keys(input_value)
        self.driver.find_element_by_xpath(continue_btn_xpath).click()

    def check_html_element_exists(self, element_xpath: str, wait_time: int, fail_message: str):
        try:
            element_present = EC.visibility_of_element_located((By.XPATH, element_xpath))
            WebDriverWait(self.driver, wait_time).until(element_present)
            time.sleep(2)
        except TimeoutException:
            self.driver.save_screenshot("../info/errors/screenshot.png")
            with open('../info/errors/page.html', 'w') as file:
                file.write(self.driver.page_source)
            self.driver.quit()
            raise CloseSpider(fail_message)

    def check_text_equals(self, text_xpath: str, text_check: str):
        sel = Selector(text=self.driver.page_source)
        text = sel.xpath(text_xpath).get()
        return text == text_check
