from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
    return display_servers(request, "")

def display_servers(request, err_msg):
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
    return render(request, 'servers.html', {'servs': servs, 'err_msg':err_msg})


def add_server(request):
    ip_addr = request.POST.get('server_ip', '')
    port = request.POST.get('server_port', '')

    if (ip_addr == '' or port == ''):
        return display_servers(request, '')

    cnx = mysql.connector.connect(user=conf.getuser(), host = conf.gethost(), password = conf.getpwd(),
            database=conf.getdb(), port=conf.getport())
    cursor = cnx.cursor()
    cnx.get_warnings = True
    cursor.execute("select server_id from servers where ip_addr = %s and port = %s", (ip_addr, port))
    results = cursor.fetchall()

    if results:
        cursor.close()
        cnx.close()
        err_msg = "Server ip = %s, port = %s is already exist" % (ip_addr, port)
        return display_servers(request, err_msg)


    cursor.execute("insert into servers (ip_addr, port) value (%s, %s)", (ip_addr, port))
    if cursor.fetchwarnings():
        cursor.close()
        cnx.close()
        err_msg = "Add server ip = %s, port = %s failed" % (ip_addr, port)
        return display_servers(request, err_msg)

    cnx.commit()
    cursor.close()
    cnx.close()

    return servers(request)


def delete_server(request):
    del_ids = request.POST.get('del_ids', '').split(":")
    cnx = mysql.connector.connect(user=conf.getuser(), host = conf.gethost(), password = conf.getpwd(),
            database=conf.getdb(), port=conf.getport())
    cursor = cnx.cursor()
    for serv_id in del_ids:
        cursor.execute(("select table_id from asso_serv_tb where server_id = %s"), (serv_id, ))
        tb_ids = cursor.fetchall()
        for tb_id in tb_ids:
            tb_id = tb_id[0]
            cursor.execute(("select count(*) from asso_serv_tb where table_id = %s"), (tb_id,))
            count = cursor.fetchall()[0]
            if (1 == count):
                cursor.execute(("delete from asso_serv_tb where table_id = %s"), (tb_id,))
                cursor.execute(("delete from tbs where table_id = %s"), (tb_id,))


        cursor.execute(("select database_id from asso_serv_db where server_id = %s"), (serv_id,))
        db_ids = cursor.fetchall()
        for db_id in db_ids:
            db_id = db_id[0]
            cursor.execute(("select count(*) from asso_serv_db where database_id = %s"), (db_id,))
            count = cursor.fetchall()[0]
            if (1 == count):
                cursor.execute(("delete from asso_serv_db where database_id = %s"), (db_id,))
                cursor.execute(("delete from dbs where database_id = %s"), (db_id,))
        cursor.execute(("delete from servers where server_id = %s"), (serv_id,))

    cnx.commit()
    cursor.close()
    cnx.close()
    return display_servers(request, "")

def all(request):
    return render(request, request.path[1:])
