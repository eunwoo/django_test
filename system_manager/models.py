from django.db import models

# 하나만 생성 가능
# 현장 등록
class Field(models.Model):
    title = models.CharField(max_length=90)  # 공사명
    callNum = models.CharField(max_length=20)  # 현장 전화번호
    address = models.TextField()  # 현장 주소
    orderer = models.CharField(max_length=30)  # 발주자 성함
    constructComp = models.CharField(max_length=40)  # 공사 회사
    supervision = models.CharField(max_length=40)  # 감리 및 CM 업체 명
    startDay = models.DateField()  # 공사 시작일
    endDay = models.DateField()  # 공사 종료일

    def __str__(self):
        return self.title


# 전문건설업체 관리자 연락처
class ConstructManager(models.Model):
    name = models.CharField(max_length=30)  # 공사 관리자 성함
    belong = models.CharField(max_length=30)  # 공사 관리자 소속
    phone = models.CharField(max_length=20)  # 공사 관리자 연락처

    def __str__(self):
        return self.name


# 관리대상 조립가설기자재 종류
class EquipmentTypes(models.Model):
    type = models.CharField(max_length=30)  # 종류 (강관 비계, 시스템 비계, 시스템 동바리 중 한 개)
    isActive = models.BooleanField(default=False)  # 활성화 여부

    def __str__(self):
        return self.type


# 설치 위치 클래스1
class InstallLocateClass1(models.Model):
    class1 = models.CharField(max_length=100)  # 클래스1


# 설치 위치 클래스3
class InstallLocateClass2(models.Model):
    class1 = models.ForeignKey(
        InstallLocateClass1, on_delete=models.CASCADE, related_name="class2"
    )  # 클래스1
    class2 = models.CharField(max_length=100)  # 클래스2


# 설치 위치 명
class InstallLocate(models.Model):
    class2 = models.ForeignKey(
        InstallLocateClass2, on_delete=models.CASCADE, related_name="class3"
    )  # 클래스2
    class3 = models.CharField(max_length=30)  # 구분 3

    def __str__(self):
        return self.class2.class1.class1 + " " + self.class2.class2 + " " + self.class3


# 설치 위치 구분
class LocateClass(models.Model):
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 문서 등록
class DocsFile(models.Model):
    file = models.FileField(upload_to="docs/")  # 파일
    filename = models.CharField(max_length=100)  # 파일명
    type = models.CharField(max_length=30, db_index=True)  # 파일 타입

    def __str__(self):
        return self.filename
