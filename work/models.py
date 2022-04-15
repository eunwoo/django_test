from django.db import models


from user.models import CustomUser
from system_manager.models import DocsFile, InstallLocate, Field

# 구조 안전성 검토 신고서 관련 문서


class SafetyReport(models.Model):
    docNum = models.AutoField(primary_key=True)
    date = models.DateField()  # 작성 일자
    title = models.CharField(max_length=90)  # 제목
    constructType = models.CharField(max_length=90)  # 공증
    text = models.TextField()  # 내용
    replyDate = models.DateField(null=True)  # 회신 일자
    result_choices = (
        ("1", "승인-제출한 내용대로 진행"),
        ("2", "조건부 승인-의견반영 후 진행"),
        ("3", "승인 불가"),
    )
    result = models.CharField(max_length=10, choices=result_choices)  # 결과 내용
    generalEngineerText = models.TextField(null=True)  # 담당자 의견
    totalEngineerText = models.TextField(null=True)  # 총괄 담당자 의견

    isSaveManager = models.BooleanField(default=False)
    isSaveAgent = models.BooleanField(default=False)
    isSaveGeneralEngineer = models.BooleanField(default=False)
    isSaveTotalEngineer = models.BooleanField(default=False)

    isCheckManager = models.BooleanField(default=False)
    isCheckAgent = models.BooleanField(default=False)
    isCheckGeneralEngineer = models.BooleanField(default=False)
    isSuccess = models.BooleanField(default=False)

    # 체크리스트 전용 속성
    checklistDate = models.DateField(null=True)
    checklistConstructType = models.CharField(max_length=90, null=True)

    docs = models.ManyToManyField(
        DocsFile,
        blank=True,
        related_name="safety_docs",
    )

    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="safety_report_writer",
        blank=True,
        null=True,
    )
    agentId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="safety_report_agent",
        blank=True,
        null=True,
    )
    generalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="safety_report_general_engineer",
    )
    totalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="safety_report_total_engineer",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    requested_at = models.DateTimeField(null=True)

    def __str__(self):
        return "구조 안전성 검토 신고서 - " + self.docNum


class SafetyCheckType(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class SafetyCheckMenu(models.Model):
    content = models.TextField()
    checkType = models.ForeignKey(SafetyCheckType, on_delete=models.CASCADE)
    initItem = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class SafetyCheckList(models.Model):
    result_choices = (
        ("1", "예"),
        ("2", "아니요"),
        ("3", "해당사항 없음"),
    )
    result = models.CharField(
        max_length=60,
        choices=result_choices,
        default="1",
    )
    safetyReportId = models.ForeignKey(
        SafetyReport,
        on_delete=models.CASCADE,
        related_name="safety_check_list",
    )
    safetyCheckMenuId = models.ForeignKey(
        SafetyCheckMenu,
        on_delete=models.CASCADE,
        related_name="safety_check_list",
    )

    def __str__(self):
        return str(self.result)


# =============================================================================


# 자재 공급원 신고서 관련 문서
class MaterialSupplyReport(models.Model):
    docNum = models.AutoField(primary_key=True)
    date = models.DateField()  # 작성 일자
    constructType = models.CharField(max_length=90)  # 공증
    text = models.TextField()  # 기타사항

    title = models.CharField(max_length=90)  # 제목
    replyDate = models.DateField(null=True)  # 회신 일자
    generalEngineerText = models.TextField(null=True)  # 담당자 의견
    totalEngineerText = models.TextField(null=True)  # 총괄 담당자 의견
    result_choices = (
        ("1", "승인-제출한 내용대로 진행"),
        ("2", "조건부 승인-의견반영 후 진행"),
        ("3", "승인 불가"),
    )
    fieldId = models.ForeignKey(
        Field,
        on_delete=models.SET_NULL,
        null=True,
        related_name="material_supply",
    )
    result = models.CharField(
        max_length=10,
        choices=result_choices,
        blank=True,
    )  # 결과 내용

    docs = models.ManyToManyField(
        DocsFile,
        blank=True,
        related_name="material_docs",
    )

    isSaveManager = models.BooleanField(default=False)
    isSaveAgent = models.BooleanField(default=False)
    isSaveGeneralEngineer = models.BooleanField(default=False)
    isSaveTotalEngineer = models.BooleanField(default=False)

    isCheckManager = models.BooleanField(default=False)
    isCheckAgent = models.BooleanField(default=False)
    isCheckGeneralEngineer = models.BooleanField(default=False)
    isSuccess = models.BooleanField(default=False)

    businessLicense = models.FileField(
        upload_to="business_license",
        blank=True,
        null=True,
    )  # 사업자 등록증
    deliveryPerformanceCertificate = models.FileField(
        upload_to="delivery_performance_certificate",
        blank=True,
        null=True,
    )  # 납품실적증명서
    safetyCertificate = models.FileField(
        upload_to="safety_certificate",
        blank=True,
        null=True,
    )  # 안전인증서
    qualityTestReport = models.FileField(
        upload_to="quality_test_report",
        blank=True,
        null=True,
    )  # 품질시험성적서
    testPerformanceComparisonTable = models.FileField(
        upload_to="test_performance_comparison_table",
        blank=True,
        null=True,
    )  # 시험성과대비표

    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="material_report_writer",
        blank=True,
        null=True,
    )
    agentId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="material_report_agent",
        blank=True,
        null=True,
    )
    generalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="material_report_general_engineer",
    )
    totalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="material_report_total_engineer",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "자재 공급원 신고서 - " + self.docNum


