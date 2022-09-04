from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'member/index.html')


#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'member/customerclick.html')

#for showing signup/login button for staffmembers
def staffmembersclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'member/staffmembersclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'member/customersignup.html',context=mydict)


def staffmember_signup_view(request):
    userForm=forms.staffmemberUserForm()
    staffmemberForm=forms.staffmemberForm()
    mydict={'userForm':userForm,'staffmemberForm':staffmemberForm}
    if request.method=='POST':
        userForm=forms.staffmemberUserForm(request.POST)
        staffmemberForm=forms.staffmemberForm(request.POST,request.FILES)
        if userForm.is_valid() and staffmemberForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staffmember=staffmemberForm.save(commit=False)
            staffmember.user=user
            staffmember.save()
            my_staffmember_group = Group.objects.get_or_create(name='staffmember')
            my_staffmember_group[0].user_set.add(user)
        return HttpResponseRedirect('staffmemberlogin')
    return render(request,'member/staffmembersignup.html',context=mydict)


#for checking user customer, staffmember or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_staffmember(user):
    return user.groups.filter(name='staffmember').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')
    elif is_staffmember(request.user):
        accountapproval=models.staffmember.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('staffmember-dashboard')
        else:
            return render(request,'member/staffmember_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start
#============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_staffmember':models.staffmember.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'member/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'member/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'member/admin_view_customer.html',{'customers':customers})


@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'member/update_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'member/admin_add_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'member/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'member/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_staffmember_view(request):
    return render(request,'member/admin_staffmember.html')


@login_required(login_url='adminlogin')
def admin_approve_staffmember_view(request):
    staffmembers=models.staffmember.objects.all().filter(status=False)
    return render(request,'member/admin_approve_staffmember.html',{'staffmembers':staffmembers})

@login_required(login_url='adminlogin')
def approve_staffmember_view(request,pk):
    staffmemberSalary=forms.staffmemberSalaryForm()
    if request.method=='POST':
        staffmemberSalary=forms.staffmemberSalaryForm(request.POST)
        if staffmemberSalary.is_valid():
            staffmember=models.staffmember.objects.get(id=pk)
            staffmember.salary=staffmemberSalary.cleaned_data['salary']
            staffmember.status=True
            staffmember.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-staffmember')
    return render(request,'member/admin_approve_staffmember_details.html',{'staffmemberSalary':staffmemberSalary})


@login_required(login_url='adminlogin')
def delete_staffmember_view(request,pk):
    staffmember=models.staffmember.objects.get(id=pk)
    user=models.User.objects.get(id=staffmember.user_id)
    user.delete()
    staffmember.delete()
    return redirect('admin-approve-staffmember')


@login_required(login_url='adminlogin')
def admin_add_staffmember_view(request):
    userForm=forms.staffmemberUserForm()
    staffmemberForm=forms.staffmemberForm()
    staffmemberSalary=forms.staffmemberSalaryForm()
    mydict={'userForm':userForm,'staffmemberForm':staffmemberForm,'staffmemberSalary':staffmemberSalary}
    if request.method=='POST':
        userForm=forms.staffmemberUserForm(request.POST)
        staffmemberForm=forms.staffmemberForm(request.POST,request.FILES)
        staffmemberSalary=forms.staffmemberSalaryForm(request.POST)
        if userForm.is_valid() and staffmemberForm.is_valid() and staffmemberSalary.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staffmember=staffmemberForm.save(commit=False)
            staffmember.user=user
            staffmember.status=True
            staffmember.salary=staffmemberSalary.cleaned_data['salary']
            staffmember.save()
            my_staffmember_group = Group.objects.get_or_create(name='staffmember')
            my_staffmember_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-staffmember')
        else:
            print('problem in form')
    return render(request,'member/admin_add_staffmember.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_staffmember_view(request):
    staffmembers=models.staffmember.objects.all()
    return render(request,'member/admin_view_staffmember.html',{'staffmembers':staffmembers})


@login_required(login_url='adminlogin')
def delete_staffmember_view(request,pk):
    staffmember=models.staffmember.objects.get(id=pk)
    user=models.User.objects.get(id=staffmember.user_id)
    user.delete()
    staffmember.delete()
    return redirect('admin-view-staffmember')


@login_required(login_url='adminlogin')
def update_staffmember_view(request,pk):
    staffmember=models.staffmember.objects.get(id=pk)
    user=models.User.objects.get(id=staffmember.user_id)
    userForm=forms.staffmemberUserForm(instance=user)
    staffmemberForm=forms.staffmemberForm(request.FILES,instance=staffmember)
    mydict={'userForm':userForm,'staffmemberForm':staffmemberForm}
    if request.method=='POST':
        userForm=forms.staffmemberUserForm(request.POST,instance=user)
        staffmemberForm=forms.staffmemberForm(request.POST,request.FILES,instance=staffmember)
        if userForm.is_valid() and staffmemberForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staffmemberForm.save()
            return redirect('admin-view-staffmember')
    return render(request,'member/update_staffmember.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_staffmember_salary_view(request):
    staffmembers=models.staffmember.objects.all()
    return render(request,'member/admin_view_staffmember_salary.html',{'staffmembers':staffmembers})

@login_required(login_url='adminlogin')
def update_salary_view(request,pk):
    staffmemberSalary=forms.staffmemberSalaryForm()
    if request.method=='POST':
        staffmemberSalary=forms.staffmemberSalaryForm(request.POST)
        if staffmemberSalary.is_valid():
            staffmember=models.staffmember.objects.get(id=pk)
            staffmember.salary=staffmemberSalary.cleaned_data['salary']
            staffmember.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-staffmember-salary')
    return render(request,'member/admin_approve_staffmember_details.html',{'staffmemberSalary':staffmemberSalary})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'member/admin_request.html')

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'member/admin_view_request.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.staffmember=adminenquiry.cleaned_data['staffmember']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'member/admin_approve_request_details.html',{'adminenquiry':adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')



@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry=forms.RequestForm()
    adminenquiry=forms.AdminRequestForm()
    mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        adminenquiry=forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=adminenquiry.cleaned_data['customer']
            enquiry_x.staffmember=adminenquiry.cleaned_data['staffmember']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status='Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request,'member/admin_add_request.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'member/admin_approve_request.html',{'enquiry':enquiry})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.staffmember=adminenquiry.cleaned_data['staffmember']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'member/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'member/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request,'member/update_cost.html',{'updateCostForm':updateCostForm})



