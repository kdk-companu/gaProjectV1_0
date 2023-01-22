from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class Workers_Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('workers')

    def get(self, *args, **kwargs):
        # Перекидывать по ленивым ссылкам
        if self.request.user.is_authenticated:
            return redirect('base_page', permanent=True)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class Workers_Logout(LoginRequiredMixin, LogoutView):
    template_name = 'prg_users/test.html'
    success_url = reverse_lazy('')
    login_url = 'login'
    redirect_field_name = ''

