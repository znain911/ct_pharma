from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import localtime
from good_recieve.models import CompanyList , MedList ,PharmacyList, OrderList, OrderedMed , med_unit , generic_list
from inventory.models import InventoryList , InventoryMed
from login.models import owner
from django.core import serializers
from datetime import datetime  
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.cache import cache

#for pdf

from io import BytesIO
from django.template.loader import get_template

from xhtml2pdf import pisa



def members(request):
    #return HttpResponse("Hello world!")
    args = {}
    array = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
        }
    people = {1: {'name': 'John', 'age': '27', 'sex': 'Male'},
          2: {'name': 'Marie', 'age': '22', 'sex': 'Female'}}
    
    thislist = ["apple", "banana", "cherry"]
    thislist.insert(1, "orange")
    thislist.remove("banana")
    cars = ["Ford", "Volvo", "BMW"]
    name = 'mishu'
    args['name'] = name
    args['cars'] = cars
    args['array'] = array
    args['thislist'] = thislist
    args['peoples'] = people
    args['today'] = localtime().date()

    return render(request, '1.html',args)

def good_recieved(request):

    if 'role' in request.session:
        if request.session['role'] == 'admin' or request.session['role'] == '1' or request.session['role'] == '4':
            company = CompanyList.objects.all()
            units = med_unit.objects.all()
            generic_lis = generic_list.objects.all()
            #pharmacy = PharmacyList.objects.all()
            #medList = MedList.objects.all()
            if request.session['role'] == '1':
                outletid =request.session['outletid']
                orderlist = OrderList.objects.filter(status	='Good Recieve', outlet_id = outletid).select_related('company_id')
                pharmacy = PharmacyList.objects.filter(id = outletid)

                paginator = Paginator(orderlist, 10)
                page = request.GET.get('page')
                page_obj = paginator.get_page(page)
            elif request.session['role'] == '2':
                outletid =request.session['outletid']
                starttime =request.session['starttime']
                endtime =request.session['endtime']
                endtimereduce = int(endtime) - 1
                orderlist = OrderList.objects.filter(status	='Good Recieve', outlet_id = outletid,create_date__hour__range=(int(starttime), endtimereduce)).select_related('company_id')
                pharmacy = PharmacyList.objects.filter(id = outletid)
                
            else:
                orderlist = OrderList.objects.filter(status	='Good Recieve').select_related('company_id')
                pharmacy = PharmacyList.objects.all()

                paginator = Paginator(orderlist, 10)
                page = request.GET.get('page')
                page_obj = paginator.get_page(page)
            #print(orderlist[0])
            return HttpResponse(render(request, 'good_recieved.html',{"companies": company , "pharmacy": pharmacy, "orderlist": page_obj,
                                                        "role": request.session['role'], "units": units , "generic_list": generic_lis}))
        else:
            return redirect( 'login')
    else:
        return redirect('login')
   
    
def rePdf(request):

    if request.session.has_key('username'):
        if 'reid' in request.GET:
            reid = request.GET.get('reid')
            orderlist = OrderList.objects.filter( id = reid).select_related('company_id')

            companyName = orderlist[0].company_id.companyName
            requisitionId = orderlist[0].pr_id
            date = str(orderlist[0].create_date).split(" ")
            modifyDate = date[0].split("-")
            finalDate = modifyDate[2]+'-'+modifyDate[1]+'-'+modifyDate[0]

            reqBy = owner.objects.filter(id = orderlist[0].order_by)
            reqByName = reqBy[0].fullname

            purchaseFor = PharmacyList.objects.filter( id = orderlist[0].outlet_id)
            purchaseForName = purchaseFor[0].outlet

            meds = OrderedMed.objects.filter(order_id_id = reid)

            tem_path = 'requisition.html'
            context = {'companyName' : companyName,'requisitionId' : requisitionId,'date' : finalDate ,'reqByName' : reqByName,
                       'purchaseFor' : purchaseForName ,'meds' : meds}

            response = HttpResponse(content_type = 'application/pdf')
            response['Content-Disposition'] = 'attachment; filename = "requisition'+requisitionId+'.pdf"'
            template = get_template(tem_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html,dest = response)

            # buf = io.BytesIO()

            # PAGE_WIDTH  = defaultPageSize[0]
            # PAGE_HEIGHT = defaultPageSize[1]

            # c= canvas.Canvas(buf, pagesize=letter , bottomup=0)
            # textob = c.beginText()
            # textob.setTextOrigin(inch , inch)
            # textob.setFont("Helvetica", 20)

            # lines = 'BADAS PHARMACY'
            # textob.setFont("Helvetica", 14)
            # lines += '122,Kazi nazrul Islam Avenue, Shabag,Dhaka-1000'
            
            
            # textob.textLine(lines)
            # c.drawText(textob)
            # c.showPage()
            # c.save()
            # buf.seek(0)

            return response

        else:
            return JsonResponse('if did not work')
    else:
        return redirect( 'login')

