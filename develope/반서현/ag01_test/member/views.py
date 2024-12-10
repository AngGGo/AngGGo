from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from django.core import serializers 
from member.models import Member
from django.core.mail import get_connection, EmailMessage
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ### 약관동의에 체크했는지 확인
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

### ---------------------- 아이디/닉네임/이메일 중복 확인 ----------------------
## 이메일 중복 확인
def emailDupChk(request):
  userEmail = request.POST.get("email")
  if Member.objects.filter(email=userEmail):
    return JsonResponse({"result": "error", "message": "이미 사용 중인 이메일입니다."})
  return JsonResponse({"result": "success", "message": "사용 가능한 이메일입니다."})

## 닉네임 중복 확인
def nicknameDupChk(request):
  userNickname = request.POST.get("nickname")
  if Member.objects.filter(nickname=userNickname):
    return JsonResponse({"result": "error", "message": "이미 사용 중인 닉네임입니다."})
  return JsonResponse({"result": "success", "message": "사용 가능한 닉네임입니다."})

## 아이디 중복 확인
def idDupChk(request):
  userId = request.POST.get("id")
  if Member.objects.filter(id=userId):
    return JsonResponse({"result": "error", "message": "이미 사용 중인 아이디입니다."})
  return JsonResponse({"result": "success", "message": "사용 가능한 아이디입니다."})

### 회원가입 - signup
def signup(request):
  if request.method == "GET":
    return render(request, "signup.html")
  else:
    id = request.POST.get("id")
    pw = request.POST.get("pw")
    name = request.POST.get("name")
    nickname = request.POST.get("nickname")
    tel = request.POST.get("tel")
    email = request.POST.get("email")

    # 중복 검사 (이미 중복 검사를 했지만 추가로 서버 측에서 한번 더 확인하는 것이 좋습니다)
    if Member.objects.filter(id=id).exists():
      return JsonResponse({"result": "error", "message": "아이디가 중복되었습니다."})
    if Member.objects.filter(nickname=nickname).exists():
      return JsonResponse({"result": "error", "message": "닉네임이 중복되었습니다."})
    if Member.objects.filter(email=email).exists():
      return JsonResponse({"result": "error", "message": "이메일이 중복되었습니다."})
    
    Member.objects.create(
      id=id,
      pw=pw,
      name=name,
      nickname=nickname,
      tel=tel,
      email=email
    )

    # 회원가입 후 로그인 페이지로 이동
    return redirect("/member/login/")

### ---------------------------- 아이디/비밀번호 찾기 ----------------------------
# ---------------------------- 비밀번호 찾기 ----------------------------
# 인증번호 확인 버튼
def verify_code(request):
  if request.method == 'POST':
    input_code = request.POST.get('chkEmailCode')  # 유저가 입력한 인증번호
    saved_code = request.session.get('verification_code')  # 세션에서 인증번호 가져오기

    if not input_code:
      return JsonResponse({"result": "error", "message": "인증번호를 입력하세요."})
    if not saved_code:
      return JsonResponse({"result": "error", "message": "인증번호를 먼저 요청하세요."})

    # 인증번호 일치 여부 확인
    if input_code == saved_code:
      # 인증번호가 일치하면 비밀번호를 화면에 띄우기
      member_id = request.session['member_id']
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

    try:
      # 이름과 이메일이 존재하는지 확인
      member = Member.objects.get(name=name, email=email)
    except Member.DoesNotExist:
      return JsonResponse({"result": "error", "message": "존재하지 않는 회원입니다."})

    # 랜덤 6자리 인증번호 생성
    verification_code = str(random.randint(100000, 999999))

    # 세션에 인증번호와 회원 ID 저장
    request.session['verification_code'] = verification_code
    request.session['member_id'] = member.id

    # 이메일로 인증번호 전송
    try:
      smtpName = "smtp.naver.com"
      smtpPort = 587
      sendEmail = "bd8860@naver.com"
      pw = "YTZTLRBETCV2"
      recvEmail = email
      title = "비밀번호 찾기용 인증번호"
      content = f"인증번호는 {verification_code} 입니다."

      msg = MIMEText(content)
      msg['Subject'] = title
      msg['From'] = sendEmail
      msg['To'] = recvEmail

      s = smtplib.SMTP(smtpName, smtpPort)
      s.starttls()
      s.login(sendEmail, pw)
      s.sendmail(sendEmail, recvEmail, msg.as_string())
      s.quit()

      context = {"result":"success"}
      return JsonResponse(context)
    except Exception as e:
      return JsonResponse({"result": "error", "message": f"메일 전송 실패: {str(e)}"})
    
   
### 비밀번호 찾기 버튼 - 이름, 이메일, 인증번호 맞는지 확인
def findPassword(request):
  if not request.session.get("verification_code", None):
    return JsonResponse({"success": "error", "message": "인증번호를 확인해주세요."})
  
  if request.method == "POST":
      ## 사용자가 입력한 정보
      name = request.POST.get("name", "")
      email = request.POST.get("email", "")
      chkEmailCode = request.POST.get("chkEmailCode", "")

      print(f"이름 : {name}\n이메일 주소 : {email}\n인증번호 : {chkEmailCode}")

      if not name or not email:
        return JsonResponse({"result": "error", "message": "이름과 이메일을 모두 입력하세요."})

      # 사용자 조회
      try:
        qs = Member.objects.filter(name=name, email=email)
        if qs.exists():
          user = qs.first()  # 첫 번째 일치하는 사용자
          
          # 인증번호 확인
          if chkEmailCode != request.session.get("verification_code"):
            return JsonResponse({"result": "error", "message": "인증번호가 일치하지 않습니다."})
          
          return JsonResponse({
            "result": "success", "name": user.name, "user_pw": user.pw
          })
        else:
          return JsonResponse({"result": "error", "message": "존재하지 않는 회원입니다."})
      except Exception as e:
        return JsonResponse({"result": "error", "message": f"서버 오류: {str(e)}"})


# ---------------------------- 아이디 찾기 ----------------------------
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
### // --------------------------- 아이디/비밀번호 찾기 ----------------------------


### 로그아웃
def logout(request):
  request.session.clear()
  return redirect("/")

### 로그인 - 아이디/비밀번호 일치 확인
def loginChk(request):
  id = request.POST.get("id", "")
  pw = request.POST.get("pw", "")

  ## db확인
  qs = Member.objects.filter(id=id, pw=pw)
  print(f"[ 아이디/비밀번호 확인 ]\n아이디 : {id}\n비밀번호 : {pw}")

  # 아이디비밀번호일치
  if qs:
    request.session['session_id'] = qs[0].id
    request.session['session_nickname'] = qs[0].nickname
    list_qs = list(qs.values()) # 아이디 비밀번호 묶어서 list_qs에 저장
    context = {"result":"success", "member":list_qs} # member라는 이름으로 list_qs 보내기
  else:
    context = {"result":"fail"}

  return JsonResponse(context)


### 로그인페이지
def login(request):
  return render(request, "login.html")
