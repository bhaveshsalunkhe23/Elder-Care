"""
member 
"""
from django.contrib import admin
from django.urls import path
from member import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home_view,name=''),

    path('adminclick', views.adminclick_view),
    path('customerclick', views.customerclick_view),
    path('staffmembersclick', views.staffmembersclick_view),

    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('staffmembersignup', views.staffmember_signup_view,name='staffmembersignup'),

    path('customerlogin', LoginView.as_view(template_name='member/customerlogin.html'),name='customerlogin'),
    path('staffmemberlogin', LoginView.as_view(template_name='member/staffmemberlogin.html'),name='staffmemberlogin'),
    path('adminlogin', LoginView.as_view(template_name='member/adminlogin.html'),name='adminlogin'),



    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-customer', views.admin_customer_view,name='admin-customer'),
    path('admin-view-customer',views.admin_view_customer_view,name='admin-view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-add-customer', views.admin_add_customer_view,name='admin-add-customer'),
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view,name='admin-view-customer-enquiry'),
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view,name='admin-view-customer-invoice'),


    path('admin-request', views.admin_request_view,name='admin-request'),
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view,name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view,name='admin-delete-request'),
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    path('admin-approve-request',views.admin_approve_request_view,name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    
    path('admin-view-service-cost',views.admin_view_service_cost_view,name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view,name='update-cost'),

    path('admin-staffmember', views.admin_staffmember_view,name='admin-staffmember'),
    path('admin-view-staffmember',views.admin_view_staffmember_view,name='admin-view-staffmember'),
    path('delete-staffmember/<int:pk>', views.delete_staffmember_view,name='delete-staffmember'),
    path('update-staffmember/<int:pk>', views.update_staffmember_view,name='update-staffmember'),
    path('admin-add-staffmember',views.admin_add_staffmember_view,name='admin-add-staffmember'),
    path('admin-approve-staffmember',views.admin_approve_staffmember_view,name='admin-approve-staffmember'),
    path('approve-staffmember/<int:pk>', views.approve_staffmember_view,name='approve-staffmember'),
    path('delete-staffmember/<int:pk>', views.delete_staffmember_view,name='delete-staffmember'),
    path('admin-view-staffmember-salary',views.admin_view_staffmember_salary_view,name='admin-view-staffmember-salary'),
    path('update-salary/<int:pk>', views.update_salary_view,name='update-salary'),

    path('admin-staffmember-attendance', views.admin_staffmember_attendance_view,name='admin-staffmember-attendance'),
    path('admin-take-attendance', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance', views.admin_view_attendance_view,name='admin-view-attendance'),
    path('admin-feedback', views.admin_feedback_view,name='admin-feedback'),

    path('admin-report', views.admin_report_view,name='admin-report'),

    path('staffmember-dashboard', views.staffmember_dashboard_view,name='staffmember-dashboard'),
    path('staffmember-work-assigned', views.staffmember_work_assigned_view,name='staffmember-work-assigned'),
    path('staffmember-update-status/<int:pk>', views.staffmember_update_status_view,name='staffmember-update-status'),
    path('staffmember-feedback', views.staffmember_feedback_view,name='staffmember-feedback'),
    path('staffmember-salary', views.staffmember_salary_view,name='staffmember-salary'),
    path('staffmember-profile', views.staffmember_profile_view,name='staffmember-profile'),
    path('edit-staffmember-profile', views.edit_staffmember_profile_view,name='edit-staffmember-profile'),

    path('staffmember-attendance', views.staffmember_attendance_view,name='staffmember-attendance'),



    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customer-request', views.customer_request_view,name='customer-request'),
    path('customer-add-request',views.customer_add_request_view,name='customer-add-request'),

    path('customer-profile', views.customer_profile_view,name='customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile_view,name='edit-customer-profile'),
    path('customer-feedback', views.customer_feedback_view,name='customer-feedback'),
    path('customer-invoice', views.customer_invoice_view,name='customer-invoice'),
    path('customer-view-request',views.customer_view_request_view,name='customer-view-request'),
    path('customer-delete-request/<int:pk>', views.customer_delete_request_view,name='customer-delete-request'),
    path('customer-view-approved-request',views.customer_view_approved_request_view,name='customer-view-approved-request'),
    path('customer-view-approved-request-invoice',views.customer_view_approved_request_invoice_view,name='customer-view-approved-request-invoice'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='member/index.html'),name='logout'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
]
