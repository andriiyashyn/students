from datetime import date, datetime

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.db import transaction

from core.models_dir.organization_models import OrganizationCategory, OrganizationHasOrganizationCategory, Organization
from core.models_dir.party_models import PartyType, Party, Relationship
from core.models_dir.person_models import Person

organization_category_caption = 'Група'
party_type = 'ORGANIZATION'


class GroupList(TemplateView):
    template_name = 'groups.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('searchText') is not None:
            context['group_list'] = load_group_by_search_text(self.request.GET.get('searchText'),
                                                              organization_category_caption)
        else:
            context['group_list'] = load_group(organization_category_caption)
        return context


class EditGroup(TemplateView):
    template_name = 'group_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        group = Organization.objects.get(id=pk)
        context['group'] = group
        context['student_list'] = load_students_per_group(group)
        return context


class DeleteGroup(TemplateView):
    template_name = 'groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_group(kwargs['id'])
        context['group_list'] = load_group(organization_category_caption)
        return context


class SaveGroup(TemplateView):
    template_name = 'groups.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('id') is None:
            save_group(request.POST)
        else:
            update_group(kwargs['id'], request.POST)
        context['group_list'] = load_group(organization_category_caption)
        return HttpResponseRedirect('/groups')


class CreateGroup(TemplateView):
    template_name = 'group_edit.html'


def load_group(caption):
    group_category = OrganizationCategory.objects.get(caption=caption)
    group_has_group_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=group_category)
    groups = []
    for group_id in group_has_group_category:
        if group_id.organization.party.state == 'ACT':
            groups.append(group_id.organization)
    return groups


def load_group_by_search_text(search_text, caption):
    group_category = OrganizationCategory.objects.get(caption=caption)
    group_has_group_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=group_category)
    groups = []
    for group_id in group_has_group_category:
        if group_id.organization.party.state == 'ACT':
            if str(search_text).lower() in group_id.organization.name.lower():
                groups.append(group_id.organization)
    return groups


@transaction.atomic
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
    group = Organization()
    group.party = party
    group.startDate = date.today()
    group.endDate = date.max
    group.name = data.get('name')
    group.infoText = data.get('infoText')
    group.save()
    return group


def get_group_category():
    group_category = OrganizationCategory.objects.get(caption=organization_category_caption)
    return group_category


def create_group_has_group_category(group_category, group):
    group_has_group_category = OrganizationHasOrganizationCategory()
    group_has_group_category.organizationCategory = group_category
    group_has_group_category.organization = group
    group_has_group_category.startDate = datetime.now()
    group_has_group_category.endDate = date.max
    group_has_group_category.save()
    return group_has_group_category


@transaction.atomic
def update_group(pk, data):
    group = Organization.objects.get(id=pk)
    group.name = data.get('name')
    group.infoText = data.get('infoText')
    group.save()


@transaction.atomic
def delete_group(pk):
    group = Organization.objects.get(id=pk)
    party = group.party
    party.state = 'DEL'
    group.endDate = datetime.now()
    party.save()

    Relationship.objects.filter(srcParty=party).update(endDate=datetime.now())


def load_students_per_group(group):
    party_group = group.party
    students_parties = Relationship.objects.filter(srcParty=party_group)
    students = []
    for students_party in students_parties:
        person = Person.objects.get(party=students_party.destParty)
        if person not in students:
            if person.party.state == 'ACT':
                students.append(person)
    return students
