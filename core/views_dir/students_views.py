from datetime import datetime, date
from django.shortcuts import redirect
from django.views.generic import TemplateView

from django.db import transaction

from core.models_dir.organization_models import OrganizationCategory, OrganizationHasOrganizationCategory, Organization
from core.models_dir.party_models import Relationship, RelationshipType, Party, PartyType, PartyContact, ContactType
from core.models_dir.person_models import Person, PersonCategory, PersonHasPersonCategory

organization_category = 'Група'
person_category = 'Студент'
party_type = 'PERSON'


class StudentList(TemplateView):
    template_name = 'students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('searchText') is not None:
            context['student_list'] = load_students_per_search_text(self.request.GET.get('searchText'))
        else:
            context['student_list'] = load_students()
        return context


class EditStudent(TemplateView):
    template_name = 'student_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        person = Person.objects.get(id=pk)
        context['person'] = person
        context['group_list'] = load_group(organization_category)
        context['group_relationship'] = load_person_groups(load_all_group(organization_category),
                                                                        person)
        context['contacts'] = load_contact_information(person)
        context['contact_types'] = load_contact_types()
        context['now_date'] = datetime.now()
        return context


class DeleteStudent(TemplateView):
    template_name = 'students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_student(kwargs['id'])
        context['student_list'] = load_students()
        return context


class SaveStudent(TemplateView):
    template_name = 'students.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('id') is None:
            person_id = save_student(request.POST).id
        else:
            update_student(kwargs['id'], request.POST)
            person_id = kwargs['id']
        context['student_list'] = load_students()
        return redirect('/student/edit/' + str(person_id))


class CreateStudent(TemplateView):
    template_name = 'student_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_list'] = load_group(organization_category)
        return context


class DeleteRelationshipView(TemplateView):
    template_name = 'student_edit.html'

    def get(self, request, *args, **kwargs):
        person = delete_relationship(kwargs['id'])
        return redirect('/student/edit/' + str(person.id))


class SaveRelationshipView(TemplateView):
    template_name = 'student_edit.html'

    def post(self, request, *args, **kwargs):
        create_relation(request.POST, Person.objects.get(pk=kwargs['id']))
        return redirect('/student/edit/' + str(kwargs['id']))


class SaveContactInfoView(TemplateView):
    template_name = 'student_edit.html'

    def post(self, request, *args, **kwargs):
        create_contact_info(request.POST, Person.objects.get(pk=kwargs['id']))
        return redirect('/student/edit/' + str(kwargs['id']))


class SaveContactTypeView(TemplateView):
    template_name = 'student_edit.html'

    def post(self, request, *args, **kwargs):
        create_contact_type(request.POST)
        return redirect('/student/edit/' + str(kwargs['id']))


class DeleteContactTypeView(TemplateView):
    template_name = 'student_edit.html'

    def get(self, request, *args, **kwargs):
        person = delete_contact(kwargs['id'])
        return redirect('/student/edit/' + str(person.id))


def load_group(caption):
    group_category = OrganizationCategory.objects.get(caption=caption)
    group_has_group_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=group_category)
    groups = []
    for group_id in group_has_group_category:
        if group_id.organization.party.state == 'ACT':
            groups.append(group_id.organization)
    return groups


def load_all_group(caption):
    group_category = OrganizationCategory.objects.get(caption=caption)
    group_has_group_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=group_category)
    groups = []
    for group_id in group_has_group_category:
        groups.append(group_id.organization)
    return groups


def load_person_groups(group_list, person):
    party_person = person.party
    relationships = Relationship.objects.filter(destParty=party_person)
    group_relationship = []
    for relationship in relationships:
        for group in group_list:
            if relationship.srcParty == group.party:
                relationship_group = RelationshipOrganization()
                relationship_group.relationship = relationship
                relationship_group.group = group
                group_relationship.append(relationship_group)

    return group_relationship


def load_students():
    student_category = PersonCategory.objects.get(caption=person_category)
    student_has_student_category = PersonHasPersonCategory.objects.filter(
        personCategory=student_category)
    students = []
    for student_id in student_has_student_category:
        if student_id.person.party.state == 'ACT':
            students.append(student_id.person)
    return students


