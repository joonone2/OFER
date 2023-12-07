from django.shortcuts import render
from rest_framework.views import APIView
from django.views.generic import TemplateView



class Sub(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "OFER/main.html")

    def post(self,request):
        print("포스트로 호출")
        return render(request,"OFER/main.html")


class MainView(TemplateView):
    template_name = 'OFER/main.html'  # 기본 페이지 템플릿 파일의 이름