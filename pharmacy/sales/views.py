from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from good_recieve.models import CompanyList , MedList ,PharmacyList
from inventory.models import InventoryList , InventoryMed
from sales.models import customers
from django.core import serializers
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

# Create your views here.


def sales(request):

    if request.session.has_key('role') and (request.session['role'] == 'admin' or request.session['role'] == '1'or request.session['role'] == '2'or request.session['role'] == '3'):

        if request.session['role'] == '1' or request.session['role'] == '2'or request.session['role'] == '3':
            outletid =request.session['outletid']
            pharmacy = PharmacyList.objects.filter(id = outletid)
        else:
            pharmacy = PharmacyList.objects.all()
        return render(request, 'sales.html',{"pharmacy": pharmacy})
    else:
        return redirect( 'login')
    
def get_med_sale(request):

    if request.session.has_key('username'):
        if 'q' in request.GET:
            qs = MedList.objects.filter(med_name__contains=request.GET.get('q') )[:5]
            #serialized_queryset = serializers.serialize('python', qs)
            
            meds = list()
            for medicine in qs:
                meds.append(medicine.med_name)
            return JsonResponse(meds, safe=False)
        
        else:
            return JsonResponse('if did not work')
    else:
        return redirect( 'login')
    

def get_customer(request):

    if request.session.has_key('username'):
        if 'q' in request.GET:
            qs = customers.objects.filter(name__contains=request.GET.get('q') )[:5]
            #serialized_queryset = serializers.serialize('python', qs)
            
            buyer = list()
            for customer in qs:
                buyer.append(customer.name)
            return JsonResponse(buyer, safe=False)
        
        else:
            return JsonResponse('if did not work')
    else:
        return redirect( 'login')

def get_customer_id(request):

    if request.session.has_key('username'):
        if 'name' in request.GET:
            name = request.GET.get('name').replace("_", " ")
            qs = customers.objects.filter(name=name)[:1]
            #serialized_queryset = serializers.serialize('python', qs)
            
            buyer = qs[0].id
            
            return JsonResponse(buyer, safe=False)
        
        else:
            return JsonResponse('if did not work')
    else:
        return redirect( 'login')
    
def get_med_stock_info(request):

    if request.session.has_key('username'):
        if 'med' in request.GET:
            med = request.GET.get('med').replace("_", " ")
            dt = datetime.now()
            df = DateFormat(dt)
            date = df.format('Y-m-d')
            medinfo = InventoryMed.objects.filter(med_name=med, status = None ,expired_date__gt =date )[:2]
            serialized_queryset = serializers.serialize('python', medinfo)

            coid = None
            med_inId1 = None 
            med_inId2 = None
            med_inStock1 = None
            med_inStock2 = None

            if medinfo:
                if medinfo[0]:
                    coid = medinfo[0].company_id_id 
                    med_inId1 = medinfo[0].id
                    med_inStock1 = medinfo[0].quantity_stock
                if medinfo[1]:
                    med_inId2 = medinfo[1].id
                    med_inStock2 = medinfo[1].quantity_stock
                
            

            data = {}
            data['coid'] = coid
            data['med_inId1'] = med_inId1
            data['med_inId2'] = med_inId2
            data['med_inStock1'] = med_inStock1
            data['med_inStock2'] = med_inStock2
            data['date'] = date


            
            #meds = list()
            # for medicine in qs:
            #     meds.append(medicine.med_name)
            return JsonResponse(data, safe=False)
        
        else:
            return JsonResponse('if did not work')
    else:
        return redirect( 'login')
