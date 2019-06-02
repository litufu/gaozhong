from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from database import GaoZhong, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import json
import time


engine = create_engine('sqlite:///gaozhong.sqlite?check_same_thread=False')
Base.metadata.bind = engine


class GaoZhongSpider(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        self.session = session
        self.provinces = [
            "四川省",
            "贵州省",
            "云南省",
            "西藏自治区",
            "陕西省",
            "甘肃省",
            "青海省",
            "宁夏回族自治区",
            "新疆维吾尔自治区",
        ]
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(
            executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
            options=chrome_options)
        self.driver.set_window_size(1200, 900)
        self.driver.get(url='https://gaokao.chsi.com.cn/zzbm/stu/info/queryXyxx.action')
        self.set_cookie()
        self.is_login()

    def is_login(self):
        # 判断是否登录
        html = self.driver.page_source
        if html.find('litufu@gewu.org.cn') == -1:  # 利用用户名判断是否登陆
            # 没登录 ,则手动登录
            print('你没有登录')
            self.login()

    def save_cookie(self):
        '''保存cookie'''
        # 将cookie序列化保存下来
        f1 = open('{}.txt'.format(self.username), 'w')
        f1.write(json.dumps(self.driver.get_cookies()))
        f1.close

    def set_cookie(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        try:
            f1 = open('{}.txt'.format(self.username))
            cookies = f1.read()
            cookies = json.loads(cookies)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            time.sleep(3)
        except Exception as e:
            print(e)

    def login(self):
        # 登陆
        print('start login ...')
        time.sleep(3)
        self.driver.find_element_by_id("username").click()
        user_input = self.driver.find_element_by_id("username")
        user_input.clear()
        user_input.send_keys(self.username)
        psw = self.driver.find_element_by_id("password")
        psw.clear()
        psw.send_keys(self.password)
        self.driver.find_element_by_class_name("button01").click()
        time.sleep(3)
        self.save_cookie()

    def get_code(self):
        self.driver.get(url="https://gaokao.chsi.com.cn/zzbm/stu/info/queryXyxx.action")
        time.sleep(3)
        province_select = self.driver.find_element_by_id('xjxxszdSslist')
        province_list = province_select.find_elements_by_tag_name('option')
        for province in province_list:
            province_code = province.get_attribute("value")
            province_name = province.text
            if province_name not in self.provinces:
                continue
            print("province is: " + province_code)
            print("province is:" + province_name)
            Select(province_select).select_by_value(province_code)
            time.sleep(3)
            city_select = self.driver.find_element_by_id('xjxxszdXjslist')
            city_list = city_select.find_elements_by_tag_name('option')
            for city in city_list:
                city_code = city.get_attribute("value")
                city_name = city.text
                print("city Value is: " + city_code)
                print("city Text is:" + city_name)
                Select(city_select).select_by_value(city_code)
                time.sleep(3)
                area_select = self.driver.find_element_by_id('xjxxszdDqlist')
                area_list = area_select.find_elements_by_tag_name('option')
                for area in area_list:
                    area_code = area.get_attribute("value")
                    area_name = area.text
                    print("area Value is: " + area_code)
                    print("area Text is:" + area_name)
                    Select(area_select).select_by_value(area_code)
                    time.sleep(3)
                    school_select = self.driver.find_element_by_id('xjxxszdXxlist')
                    school_list = school_select.find_elements_by_tag_name('option')
                    for school in school_list:
                        school_code = school.get_attribute("value")
                        school_name = school.text

                        print("school Value is: " + school_code)
                        print("school Text is:" + school_name)
                        if school_name == "请选择":
                            continue
                        if len(self.session.query(GaoZhong).filter(GaoZhong.shool_code == school_code).all()) > 0:
                            continue
                        gaozhong = GaoZhong(province_name=province_name,province_code=province_code,
                                            city_name=city_name,city_code=city_code,
                                            area_name=area_name,area_code=area_code,
                                            school_name=school_name,shool_code=school_code
                                            )
                        self.session.add(gaozhong)
                    self.session.commit()



if __name__ == '__main__':
    gaozhong = GaoZhongSpider(username='litufu@gewu.org.cn',password='123456abc')
    gaozhong.get_code()