from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        # get_context_data возвращает словарь
        context = super().get_context_data(**kwargs)
        # exists() проверяет, существует ли список filter(name='authors')
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        # возвращаем пополненный переменной ['is_not_authors'] контекст
        return context
