from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from member.models import Member
from event.models import Attendance
from datetime import date



def calendar(request):
  if request.method == "GET":
    return render(request, 'calendar.html')
  else:
    # 세션에서 aId 가져오기
    aId = request.session.get('session_id')
    today = date.today() # 오늘 날짜 today에 저장
    print(aId,today)

    # 클릭 시점의 날짜와 시간을 저장하여 출석 체크
    attendance = Attendance.objects.filter(aDate=today).exists() # 오늘 날짜가 존재한다
    qs = Attendance.objects.filter(aId=aId)
    ## 매달 마지막 날 자정에 count 리셋
    # ↓ 현재 날짜(now)의 해당 월의 마지막 날을 계산합니다.
    last_day_of_month = (today.replace(day=1) + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(days=1)
    # now.replace(day=1): 현재 날짜의 일(day)을 1로 설정하여 해당 월의 첫 번째 날로 변경 => 출석한 날짜의 일수만 1일로 변경
    # + timezone.timedelta(days=31): 첫 번째 날에 31일을 더합니다. 이는 다음 달의 날짜로 넘어가게 함 => 31일이 마지막인날은 30 더하면 담달로 안넘어가니까 31을 더함
    # .replace(day=1): 그 결과를 다시 첫 번째 날로 설정하여 다음 달의 첫 번째 날로 변경
    # - timezone.timedelta(days=1): 마지막으로, 그 날짜에서 하루를 빼서 현재 월의 마지막 날을 구함
    # 결과적으로, last_day_of_month는 현재 월의 마지막 날을 나타냄

    if today.date() == last_day_of_month:
      qs[0].count = 0 # 카운트 리셋
      qs[0].save()

    if not attendance:
      print("오늘 날짜 체크가 없습니다. 1를 증가")
      qs[0].count += 1 # 카운트 증가(출석 횟수 증가)
      qs[0].save()
      return JsonResponse({"result":"success","count":qs[0].count})
    else:
      print("이미 출석체크 완료")
      return JsonResponse({"result":"already_checked"})
      

      


