from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from mysql.connector import errorcode
import readconfig
# Create your views here.

conf = readconfig.readconfig("./config.ini")

def index(request):
#    return HttpResponse("Hello World")
    return render(request, 'base.html')


class server:
    def __init__(self):
        self.server_id = 0
        self.server_ip = "0.0.0.0"
        self.server_port = 3306

def servers(request):
    cnx = mysql.connector.connect(user=conf.getuser(), host=conf.gethost(), password=conf.getpwd(),
            database=conf.getdb(), port=conf.getport())
    cursor = cnx.cursor()
    query_state = ("select server_id, ip_addr, port from servers")
    cursor.execute(query_state)
    results = cursor.fetchall()

    servs = []
    for row in results:
        serv = server()
        serv.server_id = row[0]
        serv.server_ip = row[1]
        serv.server_port = row[2]
        servs.append(serv)

    return render(request, 'servers.html', {'servs': servs})

def delete_server(request):
    return HttpResponse(request.GET['del_ids'])

def all(request):
    return render(request, request.path[1:])