def get_med(request):

    if request.session.has_key('username'):
        if 'q' in request.GET:
            qs = MedList.objects.filter(med_name__contains=request.GET.get('q'), company_id_id =request.GET.get('coId') )[:5]
            #serialized_queryset = serializers.serialize('python', qs)
            
            meds = list()
            for medicine in qs:
                meds.append(medicine.med_name)
            return JsonResponse(meds, safe=False)
        
        else:
            return JsonResponse('if did not work')
    else:
        return redirect( 'login')


def gr_filter(request):

    if request.session.has_key('username'):
        if 'status' in request.GET:
            status = request.GET.get('status')
            date1 = request.GET.get('date1')
            date2 = ''
            data = ''
            if request.GET.get('date2'):
                date2 = request.GET.get('date2').replace("_", " ")
            
            if status == 'same':
                if request.session['role'] == '1':
                    outletid =request.session['outletid']
                    qs = OrderList.objects.filter(create_date__contains=date1,outlet_id = outletid).select_related('company_id')
                else:
                    qs = OrderList.objects.filter(create_date__contains=date1).select_related('company_id')
                if qs is not None:
                    serialized_queryset = serializers.serialize('python', qs)
                    data = serialized_queryset

            # qs = OrderList.objects.filter(create_date__contains=date1)
            # value_1 = 'UEFA Champions League'  # or whatever is complicated
            # qs[0].update({'UCL': value_1})
            # serialized_queryset = serializers.serialize('python', qs)
            # data = serialized_queryset


            return JsonResponse(data[0], safe=False)
    else:
        return redirect( 'login')

def get_med_price(request):

    if request.session.has_key('username'):
        if 'med' in request.GET:
            med = request.GET.get('med').replace("_", " ")

            qs = MedList.objects.filter(med_name=med)
            serialized_queryset = serializers.serialize('python', qs)
            return JsonResponse(serialized_queryset[0], safe=False)
    else:
        return redirect( 'login')
    

def edit_requisition(request):
    if request.session.has_key('username'):
        reId = request.GET.get("reId", "")

        return JsonResponse(reId, safe=False)
    else:
        return redirect( 'login')


