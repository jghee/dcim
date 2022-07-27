from django.urls import path

import dcim.views
from . import views

app_name = 'dcim'

urlpatterns = [
    # Temporary
    path('', views.home, name='home'),
    path('rack_table/', views.test_rack_table, name='rack_table'),
    # Tenant groups
    # path('tenant-groups/', views.TenantGroupListView.as_view(), name='tenantgroup_list'),
    # path('tenant-groups/add/', views.TenantGroupEditView.as_view(), name='tenantgroup_add'),
    # path('tenant-groups/<int:pk>/', views.TenantGroupView.as_view(), name='tenantgroup'),
    # path('tenant-groups/<int:pk>/edit/', views.TenantGroupEditView.as_view(), name='tenantgroup_edit'),
    # path('tenant-groups/<int:pk>/delete/', views.TenantGroupDeleteView.as_view(), name='tenantgroup_delete'),

    # Tenants
    path('tenants/', views.TenantListView.as_view(), name='tenant_list'),
    path('tenants/add/', views.TenantEditView.as_view(), name='tenant_add'),
    # path('tenants/edit/', views.TenantBulkEditView.as_view(), name='tenant_bulk_edit'),
    path('tenants/<int:pk>/', views.TenantView.as_view(), name='tenant'),
    # path('tenants/<int:pk>/edit/', views.TenantEditView.as_view(), name='tenant_edit'),
    # path('tenants/<int:pk>/delete/', views.TenantDeleteView.as_view(), name='tenant_delete'),

]
