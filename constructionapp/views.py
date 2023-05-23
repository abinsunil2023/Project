from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth import logout
from textblob import TextBlob

# Create your views here.
def homepage(request):
    return render(request,'index.html')

def admin_home(request):
    return render(request,'admin/index.html')

def company_home(request):
    return render(request, "construction/index.html")

def user_home(request):
    return render(request,'user/index.html')

def logout1(request):
    logout(request)
    return redirect('login')

def logouting(request):
    logout(request)
    return redirect('login')

def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        print("post username and password")
        cursor = connection.cursor()
        cursor.execute("select * from company where name= '" + userid + "' AND password = '" + password + "' AND status = 'approved'")
        company = cursor.fetchone()

        print('level 2')
        if company == None:
            messages.error(request, 'Invalid Username Or Password!!')
            cursor.execute("select * from login where admin_id = '" + userid + "' AND password = '" + password + "'")
            admin = cursor.fetchone()
            print('level 3')

            if admin == None:
                cursor.execute("select * from user_register where email= '" + userid + "' AND password = '" + password + "'")
                user = cursor.fetchone()

                if user == None:
                    print('level 5')
                    return redirect('login')
                else:
                    u = list(user)
                    userid1 = u[1]
                    request.session["userId"] = userid1
                    return redirect('userhome')
            else:
                request.session["adminId"] = userid
                return redirect('adminhome')
        else:
            request.session["companyId"] = userid
            print("company login")
            return redirect("companyhome")
    print('failed login')
    return render(request, 'login.html')


def company_signup(request):
    if request.method == "POST":
        company_id = request.POST['name']
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        cursor = connection.cursor()
        cursor.execute("select * from company where company_id= '" + company_id + "' ")
        company = cursor.fetchone()

        if company == None:
            cursor.execute("insert into company values('" + company_id + "','" + str(name) + "','" + str(address) + "','" + str(phone) + "','" + str(email) + "','pending','" + str(password) + "','" + str(image) + "')")
            request.session["companyId"] = company_id
            return redirect("login")
        else:
            return HttpResponse("<script>alert('User Name already exists');window.location='../signup';</script>")
    else:
        return render(request,"construction/company_register.html")


def user_signup(request):
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("select * from user_register where name = '"+str(name)+"' AND email = '"+str(email)+"' AND password= '" + str(password) + "' ")
        company = cursor.fetchone()

        if company == None:
            cursor.execute("insert into user_register values(null,'" + str(name) + "','" + str(address) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "')")
            request.session["userId"] = name
            return redirect("userhome")
        else:
            return HttpResponse("<script>alert('Please enter a strong password');window.location='../usersignup';</script>")
    else:
        return render(request,"user/user_register.html")


def new_registration(request):
    cursor = connection.cursor()
    cursor.execute("select * from company where status = 'pending' ")
    company = cursor.fetchall()
    return render(request,'admin/New_company_registration.html',{'data':company})

def approve_company(request,company_id):
    cursor = connection.cursor()
    cursor.execute("update company set status = 'approved' where company_id = '"+str(company_id)+"'")
    return redirect('newregistration')

def appoved_company(request):
    cursor = connection.cursor()
    cursor.execute("select * from company where status = 'approved'")
    company = cursor.fetchall()
    return render(request,'admin/view_approved_company.html',{'data':company})

