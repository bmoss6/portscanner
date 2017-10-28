import socket
import fileinput
import ipaddress
import ipaddress

### Main Menu that displays options for user
def menu():
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print('WELCOME TO PORT SCANNER')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('++++++++++++++++++++++++++++++')
    print ('\n')
    print ('OPTIONS:')
    print ('1) Target List from Command Line ')
    print ('2) Target List from File')


    ### Gives options to enter via command line or file input
def enter_command():
    option = int(input("Enter your command: "))
    if option == 1:
        target = commandlineoption()
        return target
    elif option == 2:
        target = fileoption()
        return target
    else:
        print ("Please give a valid input")
        enter_command()



## If the command line option is chosen, user enters IP, port, and range. IP network can be specified through cidr notation
def commandlineoption():
    target_list = []
    done = 'n'
    while done !='y' and done !='Y':
        ip = input("Enter in IP Address: ")
        if ip.find('/') != -1:
            ip = ipaddress.ip_network(ip)

        port = input("Enter in Port for IP: ")
        proto = input("Enter Protocol for Port (TCP/UDP): ")
        while proto != 'tcp' and proto != 'udp':
            input("Enter in correct protocol: ")
    ##TODO ERROR CHECK FOR CORRECT IP AND PORT SYNTAX
        ip_port_tuple = (ip,port,proto)
        target_list.append(ip_port_tuple)
        done = input("Done (y/n) : ")
        print (done)
   # print(target_list)
    return target_list

## Similar to command line options except file containing comma separated IP, ports, and protocol (udp/tcp)
def fileoption():
    target_list = []
    print ("MAKE SURE FILE IS IN THE FOLLOWING FORMAT: IP,PORT,Protocol \n IP, PORT")
    print ("MAKE SURE EACH IP/PORT IS SEPARATED BY NEWLINE")
    filename = input("Enter Full path of file: ")
    filestuff = open(filename,"r")
    #print (filestuff)
    for line in filestuff:
        line = line.split(',')
        ip = line[0]
        if ip.find('/') != -1 :
            ip = ipaddress.ip_network(ip)
        port = line[1]
        proto = line[2].strip()
        ip_port_tuple = (ip,port,proto)
        target_list.append(ip_port_tuple)
  #  print (target_list)
    return target_list

## Tcp scan tried to connect to the specified port, if connection errors, then error with process. If connection does not return 0, then
## port is not open.
def tcpscan(ip, port):
 #   print ("tcp scans")
    try:
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = tcpsock.connect_ex((ip, port))
        if result == 0:
            linestring = ip + " is open on tcp port " + str(port)
            print (linestring)
            return linestring
        else:
            linestring = ip + " is not open on tcp port " + str(port)
            print (linestring)
            return linestring
        tcpsock.close()
    except socket.gaierror:
        print ("hostname could not be resolved. Exiting")
        sys.exit()
    except socket.error:
        print ("Could not connect to error")
        sys.exit()

## Udp scan sends message to host and port. If error occurs, port is not open.
def udpscan(ip, port):
    #udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        MESSAGE = "Hello, World!"
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP
        sock.sendto(data, (host, port))
        sock.settimeout(5)
        sock.recvfrom(1024)
## Used code from https://github.com/RistekCSUI/NetSOS/blob/master/python/UDP-scan.py
        linestring = ip + " is open on udp port " + str(port)
        print (linestring)
        return linestring
    except:
        linestring = ip + " is not open on udp port " + str(port)
        print (linestring)
        return linestring


## Option to export to basic html file

def exporttohtml(report_array):

    choose = input("export to html? (y/n): ")
    if choose=='y' or choose=='Y':
        filename = input("Enter in html filename: ")
        htmlfilename = filename + ".html"
        htmlfile = open(htmlfilename,'w')
        htmlstring = "<h1> Port Scan Report </h1><br>"
        for line in report_array:
            htmlstring = htmlstring + "<li>" + line + "</li>"

        htmlfile.write(htmlstring)
        htmlfile.close()
    else:
        return

### Main project loop
while 1:
    menu()
    target_list = enter_command()
#print (target_list)
    report_array = []
    for target in target_list:
        test= str(target[0])
    #print (test)
    #print (str(test.find('/')))
        if test.find('/') != -1:
            for ip in target[0]:
                if target[2] == 'udp':
                    report_array.append(udpscan(str(ip), int(target[1])))
                if target[2] == 'tcp':
                    report_array.append(tcpscan(str(ip), int(target[1])))
        elif target[2] == 'udp':
        report_array.append(udpscan(target[0],int(target[1])))
        elif target[2] == 'tcp':
        report_array.append(tcpscan(target[0],int(target[1])))

    exporttohtml(report_array)
