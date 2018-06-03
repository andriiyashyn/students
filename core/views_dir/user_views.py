from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from core.models_dir.user_model import Client


@method_decorator(login_required, name='dispatch')
class UsersList(TemplateView):
    template_name = 'user_templates/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = load_users()
        context['current_user_is_admin'] = Client.objects.get(id=self.request.user.id)
        return context


@method_decorator(login_required, name='dispatch')
class EditUser(TemplateView):
    template_name = 'user_templates/userEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        user = Client.objects.get(id=pk)
        context['user'] = user
        context['current_user_is_admin'] = Client.objects.get(id=self.request.user.id)
        return context


@method_decorator(login_required, name='dispatch')
class SaveUser(TemplateView):
    template_name = 'user_templates/users.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        update_user(kwargs['id'], request.POST)
        context['users'] = load_users()
        context['current_user_is_admin'] = Client.objects.get(id=self.request.user.id)
        return HttpResponseRedirect('/users')


@method_decorator(login_required, name='dispatch')
class CreateUser(TemplateView):
    template_name = 'user_templates/userCreate.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        create_user(request.POST)
        context['users'] = load_users()
        context['current_user_is_admin'] = Client.objects.get(id=self.request.user.id)
        return HttpResponseRedirect('/users')


@method_decorator(login_required, name='dispatch')
class DeleteUser(TemplateView):
    template_name = 'user_templates/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_user(kwargs['id'])
        context['users'] = load_users()
        context['current_user_is_admin'] = Client.objects.get(id=self.request.user.id)
        return context


def load_users():
    users = Client.objects.all()
    return users


def update_user(pk, data):
    user = Client.objects.get(id=pk)
    user.username = data.get('username')
    user.is_admin = True if data.get('is_admin') == '' else False
    user.save()


def create_user(data):
    user = Client()
    user.username = data.get('username')
    user.set_password(data.get('password'))
    user.is_admin = True if data.get('is_admin') == '' else False
    user.save()


def delete_user(pk):
    user = Client.objects.get(id=pk)
    user.delete()
