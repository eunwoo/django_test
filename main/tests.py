from django.test import TestCase
from django.core.files.images import ImageFile
from user.models import CustomUser


# Create your tests here.
class MainPageTests(TestCase):
    @classmethod
    def setUpTestData(self):
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

        CustomUser.objects.create_user(
            username="testuser2",
            password="testpassword2@",
            class1="종합 건설 업체",
            class2="일반 사용자",
            class3="해당 사항 없음",
            company="회사이름",
            name="홍길동",
            phone="010-7176-7735",
            register=False,
            signImage=ImageFile(open("tests/signimage.jpg", "rb")),
        )

    def test_home_page_status_code(self):
        """
        홈페이지 테스트 (유저 미 로그인 상태)
        """
        response = self.client.get("/")
        self.assertEquals(response.status_code, 302)

    def register_user(self):
        """
        테스트 유저 등록
        """
        self.client.login(username="testuser", password="testpassword2@")

    def test_home_page_status_code_after_login(self):
        """
        홈페이지 테스트 (유저 로그인 상태)
        """
        self.register_user()
        response = self.client.get("/")
        self.assertContains(response, "시스템 관리자")
        self.assertContains(response, "기본정보 등록")
        self.assertEquals(response.status_code, 200)

    def test_home_page_with_not_register(self):
        """
        미승인 유저 홈페이지 접속
        """

        self.client.login(username="testuser2", password="testpassword2@")
        response = self.client.get("/")
        self.assertContains(response, "죄송합니다. 이 시스템에 대한 액세스 권한이 아직 부여되지 않았습니다.")

    def test_home_page_with_register_user(self):
        """
        승인 유저 홈페이지 접속
        """
        user = CustomUser.objects.get(username="testuser2")
        user.register = True
        user.save()
        self.client.login(username="testuser2", password="testpassword2@")
        response = self.client.get("/")
        self.assertContains(response, "일반 사용자")
        self.assertContains(response, "업무")
        self.assertNotContains(response, "기본정보 등록")
        self.assertEquals(response.status_code, 200)
