from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import localtime
from good_recieve.models import CompanyList ,PharmacyList , MedList
from inventory.models import InventoryList , InventoryMed, stockTransferList, stockTransferMed
from django.core import serializers
from django.shortcuts import redirect 
from django.core.paginator import Paginator
from datetime import datetime  
from django.utils.dateformat import DateFormat

# Create your views here.


def main(request):
    
    
        if  request.session.has_key('role') and ( request.session['role'] == '1' or request.session['role'] == 'admin' or request.session['role'] == '2' or request.session['role'] == '4'):
            company = CompanyList.objects.all()

            fromOutlet = ''
            if request.session['role'] == '4' or request.session['role'] == 'admin':
                fromOutlet = PharmacyList.objects.filter(id = '1')

            return render(request, 'inventory.html',{"companies": company, "fromOutlets" : fromOutlet})
        else:
            return redirect( 'login')
    

def get_inventry_day(request):


    if request.session.has_key('username'):
        date = request.GET.get('date').replace("_", " ")
        coId = request.GET.get('coId')
        invoice = request.GET.get('invoice')
        purchaseId = request.GET.get('purchaseId')

        searchDate = ''

        if purchaseId:
            searchDate = ' '
            purchaseid = purchaseId[4:]
        elif coId:
            searchDate = ' '
        else:
            formatDate = datetime.strptime(request.GET.get('datemain'), "%Y-%m-%d").date()
            df = DateFormat(formatDate)
            datenew = df.format('M d, Y')
            searchDate = 'as of ' + datenew

        if request.session['role'] == '1':
            outletid =request.session['outletid']
            if purchaseId:
                orderlist = InventoryList.objects.filter( outlet_id_id = outletid,purchase_id = purchaseid).select_related('company_id')
            elif invoice:
                orderlist = InventoryList.objects.filter(outlet_id_id = outletid,voucher = invoice).select_related('company_id')
            elif coId:
                orderlist = InventoryList.objects.filter(create_date__lt=date,outlet_id_id = outletid,company_id_id = coId).select_related('company_id')
            else:
                orderlist = InventoryList.objects.filter(create_date__lt=date, outlet_id_id = outletid).select_related('company_id')
        elif request.session['role'] == '2':
            outletid =request.session['outletid']
            starttime =request.session['starttime']
            endtime =request.session['endtime']
            endtimereduce = int(endtime) - 1
            if purchaseId:
                orderlist = InventoryList.objects.filter( outlet_id_id = outletid,purchase_id = purchaseid,create_date__hour__range=(int(starttime), endtimereduce)).select_related('company_id')
            elif invoice:
                orderlist = InventoryList.objects.filter( outlet_id_id = outletid,voucher = invoice,create_date__hour__range=(int(starttime), endtimereduce)).select_related('company_id')
            elif coId:
                orderlist = InventoryList.objects.filter(create_date__lt=date, outlet_id_id = outletid,company_id_id = coId,create_date__hour__range=(int(starttime), endtimereduce)).select_related('company_id')
            else:
                orderlist = InventoryList.objects.filter(create_date__lt=date, outlet_id_id = outletid,company_id_id = coId,create_date__hour__range=(int(starttime), endtimereduce)).select_related('company_id')
        else:

            

            if purchaseId:
                orderlist = InventoryList.objects.filter(purchase_id = purchaseid).select_related('company_id')
            elif invoice:
                orderlist = InventoryList.objects.filter(voucher = invoice).select_related('company_id')
            elif coId:
                orderlist = InventoryList.objects.filter(create_date__lt=date,company_id_id = coId).select_related('company_id')
            else:
                orderlist = InventoryList.objects.filter(create_date__lt=date).select_related('company_id')

        # paginator = Paginator(orderlist, 10)
        # page = request.GET.get('page')
        # page_obj = paginator.get_page(page)

        view = ''
        view2 = ''

        count = 1
        inIds = list()
        view = '<thead style="background-color: #003E6C; font-size: small;">'
        view += '<tr>'
        view += '<th scope="col">SL</th>'
        view += '<th scope="col">Company Name</th>'
        view += '<th scope="col">PR Id</th>'
        view += '<th scope="col">PO Id</th>'
        view += '<th scope="col">Purchase ID</th>'
        view += '<th scope="col">CHECK Detail</th>'
        view += '</tr>'
        view += '</thead>'
        view += '<tbody style="background-color: #154883" id="purchaseTable" >'
        for order in orderlist:
        
            inIds.append(order.id)
            if order.pr_id :
                pr_id = order.pr_id 
            else:
                pr_id = ''

            if order.po_id :
                po_id = order.po_id 
            else:
                po_id = ''

            if order.purchase_id :
                purchase_id = order.outlet_shortcode + order.purchase_id 
            else:
                purchase_id = ''
            

            
            countStr = str(count)


            view += '<tr> <th scope="col">'+countStr+'</th> <th scope="col">'+order.company_id.companyName+ '</th>'
            view += '<th scope="col">'+pr_id +'</th>'
            view += '<th scope="col">'+po_id +'</th>'
            view += '<th scope="col">'+purchase_id+'</th>'
            view += '<th scope="col"><button value = "'+str(order.id)+'" class=" buttons viewEvent" style="color: #000000;background-color:#fafbfc; border: none;" type="button" id="" class="btn btn-info" data-bs-dismiss="modal">Details</button></th>'

            view += '</tr>'
    
            count = count + 1
        view += '</tbody>'

        # view2 += '<div class="pagination">'
        # view2 += '<span class="step-links">'
        # if page_obj.has_previous:
        #     view2 += '<a href="?page=1">&laquo; first</a>'
        #     view2 += '<a href="?page='+str(page_obj.previous_page_number)+'">previous</a>'
        
        # view2 += '<span class="current"> Page '+str(page_obj.number)+' of '+ str(page_obj.paginator.num_pages)+'</span>'
        # if page_obj.has_next:
        #     view2 += '<a href="?page='+ str(page_obj.next_page_number)+'">next</a>'
        #     view2 += '<a href="?page='+ str(page_obj.paginator.num_pages)+'">last &raquo;</a>'
        
        # view2 += '</span> </div>'
        
        
        #serialized_queryset = serializers.serialize('python', orderlist)
        data = {}
        data['view'] = view
        data['view2'] = view2
        data['inIds'] = inIds
        data['searchDate'] = searchDate
        data['coId'] = coId
        #data['orderlist'] = serialized_queryset

        return JsonResponse(data, safe=False)
    else:
        return redirect( 'login')
    
