import scrapy
from ..items import WeixinSpiderItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from ..util import getScrapTime
import time
cookMap = {}
class weixin_spider(scrapy.spiders.Spider):
    name = "weixin"
    items = []
    def __init__(self, category=None, *args, **kwargs):
        super(weixin_spider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        try:
            print('准备进入 WeiXinSouGou...')
            self.driver = webdriver.Chrome(executable_path=(r'D:\C_Download\chromedriver_win32\chromedriver.exe'))
            self.driver.get("https://weixin.sogou.com/")
            self.query_key = category
            elem_input = self.driver.find_element_by_name("query")
            elem_input.send_keys(self.query_key)
            elem_input.send_keys(Keys.RETURN)
            time.sleep(2) #wait for two seconds
        except Exception as e:
            print("Error: ", e)

    def start_requests(self):
        pageNum = 10
        self.getContent()
        try:
            for i in range(2, pageNum + 1):
                elem_page = self.driver.find_elements_by_id("sogou_page_" + str(i))[0]
                elem_page.click()
                self.getContent()
        except BaseException as e:
            print("Error: ",e)
            self.driver.quit()
        yield scrapy.Request(url="https://ctf.sixstars.team/", callback=self.parse)

    def parse(self,response):
        for item in self.items:
            yield item

    def getContent(self):
        pagecounts = 10
        time.sleep(2)
        driver = self.driver
        try:
            for i in range(pagecounts):
                data = WeixinSpiderItem()
                elem = driver.find_elements_by_css_selector("h3 a")[i]
                data['title'] = elem.text
                data['uniid'] = data['url'] = elem.get_attribute("href")
                data['sendtime'] = driver.find_elements_by_css_selector("span.s2")[i].text
                data['scraptime'] = getScrapTime()
                data['searchstr'] = self.query_key
                driver.find_elements_by_css_selector("h3 a")[i].click()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[i + 2])
                data['content'] = driver.find_elements_by_css_selector("div#js_article")[0].text.replace("\n","").replace("'","")
                data['username'] = driver.find_elements_by_css_selector("a#js_name")[0].text
                driver.switch_to.window(driver.window_handles[0])
                self.items.append(data)
        except BaseException as e:
            raise RuntimeError("IP is sealed!")