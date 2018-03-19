from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.db.models import Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView

from adv.forms import SearchStudentForm, AddStudentForm, AddGradeForm,\
    PresenceListForm, SchoolSubjectForm, MessageForm, LoginForm, UserCreateForm,\
    ResetPasswordForm
from .models import SCHOOL_CLASS, Student, SchoolSubject, StudentGrades,\
    PresenceList, StudentNotice


class SchoolView(View):
    def get(self, request):
        ctx = {
            'school_classes': SCHOOL_CLASS,
        }
        return render(request, 'school.html', ctx)


class SchoolClassView(View):
    def get(self, request, school_class):
        students = Student.objects.filter(school_class=school_class)
        school_classes = dict(SCHOOL_CLASS)
        ctx = {
            "students": students,
            "class_name": school_classes[int(school_class)]
        }
        return render(request, "class.html", ctx)


class StudentView(View):
    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        school_classes = dict(SCHOOL_CLASS)
        subjects = SchoolSubject.objects.all()
        ctx = {
            "student": student,
            "class_name": school_classes[student.school_class],
            "subjects": subjects,
        }
        return render(request, "student.html", ctx)


class GradesView(View):
    def get(self, request, student_id, subject_id):
        student = Student.objects.get(id=student_id)
        subject = SchoolSubject.objects.get(id=subject_id)
        student_grades = StudentGrades.objects.filter(
            student_id=student_id,
            school_subject_id=subject_id
        )
        grades = [
            student_grade.grade
            for student_grade in student_grades
        ]

        ctx = {
            "student": student,
            "subject": subject,
            "grades": grades,
            "average": sum(grades) / len(grades),
            "average2": student_grades.aggregate(avg2=Avg('grade')),
            "student_grades": student_grades,
        }
        return render(request, "grades.html", ctx)


class SearchStudentView(View):
    def get(self, request):
        ctx = {
            'form': SearchStudentForm,
        }
        return render(request, 'searchstudent.html', ctx)

    def post(self, request):
        form = SearchStudentForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            students = Student.objects.filter(last_name__icontains=last_name)
            ctx = {
                'form': form,
                'students': students,
            }
            return render(request, 'searchstudent.html', ctx)


class AddStudentView(View):
    def get(self, request):
        ctx = {
            'form': AddStudentForm,
        }
        return render(request, 'addstudent.html', ctx)

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            student = Student.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(
                reverse('student-info', kwargs={'student_id': student.id})
            )

        ctx = {
            'form': form,
        }
        return render(request, 'addstudent.html', ctx)


class AddGradeView(View):
    def get(self, request):
        ctx = {
            'form': AddGradeForm,
        }
        return render(request, 'addgrade.html', ctx)

    def post(self, request):
        form = AddGradeForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            grade = form.cleaned_data['grade']

            StudentGrades.objects.create(
                student=student,
                school_subject=subject,
                grade=grade,
            )

            return HttpResponseRedirect(
                reverse('student-info', kwargs={'student_id': student.id})
            )


class PresenceListView(View):
    def get(self, request, student_id, day):
        form = PresenceListForm(initial={
            'day': day,
            'student': student_id,
        })
        ctx = {
            'form': form,
        }
        return render(request, 'presencelist.html', ctx)

    def post(self, request, student_id, day):
        form = PresenceListForm(request.POST)
        if form.is_valid():
            PresenceList.objects.create(**form.cleaned_data)
            return HttpResponse('Zapisano obecność ucznia!')


class SetBackgroundColorView(View):
    def get(self, request):
        ctx = {
            'form': SetBackgroundColorForm,
        }
        return render(request, 'setbackgroundcolor.html', ctx)

    def post(self, request):
        form = SetBackgroundColorForm(request.POST)

        ctx = {
            'form': form,
        }

        if form.is_valid():
            colors = dict(COLORS)
            ctx['color'] = colors[int(form.cleaned_data['background_color'])]

        return render(request, 'setbackgroundcolor.html', ctx)


class UpdateProductView(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        form = ProductForm(instance=product)
        ctx = {
            'form': form,
        }
        return render(request, "update_product.html", ctx)

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponse('Dzięki za modyfikacje produktu')
        ctx = {
            'form': form,
        }
        return render(request, "update_product.html", ctx)


class AddSchoolSubjectView(View):
    def get(self, request):
        ctx = {
            'form': SchoolSubjectForm,
        }
        return render(request, "create_subject.html", ctx)

    def post(self, request):
        form = SchoolSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Dzięki za dodanie przedmiotu')
        ctx = {
            'form': form,
        }
        return render(request, "create_subject.html", ctx)


class AddMessageView(View):
    def get(self, request):
        ctx = {
            'form': MessageForm,
        }
        return render(request, "create_message.html", ctx)

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Dzięki za dodanie wiadomości!')
        ctx = {
            'form': form,
        }
        return render(request, "create_message.html", ctx)


class StudentNoticesView(View):
    def get(self, request, student_id):
        notices = StudentNotice.objects.filter(to_id=student_id)
        ctx = {
            'notices': notices
        }
        return render(request, "notices.html", ctx)


class StudentNoticeCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'adv.add_studentnotice'
    raise_exception = True
    model = StudentNotice
    fields = '__all__'

    def get_success_url(self):
        return reverse('notices', kwargs={'student_id': self.object.to.id})


class StudentNoticeDeleteView(DeleteView):
    model = StudentNotice

    def get_success_url(self):
        return reverse('notices', kwargs={'student_id': self.object.to.id})


class LoginView(View):
    def get(self, request):
        user = authenticate(username='nowy', password='passnowy1')
        if user:
            login(request, user)
            return HttpResponse('Zalogowałeś się!')
        else:
            return HttpResponse('Zły login lub hasło!')


class NormalView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('Jesteś zalogowany')
        else:
            return HttpResponse('Najpierw musisz się zalogować!')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponse('Wylogowałeś się')


class UsersListStdView(View):
    def get(self, request):
        users = User.objects.all()
        ctx = {
            'object_list': users
        }
        return render(request, 'adv/user_list.html', ctx)


class UsersListGenericView(ListView):
    model = User
    template_name = 'adv/user_list.html'


class UserLoginView(View):
    def get(self, request):
        ctx = {
            'form': LoginForm,
        }
        return render(request, 'login_form.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                url = request.GET.get('next')
                if url:
                    return redirect(url)
                return HttpResponse('Zostałeś zalogowany!')

            form.add_error(field=None, error='Zły login lub hasło!')

        ctx = {
            'form': form,
        }
        return render(request, 'login_form.html', ctx)


class UserCreateView(View):
    def get(self, request):
        ctx = {
            'form': UserCreateForm,
            'buttonvalue': 'Dodaj użytkownika',
        }
        return render(request, 'form.html', ctx)

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['confirm_password']
            user = User.objects.create_user(**form.cleaned_data)
            return HttpResponse('Utworzono nowego użytkownika o id {}'.format(user.id))

        ctx = {
            'form': form,
            'buttonvalue': 'Spróbuj ponownie',
        }
        return render(request, 'form.html', ctx)


class ResetPasswordView(PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'

    def get(self, request, user_id):
        ctx = {
            'form': ResetPasswordForm,
            'buttonvalue': 'Zmień hasło',
        }
        return render(request, 'form.html', ctx)

    def post(self, request, user_id):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return HttpResponse('Zmieniono hasło użytkownikowi {}'.format(user.username))
        ctx = {
            'form': form,
            'buttonvalue': 'Spróbuj ponownie',
        }
        return render(request, 'form.html', ctx)