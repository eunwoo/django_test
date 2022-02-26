from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..models import MaterialSupplyReport
from ..forms.material_forms import GeneralManagerMaterialSupplyReportForm


def create_material_service(request):
    form = GeneralManagerMaterialSupplyReportForm()
    last_doc = MaterialSupplyReport.objects.last()
    if not last_doc:
        docNum = 1
    else:
        docNum = last_doc.docNum + 1
    return render(
        request, "work/material/create_material.html", {"form": form, "docNum": docNum}
    )
