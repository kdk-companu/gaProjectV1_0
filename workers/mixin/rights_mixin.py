from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404


class ViewsPermissionsMixin(PermissionRequiredMixin):
    '''Опредение прав просмотра страницы'''
    permission_user = None
    permission_user_superiors = None

    def has_permission(self):
        perms = self.get_permission_required()
        '''Запросы для предоставления прав доступа'''

        if self.permission_user == None and self.permission_user_superiors == None:
            return self.request.user.has_perms(perms)
        else:
            own = self.get_object().subdivision == self.request.user.subdivision and self.get_object().department == self.request.user.department
            supervisor_right = own and self.request.user.has_perm(self.permission_user_superiors)
            # Пользователь
            base_righ = (self.get_object() == self.request.user) and self.request.user.has_perm(self.permission_user)
            return supervisor_right or base_righ

    def dispatch(self, request, *args, **kwargs):

        if not self.has_permission():
            raise Http404()

        return super().dispatch(request, *args, **kwargs)
