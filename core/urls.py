from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from django.contrib.auth import views as auth_views
from core.views_dir.groups_views import GroupList, EditGroup, DeleteGroup, SaveGroup, CreateGroup
from core.views_dir.students_views import SaveContactInfoView, SaveContactTypeView, DeleteContactTypeView, \
    DeleteRelationshipView, SaveRelationshipView, EditStudent, DeleteStudent, SaveStudent, CreateStudent, StudentList

urlpatterns = {
    path('', GroupList.as_view(), name='Groups'),

    path('group/edit/<int:id>', EditGroup.as_view(), name='EditGroup'),
    path('group/delete/<int:id>', DeleteGroup.as_view(), name='DeleteGroup'),
    path('group/save/<int:id>', SaveGroup.as_view(), name='SaveGroup'),
    path('group/save/', SaveGroup.as_view(), name='SaveGroup'),
    path('group/add', CreateGroup.as_view(), name='CreateGroup'),
    path('groups/', GroupList.as_view(), name='Groups'),
    path('groups/search/', GroupList.as_view(), name='GroupsSearch'),

    path('student/contact-info/save/<int:id>', SaveContactInfoView.as_view(), name='SaveContactInfoView'),
    path('student/contact-type/save/<int:id>', SaveContactTypeView.as_view(), name='SaveContactTypeView'),
    path('student/contact-info/delete/<int:id>', DeleteContactTypeView.as_view(), name='DeleteContactTypeView'),

    path('student/relationship/delete/<int:id>', DeleteRelationshipView.as_view(), name='DeleteRelationshipView'),
    path('student/relationship/save/<int:id>', SaveRelationshipView.as_view(), name='SaveRelationshipView'),

    path('student/edit/<int:id>', EditStudent.as_view(), name='EditStudent'),
    path('student/delete/<int:id>', DeleteStudent.as_view(), name='EditStudent'),
    path('student/save/<int:id>', SaveStudent.as_view(), name='SaveStudent'),
    path('student/save/', SaveStudent.as_view(), name='SaveStudent'),
    path('student/add', CreateStudent.as_view(), name='UpdateStudent'),
    path('students/', StudentList.as_view(), name='Students'),
    path('students/search', StudentList.as_view(), name='StudentsSearch'),

    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
