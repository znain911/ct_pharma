from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from login.models import  owner ,otp_table
from good_recieve.models import CompanyList ,PharmacyList, OrderList,med_unit,generic_list
from django.core import serializers
from random import randint
from pip._vendor import requests
import json
import hashlib 
from django.core.paginator import Paginator

# Create your views here.
def login(request):
    username = ''
    if request.session.has_key('role') and (request.session['role'] == 'admin' or request.session['role'] == '1' or request.session['role'] == '2'
                                            or request.session['role'] == '3' or request.session['role'] == '4'):
        #username = request.session['username']
        company = CompanyList.objects.all()
        units = med_unit.objects.all()
        generic_lis = generic_list.objects.all()
        #pharmacy = PharmacyList.objects.all()
    
        if request.session['role'] == '1':
            outletid =request.session['outletid']
            orderlist = OrderList.objects.filter(status	='Good Recieve', outlet_id = outletid).select_related('company_id')
            pharmacy = PharmacyList.objects.filter(id = outletid)
            
            #print(request.session['role'])
            return render(request,  'good_recieved.html',{"companies": company , "pharmacy": pharmacy, "orderlist": orderlist, "units": units, "generic_list": generic_lis})
        elif request.session['role'] == '2':
            outletid =request.session['outletid']
            starttime =request.session['starttime']
            endtime =request.session['endtime']
            endtimereduce = int(endtime) - 1
            orderlist = OrderList.objects.filter(status	='Good Recieve', outlet_id = outletid,create_date__hour__range=(int(starttime), endtimereduce)).select_related('company_id')
            pharmacy = PharmacyList.objects.filter(id = outletid)
            
            #print(request.session['endtime'])
            return render(request,  'good_recieved.html',{"companies": company , "pharmacy": pharmacy, "orderlist": orderlist, "units": units, "generic_list": generic_lis})
        elif request.session['role'] == '3':
            outletid =request.session['outletid']
            pharmacy = PharmacyList.objects.filter(id = outletid)
            return render(request, 'sales.html',{"pharmacy": pharmacy})
        else:
            orderlist = OrderList.objects.filter(status	='Good Recieve').select_related('company_id')
            pharmacy = PharmacyList.objects.all()

            paginator = Paginator(orderlist, 10)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            return render(request,  'good_recieved.html',{"companies": company , "pharmacy": pharmacy, "orderlist": page_obj, "units": units, "generic_list": generic_lis})
    else:
        return render(request, 'login.html')
    
def verify_otp(request):
    if request.method == 'POST':
        AllData = {}
        id = request.session['userid']

        otp1 = request.POST.get("otp1", "")
        otp2 = request.POST.get("otp2", "")
        otp3 = request.POST.get("otp3", "")
        otp4 = request.POST.get("otp4", "")
        otp5 = request.POST.get("otp5", "")

        otp_verified = False
        user = ''
        role = ''

        otp = otp1 + otp2 + otp3 + otp4 + otp5
        verify = otp_table.objects.filter(otp = otp ,owner_id_id  = id )

        if verify:
            otp_verified = True
            get_user = owner.objects.filter(id= id )
            user_serialized= serializers.serialize('python', get_user)
            user = user_serialized[0]
            role = get_user[0].role

            #session 
            request.session['username'] = get_user[0].fullname
            request.session['role'] = get_user[0].role
            request.session['userId'] = get_user[0].id
            request.session.save()
            #print(get_user[0].role)

            if get_user[0].role == '1' :
                request.session['outletid'] = get_user[0].outlet
            elif  get_user[0].role == '2':
                request.session['outletid'] = get_user[0].outlet
                request.session['starttime'] = get_user[0].shift_start
                request.session['endtime'] = get_user[0].shift_end
                



        AllData['id'] = id
        AllData['otp'] = otp
        AllData['otp_verified'] = otp_verified
        AllData['get_user'] = user
        AllData['role'] = role

        return JsonResponse(AllData, safe=False)
    else:
        pass