def get_inventry_all_item(request):
        
    if request.session.has_key('username'):
        reids = request.GET.get('reids')
        my_list = reids.split(",")
        orderMed = InventoryMed.objects.filter(inventory_id_id__in =my_list)
        serialized_queryset = serializers.serialize('python', orderMed)

        view = '<thead style="background-color: #003E6C; font-size: small;">'
        view += '<tr>'
        view += '<th scope="col">SL</th>'
        view += '<th scope="col">Item</th>'
        view += '<th scope="col">Generic</th>'
        view += '<th scope="col">Company</th>'
        view += '<th scope="col">QTY(rcv)</th>'
        view += '<th scope="col">QTY(stock)</th>'
        view += '<th scope="col">QTY(Total stock)</th>'
        view += '<th scope="col">TP(avg)</th>'
        view += '<th scope="col">Vat(avg)</th>'
        view += '<th scope="col">Total with vat(stock)</th>'
        view += '<th scope="col">MRP / quantity(avg)</th>'
        view += '<th scope="col">Total MRP(stock)</th>'
        view += '</tr>'
        view += '</thead>'
        view += '<tbody style="background-color: #154883" id="purchaseTable" >'

        count = 1
        for med in orderMed:

            countStr = str(count)

            prev_stock = int(med.quantity_stock) - int(med.quantity)
            totalMrp = float(med.total_vat_mrp) 

            generic_name = ''    

            company = CompanyList.objects.filter(id = med.company_id_id)
            # generic = MedList.objects.filter(med_name = med.med_name)
            # if generic:
            #     generic_name = generic[0].generic


            view += '<tr class="ccc">'
            view += '<td scope="col">'+countStr+'</td>'
            view += '<td >'+med.med_name +'</td>'
            view += '<td >'+med.generic+'</td>'
            view += '<td >'+company[0].companyName+'</td>'
            view += '<td >'+med.quantity+'</td>'
            view += '<td >'+str(prev_stock)+'</td>'
            view += '<td >'+med.quantity_stock+'</td>'
            view += '<td >'+med.buying_price+'</td>'
            view += '<td >'+med.vat_percentage+' %</td>'
            view += '<td >'+med.total_vat+'</td>'
            view += '<td >'+med.selling_price+'</td>'
            view += '<td >'+str(round(totalMrp,2))+'</td>'

            view += '</tr>'
        
            count = count + 1
        view += '</tbody>'


        data = {}
        data['view'] = view

        return JsonResponse(data, safe=False)
    else:
        return redirect( 'login')

