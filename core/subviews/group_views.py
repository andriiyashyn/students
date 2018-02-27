from datetime import datetime, date
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from core.models import Organization, OrganizationCategory, OrganizationHasOrganizationCategory, Party, PartyType

category_caption = 'Група'
party_type = 'ORGANIZATION'


class GroupList(TemplateView):
    template_name = 'group_templates/groups.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_list'] = load_group()
        return context


class EditGroup(TemplateView):
    template_name = 'group_templates/groupEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        person = Group.objects.get(id=pk)
        context['group'] = person
        return context


class DeleteGroup(TemplateView):
    template_name = 'group_templates/groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_group(kwargs['id'])
        context['group_list'] = load_group()
        return context


class SaveGroup(TemplateView):
    template_name = 'group_templates/groups.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('id') is None:
            save_group(request.POST)
        else:
            update_group(kwargs['id'], request.POST)
        context['group_list'] = load_group()
        return HttpResponseRedirect('/groups')


class CreateGroup(TemplateView):
    template_name = 'group_templates/groupEdit.html'


def load_group():
    group_category = OrganizationCategory.objects.get(caption=category_caption)
    group_has_group_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=group_category)
    groups = []
    for group_id in group_has_group_category:
        if group_id.group.party.state == 'ACT':
            groups.append(group_id.group)
    return groups


def save_group(data):
    party = create_party()
    group = create_group(data, party)
    group_category = get_group_category()
    create_group_has_group_category(group_category, group)


def create_party():
    party = Party()
    party.partyType = PartyType.objects.get(name=party_type)
    party.state = 'ACT'
    party.save()
    return party


def create_group(data, party):
    group = Group()
    group.party = party
    group.startDate = datetime.now
    group.endDate = date.max
    group.name = data.get('name')
    group.infoText = data.get('infoText')
    group.save()
    return group


def get_group_category():
    group_category = OrganizationCategory.objects.get(caption=category_caption)
    return group_category


def create_group_has_group_category(group_category, group):
    group_has_group_category = OrganizationHasOrganizationCategory()
    group_has_group_category.organizationCategory = group_category
    group_has_group_category.organization = group
    group_has_group_category.startDate = datetime.now()
    group_has_group_category.endDate = date.max
    group_has_group_category.save()
    return group_has_group_category


def update_group(pk, data):
    group = Organization.objects.get(id=pk)
    group.name = data.get('name')
    group.infoText = data.get('infoText')
    group.save()


def delete_group(pk):
    group = Organization.objects.get(id=pk)
    party = group.party
    party.state = 'DEL'
    group.endDate = datetime.now()
    party.save()
