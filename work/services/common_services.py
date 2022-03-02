from user.models import CustomUser


def assign_user(doc, user_pk: int):
    user = CustomUser.objects.get(pk=user_pk)
    if user.class2 == "현장 대리인":
        doc.agentId = user
        doc.isReadAgent = False
    elif user.class2 == "일반 건설사업관리기술인":
        doc.generalEngineerId = user
        doc.isReadAgent = True
        doc.isReadGeneralEngineer = False
    else:
        doc.totalEngineerId = user
        doc.isReadGeneralEngineer = True
        doc.isReadTotalEngineer = False
    doc.save()
    return True
