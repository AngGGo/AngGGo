from django.db import models

class Attendance(models.Model):
  #aaa,7,2024-12-05,2024-12-05
  aId = models.CharField(max_length=200,primary_key=True)
  count = models.IntegerField(default=0)
  aDate = models.DateField(max_length=100) # 출석 버튼 누르는 시각
  aTicket = models.IntegerField(default=0) # 응모권 개수
  usedTicket = models.IntegerField(default=0)  # 사용한 응모권 개수?
  
  def __str__(self):
    return f"{self.aId},{self.count},{self.aDate},{self.aTicket}"
  

  