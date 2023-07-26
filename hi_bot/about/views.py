from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    '''Обработчик статичной страницы об авторе.'''

    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    '''Обработчик статичной страницы о технологиях.'''

    template_name = 'about/tech.html'
