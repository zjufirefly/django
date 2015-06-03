from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
#    return HttpResponse("Hello World")
    return render(request, 'base.html')


class server:
    def __init__(self):
        self.server_id = 0
        self.server_ip = "0.0.0.0"
        self.server_port = 3306

def servers(request):
    serv1 = server()
    serv1.server_id = 1;
    serv1.server_ip = "10.9.3.241"
    serv1.port = 3306

    serv2 = server()
    serv2.server_id = 2;
    serv2.server_ip = "10.9.3.242"
    serv2.port = 3306

    servs = []
    servs.append(serv1)
    servs.append(serv2)

    return render(request, 'servers.html', {'servs': servs})


def all(request):
    return render(request, request.path[1:])
