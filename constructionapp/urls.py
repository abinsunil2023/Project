from django.urls import path
from . import views

urlpatterns = [
    # path('',views.login,name="login"),
    path('',views.homepage,name="homepage"),
    path('login',views.login,name="login"),
    path('logout',views.logout1,name=""),
    path('logouting',views.logouting,name="logouting"),
    path('adminhome',views.admin_home,name="adminhome"),
    path('companyhome',views.company_home,name="companyhome"),
    path('userhome',views.user_home,name="userhome"),
    path('companysignup',views.company_signup,name="companysignup"),
    path('usersignup',views.user_signup,name="usersignup"),
    path('newregistration',views.new_registration,name="newregistration"),
    path('approvecompany/<str:company_id>',views.approve_company,name="approvecompany"),
    path('approvedcompany',views.appoved_company,name="approvedcompany"),
    path('deletecompany/<str:id>',views.delete_company,name="deletecompany"),
    path('blockcompany/<str:id>',views.block_company,name="blockcompany"),
    path('unblockcompany/<str:id>',views.unblock_company,name="unblockcompany"),
    path('blockedcompany',views.view_blocked_company,name="blockedcompany"),
    path('deletecompany1/<str:id>', views.delete_company1, name="deletecompany1"),
    path('viewcompany',views.view_company,name="viewcompany"),
    path('workrequest',views.work_request,name="workrequest"),
    path('viewworkrequest',views.view_work_request,name="viewworkrequest"),
    path('responseworkrequest/<str:id>/<str:userid>',views.response_work_request,name="responseworkrequest"),
    path('sendplanrequest',views.send_plan_request,name="sendplanrequest"),
    path('viewcompanyresponse',views.view_company_response,name="viewcompanyresponse"),
    path('acceptworkrequest/<str:id>/<str:idwrk>',views.accept_work_request,name="acceptworkrequest"),
    path('deleteworkrequest/<str:id>',views.deleteworkrequest,name="deleteworkrequest"),
    ###
    path('acceptedwork',views.accepted_work,name="acceptedwork"),
    path('workrequest/<str:id>',views.work_agreement,name="workrequest"),
    path('workprogress/<str:id>',views.work_progress,name="workprogress"),
    ######
    path('add_feed/<str:id>',views.add_feed, name="add_feed"),
    path('sendfb', views.sendfb, name='sendfb'),
    path('admin_nltk_feedback', views.admin_nltk_feedback, name='admin_nltk_feedback'),

    path('bookedcompanyresponse', views.bookedcompanyresponse, name='bookedcompanyresponse'),
    path('viewworkagrement/<str:id>', views.viewworkagrement, name='viewworkagrement'),
    path('viewworkprogress/<str:id>', views.viewworkprogress, name='viewworkprogress'),

]