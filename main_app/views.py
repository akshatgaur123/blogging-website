from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.db import connection
import time
import jwt
import json
import urllib.parse

cursor=connection.cursor()

def mk_token(load):
	token=jwt.encode(payload=load,key='12345678')
	return token

def find_hash(comment,h):
	words=comment.split()
	i=0
	array=[]
	while i<len(words):
		x=words[i]
		y=x.split(h)
		if len(y)==1:
			pass
		else:
			j=1
			while j<len(y):
				array.append(y[j])
				j=j+1
		i=i+1
	return array
def add_tags(array,comment_id,h):
	global cursor
	print('add_tags')
	if h=='#':
		i=0
		while i<len(array):
			try:
				q=hash_data.objects.get(Text=array[i])
				hash_id=q.id
				if q.child=='none':
					query_string="UPDATE main_app_hash_data SET child={} WHERE id={}"
					query_string=query_string.format(str(comment_id),hash_id)
					cursor.execute(query_string)
					print('namhi')
				else:
					query_string="UPDATE main_app_hash_data SET child={} WHERE id={}"
					print('1')
					h=q.child+','+str(comment_id)
					h="'"+h+"'"
					print('2')
					query_string=query_string.format(h,hash_id)
					print(query_string)
					print('3')
					cursor.execute(query_string)

			except Exception:
				x=hash_data.objects.create(Text=array[i],child=str(comment_id))
		
			i=i+1
		return 0
	if h=='@':
		i=0
		print(11)
		while i<len(array):
			if True:
				q=tags.objects.get(Text=array[i])
				hash_id=q.id
				if q.child=='none':
					query_string="UPDATE main_app_tags SET child={} WHERE id={}"
					query_string=query_string.format(str(comment_id),hash_id)
					cursor.execute(query_string)
					print('namhi')
				else:
					query_string="UPDATE main_app_tags SET child={} WHERE id={}"
					print('1')
					h=q.child+','+str(comment_id)
					h="'"+h+"'"
					print('2')
					query_string=query_string.format(h,hash_id)
					print(query_string)
					print('3')
					cursor.execute(query_string)


				q=users.objects.get(username=array[i])
				user_id=q.id
				s=q.notifications
				if s=='none':
					query_string="UPDATE main_app_users SET notifications={} WHERE id={}"
					h=str(comment_id)+':'+'y'
					h="'"+h+"'"
					query_string=query_string.format(h,user_id)
					cursor.execute(query_string)
				else:
					query_string="UPDATE main_app_users SET notifications={} WHERE id={}"
					h=s+','+str(comment_id)+':'+'y'
					h="'"+h+"'"
					query_string=query_string.format(h,user_id)
					cursor.execute(query_string)

			#except Exception:
			#	print('trewe is except')
			#	pass
			i=i+1
		return 0

	return 0	


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]

def main_fun(request):
	global cursor
	if request.method=='GET':
		token=request.GET.get('token')
		
		cursor.execute("SELECT * FROM main_app_comments WHERE parent=0")
		data=dictfetchall(cursor)
		data=json.dumps(data)
		print(data)
		context={'data':data,'token':token}
		return render(request,'homebar.html',context)
		pass



	if request.method=='POST':
		comment=request.POST.get('comment')
		token=request.POST.get('token_field')
		if token==None:
			return render(request,'login_page.html')
		try:
			new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])          
		except Exception:
			return render(request,'login_page.html')


		comment=comment.replace('"','$%*')
		comment=comment.replace('\r\n',' ')
		q=users.objects.get(username=new_token['username'])
		image_url=q.image_url
		x=comments.objects.create(auther=new_token['username'],Text=comment,child="none",image_url=image_url)
		comment_id=x.id
		user_id=new_token['user_id']
		user=users.objects.get(id=user_id)
	

		if user.history=='none':
			query_string="UPDATE main_app_users SET history={} WHERE id={}"
			query_string=query_string.format(str(comment_id),user_id)
			cursor.execute(query_string)
		else:
			query_string="UPDATE main_app_users SET history={} WHERE id={}"
			h=user.history+','+str(comment_id)
			h="'"+h+"'"
			query_string=query_string.format(h,user_id)
			cursor.execute(query_string)



		hash_tags=find_hash(comment,'#')
		if len(hash_tags)!=0:
			add_tags(hash_tags,comment_id,'#')

		at_the_rates=find_hash(comment,'@')
		if len(at_the_rates)!=0:
			add_tags(at_the_rates,comment_id,'@')


		
		



			
		cursor.execute("SELECT * FROM main_app_comments")
		data=dictfetchall(cursor)
		data=json.dumps(data)
		context={'data':data,'token':token}
		return render(request,'homebar.html',context)




