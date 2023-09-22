from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
class Join(APIView):
        def get(self, request):
            return render(request, "user/join.html")


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")