class SupplyList(models.Model):
    name = models.CharField(max_length=60)  # 공급업체명
    goods = models.CharField(max_length=60)  # 품명
    size = models.CharField(max_length=60)  # 규격
    etc = models.TextField()  # 비고
    materialSupplyReportId = models.ForeignKey(
        MaterialSupplyReport,
        on_delete=models.CASCADE,
        related_name="supply_list",
    )

    def __str__(self):
        return self.name


# 문서 등록
class MaterialDocs(models.Model):
    file = models.FileField(upload_to="docs/")  # 파일
    filename = models.CharField(max_length=100)  # 파일명
    type = models.CharField(max_length=30, db_index=True)  # 파일 타입
    materialSupplyReport = models.ForeignKey(
        MaterialSupplyReport,
        on_delete=models.CASCADE,
        related_name="material_docs",
    )

    def __str__(self):
        return self.filename


# =============================================================================

# 품질검사 의뢰서 관련 문서
class QualityInspectionRequest(models.Model):
    docNum = models.AutoField(primary_key=True)
    title = models.CharField(max_length=90)  # 제목
    goods_choice = [
        ("", "품명을 선택해 주세요"),
        ("1", "강관비계용 부재 (비계용 강관)"),
        ("2", "강관비계용 부재(강관조인트)"),
        ("3", "조립형비계 및 동바리부재(수직재)"),
        ("4", "조립형비계 및 동바리부재(수평재)"),
        ("5", "조립형비계 및 동바리부재(가새재)"),
        ("6", "조립형비계 및 동바리부재(트러스)"),
        ("7", "립형비계 및 동바리부재(연결조인트)"),
    ]
    goods = models.CharField(max_length=60, choices=goods_choice)  # 품명
    size = models.CharField(max_length=60)  # 규격
    sampleQuentity = models.TextField()  # 시료량
    sampleOrigin = models.TextField()  # 시료 또는 자제 생산국
    testType_hweem = models.BooleanField(default=False)  # 시험검사종목 - 휨하중
    testType_zip = models.BooleanField(default=False)  # 시험검사종목 - 압축하중
    testType_tensile = models.BooleanField(default=False)  # 시험검사종목 - 인장하중
    locateId = models.ForeignKey(
        InstallLocate, on_delete=models.SET_NULL, null=True
    )  # 시료 채취 장소
    sampleDate = models.DateField()  # 시료 채취 일자
    testStandard = models.CharField(max_length=60)  # 시험 및 시방 기준

    fieldId = models.ForeignKey(
        Field,
        on_delete=models.SET_NULL,
        null=True,
        related_name="quality_inspection_request",
    )
    isImportFacility = models.TextField()  # 국가 중요시설 여부

    orderDate = models.DateField(null=True)  # 의뢰일

    isSaveManager = models.BooleanField(default=False)
    isSaveAgent = models.BooleanField(default=False)
    isSaveGeneralEngineer = models.BooleanField(default=False)

    isCheckManager = models.BooleanField(default=False)
    isCheckAgent = models.BooleanField(default=False)
    isSuccess = models.BooleanField(default=False)  # 성공 여부

    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="quality_inspection_writer",
        blank=True,
        null=True,
    )
    agentId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="quality_inspection_agent",
        blank=True,
        null=True,
    )
    generalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="quality_inspection_general_engineer",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "품질검사 의뢰서 - " + self.docNum