def save_requisition(request):
        
    if request.session.has_key('username'):
        med_array = request.POST.getlist("med_array[]", "")

        companyId = request.POST.get("companyID", "")
        totalValue = request.POST.get("totalValue", "")
        pharmacyID = request.POST.get("pharmacyID", "")
        shortCode = request.POST.get("shortCode", "")
        userId =request.session['userId']


        dt = datetime.now()
        df = DateFormat(dt)
        date = df.format('dmy')
        companyShortcode = CompanyList.objects.filter(id = companyId)
        requisitionId = OrderList.objects.filter(pr_id__contains =companyShortcode[0].shortCode).count()
        serial = str(requisitionId +1).zfill(7)
        pr_id = 'PR1122'+date + companyShortcode[0].shortCode + serial

        newentry = OrderList(pr_id = pr_id ,company_id_id = companyId,amount=totalValue,status = 'Good Recieve',outlet_id=pharmacyID,outlet_shortcode=shortCode,order_by = userId)
        newentry.validate_unique()
        newentry.save()

        for medinfo in med_array:
            med = request.POST.get("item"+medinfo, "")
            quantity = request.POST.get("quantity"+medinfo, "")
            tp = request.POST.get("price"+medinfo, "")
            mrp = request.POST.get("mrp"+medinfo, "")
            generic = request.POST.get("generic"+medinfo, "")
            unit = request.POST.get("unit"+medinfo, "")
            orderedmed = OrderedMed(med_name = med, quantity= quantity,buying_price= tp,selling_price= mrp,company_id_id =companyId,
                                    order_id_id = newentry.id,generic=generic,unit=unit)
            orderedmed.validate_unique()
            orderedmed.save()

        return JsonResponse(med, safe=False)
    else:
        return redirect( 'login')

def get_ordered(request):

    if request.session.has_key('username'):
        if 'reqid' in request.GET:
            id = request.GET.get('reqid').replace("_", " ")
            comId = request.GET.get('comId').replace("_", " ")
            outlet = request.GET.get('outlet').replace("_", " ")
            data = {}
            #qs = OrderedMed.objects.filter(order_id_id =id).select_related('company_id')
            orderMed = OrderedMed.objects.filter(order_id_id =id)
            company = CompanyList.objects.filter(id= comId)
            orderlist = OrderList.objects.filter(id= id)
            pharmacy = PharmacyList.objects.filter(id= outlet)

            serialized_queryset = serializers.serialize('python', orderMed)
            serialized_queryset2 = serializers.serialize('python', company)
            serialized_queryset3 = serializers.serialize('python', orderlist)
            serialized_queryset4 = serializers.serialize('python', pharmacy)

            

            data['orderMed'] = serialized_queryset
            data['company'] = serialized_queryset2[0]
            data['orderlist'] = serialized_queryset3[0]
            data['pharmacy'] = serialized_queryset4[0]
            data['reid'] = id

            return JsonResponse(data, safe=False)
    else:
        return redirect( 'login')
    
