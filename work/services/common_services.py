from user.models import CustomUser


def assign_user(user, doc, user_pk: int):
    target_user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "일반 관리자":
        doc.agentId = target_user
        doc.isCheckAgent = False
        doc.isCheckManager = True
    elif user.class2 == "현장 대리인":
        doc.generalEngineerId = target_user
        doc.isCheckGeneralEngineer = False
        doc.isCheckAgent = True
    elif user.class2 == "일반 건설사업관리기술인":
        doc.totalEngineerId = target_user
        doc.isCheckGeneralEngineer = True
        doc.isSuccess = False
    else:
        doc.isSuccess = True
        doc.isCheckManager = False
        doc.isCheckAgent = False
        doc.isCheckGeneralEngineer = False
    doc.save()
    return True