# =============================================================================

# 품질검사 성과 총괄표 신고서


class QualityPerformanceReport(models.Model):
    docNum = models.AutoField(primary_key=True)  # 문서번호
    date = models.DateField()  # 작성일자
    title = models.CharField(max_length=90)  # 제목
    fieldId = models.ForeignKey(
        Field,
        on_delete=models.SET_NULL,
        null=True,
        related_name="quality_performance_report",
    )  # 현장등록

    isSaveManager = models.BooleanField(default=False)
    isSaveAgent = models.BooleanField(default=False)
    isSaveGeneralEngineer = models.BooleanField(default=False)
    isSaveTotalEngineer = models.BooleanField(default=False)

    isCheckManager = models.BooleanField(default=False)
    isCheckAgent = models.BooleanField(default=False)
    isCheckGeneralEngineer = models.BooleanField(default=False)
    isSuccess = models.BooleanField(default=False)

    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="quality_performance_writer",
        blank=True,
        null=True,
    )
    agentId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="quality_performance_agent",
        blank=True,
        null=True,
    )
    generalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="quality_performance_general_engineer",
    )
    totalEngineerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="quality_performance_total_engineer",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "품질검사 성과 총괄표 신고서 - " + self.docNum


class QualityPerformance(models.Model):  # 품질검사 성과 총괄표
    goods = models.CharField(max_length=60)  # 품명
    standard = models.CharField(max_length=60)  # 규격
    testType_hweem = models.BooleanField(default=False)  # 시험검사종목 - 휨하중
    testType_zip = models.BooleanField(default=False)  # 시험검사종목 - 압축하중
    testType_tensile = models.BooleanField(default=False)  # 시험검사종목 - 인장하중
    plan = models.IntegerField()  # 계획 횟수
    conducted = models.IntegerField()  # 실시 횟수
    acceptance = models.IntegerField()  # 합격 횟수
    failed = models.IntegerField()  # 불합격 횟수
    retest = models.IntegerField()  # 재시험 횟수
    add = models.TextField()  # 비고 란
    quality_performance_report_id = models.ForeignKey(
        QualityPerformanceReport,
        on_delete=models.CASCADE,
        related_name="quality_performance",
    )

    def __str__(self):
        return self.goods


class QualityPerformanceFile(models.Model):
    title = models.CharField(max_length=60)  # 파일이름
    doc = models.FileField(upload_to="quality_performance_file")  # 파일
    quality_performance_report_id = models.ForeignKey(
        QualityPerformanceReport,
        on_delete=models.CASCADE,
        related_name="quality_performance_file",
    )

    def __str__(self):
        return self.title


# =============================================================================

