from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Tasks

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth login
from django.contrib.auth import authenticate, login





# Create your views here.


class CustomLoginView(LoginView):

	template_name = 'base/login.html'
	fields = ('__all__')
	redirect_authenticated_user = True


	def get_success_url(self):
		return reverse_lazy('task_list')

class UserRegisterView(FormView):

	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('task_list')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(UserRegisterView, self).form_valid(form)

	def get(self, *args, **kwargs):

		if self.request.user.is_authenticated:
			
			redirect('tasks')
		return super(UserRegisterView, self).get(*args, *kwargs)





class Tasklist(LoginRequiredMixin, ListView):

	model = Tasks
	context_object_name = 'tasks'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['tasks'] = context['tasks'].filter(user = self.request.user)
		context['count'] = context['tasks'].filter(completed = False).count()
		search_input = self.request.GET.get('search-area', None)

		if search_input :
			context['tasks'] = context['tasks'].filter(title__startswith = search_input)

		context['search_input'] = search_input 

		return context



class TaskDeatil(LoginRequiredMixin, DetailView):

	model = Tasks
	context_object_name = 'details'
	# template_name = 'base/taskhtml'


class CreateTask(LoginRequiredMixin, CreateView):

	model = Tasks
	fields = ['title','description', 'completed']
	success_url = reverse_lazy('task_list')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(CreateTask, self).form_valid(form)



class UpdateTask(LoginRequiredMixin, UpdateView):

	model = Tasks
	fields = ['title','description', 'completed']
	success_url = reverse_lazy('task_list')


class DeleteTask(LoginRequiredMixin, DeleteView):

	model = Tasks
	context_object_name = 'tasks'
	success_url = reverse_lazy('task_list')