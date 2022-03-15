from django.db.models import CharField, Value, F
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


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = parse.urlencode(kwargs, True)
    return HttpResponseRedirect(url + "?%s" % params)


def get_search_list(post_key, locate_value=0):
    union_list = list()
    if "safety" in post_key:
        add_query = (
            SafetyReport.objects.all()
            .values("docNum", "created_at")
            .annotate(type=Value("safety", output_field=CharField()))
        )
        for add_item in add_query:
            union_list.append(add_item)
    if "material" in post_key:
        add_query = (
            MaterialSupplyReport.objects.all()
            .values("docNum", "created_at")
            .annotate(type=Value("material", output_field=CharField()))
        )
        for add_item in add_query:
            union_list.append(add_item)
    if "quality" in post_key:
        add_query = (
            QualityInspectionRequest.objects.all()
            .values("docNum", "created_at")
            .annotate(type=Value("qty_request", output_field=CharField()))
        ).union(
            QualityPerformanceReport.objects.all()
            .values("docNum", "created_at")
            .annotate(type=Value("qty_report", output_field=CharField()))
        )
        for add_item in add_query:
            union_list.append(add_item)
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
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "equipment")
                .annotate(type=Value("beforechecklist", output_field=CharField()))
            )
            install_query = (
                InstallCheckList.objects.filter(
                    equipment__in=type_list,
                    locateId=InstallLocate.objects.get(pk=locate_value),
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "equipment")
                .annotate(type=Value("beforechecklist", output_field=CharField()))
            )
        else:
            before_install_query = (
                BeforeInstallCheckList.objects.filter(
                    equipment__in=type_list,
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "equipment")
                .annotate(type=Value("beforechecklist", output_field=CharField()))
            )
            install_query = (
                InstallCheckList.objects.filter(
                    equipment__in=type_list,
                )
                .annotate(docNum=F("pk"))
                .values("docNum", "created_at", "equipment")
                .annotate(type=Value("checklist", output_field=CharField()))
            )
        for add_item in before_install_query:
            union_list.append(add_item)
        for add_item in install_query:
            union_list.append(add_item)
    union_list.sort(key=lambda x: x["created_at"], reverse=True)
    return union_list
