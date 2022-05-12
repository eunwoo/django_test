from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from urllib import parse

# Create your views here.

from .services import get_search_list, custom_redirect


@login_required(login_url="/user/login/")
def search(request):
    if request.GET.getlist("query"):
        return custom_redirect(
            "result:search_result",
            query=request.GET.getlist("query"),
            locate=request.GET.get("locate", 0),
            search=request.GET.get("search", ""),
        )
    return render(
        request,
        "result/search.html",
    )


@login_required(login_url="/user/login/")
def search_result(request):
    page = request.GET.get("page", 1)

    result_list = get_search_list(
        request.GET.getlist("query"),
        request.GET.get("locate", 0),
        request.GET.get("search", ""),
    )

    paginator = Paginator(result_list, 10)
    page_obj = paginator.get_page(page)

    query = parse.urlencode(
        {
            "query": request.GET.getlist("query"),
            "locate": request.GET.get("locate", 0),
            "search": request.GET.get("search", ""),
        },
        True,  # True 설정시 ?query=[1,2,3,4]가 아닌 ?query=1&query=2&query=3&query=4 으로 인코딩됨
    )

    return render(
        request,
        "result/search_result.html",
        {
            "items": page_obj,
            "query": f"&{query}",
        },
    )
