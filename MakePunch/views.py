from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .AutoTimeScript import PunchHttpRequest
# Create your views here.

@api_view(['POST'])
def makePunch(HttpReq):
        email = HttpReq.data['email']        
        password = HttpReq.data['password']
        
        resp = PunchHttpRequest().makePunch(email,password)
                
        return Response(resp)