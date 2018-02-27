from datetime import datetime, date

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from core.models import PersonCategory, PersonHasPersonCategory, Person, Party, PartyType

category_caption = 'Студент'
party_type = 'PERSON'


class StudentList(TemplateView):
    template_name = 'student_templates/students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_list'] = load_students()
        return context


class EditStudent(TemplateView):
    template_name = 'student_templates/studentEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        person = Person.objects.get(id=pk)
        context['person'] = person
        return context


class DeleteStudent(TemplateView):
    template_name = 'student_templates/students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_student(kwargs['id'])
        context['student_list'] = load_students()
        return context


class SaveStudent(TemplateView):
    template_name = 'student_templates/students.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('id') is None:
            save_student(request.POST)
        else:
            update_student(kwargs['id'], request.POST)
        context['student_list'] = load_students()
        return HttpResponseRedirect('/students')


class CreateStudent(TemplateView):
    template_name = 'student_templates/studentEdit.html'


def load_students():
    student_category = PersonCategory.objects.get(caption=category_caption)
    student_has_student_category = PersonHasPersonCategory.objects.filter(
        personCategory=student_category)
    students = []
    for student_id in student_has_student_category:
        if student_id.person.party.state == 'ACT':
            students.append(student_id.person)
    return students


def save_student(data):
    party = create_party()
    student = create_student(data, party)
    person_category = create_person_category()
    create_student_has_person_category(person_category, student)


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
    student.taxCode = data.get('taxCode')
    student.infoText = data.get('infoText')
    student.save()
    return student


def create_person_category():
    person_category = PersonCategory.objects.get(caption=category_caption)
    return person_category


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
    student.infoText = data.get('infoText')
    student.save()


def delete_student(pk):
    person = Person.objects.get(id=pk)
    party = person.party
    party.state = 'DEL'
    person.endDate = datetime.now()
    party.save()
