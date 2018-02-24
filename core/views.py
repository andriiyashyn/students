from django.views.generic import TemplateView

from core.models import Organization, PersonCategory, PersonHasPersonCategory, Person


class OrganizationList(TemplateView):
    template_name = 'groups.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org_list'] = Organization.objects.all()
        return context


class StudentsList(TemplateView):
    template_name = 'students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personCategory = PersonCategory.objects.get(caption='Student')
        personHasPersonCategory = PersonHasPersonCategory.objects.filter(
            personCategory=personCategory)
        students = []
        for student in personHasPersonCategory:
            students.append(student.person)

        context['student_list'] = students
        return context
