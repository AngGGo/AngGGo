from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from django.core import serializers 
from member.models import Member
from django.core.mail import get_connection, EmailMessage
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from .models import EmailVerification  # 인증번호를 저장할 모델을 사용할 것
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

### 약관동의에 체크했는지 확인
def agreeChk(request):
  if request.method == "POST":
    agree1 = request.POST.get("agree1")
    agree2 = request.POST.get("agree2","")

    if agree1 == 1:
      request.session['agree1'] = agree1
    if agree2 == 1:
      request.session['agree2'] = agree2
    today = datetime.now().strftime("y-m-d")
    context = {"result":"success","today":today}
    return JsonResponse(context)
    

    # ## db저장 아 이거 아닌데????? 아니벌써저장하면안되고 쿠키나세션에저장하고 나중에같이보내야돼
    # Member.objects.create(agree1, agree2)
    # print(f"[ 필수/선택 약관동의 확인 ]\n필수 : {agree1}\선택 : {agree2}")



### 회원가입 - step01. 약관동의
def join01(request):
  return render(request, "join01.html")

# ---------------------------- 아이디/패스워드 찾기 (인증번호) ----------------------------
## 인증번호 확인
def verify_code(request):
  if request.method == 'POST':
    input_code = request.POST.get('verification_code')
    saved_code = request.session.get('verification_code')

    if not input_code or not saved_code:
      return JsonResponse({"result": "error", "message": "인증번호를 입력하세요."})

    if input_code == saved_code:
        # 인증번호가 일치하면 비밀번호를 화면에 띄우기
      member_id = request.session.get('member_id')
      member = Member.objects.get(id=member_id)

      return JsonResponse({"result": "success", "message": f"인증되었습니다. 비밀번호는 {member.pw}입니다."})
    else:
      return JsonResponse({"result": "error", "message": "인증번호가 일치하지 않습니다."})


### 인증번호 보내기
def send_verification_code(request):
  if request.method == "GET":
    return JsonResponse({"result": "error", "message": "잘못된 요청입니다."})
  else:
    name = request.POST.get("name")
    email = request.POST.get('email')

    # 이름과 이메일이 존재하는지 확인
    try:
      member = Member.objects.get(name=name, email=email)
    except Member.DoesNotExist:
      return JsonResponse({"result": "error", "message": "존재하지 않는 회원입니다."})

    # 랜덤 6자리 인증번호 생성
    verification_code = str(random.randint(100000, 999999))

    # 세션에 인증번호와 회원 ID 저장
    request.session['verification_code'] = verification_code
    request.session['member_id'] = member.id

    smtpName = "smtp.naver.com"
    smtpPort = 587

    # id, pw, 받는사람 이메일주소
    sendEmail = "bd8860@naver.com"
    pw = "YTZTLRBETCV2"
    recvEmail = email
    title = "제목 : 파이썬 이메일 보내기 안내"
    content = f"""{verification_code}"""  # """ >> 쌍따옴표 안에 공백도 포함

    # 설정
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = sendEmail
    msg['To'] = recvEmail
    print("msg 데이터 : ",msg.as_string())

    # 서버 이름, 서버 포트 설정
    s = smtplib.SMTP(smtpName,smtpPort)
    s.starttls()
    s.login(sendEmail,pw)
    s.sendmail(sendEmail,recvEmail,msg.as_string())
    s.quit()

    # 메일발송 완료
    print("메일을 발송했습니다.")

    context = {"result":"success"}
    return JsonResponse(context)
    
   
### 아이디 찾기 - 이름, 이메일 맞는지 확인
def findId(request):
  try:
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")

    print(f"이름 : {name}\n이메일 주소 : {email}")

    qs = Member.objects.filter(name=name, email=email)
    if qs.exists():
      user = qs.first()  # 첫 번째 일치하는 사용자
      return JsonResponse({
        "result": "success", "name": user.name, "user_id": user.id
      })
    else:
      return JsonResponse({"result": "fail", "message": "존재하지 않는 회원입니다."})
  except Exception as e:
    print(f"오류 발생 : {e}")
    return JsonResponse({"result": "error", "message": "서버 오류 발생"})

### 아이디/비밀번호 찾기 페이지
def findInfo(request):
    return render(request, "findInfo.html")
# // --------------------------- 아이디/패스워드 찾기 (인증번호) ----------------------------

### 로그아웃
def logout(request):
  request.session.clear()
  return redirect("/")

### 로그인 - 아이디/패스워드 일치 확인
def loginChk(request):
  id = request.POST.get("id", "")
  pw = request.POST.get("pw", "")

  ## db확인
  qs = Member.objects.filter(id=id, pw=pw)
  print(f"[ 아이디/패스워드 확인 ]\n아이디 : {id}\n패스워드 : {pw}")

  # 아이디패스워드일치
  if qs:
    request.session['session_id'] = qs[0].id
    request.session['session_nickname'] = qs[0].nickname
    list_qs = list(qs.values()) # 아이디 패스워드 묶어서 list_qs에 저장
    context = {"result":"success", "member":list_qs} # member라는 이름으로 list_qs 보내기
  else:
    context = {"result":"fail"}

  return JsonResponse(context)


### 로그인페이지
def login(request):
  return render(request, "login.html")