def tag_fun(request):
	token=request.GET.get("token")
	try:
		new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
	except Exception:
		return render(request,'login_page.html')
	username=new_token['username']
	q=tags.objects.get(Text=username)
	child_text=q.child
	child=child_text.split(',')
	data=[]
	if child_text!='none':
		child=child_text.split(',')
		i=0
		while i<len(child):
			child[i]=int(child[i])
			i=i+1
		i=0
		while i<len(child):
			q=comments.objects.get(id=child[i])
			f={'id':child[i],'auther':q.auther,'Text':q.Text,'child':q.child,'parent':q.parent,'image_url':q.image_url}
			data.append(f)
			i=i+1
	data=json.dumps(data)
	context={'data':data,'token':token}
	return render(request,'tags.html',context)








def history_fun(request):
	token=request.GET.get("token")
	try:
		new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
	except Exception:
		return render(request,'login_page.html')
	username=new_token['username']
	q=users.objects.get(username=username)
	child_text=q.history
	child=child_text.split(',')
	data=[]
	if child_text!='none':
		child=child_text.split(',')
		
		i=0
		while i<len(child):
			child[i]=int(child[i])
			i=i+1
		i=0
		while i<len(child):
			try:
				q=comments.objects.get(id=child[i])
				f={'id':child[i],'auther':q.auther,'Text':q.Text,'child':q.child,'parent':q.parent,'image_url':q.image_url}
				data.append(f)
			except Exception:
				pass
			i=i+1

	data=json.dumps(data)
	context={'data':data,'token':token}
	return render(request,'tags.html',context)

	pass


def login_fun(request):
	if request.method!='POST':
		return render(request,'login_page.html')
	else:
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=users.objects.filter(username=username,password=password)
		d=0
		for i in user:
			preference=i.preference
			history=i.history
			user_id=i.id
			d=1
		if d==0:
			context={'res':'incorrect username or password'}
			return render(request,'login_page.html',context)
		
		if d==1:
			load={}
			load['preference']=preference
			load['history']=history
			load['username']=username
			load['password']=password
			load['user_id']=user_id
			load['exp']=time.time()+20*60
			token=mk_token(load)
			context={'token':token}
			url_encoded_token=urllib.parse.quote(token)
			url_string='/posts?token=%s'%url_encoded_token
			return redirect(url_string)



def replay_fun(request):
	if request.method=='POST':
		if request.POST.get("purpose")=='veiw_replay':
			token=request.POST.get('token_field')
			parent_id=request.POST.get('parent_id')
			try:
				new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
			except Exception:
				return render(request,'login_page.html')
			print(parent_id)
			e=comments.objects.get(id=parent_id)
			child_text=e.child
			data=[]
			if child_text!='none':
				child=child_text.split(',')
				i=0
				while i<len(child):
					child[i]=int(child[i])
					i=i+1
				i=0
				while i<len(child):
					q=comments.objects.get(id=child[i])
					f={'id':q.id,'auther':q.auther,'Text':q.Text,'child':q.child,'parent':q.parent,'image_url':q.image_url}
					data.append(f)
					i=i+1
			data=json.dumps(data)

			parent_auther=e.auther
			parent_text=e.Text
			context={'token':token,'parent_id':parent_id,'data':data,'parent_auther':parent_auther,'parent_text':parent_text}
			return render(request,'replay_page.html',context)




		if request.POST.get("purpose")=='post_replay':
			token=request.POST.get('token_field')
			parent_id=request.POST.get('parent_id')
			try:
				new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
			except Exception:
				return render(request,'login_page.html')
			comment=request.POST.get("comment")
			auther=new_token['username']
			q=users.objects.get(username=auther)
			image_url=q.image_url
			x=comments.objects.create(auther=auther,Text=comment,child="none",parent=parent_id,image_url=image_url)
			comment_id=x.id

			parent=comments.objects.get(id=parent_id)
			if parent.child=='none':
				query_string="UPDATE main_app_comments SET child={} WHERE id={}"
				query_string=query_string.format(str(comment_id),parent_id)
				cursor.execute(query_string)
			else:
				query_string="UPDATE main_app_comments SET child={} WHERE id={}"
				h=parent.child+','+str(comment_id)
				h="'"+h+"'"
				query_string=query_string.format(h,parent_id)
				cursor.execute(query_string)

			e=comments.objects.get(id=parent_id)
			parent_auther=e.auther
			print(parent_auther)
			f=users.objects.get(username=parent_auther)
			user_id=f.id
			s=f.notifications
			if s=='none':
				query_string="UPDATE main_app_users SET notifications={} WHERE id={}"
				h=str(comment_id)+':'+'x'
				h="'"+h+"'"
				query_string=query_string.format(h,user_id)
				cursor.execute(query_string)
			else:
				query_string="UPDATE main_app_users SET notifications={} WHERE id={}"
				h=s+','+str(comment_id)+':'+'x'
				h="'"+h+"'"
				query_string=query_string.format(h,user_id)
				cursor.execute(query_string)

			child_text=e.child
			data=[]
			if child_text!='none':
				child=child_text.split(',')
				print(child)
				print(child[0])
				i=0
				while i<len(child):
					child[i]=int(child[i])
					i=i+1
				i=0
				while i<len(child):
					q=comments.objects.get(id=child[i])
					f={'id':q.id,'auther':q.auther,'Text':q.Text,'child':q.child,'parent':q.parent,'image_url':q.image_url}
					data.append(f)
					i=i+1
			print(data)
			data=json.dumps(data)
			parent_text=e.Text

			context={'token':token,'parent_id':parent_id,'data':data,'parent_auther':parent_auther,'parent_text':parent_text}
			return render(request,'replay_page.html',context)



			
