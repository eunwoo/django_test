from statistics import mode
from django.db import models


from user.models import CustomUser
from system_manager.models import DocsFile, InstallLocate

# 구조 안전성 검토 신고서 관련 문서


class SafetyReport(models.Model):
    docNum = models.AutoField(primary_key=True)
    date = models.DateField()  # 작성 일자
    title = models.CharField(max_length=90)  # 제목
    constructType = models.CharField(max_length=90)  # 공증
    text = models.TextField()  # 내용
    isReadAgent = models.BooleanField(default=False)  # 에이전트 읽음 여부
    isReadGeneralEngineer = models.BooleanField(null=True)
    isReadTotalEngineer = models.BooleanField(null=True)
    isCheckManager = models.BooleanField(null=True)
    isCheckAgent = models.BooleanField(null=True)
    isCheckGeneralEngineer = models.BooleanField(null=True)

    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="safety_report_writer",
        null=True,
    )
    agentId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="safety_report_agent",
        null=True,
    )
    generalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="safety_report_general_engineer",
    )
    totalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="safety_report_total_engineer",
    )

    def __str__(self):
        return self.title


class SafetyCheckType(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class SafetyCheckMenu(models.Model):
    content = models.TextField()
    checkType = models.ForeignKey(SafetyCheckType, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class SafetyCheckList(models.Model):
    class ResultChoice(models.IntegerChoices):
        YES = 1
        NO = 2
        NOT_INCLUDE = 3

    result = models.IntegerField(choices=ResultChoice.choices)
    safetyReportId = models.ForeignKey(
        SafetyReport, on_delete=models.CASCADE, related_name="safety_check_list"
    )
    safetyCheckMenuId = models.ForeignKey(
        SafetyCheckMenu, on_delete=models.CASCADE, related_name="safety_check_list"
    )

    def __str__(self):
        return str(self.result)


# =============================================================================


# 자재 공급원 신고서 관련 문서
class MaterialSupplyReport(models.Model):
    docNum = models.AutoField(primary_key=True)
    date = models.DateField()  # 작성 일자
    title = models.CharField(max_length=90)  # 제목
    constructType = models.CharField(max_length=90)  # 공증
    text = models.TextField()  # 내용
    acceptDocs = models.ForeignKey(
        DocsFile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="material_supply_report_accept_docs",
    )

    isReadAgent = models.BooleanField(default=False)  # 에이전트 읽음 여부
    isReadGeneralEngineer = models.BooleanField(null=True)
    isReadTotalEngineer = models.BooleanField(null=True)
    isCheckManager = models.BooleanField(null=True)
    isCheckAgent = models.BooleanField(null=True)
    isCheckGeneralEngineer = models.BooleanField(null=True)

    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="material_report_writer",
        null=True,
    )
    agentId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="material_report_agent",
        null=True,
    )
    generalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="material_report_general_engineer",
    )
    totalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="material_report_total_engineer",
    )

    def __str__(self):
        return self.title


class SupplyList(models.Model):
    name = models.CharField(max_length=60)  # 공급업체명
    goods = models.CharField(max_length=60)  # 품명
    size = models.CharField(max_length=60)  # 규격
    etc = models.TextField()  # 비고
    materialSupplyReportId = models.ForeignKey(
        MaterialSupplyReport, on_delete=models.CASCADE, related_name="supply_list"
    )

    def __str__(self):
        return self.name


class MaterialDocs(models.Model):
    title = models.CharField(max_length=60)  # 문서 이름
    docs = models.FileField(upload_to="material_docs/")  # 파일 업로드
    type = models.CharField(max_length=60)  # 문서 타입
    materialSupplyReportId = models.ForeignKey(
        MaterialSupplyReport, on_delete=models.CASCADE, related_name="material_docs"
    )

    def __str__(self):
        return self.title


# =============================================================================

# 품질검사 의뢰서 관련 문서
class QualityInspectionRequest(models.Model):
    docNum = models.AutoField(primary_key=True)
    goods = models.CharField(max_length=60)  # 품명
    size = models.CharField(max_length=60)  # 규격
    sampleQuentity = models.TextField()  # 시료량
    sampleOrigin = models.TextField()  # 시료 또는 자제 생산국
    testType = models.CharField(max_length=60)  # 시험검사 종목
    locateId = models.ForeignKey(
        InstallLocate, on_delete=models.SET_NULL, null=True
    )  # 시료 채취 장소
    sampleDate = models.DateField()  # 시료 채취 일자
    testStandard = models.CharField(max_length=60)  # 시험 및 시방 기준

    isReadAgent = models.BooleanField(default=False)  # 에이전트 읽음 여부
    isReadGeneralEngineer = models.BooleanField(null=True)
    isReadTotalEngineer = models.BooleanField(null=True)
    isCheckManager = models.BooleanField(null=True)
    isCheckAgent = models.BooleanField(null=True)
    isCheckGeneralEngineer = models.BooleanField(null=True)

    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="material_report_writer",
        null=True,
    )
    agentId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="material_report_agent",
        null=True,
    )
    generalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="material_report_general_engineer",
    )
    totalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="material_report_total_engineer",
    )

    def __str__(self):
        return self.title
