from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from core.subviews.group_views import GroupList, EditGroup, DeleteGroup, SaveGroup, \
    CreateGroup
from core.subviews.student_views import EditStudent, DeleteStudent, SaveStudent, CreateStudent, StudentList

urlpatterns = {
    path('', GroupList.as_view(), name='Groups'),
    path('group/edit/<int:id>', EditGroup.as_view(), name='EditGroup'),

    path('group/delete/<int:id>', DeleteGroup.as_view(), name='DeleteGroup'),
    path('group/save/<int:id>', SaveGroup.as_view(), name='SaveGroup'),
    path('group/save/', SaveGroup.as_view(), name='SaveGroup'),
    path('group/add', CreateGroup.as_view(), name='CreateGroup'),
    path('groups/', GroupList.as_view(), name='Groups'),

    path('student/edit/<int:id>', EditStudent.as_view(), name='EditStudent'),
    path('student/delete/<int:id>', DeleteStudent.as_view(), name='EditStudent'),
    path('student/save/<int:id>', SaveStudent.as_view(), name='SaveStudent'),
    path('student/save/', SaveStudent.as_view(), name='SaveStudent'),
    path('student/add', CreateStudent.as_view(), name='UpdateStudent'),
    path('students/', StudentList.as_view(), name='Students'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
