from django.http import Http404
from django.shortcuts import render, redirect

from ..models import (
    SafetyReport,
    MaterialSupplyReport,
    QualityInspectionRequest,
    QualityPerformanceReport,
)


def get_unread_docs_list(user):
    context = {}
    if user.class2 == "일반 관리자":
        context["workCount"] = SafetyReport.objects.filter(
            writerId=user, isCheckManager=False
        ).count()
        context["materialCount"] = MaterialSupplyReport.objects.filter(
            writerId=user, isCheckManager=False
        ).count()
        context["qtyCount"] = (
            QualityInspectionRequest.objects.filter(
                writerId=user, isCheckManager=False
            ).count()
            + QualityPerformanceReport.objects.filter(
                writerId=user, isCheckManager=False
            ).count()
        )
    elif user.class2 == "현장 대리인":
        context["workCount"] = SafetyReport.objects.filter(
            agentId=user, isCheckAgent=False
        ).count()
        context["materialCount"] = MaterialSupplyReport.objects.filter(
            agentId=user, isCheckAgent=False
        ).count()
        context["qtyCount"] = (
            QualityInspectionRequest.objects.filter(
                agentId=user, isCheckAgent=False
            ).count()
            + QualityPerformanceReport.objects.filter(
                agentId=user, isCheckAgent=False
            ).count()
        )
    elif user.class2 == "일반 건설사업관리기술인":
        context["workCount"] = SafetyReport.objects.filter(
            generalEngineerId=user, isCheckGeneralEngineer=False
        ).count()
        context["materialCount"] = MaterialSupplyReport.objects.filter(
            generalEngineerId=user, isCheckGeneralEngineer=False
        ).count()
        context["qtyCount"] = (
            QualityInspectionRequest.objects.filter(
                generalEngineerId=user, isSuccess=False
            ).count()
            + QualityPerformanceReport.objects.filter(
                generalEngineerId=user, isCheckGeneralEngineer=False
            ).count()
        )
    elif user.class2 == "총괄 건설사업관리기술인":
        context["workCount"] = SafetyReport.objects.filter(
            totalEngineerId=user, isSuccess=False
        ).count()
        context["materialCount"] = MaterialSupplyReport.objects.filter(
            totalEngineerId=user, isSuccess=False
        ).count()
        context["qtyCount"] = QualityPerformanceReport.objects.filter(
            totalEngineerId=user, isSuccess=False
        ).count()
    return context


def get_unread_quality_docs(user):
    context = {}
    if user.class2 == "일반 관리자":
        context["qtyItems"] = QualityInspectionRequest.objects.filter(
            writerId=user, isCheckManager=False
        ).count()
        context["summaryItems"] = QualityPerformanceReport.objects.filter(
            writerId=user, isCheckManager=False
        ).count()
    elif user.class2 == "현장 대리인":
        context["qtyItems"] = QualityInspectionRequest.objects.filter(
            agentId=user, isCheckAgent=False
        ).count()
        context["summaryItems"] = QualityPerformanceReport.objects.filter(
            agentId=user, isCheckAgent=False
        ).count()
    elif user.class2 == "일반 건설사업관리기술인":
        context["qtyItems"] = QualityInspectionRequest.objects.filter(
            generalEngineerId=user, isSuccess=False
        ).count()
        context["summaryItems"] = QualityPerformanceReport.objects.filter(
            generalEngineerId=user, isCheckGeneralEngineer=False
        ).count()
    elif user.class2 == "총괄 건설사업관리기술인":
        context["summaryItems"] = QualityPerformanceReport.objects.filter(
            totalEngineerId=user, isSuccess=False
        ).count()
    return context
