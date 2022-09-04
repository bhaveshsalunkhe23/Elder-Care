# Elder-Care
Elder Care Technology platform provide services to your seniors, who could be your parents, uncles, grandparents, with the help of an Elder Care web app. When in an emergency or they need services like Home modifications, Personal care, Household maintenance we provide our members/workers who can provide the best care to your elderly even when you are not around.
---
![developer](https://img.shields.io/badge/Developed%20By%20%3A-Bhavesh%20Salunkhe-red)
---
## SCREENSHOTS
## Home Page
![home1](https://user-images.githubusercontent.com/85333458/188221047-c39b9013-f604-4af8-ad35-60af7f1b89e9.png)
-
![home2](https://user-images.githubusercontent.com/85333458/188221065-b22e92a5-8f85-41e2-9e00-0796dad33d43.png)


## Admin Dashboard
### Dark theme
![admin-dark](https://user-images.githubusercontent.com/85333458/188221253-18f8824b-277f-4187-9383-ef71a4ea7fdf.png)
### Light theme
![admin-light](https://user-images.githubusercontent.com/85333458/188220861-7116f3aa-1273-4376-8a98-e0159b32fda2.png)
### Customers
![customer](https://user-images.githubusercontent.com/85333458/188221815-ed46eacb-d01d-4ae6-86ac-a15e4f8aa0e6.png)
### Staff Members
![staff-member](https://user-images.githubusercontent.com/85333458/188221858-7deda5a6-776d-4c94-a346-cb1e71fd0fdf.png)

## Customer Dashboard
![customer-request](https://user-images.githubusercontent.com/85333458/188222129-2aa4d2fe-4ce2-438f-bf8f-ae5a0bc10b1e.png)

## Staff Member Dashboard
![staff-member](https://user-images.githubusercontent.com/85333458/188222041-1076d49e-bb65-43af-b300-c457ba626471.png)

## FUNCTIONS
## Customer
- customer will signup and login into system
- customer can make request for service of they want by providing details (Elder Name, Age, Services, Requirement description etc.)
- After Request approved by admin, customer can check cost, status of service
- customer can delete request (Enquiry) if customer change their mind or not approved by admin (ONLY PENDING REQUEST CAN BE DELETED )
- customer can check status of Request(Enquiry) that is Pending, Approved, Service Done, Released
- customer can check invoice details or Service Done
- customer can send feedback to admin
- customer can see/edit their profile
---
## Staff Member
- Member will apply for job by providing details like (Service Skills, Address, Mobile etc.)
- Admin will hire(approve) member account based on skill
- After account approval, member can login into system
- member can see how many work (Services to be) is assigned to me
- member can change status of service ('Pending Task', 'Task Done') according to work progress
- member can see salary and how many Services he/she have done so far
- member can send feedback to admin
- member can see/edit their profile
---
### Admin
- First admin will login ( for username/password run following command in cmd )
```
py manage.py createsuperuser
```
- Give username, email, password and your admin account will be created.
- After login , admin can see how many customer, staff member, recent service orders on dashboard
- Admin can see/add/update/delete customers
- Admin can see each customer invoice (if two request made by same customer it will show total sum of both request)
- Admin can see/add/update/delete members
- Admin can approve(hire) staff member (requested by members) based on their skills
- Admin can see/update member salary
- Admin can see/update/delete request/enquiry for service sent by customer
- Admin can also make request for service (suppose customer directly reached to service center/office)
- Admin can approve request for service made by customer and assign to member for repairing and will provide cost according to Requirement description
- Admin can see all service cost of request (both approved and pending)
- Admin can see feedbacks sent by customer/member
---
### Other Features
- we can change theme of website day(white) and night(black)
- if customer is deleted by admin then their request(Enquiry) will be deleted automatically

## Requirement/Tech Stack Use
```
python==3.10.1
asgiref==3.2.7
Django==3.0.5
django-widget-tweaks==1.4.8
pytz==2020.1
sqlparse==0.3.1

```

## Feedback
Any suggestion and feedback is welcome. You can message me on linkedin
- [Connect me on Linkedin](https://www.linkedin.com/in/bhavesh-salunkhe-2002)
- [Visit my website](https://bhaveshsalunkhe.me/)