def verify_user(request):

    phone = request.POST.get("phone", "")
    #password = request.POST.get("pass", "")
    role = request.POST.get("role", "")

    #result = hashlib.sha1(password.encode()) 

    data = ''
    setrole = ''
    otp = ''
    ac_active = False
    AllData = {}
    otpStatus = 'False'

   # verify = owner.objects.filter(phone = phone , password = result.hexdigest(), active = '1')
    verify = owner.objects.filter(phone = phone ,role = role)
    if verify:
        serialized_queryset = serializers.serialize('python', verify)
        data = serialized_queryset[0]
        phone = None
        if verify[0].active == '1':
            ac_active = True
            range_start = 10**(5-1)
            range_end = (10**5)-1
            otp = randint(range_start, range_end)
            otptext = 'Your OTP ' + str(otp)

            insertOtp = otp_table(owner_id_id = verify[0].id, outlet_id = verify[0].outlet,otp= str(otp))
            insertOtp.validate_unique()
            insertOtp.save()

            request.session['userid'] = verify[0].id

            url = ""

            payload = {"api_key" : "",
                        "type" : "text",
                        "contacts" : verify[0].phone,
                        "senderid" : "",
                        "msg": otptext
                        }
            headers = {}

            response = requests.post( url, headers=headers, data=payload,verify=False)
            if 'SMS SUBMITTED:' in response.text:
                otpStatus = 'True'
                phone = verify[0].phone
            else:
                otpStatus =response.text

            #print(response.text)
            
            if verify[0].role == 'admin':
                setrole = 'admin'
                # request.session['username'] = verify[0].fullname
                # request.session['role'] = verify[0].role
        
        # request.session['username'] = verify[0].fullname
        # request.session['role'] = verify[0].role
            #request.session['role'] = 'user'

    AllData['ac_active'] = ac_active
    AllData['data'] = data
    AllData['role'] = setrole
    AllData['otp'] = otp
    AllData['otpStatus'] = otpStatus
    AllData['Phone'] = phone
    return JsonResponse(AllData, safe=False)

def registration(request):
    username = ''
    if request.session.has_key('role') and request.session['role'] == 'admin':
        user = owner.objects.all().exclude(role = 'admin')
        pharmacy = PharmacyList.objects.all()

        return render(request, 'registration.html',{"users" :user, "pharmacy": pharmacy})
    else:
        return render(request, 'login.html')
    
def update_user(request):
    if request.session.has_key('role') and request.session['role'] == 'admin':

        role = request.GET.get("role", "")
        id = request.GET.get("id", "")
        shift = None
        splitString = None
        shiftStart = None
        shiftEnd = None
        if role != ' ':

            if role == '1':
                t = owner.objects.get(id=id )
                t.role = role
                t.active = '1'
                t.save()
            elif role == '2' or role == '3':
                shift = request.GET.get("shift", "")
                splitString = shift.split('to')
                shiftStart = splitString[0]
                shiftEnd = splitString[1]

                t = owner.objects.get(id=id )
                t.shift_end = shiftEnd
                t.shift_start = shiftStart
                t.role = role
                t.active = '1'
                t.save()

        else:
            t = owner.objects.get(id=id )
            #t.role = 'inactive'
            # t.active = '0'
            # t.save()


        return JsonResponse(shiftEnd, safe=False)
    else:
        return render(request, 'login.html')
    
def register_user(request):

    if request.session.has_key('role') and request.session['role'] == 'admin':

        name = request.POST.get("name", "")
        gender = request.POST.get("gender", "")
        phone = request.POST.get("phone", "")
        nid = request.POST.get("nid", "")
        outlet = request.POST.get("outlet", "")

        exist = ''

        userCheck = owner.objects.filter(phone = phone)
        if not userCheck:
            newuser = owner(fullname = name,phone=phone,gender = gender,nid=nid,outlet=outlet)
            newuser.validate_unique()
            newuser.save()
        else:
            exist = 'exist'
        

        return JsonResponse(exist, safe=False)
    else:
        return render(request, 'login.html')
