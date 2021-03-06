from django.db.models import (
    CharField,
    Value,
    F,
    Q,
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib import parse

from work.models import (
    SafetyReport,
    MaterialSupplyReport,
    QualityInspectionRequest,
    QualityPerformanceReport,
    BeforeInstallCheckList,
    InstallCheckList,
)

from system_manager.models import InstallLocate


# 리다이렉트 URL 설정
def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = parse.urlencode(kwargs, True)
    return HttpResponseRedirect(url + "?%s" % params)


# 결과보고 검색
def get_search_list(post_key, locate_value=0, search=""):
    union_list = list()
    # 구조 안전성 검토 결과
    if "safety" in post_key:
        type_list = []
        if "type1" in post_key:
            type_list.append("강관 비계")
        if "type2" in post_key:
            type_list.append("시스템 비계")
        if "type3" in post_key:
            type_list.append("시스템 동바리")
        q = Q()
        q.add(Q(checklistTitle__icontains=search), Q.OR)
        q.add(Q(title__icontains=search), Q.OR)
        q.add(Q(isSuccess=True), Q.AND)
        q.add(Q(checklistConstructType__in=type_list), Q.AND)
        if "locate" in post_key:
            q.add(Q(locateId=InstallLocate.objects.get(pk=locate_value)), Q.AND)
        add_query = (
            SafetyReport.objects.filter(q)
            .values("docNum", "created_at", "title")
            .annotate(type=Value("safety", output_field=CharField()))
        )
        for add_item in add_query:
            union_list.append(add_item)
    # 자재 공급 결과
    if "material" in post_key:
        add_query = (
            MaterialSupplyReport.objects.filter(
                isSuccess=True,
                title__icontains=search,
            )
            .values("docNum", "created_at", "title")
            .annotate(type=Value("material", output_field=CharField()))
        )
        for add_item in add_query:
            union_list.append(add_item)
    # 품질 검사 결과
    if "quality" in post_key:
        add_query = (
            QualityInspectionRequest.objects.filter(
                isSuccess=True,
                title__icontains=search,
            )
            .values("docNum", "created_at", "title")
            .annotate(type=Value("qty_request", output_field=CharField()))
        ).union(
            QualityPerformanceReport.objects.filter(
                isSuccess=True,
                title__icontains=search,
            )
            .values("docNum", "created_at", "title")
            .annotate(type=Value("qty_report", output_field=CharField()))
        )
        for add_item in add_query:
            union_list.append(add_item)
    # 설치작업 결과
    if "install" in post_key:
        type_list = []
        if "type1" in post_key:
            type_list.append("강관 비계")
        if "type2" in post_key:
            type_list.append("시스템 비계")
        if "type3" in post_key:
            type_list.append("시스템 동바리")
        if "locate" in post_key:
            before_install_query = (
                BeforeInstallCheckList.objects.filter(
                    equipment__in=type_list,
                    locateId=InstallLocate.objects.get(pk=locate_value),
                    title__icontains=search,
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "title", "equipment")
                .annotate(type=Value("beforechecklist", output_field=CharField()))
            )
            install_query = (
                InstallCheckList.objects.filter(
                    equipment__in=type_list,
                    locateId=InstallLocate.objects.get(pk=locate_value),
                    title__icontains=search,
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "title", "equipment")
                .annotate(type=Value("beforechecklist", output_field=CharField()))
            )
        else:
            before_install_query = (
                BeforeInstallCheckList.objects.filter(
                    equipment__in=type_list,
                    title__icontains=search,
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "title", "equipment")
                .annotate(type=Value("beforechecklist", output_field=CharField()))
            )
            install_query = (
                InstallCheckList.objects.filter(
                    equipment__in=type_list,
                    title__icontains=search,
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "title", "equipment")
                .annotate(type=Value("checklist", output_field=CharField()))
            )
        for add_item in before_install_query:
            union_list.append(add_item)
        for add_item in install_query:
            union_list.append(add_item)
    union_list.sort(key=lambda x: x["created_at"], reverse=True)
    return union_list