# 설치작업 전 체크리스트
class BeforeInstallCheckList(models.Model):
    # docNum <= 중간 삭제가 없으므로 생략해도 될듯
    date = models.DateField()  # 확인 일자
    title = models.CharField(max_length=90)  # 제목
    locateId = models.ForeignKey(
        InstallLocate,
        on_delete=models.SET_NULL,
        null=True,
        related_name="before_checklist",
    )  # 설치 위치명
    detailLocate = models.CharField(max_length=80, blank=True)  # 설치 위치 상세명
    equipment = models.CharField(
        max_length=60,
    )  # 강관 비계, 시스템 동바리, 시스템 비계 택1
    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="before_install_checklist_writer",
        null=True,
    )
    isSuccess = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BeforeInspectionItem(models.Model):
    title = models.CharField(max_length=60)  # 점검 항목
    equipment_choices = (("1", "강관 비계"), ("2", "시스템 비계"), ("3", "시스템 동바리"))
    equipment = models.CharField(
        max_length=60, choices=equipment_choices
    )  # 강관 비계, 시스템 동바리, 시스템 비계 택1
    init_item = models.BooleanField(default=False)  # 초기 점검 항목인지 여부


class BeforeInspectionResult(models.Model):
    result_choices = (("1", "양호"), ("2", "미흡"), ("3", "해당사항 없음"))
    result = models.CharField(
        max_length=10,
        choices=result_choices,
        default="1",
    )  # 결과
    content = models.TextField(blank=True)  # 조치사항 확인 내용
    before_install_checklist_id = models.ForeignKey(
        BeforeInstallCheckList,
        on_delete=models.CASCADE,
        related_name="before_inspection_result",
    )
    before_inspection_item_id = models.ForeignKey(
        BeforeInspectionItem,
        on_delete=models.SET_NULL,
        null=True,
        related_name="before_inspection_result",
    )


class BeforeMeasure(models.Model):
    img = models.ImageField(upload_to="before_measure")
    beforeInspectionResult = models.ForeignKey(
        BeforeInspectionResult,
        on_delete=models.CASCADE,
        related_name="measures",
        blank=True,
        null=True,
    )


# =============================================================================

# 설치작업 중 체크리스트
class InstallCheckList(models.Model):
    # docNum <= 중간 삭제가 없으므로 생략해도 될듯
    date = models.DateField()  # 확인 일자
    title = models.CharField(max_length=90)  # 제목
    locateId = models.ForeignKey(
        InstallLocate,
        on_delete=models.SET_NULL,
        null=True,
        related_name="install_checklist",
    )  # 설치 위치명
    detailLocate = models.CharField(max_length=80, blank=True)  # 설치 위치 상세명
    equipment = models.CharField(
        max_length=60,
    )  # 강관 비계, 시스템 동바리, 시스템 비계 택1
    writerId = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="install_checklist_writer",
        null=True,
    )
    isSuccess = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InspectionItemCategory(models.Model):
    type = models.CharField(max_length=60)  # 점검 항목 대분류


class InspectionItem(models.Model):
    title = models.CharField(max_length=60)  # 점검 항목
    categoryId = models.ForeignKey(
        InspectionItemCategory,
        on_delete=models.CASCADE,
        related_name="inspection_item",
    )
    equipment_choices = (("1", "강관 비계"), ("2", "시스템 비계"), ("3", "시스템 동바리"))
    equipment = models.CharField(
        max_length=60, choices=equipment_choices
    )  # 강관 비계, 시스템 동바리, 시스템 비계 택1
    init_item = models.BooleanField(default=False)  # 초기 점검 항목인지 여부


class InspectionResult(models.Model):
    result_choices = (("1", "양호"), ("2", "미흡"), ("3", "해당사항 없음"))
    result = models.CharField(
        max_length=10,
        choices=result_choices,
        default="1",
    )  # 결과
    content = models.TextField()  # 조치사항 확인 내용
    install_checklist_id = models.ForeignKey(
        InstallCheckList,
        on_delete=models.CASCADE,
        related_name="inspection_result",
    )
    inspection_item_id = models.ForeignKey(
        InspectionItem,
        on_delete=models.SET_NULL,
        null=True,
        related_name="inspection_result",
    )


class Measure(models.Model):
    img = models.ImageField(upload_to="measure")
    inspectionResult = models.ForeignKey(
        InspectionResult,
        on_delete=models.CASCADE,
        related_name="measures",
        blank=True,
        null=True,
    )
