from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^admin/entry/$', views.AdminEntryListView.as_view(), name='admin-entry'),
	url(r'^admin/entry/(?P<city>[\w-]+)/(?P<category>[\w-]+)/(?P<entry>[\w-]+)/update/$',
	    views.AdminEntryUpdateView.as_view(), name='admin-entry-update'),
	url(r'^admin/entry/add/$', views.AdminEntryCreateView.as_view(), name='admin-new-entry'),

	url(r'^admin/entry/(?P<city>[\w-]+)/(?P<category>[\w-]+)/(?P<entry>[\w-]+)/delete/$',
	    views.EntryDeleteView.as_view(), name='admin-entry-delete'),
	url(r'^admin/entry/(?P<city>[\w-]+)/(?P<category>[\w-]+)/add', views.EntryCreateView.as_view(), name='createentry'),
	# PROFILE
	url(r'^myprofile/$', views.MyProfileTemplateView.as_view(), name='myprofile'),
	url(r'^admin/myprofile/$', views.AdminProfileView.as_view(), name='admin'),
	url(r'^admin/city/$', views.AdminCityListView.as_view(), name='admin-city'),
	url(r'^admin/city/(?P<city>[\w-]+)/update/$', views.AdminCityUpdateView.as_view(), name='admin-city-update'),
	url(r'^admin/city/(?P<city>[\w-]+)/delete/$', views.CityDeleteView.as_view(), name='admin-city-delete'),
	url(r'^admin/category/$', views.AdminCategoryListView.as_view(), name='admin-category'),
	url(r'^admin/category/(?P<category>[\w-]+)/update/$', views.AdminCategoryUpdateView.as_view(),
	    name='admin-category-update'),
	url(r'^admin/category/(?P<category>[\w-]+)/delete/$', views.CategoryDeleteView.as_view(),
	    name='admin-category-delete'),
	url(r'^admin/reviews/$', views.AdminReviewsListView.as_view(), name='admin-review'),
	url(r'^admin/reviews/add/$', views.AdminReviewCreateView.as_view(), name='admin-new-review'),
	url(r'^admin/reviews/(?P<entry>[\w-]+)/add/$',views.AdminEntryReviewCreateView.as_view(),name='admin-review-entry-create'),
	url(r'^admin/reviews/(?P<entry>[\w-]+)/(?P<review>[\w-]+)/delete/$',views.AdminReviewDeleteView.as_view(),name='admin-review-delete'),


	# LOGIN
	url(r'^login/$', views.InfoLoginView.as_view(), name='login'),
	url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^confirm_registration/$', views.ConfirmRegistrationView.as_view(), name='confirm_registration'),

	url(r'^activate/(?P<code>[a-z0-9].*)/$', views.activate_user_view, name='activate'),

	# url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/form-3/index.html'), name='login'),

	url(r'^logout/$', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

	# PASSWORD RESET

	url(r'^password-change/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',
	                                                                 success_url=reverse_lazy(
		                                                                 'myapp:password_changed')),
	    name='password_change'),
	url(r'^password-change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name=
	                                                                          'registration/change_success.html'),
	    name='password_changed'),
	url(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',
	                                                               success_url=reverse_lazy('myapp:reset-email-sent')),
	    name='password-reset'),

	url(r'^password-reset/email-sent/$', auth_views.PasswordResetDoneView.as_view(template_name=
	                                                                              'registration/reset_email_sent.html'),
	    name='reset-email-sent'),
	url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    auth_views.PasswordResetConfirmView.as_view(template_name=
	                                                'registration/password_reset_confirm.html',
	                                                success_url=reverse_lazy('myapp:password_reset_completed')),
	    name='password_reset_confirm'),
	url(r'^password-reset/completed/$', auth_views.PasswordResetCompleteView.as_view(
		template_name='registration/password_reset_completed.html'),
	    name='password_reset_completed'),

	# CREATE VIEWS

	url(r'^addcategory/$', views.CategoryCreateView.as_view(), name='createcategory'),

	url(r'^addcity/$', views.CityCreateView.as_view(), name='createcity'),

	# CITY

	url(r'^(?P<city>[\w-]+)/$', views.CityDetailView.as_view(), name='city'),

	# url(r'^(?P<slug>[\w-]+)/update/$', views.CityUpdateView.as_view(), name='updatecity'),

	# ENTRY



	url(r'^(?P<city>[\w-]+)/(?P<category>[\w-]+)/$', views.EntryListView.as_view(), name='entry'),

	# REVIEWS

	url(r'^(?P<city>[\w-]+)/(?P<category>[\w-]+)/(?P<entry>[\w-]+)/$', views.ReviewListView.as_view(), name='review'),

	url(r'^(?P<city>[\w-]+)/(?P<category>[\w-]+)/(?P<entry>[\w-]+)/addreview/$', views.ReviewCreateView.as_view(),
	    name='createreview'),

	url(r'^(?P<city>[\w-]+)/(?P<category>[\w-]+)/(?P<entry>[\w-]+)/(?P<review>[\w-]+)/delete/$',
	    views.ReviewDeleteView.as_view(),
	    name='deletereview'),

	url(r'^(?P<city>[\w-]+)/(?P<category>[\w-]+)/(?P<entry>[\w-]+)/(?P<review>[\w-]+)/update/$',
	    views.ReviewUpdateView.as_view(),
	    name='updatereview')

]

app_name = 'myapp'
