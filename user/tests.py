from user.models import CustomUser
from django.core.files.images import ImageFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        cls.selenium = webdriver.Firefox(options=opts)
        cls.selenium.implicitly_wait(10)
        cls.init_db()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def init_db(self):
        CustomUser.objects.create_user(
            username="testuser",
            password="testpassword2@",
            class1="종합 건설 업체",
            class2="일반 사용자",
            class3="해당 사항 없음",
            company="회사이름",
            name="홍길동",
            phone="010-7176-7735",
            is_system_manager=True,
            register=True,
            signImage=ImageFile(open("tests/signimage.jpg", "rb")),
        )

    def test_login(self):
        # 로그인 실패
        self.selenium.get("%s%s" % (self.live_server_url, "/user/login/"))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("testuser")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("testpassword2")
        self.selenium.find_element_by_xpath(
            "/html/body/main/section/div/form/div/div[2]/button"
        ).click()
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url + "/user/login/",
            "로그인 실패 테스트",
        )

        # 로그인 성공
        self.selenium.get("%s%s" % (self.live_server_url, "/user/login/"))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("testuser")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("testpassword2@")
        self.selenium.find_element_by_xpath(
            "/html/body/main/section/div/form/div/div[2]/button"
        ).click()
        self.assertEqual(
            self.selenium.current_url, self.live_server_url + "/", "로그인 성공"
        )
