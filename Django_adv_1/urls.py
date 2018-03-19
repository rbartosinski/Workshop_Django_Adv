"""Django_adv_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from adv.views import (
    GradesView,
    SchoolClassView,
    SchoolView,
    StudentView,
    SearchStudentView,
    AddStudentView,
    AddGradeView,
    PresenceListView,
    AddSchoolSubjectView,
    AddMessageView,
    StudentNoticesView,
    StudentNoticeCreateView,
    StudentNoticeDeleteView,
    LoginView,
    NormalView,
    LogoutView,
    UsersListStdView,
    UsersListGenericView,
    UserLoginView,
    UserCreateView,
    ResetPasswordView
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SchoolView.as_view(), name="index"),
    url(r'^class/(?P<school_class>(\d)+)', SchoolClassView.as_view(), name="school-class"),
    url(r'^student/(?P<student_id>\d+)', StudentView.as_view(), name='student-info'),
    url(r'^student_search', SearchStudentView.as_view()),
    url(r'^add_student', AddStudentView.as_view()),
    url(r'^add_subject/$', AddSchoolSubjectView.as_view()),
    url(r'^add_message/$', AddMessageView.as_view()),
    url(r'^add_grade', AddGradeView.as_view()),
    url(r'^notices/(?P<student_id>\d+)/$', StudentNoticesView.as_view(), name='notices'),
    url(r'^create_notice/$', StudentNoticeCreateView.as_view(), name='create-notice'),
    url(r'^delete_notice/(?P<pk>\d+)/$', StudentNoticeDeleteView.as_view(), name='delete-notice'),
    url(r'^grades/(?P<student_id>\d+)/(?P<subject_id>\d+)', GradesView.as_view()),
    url(r'^class_presence/(?P<student_id>\d+)/(?P<day>\d{4}-\d{2}-\d{2})', PresenceListView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^normal/$', NormalView.as_view()),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^users_std/$', UsersListStdView.as_view()),
    url(r'^users_generic/$', UsersListGenericView.as_view()),
    url(r'^userlogin/$', UserLoginView.as_view(), name='login'),
    url(r'^add_user/$', UserCreateView.as_view(), name='add-user'),
    url(r'^reset_password/(?P<user_id>\d+)/$', ResetPasswordView.as_view(), name='reset-password'),
]