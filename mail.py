#!/usr/bin/env python3

import sys
import smtplib
import argparse
from email.mime.text import MIMEText
from time import localtime, strftime

DEBUG = True

__version = "Version: 1.0"
__encoding = sys.getdefaultencoding()

settings, logs = [""], [""]
file_name = "mail_settings.txt"
status = ""
saved = ""

def exit_program():
	print("\n") 	
	print("Program is closing..")
	print("Bye.")
	sys.exit()

def load_settings():
	global settings, saved, account, password

	with open(file_name,"a", encoding=__encoding) as startFile: #kayit yoksa ac, varsa gir bak sadece
		pass

	with open(file_name, encoding=__encoding) as readFile: #kayitlari settings dizisine at
		for i in readFile.readlines():
			settings.append(i)

	try:
		saved = settings[1][:-1] # just for check
		saved == "True"
	except:
		saved == "False"
	else:
		try:
			account = settings[2][:-1]
			password = settings[3]
		except: # Bu kısım .txt belgesinde eksik bir satir varsa calisir
			print("[-] File Content Incorrect: "+file_name)
			exit_program()


def save_settings():

	if(args.save):

		with open(file_name, "a", encoding=__encoding) as startFile:
			pass

		settings = [""]
		settings.append("True" + "\n")
		settings.append(args.account + "\n")
		settings.append(args.password)

		with open(file_name, "w", encoding=__encoding) as writeFile:

			for i in settings:
				writeFile.write(i)

			print("[+] Settings Saved: "+file_name)

def save_log():
	if(args.log):
		log_name = "log_" + strftime("%Y%m%d_%H%M%S", localtime()) + ".txt"
		with open(log_name, "a", encoding=__encoding) as startLog:
			pass
		logs.append("FROM: " + args.account)
		logs.append("\n")
		logs.append("TO: " + mails)
		logs.append("\n")
		logs.append("SUBJECT: " + args.subject)
		logs.append("\n")
		logs.append("MESSAGE: " + args.message)
		logs.append("\n")
		logs.append("STATUS: "+ status)
		with open(log_name, "w", encoding=__encoding) as writeLog:
			for i in logs:
				writeLog.write(str(i))
			print("[+] Log Saved: "+log_name)

def find_method():
	type = find_domain()
	if(args.type == "TLS"):
		if(type == "outlook.com"):
			smtp_url = "smtp-mail.outlook.com"
		elif(type == "gmail.com"):
			smtp_url = "smtp.gmail.com"
		elif(type == "yahoo.com"):
			smtp_url = "smtp.mail.yahoo.com"
		else:
			print("Your mail's domain not supported in this program.")
			exit_program()
		connect_with_tls(smtp_url)
	else:
		pass #SSL Baglanti Durumunda Olacaklar

def print_info():
	global args, mails
	print(" ")
	print("FROM\t >    {}".format(args.account))
	mails=""
	for i in args.to[0]:
		mails = mails + i + ", "
	mails =  mails[:-2]
	print("TO\t >    "+mails)
	print("SUBJECT\t >    {}".format(args.subject))
	print("MESSAGE\t >    {}".format(args.message))
	print(" ")
	print("[+] Connecion Type: "+args.type)
	print("[+] Port: "+str(args.port))

def find_domain():
	domain = format(args.account).split('@')
	service_name = domain[1]
	return service_name

def connect_with_tls(url):
	global server
	print("[+] SMTP Server URL: "+url)

	server = smtplib.SMTP(url, args.port)

	try:
		server.ehlo() # Herhangi bir bağlantı problemi olup olmadığı kontrol ediliyor.
		print("[+] Connection Problem Not Found.")
	except:
		print("[-] Connection Problem Found.")
		exit_program()

	try:
		server.starttls() # Server ile TLS (şifreli) bağlantı kuruyoruz
		print("[+] Establishment was of TLS Connection with SMTP Server.")
	except:
		print("[-] Unable to Connect to TLS with SMTP Server.")
		exit_program()

	try:
		server.login(args.account, args.password) # SMTP Server'a giriş yapıyoruz.
		print("[+] SMTP Server User Login Successful.")
	except:
		print("[-] SMTP Server User Login Failed.")
		exit_program()


def send_mail():
	global mail, server, status

	mail = MIMEText(args.message, 'html', __encoding)
	mail['From'] = args.account
	mail['Subject'] = args.subject
	mail['To'] = ','.join(args.to[0])
	mail = mail.as_string()

	try:
		if(DEBUG):
			print("[DEBUG] Email Sending Successful.")
			status = "Debug Active"
		else:
			server.sendmail(args.account, args.to[0], mail)
			print("[+] Email Sending Successful.")
			status = "Success"
	except:
		print("[-] Email Sending Failed.")
		status = "Failed"

def init():
	global parser, args
	parser = argparse.ArgumentParser(description="This is a Cli Tool for Your EMails", epilog="And that's how you'd send mail via terminal", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	if(saved == "True"):
		parser.add_argument("-account","-a", help="type your account name", default=account)
		parser.add_argument("-password","-p", help="type your password", default=password)
	else:
		parser.add_argument("-account","-a", required=True, help="type your account name")
		parser.add_argument("-password","-p", required=True, help="type your password")
	
	parser.add_argument("-subject","-s", help="type your subject", default="My Awesome Subject")
	parser.add_argument("-message","-m", help="type your message", default="My Awesome Message")
	parser.add_argument("-to","-t",nargs='+',metavar='RECEIVER', required=True, action='append', help="type receiver mails")
	parser.add_argument("-log","-l", help="save content as a log", action='store_true')
	parser.add_argument("--type", help="change connection type",default="TLS", choices=["TLS", "SSL"])
	parser.add_argument("--port", help="change connection port",default=587, choices=[587, 465, 25],type=int)
	parser.add_argument("--save", help="save account and password information", action='store_true')
	parser.add_argument('--version','-v', action='version', version=__version)
	args = parser.parse_args() # Gelen argümanları bir listeye aktarıyoruz

def main():
	load_settings()
	init()
	print_info()
	find_method()
	send_mail()
	save_settings()
	save_log()

main()

"""
TODO

+ POP protokolu ile mail gondermek
+ IMAP protokolü ile mail gonderebilmek
+ log argümanı bir klasöre gösterilebilsin, gösterilen klasör save olsun ve bir dahikine bunu kullanalım
+ log argümanı parametre alırsa aldığı parametre adında log dosyasını kaydetsin
+ sürükli log alma save edilebilsin
+ to kısmına .txt dosya gostermek
+ message argümanına .txt dosya gosterebilmek

BUG

-

"""