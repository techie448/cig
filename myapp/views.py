from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, get_list_or_404, resolve_url, redirect
from django.urls.base import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import views as auth_views
from django.views.generic.list import ListView
from .forms import CityForm, CategoryForm, EntryForm, ReviewForm, NewEntryForm, NewReviewForm, RegisterForm
from .models import City, Category, Entry, Review, InfoUser

def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = InfoUser.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated=True
                profile.activation_key=None
                profile.save()
                return redirect("/login")
    return redirect("/login")


class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'registration/form-3/register.html'
	success_url = '/confirm_registration/'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('myapp:logout')
		return super(RegisterView, self).dispatch(request,*args, **kwargs)

class ConfirmRegistrationView(TemplateView):
	template_name = 'registration/confirm_registration.html'

class InfoLoginView(auth_views.LoginView):
	template_name = 'registration/form-3/index.html'

	def get_success_url(self):
		if self.request.user.is_staff:
			return reverse_lazy('myapp:admin')
		return resolve_url(settings.LOGIN_REDIRECT_URL)


class IndexView(LoginRequiredMixin, generic.ListView):
	model = City


class CityDetailView(LoginRequiredMixin, generic.DetailView):
	model = City
	slug_url_kwarg = 'city'

	def get_context_data(self, **kwargs):
		context = super(CityDetailView, self).get_context_data(**kwargs)
		context['category_list'] = Category.objects.all();
		return context


