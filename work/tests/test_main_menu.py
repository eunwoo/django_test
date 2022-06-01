from django.test import TestCase
from user.models import CustomUser
from django.core.files.images import ImageFile
from django.urls import reverse

# Create your tests here.


class MenuTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
            class2="현장 대리인",
            class3="해당 사항 없음",
            company="회사이름",
            name="홍길동",
            phone="010-7176-7735",
            register=False,
            signImage=ImageFile(open("tests/signimage.jpg", "rb")),
        )

    def login_general_manager(self):
        self.client.logout()
        self.client.login(username="testuser", password="testpassword2@")

    def login_supervisor(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword2@")

    def test_gm_menu(self):
        """
        일반 관리자 홈페이지 테스트
        """
        self.login_general_manager()
        response = self.client.get(reverse("work:index"))
        self.assertContains(response, "설치작업 점검")
        self.assertContains(response, "구조 안전성 검토")

    def test_agent_menu(self):
        """
        현장 대리인 홈페이지 테스트
        """
        self.login_supervisor()
        response = self.client.get(reverse("work:index"))
        self.assertNotContains(response, "설치작업 점검")
        self.assertContains(response, "구조 안전성 검토")