def get_traoutletl_list(request):

    if request.session.has_key('username'):
        outletId = request.GET.get('id')
        count = request.GET.get('count')

        # if ',' in count:
        #     my_list = count.split(",")
        # else: 
        #     my_list = count

        if outletId == '1':
            totalid = outletId
        else:
            totalid = '1,' +outletId
            totalid = totalid.split(",")
        
        fromOutlet = PharmacyList.objects.all().exclude(id__in = totalid)
        #fromOutlet_queryset = serializers.serialize('python', fromOutlet)

        view = '<option value=""></option>'

        for outlet in fromOutlet:
            view += '<option value="'+str(outlet.id)+'">'+outlet.outlet+'</option>'
        

        data = {}
        data['view'] = view
        data['count'] = count

        return JsonResponse(data, safe=False)
    else:
        return redirect( 'login')


def transfer(request):
    if request.session.has_key('username'):

        puid = request.GET.get('puid')
        outletCode = request.GET.get('outletCode')
        fromid = request.GET.get('fromid')
        toid = request.GET.get('toid')
        medName = request.GET.get('medName')
        generic = request.GET.get('generic')
        exdt = request.GET.get('exdt')
        unit = request.GET.get('unit')
        inserted = request.GET.get('quantity')
        buyPrice = request.GET.get('buyPrice')
        sellingPrice = request.GET.get('sellingPrice')
        companyId = request.GET.get('companyId')
        invoice = request.GET.get('invoice')
        inventoryId = request.GET.get('inventoryId')
        userId =request.session['userId']

        InventoryMedStatus = InventoryMed.objects.filter(med_name = medName, inventory_id_id = inventoryId)

        quantitySold = 0

        if InventoryMedStatus[0].quantity_sold  is not None:
            
            quantitySold = InventoryMedStatus[0].quantity_sold

        remainMed = int(InventoryMedStatus[0].quantity) - int(quantitySold)

        overflow = 'right'

        if remainMed >= int(inserted):

            overflow = 'wrong'

            transferInfo = stockTransferList.objects.filter(purchase_id = puid,to_outlet_id=toid)
            transferListId = ''

            if transferInfo:
                transferListId = transferInfo[0].id
            else:
                transferProduct = stockTransferList(purchase_id=puid,outlet_shortcode =outletCode,voucher = invoice,receive_by = userId,company_id_id = companyId,
                                            to_outlet_id =toid,from_outlet_id=fromid,inventory_id_id = inventoryId)
            
                transferProduct.validate_unique()
                transferProduct.save()
                transferListId =transferProduct.id

            transferInfo = stockTransferMed.objects.filter(med_name = medName,outlet_id=toid, status = None)

            if transferInfo:
                totalQuantity = int(transferInfo[0].quantity_stock) + int(inserted) - int(transferInfo[0].quantity_sold)
            else:
                totalQuantity = int(inserted)

            total = float(sellingPrice) * float(inserted)
            totalVat = total + (total * 17.4) / 100

            
            transferMed = stockTransferMed(med_name = medName , quantity = inserted,quantity_stock =totalQuantity,quantity_sold = '0' ,buying_price = buyPrice , selling_price = sellingPrice,total=total,
                                           vat_percentage = '17.4',total_vat = totalVat, total_vat_mrp = '0',expired_date = exdt,unit = unit,
                                           generic= generic,outlet_id = toid,company_id_id = companyId,transfer_id_id =transferListId)
            transferMed.validate_unique()
            transferMed.save()
        

            getInventoryMed = InventoryMed.objects.filter(med_name = medName,inventory_id_id = inventoryId)

            if getInventoryMed:
                if getInventoryMed[0].quantity_sold:
                    updateQuantity = int(getInventoryMed[0].quantity_sold) + int(inserted)
                else:
                    updateQuantity = inserted
            
            updateInventoryMed = InventoryMed.objects.get(med_name = medName,inventory_id_id = inventoryId)
            updateInventoryMed.quantity_sold = updateQuantity
            updateInventoryMed.save()

        data = {}
        data['overflow'] = overflow
        data['remainMed'] = remainMed

        return JsonResponse(data, safe=False)
    else:
        return redirect( 'login')