def notifications(request):
	token=request.GET.get('token')
	try:
		new_token=jwt.decode(token,key='12345678',algorithms=['HS256', ])
	except Exception:
		return render(request,'login_page.html')
	username=new_token['username']
	print(username)
	q=users.objects.get(username=username)
	data=[]
	nat=q.notifications
	if nat!='none':
		nat=nat.split(',')
		i=0
		new_nat=[]
		while i<len(nat):                               
			a=nat[i].split(':')
			new_nat.append(a)
			i=i+1
		i=0
		while i<len(new_nat):
			try:
				comment_id=int(new_nat[i][0])
				e=comments.objects.get(id=comment_id)
				parent_id=e.parent
				if parent_id!=0:
					f=comments.objects.get(id=parent_id)
					parent_text=f.Text
				else:
					parent_text='none'

				if e.auther!=username:
					print('image',e.image_url)
					b={'id':e.id,'auther':e.auther,'Text':e.Text,'child':e.child,'parent':e.parent,'action':new_nat[i][1],'parent_text':parent_text,'image_url':e.image_url}
					data.append(b)
			except Exception:
				pass
			i=i+1
	data=json.dumps(data)
	context={'data':data,'token':token}
	return render(request,'notification.html',context)



def search_fun(request):
	if request.method=='POST':
		search_query=request.POST.get('search_bar')
		token=request.POST.get('token_field')
		print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
		print(token)
		child=[]
		try:
			q=hash_data.objects.get(Text=search_query)
			child_text=q.child
			child=child_text.split(',')
		except Exception:
			child=[]
			pass

		data=[]	
		i=0
		while i<len(child):
			child[i]=int(child[i])
			i=i+1
		i=0
		while i<len(child):
			q=comments.objects.get(id=child[i])
			f={'id':q.id,'auther':q.auther,'Text':q.Text,'child':q.child,'parent':q.parent}
			data.append(f)
			i=i+1

		try:
			q=tags.objects.get(Text=search_query)
			child_text=q.child
			child=child_text.split(',')
		except Exception:
			child=[]
			pass

		i=0
		while i<len(child):
			child[i]=int(child[i])
			i=i+1

		i=0
		while i<len(child):
			q=comments.objects.get(id=child[i])
			f={'id':q.id,'auther':q.auther,'Text':q.Text,'child':q.child,'parent':q.parent}
			data.append(f)
			i=i+1

		try:
			q=users.objects.get(username=search_query)
			child_text=q.history
			child=child_text.split(',')
		except Exception:
			child=[]

		i=0
		while i<len(child):
			child[i]=int(child[i])
			i=i+1
		i=0
		while i<len(child):
			q=comments.objects.get(id=child[i])
			f={'id':q.id,'auther':q.auther,'Text':q.Text,'child':q.child,'parent':q.parent}
			data.append(f)
			i=i+1

		data=json.dumps(data)

		if len(data)==0:
			res='No matches found'
			context={'data':data,'token':token,'res':res}
			return render(request,'search.html',context)
		else:
			res=''
			context={'data':data,'token':token,'res':res}
			return render(request,'search.html',context)

	
def sign_up_fun(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		try:
			q=users.objects.get(username=username)
			res='username already exists try different username '
			context={'res':res}
			return render(request,'sign_up.html',context)

		except Exception:
			x=users.objects.create(password=password,username=username)
			y=tags.objects.create(Text=username,child='none')
			return render(request,'login_page.html')
	else:
		return render(request,'sign_up.html')
