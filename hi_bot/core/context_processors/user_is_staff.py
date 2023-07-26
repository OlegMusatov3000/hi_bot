def user_is_staff(request):
    '''
    Добавляет в шаблон переменную, проверяющую, что
    пользователь является модератором или админом.
    '''
    user_is_staff = False
    if (
        request.user.is_authenticated
        and request.user.role in ('moderator', 'admin')
    ):
        user_is_staff = True
    return {
        'user_is_staff': user_is_staff
    }
