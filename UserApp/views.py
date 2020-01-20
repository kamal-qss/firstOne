from django.shortcuts import redirect, render, render_to_response
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from UserApp.tokens import account_activation_token
from django.core.mail import EmailMessage
from UserApp.forms import FormUser,UserInputForm
# from passlib.hash import django_pbkdf2_sha256 as handler
from UserApp.models import User
from django.conf import settings
from UserApp import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse

from elasticsearch import Elasticsearch
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from dateutil.relativedelta import relativedelta
import csv
import psycopg2
from django.template.context import RequestContext

def signup(request):
	if request.method == 'POST':
		formvalue = User.objects._create_user(first_name = request.POST['sfirstname'],last_name=request.POST['slastname'],email=request.POST['semail'],password=request.POST['spassword'])
		formvalue.save()

		current_site = get_current_site(request)
		mail_subject = 'Activate your account!'
		message = render_to_string('UserApp/acc_active_email.html', {
			'user': formvalue,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(formvalue.pk)).decode(),
			'token':account_activation_token.make_token(formvalue),
		})
		to_email = request.POST.get('semail')
		email = EmailMessage(
			mail_subject, message, to=[to_email]
		)
		email.send()
		return render(request, 'UserApp/UserHome.html', {})
	
		# return HttpResponse('Please confirm your email address to complete the registration')
	else:
		formvalue = FormUser
	return render(request, 'UserApp/UserForm.html', {'formvalue': formvalue})

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		return HttpResponse('Thank you for your email confirmation. Now you can login your account,{}'.format(user.first_name))
	else:
		return HttpResponse('Activation link is invalid!')


# def userlogin(request):
# 	if request.method == 'POST':
# 		try:
# 			username = request.POST.get('lemail')
# 			password = request.POST.get('lpassword')
# 			loginUser = authenticate(username=username,password=password)
# 			if loginUser is not None:
# 					login(request,loginUser)
# 					return render(request, 'UserApp/UserHome.html', {"loginUser":loginUser})
# 			else:
# 					return HttpResponse('User None!!')
# 		except User.DoesNotExist:
# 			loginUser = None
# 			return HttpResponse('No Valid object found!!!')
# 	return render(request, 'UserApp/SUserlogin.html', {})

def userlogin(request):
	if request.method=='POST':
		username = request.POST.get('lemail')
		password = request.POST.get('lpassword')
		user = authenticate(email=username, password=password)
		try:
			obj = User.objects.get(email=username)
			if user is not None and user.is_active:
				login(request, user)
				print(user)
				return redirect('../userHome')
			elif obj.get_isActiveStatus() == False:
				messages.info(request, 'User is not active')
				return redirect("../userlogin")
			elif obj.get_isActiveStatus() == True:
				#messages.info(request, 'Your password is incorrect!!')
				return render(request,'UserApp/SUserlogin.html',{'messages':1})	
			else:
				return HttpResponse("You are not registered!!")
		except User.DoesNotExist:
			messages.info(request, 'You are not registered!!')
			return redirect("../userlogin")
	else:
		formvalue = UserInputForm
		return render(request,'UserApp/SUserlogin.html',{'formvalue':formvalue})
		# return HttpResponseRedirect('Thanks')


def userHome(request):
	if request.user.is_authenticated:
		loginUser = request.user
	else:
		loginUser = None
	print(loginUser)
	try:
		def decode_utf8(input_iterator):
			for l in input_iterator:
				yield l.decode('utf-8')
		conn = psycopg2.connect(dbname="VTIONData",host= "vtionproddb.chgz4nqwpdta.ap-south-1.rds.amazonaws.com", user="vtion", password="per4mance")
		cur = conn.cursor()
		if request.method == 'POST':
			reader = csv.DictReader(decode_utf8(request.FILES['document']))
			for row in reader:
				if len(row.get('Ad')) == 10:
					if int(row.get('Uninstalls')) >= int(row.get('Installs')):
						status = True
					else:
						status = False
					number = row.get('Ad')
					cur.execute('''SELECT installs FROM public.appsflyer where number = '{}' '''.format(number))
					check = cur.fetchone()
					if check:
						print("Updation")
						try:
							cur.execute(''' UPDATE public.appsflyer SET installs = '{}', uninstalls = '{}', i_status = '{}', accessibility = '{}',
										video_tuned = '{}', fm_tuned = '{}', audio_tuned = '{}' 
										WHERE number = '{}' '''.format(row.get('Installs'), row.get('Uninstalls'),
										status, row.get('accessibilitystate (Unique Users)'), row.get('video_tuned (Event Counter)'), row.get('fm_tuned (Event Counter)'),
										row.get('audio_tuned (Event Counter)'), number))
							conn.commit()
						except Exception as e:
							print(e)
					else:
						print("New")
						kk = '''INSERT INTO appsflyer(number, installs, uninstalls, i_status, accessibility, video_tuned, fm_tuned, audio_tuned) 
								VALUES('{}','{}','{}','{}','{}','{}','{}','{}')'''.format(number, 
                                row.get('Installs'), row.get('Uninstalls'),status, row.get('accessibilitystate (Unique Users)'), row.get('video_tuned (Event Counter)'),
                                row.get('fm_tuned (Event Counter)'),row.get('audio_tuned (Event Counter)'))
						print(kk)
						cur.execute(kk)
						conn.commit()
	except :
		print("Passed due to error")
		pass
	# return HttpResponseRedirect('UserApp/UserHome.html')
	return render(request, 'UserApp/UserHome.html', {'loginUser':loginUser})
	# return render_to_response("normal/template.html", context_instance=RequestContext(request))
	# return HttpResponseRedirect('Thanks')
	# return redirect("/")