class CityCreateView(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
	permission_required = ['is_staff']
	form_class = CityForm
	template_name = 'myapp/city_form.html'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(CityCreateView, self).form_valid(form)


class CategoryCreateView(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
	permission_required = ['is_staff']
	form_class = CategoryForm
	template_name = 'myapp/category_form.html'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(CategoryCreateView, self).form_valid(form)


class EntryListView(LoginRequiredMixin, generic.ListView):
	def get_queryset(self):
		return Entry.objects.filter(city__slug=self.kwargs['city'], category__slug=self.kwargs['category'])
		# return get_list_or_404(Entry, city__slug=self.kwargs['city'], category__slug=self.kwargs['category'])

	def get_context_data(self, **kwargs):
		context = super(EntryListView, self).get_context_data(**kwargs)
		context['category'] = get_object_or_404(Category, slug=self.kwargs['category'])
		context['city'] = get_object_or_404(City, slug=self.kwargs['city'])
		return context


class EntryCreateView(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
	permission_required = ['is_staff']
	form_class = EntryForm
	template_name = 'myapp/entry_form.html'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.city = get_object_or_404(City, slug=self.kwargs['city'])
		instance.user = self.request.user
		instance.category = get_object_or_404(Category, slug=self.kwargs['category'])
		return super(EntryCreateView, self).form_valid(form)


class ReviewListView(LoginRequiredMixin, generic.ListView):
	template_name = 'myapp/review_list.html'

	def get_queryset(self):
		return Review.objects.filter(entry__slug=self.kwargs['entry'])

	def get_context_data(self, **kwargs):
		context = super(ReviewListView, self).get_context_data(**kwargs)
		entry = get_object_or_404(Entry, slug=self.kwargs['entry'])
		category = get_object_or_404(Category, slug=self.kwargs['category'])
		city = get_object_or_404(City, slug=self.kwargs['city'])
		context['entry'] = entry
		context['city'] = city
		context['category'] = category
		return context


class ReviewCreateView(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
	permission_required = ['myapp.viewer']
	form_class = ReviewForm
	template_name = 'myapp/review_form.html'

	# def get_form_kwargs(self):
	# 	entry = self.kwargs.get('entry')
	# 	kwargs = super(ReviewCreateView, self).get_form_kwargs()
	# 	kwargs.update({'entry': entry})
	# 	kwargs.update({'user': self.request.user.pk})
	# 	# form = ReviewForm(initial = { 'entry' : Entry.Object.get(slug=entry) })
	# 	return kwargs

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.entry = get_object_or_404(Entry, slug=self.kwargs['entry'])
		instance.user = self.request.user
		return super(ReviewCreateView, self).form_valid(form)

class ReviewUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	form_class = ReviewForm
	slug_url_kwarg = 'review'
	template_name = 'myapp/review_update.html'
	def get_queryset(self):
		return Review.objects.filter(slug=self.kwargs['review'])

	def test_func(self):
		return self.request.user == Review.objects.get(slug=self.kwargs['review']).user


class ReviewDeleteView(UserPassesTestMixin,LoginRequiredMixin, DeleteView):
	model = Review
	slug_url_kwarg = 'review'
	success_url = '/'
	def test_func(self):
		return self.request.user == Review.objects.get(slug=self.kwargs['review']).user


class MyProfileTemplateView(LoginRequiredMixin, TemplateView):
	template_name = 'myapp/my_profile.html'


class AdminProfileView(PermissionRequiredMixin,LoginRequiredMixin, TemplateView):
	permission_required = ['is_staff']
	template_name = 'myapp/administrator/my_profile.html'

class AdminCityListView(PermissionRequiredMixin,LoginRequiredMixin, ListView):
	permission_required = ['is_staff']
	model = City
	template_name = 'myapp/administrator/city.html'


class AdminCityUpdateView(PermissionRequiredMixin,LoginRequiredMixin, UpdateView):
	permission_required = ['is_staff']
	form_class = CityForm
	slug_url_kwarg = 'city'
	template_name = 'myapp/administrator/city-update.html'
	def get_queryset(self):
		return City.objects.filter(slug=self.kwargs['city'])

class AdminCategoryListView(PermissionRequiredMixin,LoginRequiredMixin, ListView):
	permission_required = ['is_staff']
	model = Category
	template_name = 'myapp/administrator/category.html'

class AdminCategoryUpdateView(PermissionRequiredMixin,LoginRequiredMixin, UpdateView):
	permission_required = ['is_staff']
	form_class = CategoryForm
	slug_url_kwarg = 'category'
	template_name = 'myapp/administrator/category-update.html'
	def get_queryset(self):
		return Category.objects.filter(slug=self.kwargs['category'])

class AdminEntryListView(PermissionRequiredMixin,LoginRequiredMixin, ListView):
	permission_required = ['is_staff']
	model = Entry
	template_name = 'myapp/administrator/entry.html'
	def get_context_data(self, **kwargs):
		context = super(AdminEntryListView, self).get_context_data(**kwargs)
		context['city'] = set([b.city for b in Entry.objects.all()])
		context['category'] = set([a.category for a in Entry.objects.all()])
		return context

class CityDeleteView(PermissionRequiredMixin,LoginRequiredMixin, DeleteView):
	permission_required = ['is_staff']
	model = City
	slug_url_kwarg = 'city'
	success_url = reverse_lazy('myapp:admin-city')

class CategoryDeleteView(PermissionRequiredMixin,LoginRequiredMixin, DeleteView):
	permission_required = ['is_staff']
	model = Category
	slug_url_kwarg = 'category'
	success_url = reverse_lazy('myapp:admin-category')

class EntryDeleteView(PermissionRequiredMixin,LoginRequiredMixin, DeleteView):
	permission_required = ['is_staff']
	model = Entry
	slug_url_kwarg = 'entry'
	success_url = reverse_lazy('myapp:admin-entry')


class AdminEntryUpdateView(PermissionRequiredMixin,LoginRequiredMixin, UpdateView):
	permission_required = ['is_staff']
	form_class = EntryForm
	slug_url_kwarg = 'entry'
	template_name = 'myapp/administrator/entry-update.html'
	success_url = reverse_lazy('myapp:admin-entry')
	def get_queryset(self):
		return Entry.objects.filter(slug=self.kwargs['entry'])

class AdminEntryCreateView(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
	permission_required = ['is_staff']
	form_class = NewEntryForm
	template_name = 'myapp/entry_form.html'
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(AdminEntryCreateView, self).form_valid(form)

class AdminReviewsListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
	permission_required = ['is_staff']
	model = Review
	template_name = 'myapp/administrator/reviews.html'

	def get_context_data(self, **kwargs):
		context = super(AdminReviewsListView, self).get_context_data(**kwargs)
		context['entry'] = set([b.entry for b in Review.objects.all()])
		return context



class AdminReviewCreateView(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
	permission_required = ['is_staff']
	form_class = NewReviewForm
	template_name = 'myapp/administrator/review_form.html'
	success_url = reverse_lazy('myapp:admin-review')

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super(AdminReviewCreateView, self).form_valid(form)

class AdminReviewDeleteView(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
	permission_required = ['is_staff']
	model = Review
	slug_url_kwarg = 'review'
	success_url = reverse_lazy('myapp:admin-review')
	template_name = 'myapp/administrator/review_confirm_delete.html'
	#success_url = reverse_lazy('myapp:admin-review')

class AdminEntryReviewCreateView(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
	permission_required = ['is_staff']
	form_class = ReviewForm
	template_name = 'myapp/administrator/review_form.html'
	success_url = reverse_lazy('myapp:admin-review')

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.entry = get_object_or_404(Entry, slug=self.kwargs['entry'])
		instance.user = self.request.user
		return super(AdminEntryReviewCreateView, self).form_valid(form)
