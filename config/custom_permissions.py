from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class OnlySuperUser(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
    