def get_inventry_med(request):
        
    if request.session.has_key('username'):

        reqid = request.GET.get('reqid').replace("_", " ")

        orderMed = InventoryMed.objects.filter(inventory_id_id =reqid).select_related('company_id','inventory_id')

        if orderMed[0].inventory_id.outlet_id_id: 
            outletDetail = PharmacyList.objects.filter(id = orderMed[0].inventory_id.outlet_id_id)
        

        if orderMed[0].inventory_id.pr_id :
            pr_id = orderMed[0].inventory_id.pr_id 
        else:
            pr_id = ''

        if orderMed[0].inventory_id.po_id :
            po_id = orderMed[0].inventory_id.po_id 
        else:
            po_id = ''

        if orderMed[0].inventory_id.purchase_id :
            purchase_id = orderMed[0].inventory_id.outlet_shortcode + orderMed[0].inventory_id.purchase_id 
        else:
            purchase_id = ''

        view = ''
        count = 1
        totalPrice = 0.00
        subtotalMrp = 0.00
        stock_total_vat = 0.00
        view += '<table class="table" id="allProductTableList">'
        view += '<thead class="tbodyresult3">'
        view += '<tr><th scope="col">SL</th>'
        view += '<th scope="col">ITEM</th><th scope="col">Generic</th><th scope="col">QTY(rcv)</th><th scope="col">QTY(stock)</th>'
        view += '<th scope="col">QTY(Total stock)</th><th scope="col">TP(avg)</th><th scope="col">Vat(avg)</th><th scope="col">Total with vat(stock)</th>'
                                            
        view += ' <th scope="col">MRP / quantity(avg)</th><th scope="col">Total MRP(stock)</th></tr></thead>'
        view += '<tbody >'
        totalMedCount= ''
        for med in orderMed:

            countStr = str(count)
            if str(count) == '1':
                totalMedCount = countStr
            else:
                totalMedCount = totalMedCount +','+countStr

            #totalMrp = float(med.selling_price) * float(med.quantity)
            totalMrp = float(med.total_vat_mrp) 

            prev_stock = int(med.quantity_stock) - int(med.quantity)
            if med.quantity_sold:
                transferAmount = int(med.quantity) - int(med.quantity_sold)
            else:
                transferAmount = int(med.quantity) 
            #MedForStock_queryset = serializers.serialize('python', MedForStock)

            view += '<tr class="ccc">'
            view += '<td scope="col">'+countStr+'</td> <td scope="col">'+med.med_name + '</td>'
            view += '<td><p><span>'+med.generic+'</span></p></td>'
            view += '<td><p><span>'+med.quantity+'</span> pcs</p></td>'
            view += '<td><p><span class = "stockToPresent'+countStr+'">'+str(prev_stock)+'</span> pcs</p></td>'
            view += '<td><p><span class = "stockToAfter'+countStr+'">'+med.quantity_stock+'</span> pcs</p></td>'
            view += '<td >'+med.buying_price+'</td>'
            view += '<td >'+med.vat_percentage+'  %</td>'
            view += '<td >'+med.total_vat+'</td>'
            view += '<input   value = "'+med.expired_date+'" type="hidden" readonly>'
            view += '<input   value = "'+med.unit+'" type="hidden" readonly>'
            view += '<input   value = "'+med.selling_price+'" type="hidden" readonly>'
            view += '<input   value = "'+med.buying_price+'" type="hidden" readonly>'
            view += '<input class = "medName'+countStr+'"  value = "'+med.med_name+'" type="hidden" readonly>'
            view += '<input   value = "'+med.generic+'" type="hidden" readonly>'
            view += '<td ><span class = "mrpText">'+med.selling_price+'</span><input type="number" id="" name = "transfer'+countStr+'" class = "stock " placeholder = "Insert transfer amount" style = "display: None" ></td>'
            view += '<input   value = "'+str(transferAmount)+'" type="hidden" readonly>'
            view += '<td > <span class = "mrpText">'+str(round(totalMrp,2))+'</span><button type="button" class="btn btn-primary stockBtn" style = "display: None" disabled>Submit</button></td>'
            view += '</tr>'

            totalPrice = float(totalPrice) + float(med.total_vat)
            subtotalMrp = float(subtotalMrp) + totalMrp

            count = count + 1
        if orderMed:
            companyName = orderMed[0].company_id.companyName
            date = orderMed[0].inventory_id.create_date
            outletName = outletDetail[0].outlet
            view += '<tr style = "border-top: #181818 4px solid;">'
            view += '<td >Subtotal</td>'
            view += '<td ></td>'
            view += '<td ></td>'
            view += '<td ></td>'
            view += '<td ></td>'
            view += '<td ></td>'
            view += '<td ></td>'
            view += '<td ></td>'
            view += '<td >'+str(round(totalPrice,2))+'</td>'
            view += '<td ></td>'
            view += '<td >'+str(round(subtotalMrp,2))+'</td>'
            
            view += '</tr>'
        else:
            companyName = ''
            date = ''
            outletName = ''

       
        
        view += '</tbody> </table>'

        data = {}
        data['companyName'] = companyName
        data['companyId'] = companyName = orderMed[0].company_id.id
        data['invoice'] = orderMed[0].inventory_id.voucher 
        data['inventoryId'] = orderMed[0].inventory_id.id 
        data['date'] = date
        data['pr_id'] = pr_id
        data['po_id'] = po_id
        data['purchase_id'] = purchase_id
        data['outletName'] = outletName
        data['view'] = view
        data['totalMedCount'] = totalMedCount
        #data['MedForStock'] = MedForStock_queryset

        return JsonResponse(data, safe=False)
    else:
        return redirect( 'login')
