from datetime import datetime as dt


def year(request):
    '''Добавляет в шаблон переменную с текущим годом.'''
    return {
        'year': dt.utcnow().year
    }
