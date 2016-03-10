#Build 1.0.5

from getopt import getopt, GetoptError
from smtplib import SMTP
from socket import socket, AF_INET, gethostname, SOCK_DGRAM
from sys import argv, exit

def getIP():
    #Makes a connection to get the local IP of device
    s = socket(AF_INET, SOCK_DGRAM)
    #Gmail can be replaced with 8.8.8.8 for example, or local ip if not internet connected
    s.connect(("gmail.com", 80))
    ipaddr = s.getsockname()[0]
    s.close
    return ipaddr

def sendEmail(fromaddr, toaddr, hostname, username, password):
    #Build email to send via GMail SMTP
    msg = '\r\n'.join(['From: ' + fromaddr, 'To: ' + toaddr, 'Subject: ' + hostname + ' Just Turned On!', '', 'The Local IP is: ' + getIP()])
    server = SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

def main(argv):
    #Initialise argument variables
    fromaddr = ''
    toaddr = ''
    username = ''
    password = ''
    #Get argument input
    try:
        opts, args = getopt(argv, 'f:t:u:p:', ['from=','to=', 'username=', 'password='])
    except GetoptError:
        print('IP_Notify.py -f <fromaddress> -t <toaddress> -u <username> -p <password>')
        exit(1)
    for opt, arg in opts:
        if opt in ('-f', '--from'):
            fromaddr = arg
        elif opt in ('-t', '--to'):
            toaddr = arg
        elif opt in ('-u', '--username'):
            username = arg
        elif opt in ('-p', '--password'):
            password = arg
    #Send Email
    sendEmail(fromaddr, toaddr, gethostname(), username, password)

if __name__ == "__main__":
    exit(int(main(argv[1:]) or 0))