@login_required(login_url='adminlogin')
def admin_staffmember_attendance_view(request):
    return render(request,'member/admin_staffmember_attendance.html')


@login_required(login_url='adminlogin')
def admin_take_attendance_view(request):
    staffmembers=models.staffmember.objects.all().filter(status=True)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                print(staffmembers[i].id)
                print(int(staffmembers[i].id))
                staffmember=models.staffmember.objects.get(id=int(staffmembers[i].id))
                AttendanceModel.staffmember=staffmember
                AttendanceModel.save()
            return redirect('admin-view-attendance')
        else:
            print('form invalid')
    return render(request,'member/admin_take_attendance.html',{'staffmembers':staffmembers,'aform':aform})

@login_required(login_url='adminlogin')
def admin_view_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date)
            staffmemberdata=models.staffmember.objects.all().filter(status=True)
            mylist=zip(attendancedata,staffmemberdata)
            return render(request,'member/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'member/admin_view_attendance_ask_date.html',{'form':form})

@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'member/admin_report.html',context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'member/admin_feedback.html',{'feedback':feedback})

#============================================================================================
# ADMIN RELATED views END
#============================================================================================


#============================================================================================
# CUSTOMER RELATED views start
#============================================================================================

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(customer_id=customer.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Pending") | Q(status="Approved")).count()
    bill=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_request_made':new_request_made,
    'bill':bill['cost__sum'],
    'customer':customer,
    }
    return render(request,'member/customer_dashboard.html',context=dict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'member/customer_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'member/customer_view_request.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'member/customer_view_approved_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'member/customer_view_approved_request_invoice.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.RequestForm()
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        if enquiry.is_valid():
            customer=models.Customer.objects.get(user_id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=customer
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request,'member/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'member/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'member/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'member/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'member/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'member/customer_feedback.html',{'feedback':feedback,'customer':customer})
#============================================================================================
# CUSTOMER RELATED views END
#============================================================================================






#============================================================================================
# staffmember RELATED views start
#============================================================================================


@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def staffmember_dashboard_view(request):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(staffmember_id=staffmember.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(staffmember_id=staffmember.id,status='Repairing Done').count()
    new_work_assigned=models.Request.objects.all().filter(staffmember_id=staffmember.id,status='Approved').count()
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_work_assigned':new_work_assigned,
    'salary':staffmember.salary,
    'staffmember':staffmember,
    }
    return render(request,'member/staffmember_dashboard.html',context=dict)

@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def staffmember_work_assigned_view(request):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    works=models.Request.objects.all().filter(staffmember_id=staffmember.id)
    return render(request,'member/staffmember_work_assigned.html',{'works':works,'staffmember':staffmember})


@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def staffmember_update_status_view(request,pk):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    updateStatus=forms.staffmemberUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.staffmemberUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/staffmember-work-assigned')
    return render(request,'member/staffmember_update_status.html',{'updateStatus':updateStatus,'staffmember':staffmember})

@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def staffmember_attendance_view(request):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    attendaces=models.Attendance.objects.all().filter(staffmember=staffmember)
    return render(request,'member/staffmember_view_attendance.html',{'attendaces':attendaces,'staffmember':staffmember})





@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def staffmember_feedback_view(request):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'member/feedback_sent.html',{'staffmember':staffmember})
    return render(request,'member/staffmember_feedback.html',{'feedback':feedback,'staffmember':staffmember})

@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def staffmember_salary_view(request):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(staffmember_id=staffmember.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'member/staffmember_salary.html',{'workdone':workdone,'staffmember':staffmember})

@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def staffmember_profile_view(request):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    return render(request,'member/staffmember_profile.html',{'staffmember':staffmember})

@login_required(login_url='staffmemberlogin')
@user_passes_test(is_staffmember)
def edit_staffmember_profile_view(request):
    staffmember=models.staffmember.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=staffmember.user_id)
    userForm=forms.staffmemberUserForm(instance=user)
    staffmemberForm=forms.staffmemberForm(request.FILES,instance=staffmember)
    mydict={'userForm':userForm,'staffmemberForm':staffmemberForm,'staffmember':staffmember}
    if request.method=='POST':
        userForm=forms.staffmemberUserForm(request.POST,instance=user)
        staffmemberForm=forms.staffmemberForm(request.POST,request.FILES,instance=staffmember)
        if userForm.is_valid() and staffmemberForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            staffmemberForm.save()
            return redirect('staffmember-profile')
    return render(request,'member/edit_staffmember_profile.html',context=mydict)






#============================================================================================
# staffmember RELATED views start
#============================================================================================




# for aboutus and contact
def aboutus_view(request):
    return render(request,'member/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'member/contactussuccess.html')
    return render(request, 'member/contactus.html', {'form':sub})