def delete_company(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from company where company_id ='"+str(id)+"'")
    return redirect('newregistration')

def delete_company1(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from company where company_id ='"+str(id)+"' ")
    return redirect('approvedcompany')

def block_company(request,id):
    cursor = connection.cursor()
    cursor.execute("update company set status = 'block' where company_id = '"+str(id)+"'")
    return redirect('approvedcompany')

def unblock_company(request,id):
    cursor = connection.cursor()
    cursor.execute("update company set status = 'approved' where company_id = '"+str(id)+"'")
    return redirect('approvedcompany')

def view_blocked_company(request):
    cursor = connection.cursor()
    cursor.execute("select * from company where status = 'block'")
    company = cursor.fetchall()
    return render(request, 'admin/blocked_company.html', {'data': company})

def view_company(request):
    cursor = connection.cursor()
    cursor.execute("select * from company where status = 'approved' ")
    company = cursor.fetchall()
    return render(request,'user/view_company.html',{'data':company})

def work_request(request):
    if request.method == 'POST':
        user_id =request.session["userId"]
        phone = request.POST['phone']
        details = request.POST['details']
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        cursor = connection.cursor()
        cursor.execute("insert into work_request values(null,'"+str(user_id)+"','"+str(details)+"','"+str(image)+"',curdate(),'pending','"+str(phone)+"')")
        print('data inserted into table')
        return redirect('workrequest')
    else:
        return render(request,'user/work_request.html')


def view_work_request(request):
    cursor = connection.cursor()
    cursor.execute("select * from work_request where status = 'pending'")
    work = cursor.fetchall()
    return render(request,'construction/view_work_request.html',{'data':work})

def response_work_request(request,id,userid):
    if request.method=='POST':
        print("post working")
        company_id = request.session["companyId"]
        idwork_request = id
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        amount = request.POST['amount']
        user_id = userid
        cursor = connection.cursor()
        print("______________")
        cursor.execute("insert into company_plan_images values(null,'"+str(company_id)+"','"+str(idwork_request)+"',curdate(),'"+str(image)+"','"+str(amount)+"','pending','"+str(user_id)+"')")
        return redirect('responseworkrequest',id=id,userid=userid)

    return render(request,'construction/company_plan_image.html')


def send_plan_request(request):
    cursor = connection.cursor()
    company_id = request.session["companyId"]
    cursor.execute("SELECT company_plan_images.*, work_request.requirement_details from company_plan_images join work_request where company_plan_images.idwork_request = work_request.idwork_request and company_plan_images.company_id = '"+str(company_id)+"'")
    data = cursor.fetchall()
    connection.close()
    return render(request,'construction/send_plan_request.html',{'data':data})


def view_company_response(request):
    cursor = connection.cursor()
    userid = request.session["userId"]
    cursor.execute("select * from company_plan_images where user_id = '"+str(userid)+"' and status = 'pending'")
    data = cursor.fetchall()
    connection.close()
    return render(request,'user/view_company_response.html',{'data':data})


def accept_work_request(request,id,idwrk):
    cursor = connection.cursor()
    if request.method == 'POST':
        card_number = request.POST['card_no']
        cvv = request.POST['cvv']
        date = request.POST['date']
        card_holder = request.POST['card_holder']
        userid =  request.session["userId"]

        cursor.execute("select * from account_table where card_no = '" + str(card_number) + "' and cvv = '" + str(cvv) + "' and exp_date = '" + str(date) + "' and card_holder = '" + str(card_holder) + "'")
        card = cursor.fetchone()
        print("----------------------------------------------------------------------", card_number, date)
        if card == None:
            return redirect('acceptworkrequest',id,idwrk)
        else:
            cursor.execute("update company_plan_images set status = 'abort' where idwork_request = '" + str(idwrk) + "' and user_id = '"+userid+"' ")
            cursor.execute("update company_plan_images set status = 'approved' where idcompany_plan_images = '" + str(id) + "'")
            cursor.execute("delete from company_plan_images where status = 'abort'")
            cursor.execute("update work_request set status = 'approved' where idwork_request = '"+idwrk+"'")
            return render(request, 'user/success_page.html')
    else:
        cursor.execute("select * from account_table")
        value = cursor.fetchone()
        return render(request, 'user/make_payment.html', {'i': value})


def deleteworkrequest(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from company_plan_images where idcompany_plan_images = '"+id+"'")
    connection.close()
    return redirect('viewcompanyresponse')


# construction
#----------------------------------------------------------------------------------------------------------

def accepted_work(request):
    companyid = request.session['companyId']
    cursor = connection.cursor()
    cursor.execute("SELECT company_plan_images.*, work_request.requirement_details from company_plan_images join work_request where company_plan_images.status = 'approved' and company_plan_images.idwork_request = work_request.idwork_request and company_plan_images.company_id = '"+str(companyid)+"'")
    work = cursor.fetchall()
    connection.close()
    return render(request,'construction/accepted_work.html',{'data':work})

def work_agreement(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        start_date = request.POST['start']
        end_date = request.POST['end']
        total_expense  = request.POST['total']

        cursor.execute("insert into work_agrement values(null,'"+id+"','"+start_date+"','"+end_date+"','"+total_expense+"')")
        return redirect('acceptedwork')
    else:
        cursor.execute("select * from work_agrement where idcompany_plan_images = '"+id+"'")
        work = cursor.fetchone()
        if work == None:
            return render(request,'construction/add_work_agreement.html')
        else:
            return HttpResponse("<script>alert('already added work agreement');window.location='../acceptedwork';</script>")


def work_progress(request,id):
    if request.method == 'POST':
        details = request.POST['details']
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        company = request.session["companyId"]

        cursor =  connection.cursor()
        cursor.execute("insert into work_progress values(null,'"+company+"','"+id+"','"+details+"','"+str(image)+"',curdate())")
        return redirect('acceptedwork')
    else:
        return render(request,'construction/add_work_progress.html')

# CONNECTED
# ----------------------------------------------------

def add_feed(request,id):
    return render(request, "user/feedback.html", {'id':id})

def sendfb(request):
    cursor = connection.cursor()
    if request.method == "POST":
        fbdetails = request.POST['fbdetails']
        company = request.POST['company']
        user= request.session["userId"]
        cursor.execute("insert into feedback values( null,'" + str(user) + "','" + str(company) + "', '" + str(fbdetails) + "',curdate() )")
        messages.info(request, "done")
        feedback = fbdetails
        # print text
        print(feedback)
        obj = TextBlob(feedback)
        # returns the sentiment of text
        # by returning a value between -1.0 and 1.0
        sentiment = obj.sentiment.polarity
        print(sentiment)
        if sentiment == 0:
            print('The text is neutral')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk  where company ='"+str(company)+"' ")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,0,0,1,'"+str(company)+"')")
            else:
                cursor = connection.cursor()
                cursor.execute("update feedback_nltk set neutral_count=neutral_count+1  where company ='"+str(company)+"'")
        elif sentiment > 0:
            print('The text is positive')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk where company ='"+str(company)+"'")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,1,0,0,'"+str(company)+"')")
            else:
                cursor = connection.cursor()
                cursor.execute("update feedback_nltk set positive_count=positive_count+1 where company ='"+str(company)+"' ")
        else:
            print('The text is negative')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk where company ='"+str(company)+"' ")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,0,1,0,'"+str(company)+"')")
            else:
                cursor = connection.cursor()
                cursor.execute("update review_nltk set negative_count=negative_count+1 where company ='"+str(company)+"' ")

        return redirect("viewcompany")


def admin_nltk_feedback(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback_nltk")
    data = cursor.fetchall()
    connection.close()
    return render(request,'admin/feedback.html',{'data':data})

def bookedcompanyresponse(request):
    cursor = connection.cursor()
    user = request.session["userId"]
    cursor.execute("select company_plan_images.*, company.name from company_plan_images join company where company_plan_images.user_id = '"+str(user)+"' and company_plan_images.status = 'approved' and company_plan_images.company_id = company.company_id ")
    data = cursor.fetchall()
    connection.close()
    return render(request,'user/booked_plans.html',{'data':data})

def viewworkprogress(request,id):
    cursor = connection.cursor()
    user = request.session["userId"]
    cursor.execute("select work_progress.* from work_progress join company_plan_images where work_progress.idcompany_plan_images ='"+str(id)+"' and company_plan_images.user_id ='"+user+"' and work_progress.idcompany_plan_images = company_plan_images.idcompany_plan_images  ")
    data =cursor.fetchall()
    print(data)
    connection.close()
    return render(request,'user/work_progress.html',{'data':data})

def viewworkagrement(request,id):
    cursor = connection.cursor()
    user = request.session["userId"]
    cursor.execute("select work_agrement.* from work_agrement join company_plan_images where work_agrement.idcompany_plan_images ='"+str(id)+"' and company_plan_images.user_id ='"+user+"' and work_agrement.idcompany_plan_images = company_plan_images.idcompany_plan_images  ")
    data =cursor.fetchall()
    print(data)
    connection.close()
    return render(request,'user/work_agreement.html',{'data':data})