def load_students_per_search_text(search_text):
    students = load_students()
    search_text_students = []
    for student in students:
        if str(search_text).lower() in str(student.firstName).lower() or str(search_text).lower() in str(
                student.secondName).lower() or str(search_text).lower() in str(student.patronymicName).lower():
            search_text_students.append(student)
    return search_text_students


@transaction.atomic
def save_student(data):
    party = create_party()
    student = create_student(data, party)
    person_category = create_person_category()
    create_student_has_person_category(person_category, student)
    return student


@transaction.atomic
def create_relation(data, student):
    relationship_type = get_or_create_relationship_type()
    create_relationship(relationship_type, data, student)


def create_relationship(relationship_type, data, student):
    relationship = Relationship()
    relationship.caption = 'Студент '
    relationship.relationshipType = relationship_type
    relationship.srcParty = Organization.objects.get(pk=data['group']).party
    relationship.destParty = student.party
    relationship.startDate = datetime.now()
    relationship.endDate = date.max
    relationship.save()


def get_or_create_relationship_type():
    if not RelationshipType.objects.filter(caption=person_category).exists():
        relationship_type = RelationshipType()
        relationship_type.caption = person_category
        relationship_type.srcDef = organization_category
        relationship_type.dstDef = person_category
        relationship_type.save()

    return RelationshipType.objects.get(caption=person_category)


def create_party():
    party = Party()
    party.partyType = PartyType.objects.get(name=party_type)
    party.state = 'ACT'
    party.save()
    return party


def create_student(data, party):
    student = Person()
    student.party = party
    student.firstName = data.get('firstName')
    student.secondName = data.get('secondName')
    student.patronymicName = data.get('patronymicName')
    student.birthDate = data.get('birthDate')
    student.startDate = datetime.now()
    student.endDate = date.max
    student.gender = data.get('gender')
    student.infoText = data.get('infoText')
    student.save()
    return student


def create_person_category():
    person__category = PersonCategory.objects.get(caption=person_category)
    return person__category


def create_student_has_person_category(person_category, student):
    student_has_person_category = PersonHasPersonCategory()
    student_has_person_category.personCategory = person_category
    student_has_person_category.person = student
    student_has_person_category.startDate = datetime.now()
    student_has_person_category.endDate = date.max
    student_has_person_category.save()


def update_student(pk, data):
    student = Person.objects.get(id=pk)
    student.firstName = data.get('firstName')
    student.secondName = data.get('secondName')
    student.patronymicName = data.get('patronymicName')
    student.birthDate = data.get('birthDate')
    student.gender = data.get('gender')
    student.infoText = data.get('infoText')
    student.save()


@transaction.atomic
def delete_student(pk):
    person = Person.objects.get(id=pk)
    party = person.party
    party.state = 'DEL'
    person.endDate = datetime.now()
    party.save()

    Relationship.objects.filter(destParty=party).update(endDate=datetime.now())


@transaction.atomic
def delete_relationship(pk):
    relationship = Relationship.objects.get(id=pk)
    relationship.endDate = datetime.now()
    relationship.save()
    return Person.objects.get(party=relationship.destParty)


def load_contact_information(person):
    party = person.party
    return PartyContact.objects.filter(party=party)


def load_contact_types():
    return ContactType.objects.all()


@transaction.atomic
def create_contact_info(data, person):
    contact_type_id = data.get('contact_types')
    contact_type = ContactType.objects.get(pk=contact_type_id)
    contact = PartyContact()
    contact.party = person.party
    contact.contact = data.get('contact')
    contact.contactType = contact_type
    contact.save()


@transaction.atomic
def create_contact_type(data):
    contact_type = ContactType()
    contact_type.name = data.get('name')
    contact_type.template = data.get('template')
    contact_type.save()


@transaction.atomic
def delete_contact(contact_id):
    party = PartyContact.objects.get(pk=contact_id).party
    PartyContact.objects.get(pk=contact_id).delete()
    return Person.objects.get(party=party)


class RelationshipOrganization:
    group = Organization()
    relationship = Relationship()
