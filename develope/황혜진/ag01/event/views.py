from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from member.models import Member
from event.models import Attendance
from datetime import date
from django.db.models import F



def calendar(request):
  if request.method == "GET":
    aId = request.session.get('session_id')
    qs = Attendance.objects.filter(aId=aId)
    if qs:
      context = {"count":qs[0].count,"aTicket":qs[0].aTicket,"usedTicket":qs[0].usedTicket}
    else:
      context = {"count":0,"aTicket":0,"usedTicket":0}
    return render(request, 'calendar.html',context)
  else:
    # 세션에서 aId 가져오기
    aId = request.session.get('session_id')
    today = date.today() # 오늘 날짜 today에 저장
    print(aId,today)

    # Attendance 객체 가져오기 (사용자별로 출석 기록을 가져옴)
    qs = Attendance.objects.filter(aId=aId)

    ## 매달 1일에 count 리셋
    first_day_of_month = today.replace(day=1)

    if today == first_day_of_month:
      qs[0].count = 0 # 카운트 리셋
      qs[0].aTicket = 0
      qs[0].save()
      print("카운트 리셋 count",qs[0].count)


    # aDate과 today 비교
    if qs:
      if qs[0].aDate != today:
        qs[0].aDate = today
        qs.update(count=F('count')+1) # 출석 횟수 추가
        qs.update(count=F('aTicket')+1) # 응모권 개수 추가
        context = {"result":"success","count":qs[0].count,"aTicket":qs[0].aTicket}
      else:
        context = {"result":"already_checked"}
    else:
      Attendance.objects.create(aId=aId,aDate=today,count=1,aTicket=1)
      context = {"result":"success","count":1,"aTicket":1}
    return JsonResponse(context)
    
     

# 응모권 개수 차감
def apply(request):
  aId = request.session.get('session_id')
  qs = Attendance.objects.filter(aId=aId)
  ticketDeduction = int(request.POST.get('ticketDeduction',0)) # 클라이언트에서 전송한 차감할 응모권 수
  print(qs,ticketDeduction)
  if qs: 
    if qs[0].aTicket < ticketDeduction:
      return JsonResponse({"result":"all_done"}) # 응모권 부족

    else:
      qs.update(aTicket=F('aTicket')-ticketDeduction)
      qs.update(usedTicket=F('usedTicket')+ticketDeduction)
      print(qs[0].aTicket,qs[0].usedTicket)
      context = {"result":"success","aTicket":qs[0].aTicket,"usedTicket":qs[0].usedTicket}
      return JsonResponse(context)