# @login_required
def passwordreset(request):
    print(request.user.password)
    if request.method == 'POST':
            try:
                loginUser = User.objects.get(email=request.user.email)
                user = authenticate(email=loginUser.email, password=request.POST.get("currpassword"))
                if user is not None:
                	newpassword = handler.hash(request.POST.get("newpassword"))
                	print(newpassword)
                	loginUser.password = newpassword
                	loginUser.save()
                	user = authenticate(email=request.user.email, password=request.POST.get("newpassword"))
                	print(user)
                	login(request, user)
                	return redirect('../userHome')
                else:
                    return HttpResponse('Wrong password!!')
            except User.DoesNotExist:
                loginUser = None
                return HttpResponse('No Valid object found!!!')
    else:
        return render(request, 'UserApp/PasswordReset.html', {})	

# @login_required
def userLogout(request):
	logout(request)
	loginUser = None
	return render(request, 'UserApp/UserHome.html', {"loginUser":loginUser})

def activateOnRequest(request):
	if request.method == 'POST':
		aemail = request.POST.get('aemail')
		try:
			obj = User.objects.get(email=aemail)
			current_site = get_current_site(request)
			mail_subject = 'Activate your account!'
			message = render_to_string('UserApp/acc_active_email.html', {
				'user': obj,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(obj.pk)).decode(),
				'token':account_activation_token.make_token(obj),
			})
			to_email = request.POST.get('aemail')
			email = EmailMessage(
				mail_subject, message, to=[to_email]
			)
			email.send()
			messages.info(request,'Email has been send to Your Email Address!')
			return redirect('../activateOnRequest')
		except User.DoesNotExist:
			messages.info(request,"User Does not Exist, email is not found!")
			return redirect('../activateOnRequest')
	else:
		return render(request,'UserApp/Activation.html',{})

class CreateChartHomePage(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])
		data = {}
		i = 6
		data["notification_state_true"] = 0
		data["notification_state_false"] = 0
		data["fm_competingapp_true"] = 0
		data["fm_competingapp_false"] = 0
		data["fm_competingapp_nomatch"] = 0
		while i>=0:
			beforethirty = datetime.datetime.now() - relativedelta(days=i)
			date_formated = beforethirty.strftime("%m%d%Y")
			stra = "date_"+date_formated
			try:
				data["notification_state_true"] = data["notification_state_true"] + es.search(index="notification_state_true",body={"query": {"match": {"id" : stra}}})["hits"]["hits"][0]["_source"]["truecount"]
			except Exception as e:
				# data["notification_state_true"] = 0
				pass
			try:
				data["notification_state_false"] = data["notification_state_false"] + es.search(index="notification_state_false",body={"query": {"match": {"id" : stra}}})["hits"]["hits"][0]["_source"]["falsecount"]
			except Exception as e:
				# data["notification_state_false"] = 0
				# print(e)
				pass

			try:
				data["fm_competingapp_true"] = data["fm_competingapp_true"] + es.search(index="fm_competingapp_true",body={"query": {"match": {"id" : stra}}})["hits"]["hits"][0]["_source"]["truecount"]
			except Exception as e:
				# data["fm_competingapp_true"] = 0
				pass
			
			try:
				data["fm_competingapp_false"] = data["fm_competingapp_false"] + es.search(index="fm_competingapp_false",body={"query": {"match": {"id" : stra}}})["hits"]["hits"][0]["_source"]["falsecount"]	
			except Exception as e:
				# data["fm_competingapp_false"] = 0
				pass

			try:
				data["fm_competingapp_nomatch"] = data["fm_competingapp_nomatch"] + es.search(index="fm_competingapp_nomatch",body={"query": {"match": {"id" : stra}}})["hits"]["hits"][0]["_source"]["nomatchcount"]	
			except Exception as e:
				# data["fm_competingapp_nomatch"] = 0
				pass
			i = i - 1		
		# print(data)
		return Response(data)

class CreatedataHomePageInstallData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		i = 15
		datalabel = []
		datacount = []
		es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])
		while i >= 0:
			beforethirty = datetime.datetime.now() - relativedelta(days=i)
			date_formated = beforethirty.strftime("%m%d%Y")
			strid = "date_"+date_formated
			# print(strid)
			try:
				truecount = es.search(index="fm_competingapp_true",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["truecount"]
			except Exception as e:
				truecount = 0
			try:
				falsecount = es.search(index="fm_competingapp_false",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["falsecount"]	
			except Exception as e:
				falsecount = 0
			try:
				nomatchcount = es.search(index="fm_competingapp_nomatch",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["nomatchcount"]	
			except Exception as e:
				nomatchcount = 0
			
			count = truecount + falsecount + nomatchcount
			datalabel.append(strid)
			datacount.append(count)
			# print(count)
			# print(i)
			i = i - 1
		datanew = {
			"datalabel":datalabel,
			"datacount":datacount,
		}
		return Response(datanew)