def insert_inventory(request):

    if request.session.has_key('username'):
        med_array = request.POST.getlist("med_array[]", "")
        all_med_inserted = 0
        reid = request.POST.get("reid", "")
        coid = request.POST.get("coid", "")
        company_shortcode = request.POST.get("company_shortcode", "")
        amount = request.POST.get("amount", "")
        outlet_id = request.POST.get("outlet_id", "")
        prid = request.POST.get("prid", "")
        poid = request.POST.get("poid", "")
        #purchase_id = request.POST.get("purchase_id", "")
        outlet_shortcode = request.POST.get("outlet_shortcode", "")
        voucher = request.POST.get("voucher", "")
        userId =request.session['userId']

        dt = datetime.now()
        df = DateFormat(dt)
        date = df.format('dmy')

        inventoryList = InventoryList.objects.filter(purchase_id__contains =company_shortcode).count()

        serial = str(inventoryList +1).zfill(7)
        purchase_id = date + company_shortcode + serial

        insertInventory = InventoryList(purchase_id = purchase_id, company_id_id = coid, req_id_id = reid,amount= amount,outlet_id_id= outlet_id,
                                        outlet_shortcode =outlet_shortcode , voucher = voucher,receive_by = userId)
        insertInventory.validate_unique()
        insertInventory.save()

        for mednumber in med_array:
            med = request.POST.get("med"+mednumber, "")
            inserted = request.POST.get("inserted"+mednumber, "")
            quantity = request.POST.get("quantity"+mednumber, "")
            actualQuantity = request.POST.get("actualQuantity"+mednumber, "")
            buying = request.POST.get("buying"+mednumber, "")
            selling = request.POST.get("selling"+mednumber, "")
            totalTrade = request.POST.get("totalTrade"+mednumber, "")
            totalPrice = request.POST.get("totalPrice"+mednumber, "")
            inDate = request.POST.get("inDate"+mednumber, "")
            unit = request.POST.get("unit"+mednumber, "")
            generic = request.POST.get("generic"+mednumber, "")

            total_vat = None
            total_mrp = None
            stock = None
            vat = 17.4
            
            row  = 0

            all_quantity_checker = 0
            
            totalQuantity = int(quantity) + int(inserted)

            if totalQuantity != int(actualQuantity):
                all_med_inserted = 1

            if int(quantity) > 0:

                MedForStock = InventoryMed.objects.filter(med_name =med, status__isnull = True).order_by('-id')
                
                #check for previous Stock existance
                if MedForStock:
                    tp = float(buying)
                    mrp = float(selling)
                    row = MedForStock.count() +1

                    #calcultaion for avg vat, tp, mrp
                    for stock in MedForStock:
                        vat = vat + float(stock.vat_percentage)
                        tp = tp + float(stock.buying_price)
                        mrp = mrp + float(stock.selling_price)
                    vat_average = vat / row
                    tp_average = tp / row
                    mrp_average = mrp / row

                    # sold quantity from previous invontory check
                    if MedForStock[0].quantity_sold is None:
                        total_vat = float(MedForStock[0].total_vat) + float(totalPrice)
                        total_mrp = float(selling) * float(quantity) + float(MedForStock[0].total_vat_mrp)
                        stock = int(MedForStock[0].quantity_stock) + int(quantity)

                    else:
                        sold = int(MedForStock[0].quantity_sold)
                        aftersold = int(MedForStock[0].quantity) - sold
                        sold_total = aftersold * float(MedForStock[0].buying_price)
                        sold_total_vat = sold_total + ((sold_total * float(MedForStock[0].vat_percentage)) / 100)
                        total_vat = float(sold_total_vat) + float(totalPrice)
                        
                        stock = int(MedForStock[0].quantity_stock)- int(MedForStock[0].quantity_sold) + int(quantity)
                        sold_mrp = float(MedForStock[0].quantity_sold) * float(MedForStock[0].selling_price)
                        total_mrp = float(MedForStock[0].total_vat_mrp)-sold_mrp + (float(selling) * float(quantity))
                else:
                    row = 1
                    vat_average = float(vat) 
                    tp_average = float(buying)
                    mrp_average = float(selling)

                    total_vat = float(totalPrice)
                    total_mrp = float(selling) * float(quantity) 
                    stock = int(quantity)
                                                

                

                #serialized_queryset = serializers.serialize('python', MedForStock)

                if inDate:
                    t = OrderedMed.objects.get(med_name=med , order_id_id  = reid)
                    t.accept = totalQuantity
                    t.save()

                    insertInventoryMed = InventoryMed(med_name = med, company_id_id = coid,inventory_id_id = insertInventory.id,req_id_id= reid,
                                                    quantity =quantity , buying_price = round(tp_average,2),selling_price = round(mrp_average,2), 
                                                    total =totalTrade , vat_percentage = round(vat_average,2),total_vat = total_vat,quantity_stock = stock,
                                                    total_vat_mrp = total_mrp, expired_date = inDate,generic=generic,unit=unit)
                    insertInventoryMed.validate_unique()
                    insertInventoryMed.save()
                else:
                    if int(quantity) >0:
                        all_med_inserted = 1

                




        if all_med_inserted == 0:

            t = OrderList.objects.get(id=reid )
            t.status = 'Recieve done'
            t.save()
        
        

        return JsonResponse(purchase_id, safe=False)
    else:
        return redirect( 'login')
    


def logout(request):

    if request.session.has_key('username'):
       
        del request.session['username']
        
        del request.session['role']
        
        del request.session['userid']
        
        return redirect('login')
    else:
        return redirect( 'login')