from att_gui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QTableView,QTableWidget,QTableWidgetItem
from mysql.connector import connect
import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt





class Attendance(QMainWindow,Ui_MainWindow):
	def __init__(self):
		super().__init__()
		
		self.setupUi(self)
		self.registerbtn()
		self.submitbtn()
		self.loginbtn()
		self.backloginbtn()
		self.enterattbtn()
		self.attbackbtn()
		self.backbtn()
		self.enterattbtn()
		self.attsubmitbtn()
		self.viewattbtn()
		self.viewbackbtn()
		self.filebtn()
		self.updatebtn()
		self.fpassbtn()
		self.fsubmitbtn()
		self.otpsubmitbtn()
		self.newpasssubmitbtn()
		self.analysisbtn()
		self.forbackbtn()
		self.calculatebtn()
		self.backcalbtn()
		self.submitcalbtn()
		self.backcalshowbtn()

		


		

	#def dbconnect(self):
		#conn=connect(host='localhost',database='attendance',user='root',password='')
	

	def showmessagebox(self,title,message):
	 	msgbox=QMessageBox()
	 	msgbox.resize(200,100)

	 	msgbox.setIcon(QMessageBox.Information)
	 	msgbox.setWindowTitle(title)
	 	msgbox.setText(message)
	 	msgbox.setStandardButtons(QMessageBox.Ok)
	 	msgbox.exec_()

	def registerbtn(self):

		self.register_2.clicked.connect(self.on_register)

	def on_register(self):
		
		self.stackedWidget.setCurrentIndex(4)
		
		

	def submitbtn(self):
		
		self.submit.clicked.connect(self.onsubmit)


	def onsubmit(self):
		conn=connect(host='localhost',database='attendance',user='root',password='')
		name=self.name.text()
		dept=self.dept.text()
		dept=dept.lower()
		sem=int(self.sem.text())
		mobileno=int(self.mobileno.text())
		email=self.email.text()
		password=self.password.text()
		username=self.username_3.text()
		eml=len(email)-10

		if name=='' or dept=='' or sem=='' or mobileno=='' or email=='' or password=='' or username=='':
			self.showmessagebox('info','enter all info')
		if len(str(mobileno))!=10:
			self.showmessagebox('info','enter proper mobile no')
			self.mobileno.setText('')
		if email[eml:]!='@gmail.com' and  email[eml:]!='@yahoo.com':
			self.showmessagebox('info','enter proper email')
			self.email.setText('')
		else:
			query='insert into studentdetails (name,email,mobileno,dept,sem,username,password) values(%s,%s,%s,%s,%s,%s,%s)'
			datain=(name,email,mobileno,dept,sem,username,password)
			cursor=conn.cursor()
			cursor.execute(query,datain)
			conn.commit()
			cursor.close()
			self.showmessagebox('info','data entered')
			self.stackedWidget.setCurrentIndex(0)

	def fpassbtn(self):
		self.fpass.clicked.connect(self.onfpassbtn)

	def onfpassbtn(self):
		self.stackedWidget.setCurrentIndex(1)

	def fsubmitbtn(self):
		self.fsubmit.clicked.connect(self.onfsubmit)
		


	def onfsubmit(self):
		username=self.fusername.text()
		# add code if user has already used otp once
		self.unamedis.setText(username)
		conn=connect(host='localhost',database='attendance',user='root',password='')
		query='select email from studentdetails where username=%s'
		cursor=conn.cursor()
		cursor.execute(query,(username,))
		
		em=cursor.fetchone()
		if em is None:
			self.showmessagebox('error','no such user')
			self.fusername.setText('')
		else:
			#self.stackedWidget.setCurrentIndex(2)
			email=em[0]


			otp=random.randrange(1000,1000000)
			otp=str(otp)
			MY_ADDRESS = 'emailid'
			PASSWORD = 'password'
			msg = MIMEMultipart() 
			try:
				s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)

				s.ehlo()
				s.login(MY_ADDRESS, PASSWORD)
			except:
				self.showmessagebox('error','check internet connection')
				exit()
			msg['From']=MY_ADDRESS
			msg['To']=email
			msg['Subject']='OTP for password reset'
			message=otp
			msg.attach(MIMEText(message, 'plain'))
			s.send_message(msg)
			s.quit()
			query2='select * from otpdetails where username=%s'
			cursor.execute(query2,(username,))
			value=cursor.fetchall()
			if value:
				query3='update otpdetails set otp =%s where username=%s'
				cursor.execute(query3,(otp,username))
				conn.commit()
			else:
				query1='insert into otpdetails (username,otp) values (%s,%s)'
				cursor.execute(query1,(username,otp))
				conn.commit()
			cursor.close()
			self.stackedWidget.setCurrentIndex(2)
		
		

	def otpsubmitbtn(self):
		self.otpsubmit.clicked.connect(self.onotpsubmitbtn)

	def onotpsubmitbtn(self):
		otpin=self.otp.text()
		username=self.unamedis.text()
		conn=connect(host='localhost',database='attendance',user='root',password='')
		query='select otp from otpdetails where username=%s'
		cursor=conn.cursor()
		cursor.execute(query,(username,))
		row=cursor.fetchone()
		otpout=row[0]
		if otpin==otpout:
			self.showmessagebox('info','otp matched')
			self.newpassuser.setText(username)
			self.stackedWidget.setCurrentIndex(3)
		else:
			self.showmessagebox('info','otp didnt matched')

	def forbackbtn(self):
		self.forback.clicked.connect(self.onforbackbtn)
	def onforbackbtn(self):
		self.stackedWidget.setCurrentIndex(0)


		
	def newpasssubmitbtn(self):
		self.newpasssubmit.clicked.connect(self.onnewpasssubmitbtn)

	def onnewpasssubmitbtn(self):
		uname=self.newpassuser.text()
		passw=self.newpass.text()
		conn=connect(host='localhost',database='attendance',user='root',password='')
		query='update studentdetails set password=%s where username=%s'
		cursor=conn.cursor()
		cursor.execute(query,(passw,uname))
		conn.commit()
		cursor.close()
		self.showmessagebox('info','passsword updated')
		self.stackedWidget.setCurrentIndex(0)








	def loginbtn(self):
		self.login.clicked.connect(self.onlogin)

	def onlogin(self):
		conn=connect(host='localhost',database='attendance',user='root',password='')
		username2=self.username.text()
		password=self.password_2.text()
		

		query='select password,dept,username from studentdetails where username=%s'
		cursor=conn.cursor()
		cursor.execute(query,(username2,))
		passw=cursor.fetchone()
		if passw:
			pas=passw[0]
			dept=passw[1]
			unm=passw[2]
		
			cursor.close()
			if pas==password:
				self.showmessagebox('info','login successful')
				if username2=='adminit' or username2=='admincs':
					self.enteratt.setVisible(False)
					self.un.setText(unm)
					self.dept_2.setText(dept)
					self.usernameview.setText(unm)
					self.user.setText(unm)
					self.stackedWidget.setCurrentIndex(5)
				else:
					self.enteratt.setVisible(True)
					self.stackedWidget.setCurrentIndex(5)
					self.un.setText(unm)
					self.dept_2.setText(dept)
					self.usernameview.setText(unm)
					self.user.setText(unm)
					self.username.setText('')
					self.password_2.setText('')

			else:
				self.showmessagebox('info','unsuccessfull')
				self.password_2.setText('')
		else:
			self.showmessagebox('info','wrong username')
			self.username.setText('')


		

	def backloginbtn(self):
		self.backlogin.clicked.connect(self.onbacklogin)

	def onbacklogin(self):
		self.stackedWidget.setCurrentIndex(0)

	#def enterattbtn(self):
		#self.enteratt.clicked.connect(self.onenteratt)

	#def onenteratt(self):
		#self.stackedWidget.setCurrentIndex(6)

	def attbackbtn(self):
		self.attback.clicked.connect(self.onattback)

	def onattback(self):
		self.stackedWidget.setCurrentIndex(5)

	def backbtn(self):
		self.back.clicked.connect(self.onbackbtn)

	def onbackbtn(self):
		self.stackedWidget.setCurrentIndex(0)

	def enterattbtn(self):
		self.enteratt.clicked.connect(self.onenterattbtn)
	def onenterattbtn(self):

		uname=self.un.text()
		dept=self.dept_2.text()
		if uname=='adminit' or uname=='admincs':
			self.showmessagebox('warning','not possible')

		else:

			conn=connect(host='localhost',database='attendance',user='root',password='')
			query='select * from sem4 where dept=%s'
			cursor=conn.cursor()
			cursor.execute(query,(dept,))
			row=cursor.fetchone()
		
			self.sub1l.setText(row[1])
			self.sub2l.setText(row[2])
			self.sub3l.setText(row[3])
			self.sub4l.setText(row[4])
			self.sub5l.setText(row[5])
			self.sub6l.setText(row[6])
			self.user.setText(uname)

			self.stackedWidget.setCurrentIndex(6)
		
	def attsubmitbtn(self):
		self.attsubmit.clicked.connect(self.onattsubmitbtn)

		
	def onattsubmitbtn(self):
		date=self.calendar.selectedDate().toPyDate()
		
		conn=connect(host='localhost',database='attendance',user='root',password='')
	
		un=self.user.text()
		query3='select * from attrecord where date=%s and username=%s'
		cu=conn.cursor()
		cu.execute(query3,(date,un))
		r=cu.fetchall()
		if r:
			self.showmessagebox('warning','already entered for this date')
		else:

			query2='select sem,dept,username from studentdetails where username=%s'
			cursor=conn.cursor()
			cursor.execute(query2,(un,))
			row=cursor.fetchone()
			sem=row[0]
			dept=row[1]
			user=row[2]
		
			sub1=self.sub1.text()
			sub2=self.sub2.text()
			sub3=self.sub3.text()
			sub4=self.sub4.text()
			sub5=self.sub5.text()
			sub6=self.sub6.text()
			sub1l=self.sub1lec.text()
			sub2l=self.sub2lec.text()
			sub3l=self.sub3lec.text()
			sub4l=self.sub4lec.text()
			sub5l=self.sub5lec.text()
			sub6l=self.sub6lec.text()
			flag=0

			if sub1>sub1l:
				self.showmessagebox('warning','lecs attended more than total')
				self.sub1.setText('')
				flag=1
			if sub2>sub2l:
				self.showmessagebox('warning','lecs attended more than total')
				self.sub2.setText('')
				flag=1
			if sub3>sub3l:
				self.showmessagebox('warning','lecs attended more than total')
				self.sub3.setText('')
				flag=1

			if sub4>sub4l:
				self.showmessagebox('warning','lecs attended more than total')
				self.sub4.setText('')
				flag=1

			if sub5>sub5l:
				self.showmessagebox('warning','lecs attended more than total')
				self.sub5.setText('')
				flag=1
			if sub6>sub6l:
				self.showmessagebox('warning','lecs attended more than total')
				self.sub6.setText('')
				flag=1
	

			try:
				if flag!=1:
					query3='insert into attrecord values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
					indata=(user,sem,dept,date,sub1,sub2,sub3,sub4,sub5,sub6,sub1l,sub2l,sub3l,sub4l,sub5l,sub6l)
					cursor=conn.cursor()
					cursor.execute(query3,indata)
					conn.commit()
					cursor.close()
					self.showmessagebox('info','entered')
					self.sub1.setText('')
					self.sub2.setText('')
					self.sub3.setText('')
					self.sub4.setText('')
					self.sub5.setText('')
					self.sub6.setText('')
					self.sub1lec.setText('')
					self.sub2lec.setText('')
					self.sub3lec.setText('')
					self.sub4lec.setText('')
					self.sub5lec.setText('')
					self.sub6lec.setText('')

			except:
				self.showmessagebox('warning','error')
	def updatebtn(self):
		self.update.clicked.connect(self.onupdatebtn)
	def onupdatebtn(self):
		un=self.user.text()
		date=self.calendar.selectedDate().toPyDate()
		conn=connect(host='localhost',database='attendance',user='root',password='')
		query4='select * from attrecord where date=%s'
		cu=conn.cursor()
		cu.execute(query4,(date,))
		r=cu.fetchall()
		if r:
			sub1=self.sub1.text()
			sub2=self.sub2.text()
			sub3=self.sub3.text()
			sub4=self.sub4.text()
			sub5=self.sub5.text()
			sub6=self.sub6.text()
			sub1l=self.sub1lec.text()
			sub2l=self.sub2lec.text()
			sub3l=self.sub3lec.text()
			sub4l=self.sub4lec.text()
			sub5l=self.sub5lec.text()
			sub6l=self.sub6lec.text()
			try:
				query3='update  attrecord set sub1=%s,sub2=%s,sub3=%s,sub4=%s,sub5=%s,sub6=%s,sub1lec=%s,sub2lec=%s,sub3lec=%s,sub4lec=%s,sub5lec=%s,sub6lec=%s where date=%s and username=%s'
				indata=(sub1,sub2,sub3,sub4,sub5,sub6,sub1l,sub2l,sub3l,sub4l,sub5l,sub6l,date,un)
				cursor=conn.cursor()
				cursor.execute(query3,indata)
				conn.commit()
				cursor.close()
				self.showmessagebox('info','updated')
				self.sub1.setText('')
				self.sub2.setText('')
				self.sub3.setText('')
				self.sub4.setText('')
				self.sub5.setText('')
				self.sub6.setText('')
				self.sub1lec.setText('')
				self.sub2lec.setText('')
				self.sub3lec.setText('')
				self.sub4lec.setText('')
				self.sub5lec.setText('')
				self.sub6lec.setText('')
			except:
				print('error')
		else:
			self.showmessagebox('warning','no data for this date')
	



	def viewattbtn(self):
			self.viewatt.clicked.connect(self.onviewattbtn)

	def onviewattbtn(self):
			
			un=self.usernameview.text()
			#print(un)

			conn=connect(host='localhost',database='attendance',user='root',password='')
			query1='select * from sem4 where dept in(select dept from studentdetails where username=%s)'
			cur=conn.cursor()
			cur.execute(query1,(un,))
			subs=cur.fetchall()
			#print(subs)
				
			sub1=subs[0][1]
			sub2=subs[0][2]
			sub3=subs[0][3]
			sub4=subs[0][4]
			sub5=subs[0][5]
			sub6=subs[0][6]
			sub1=str(sub1)
			if un!='adminit' and un!='admincs':
				self.table.insertRow(0)
				self.table.setItem(0,0,QTableWidgetItem('Date'))
				self.table.setItem(0,1,QTableWidgetItem(sub1))
				self.table.setItem(0,2,QTableWidgetItem(sub2))
				self.table.setItem(0,3,QTableWidgetItem(sub3))
				self.table.setItem(0,4,QTableWidgetItem(sub4))
				self.table.setItem(0,5,QTableWidgetItem(sub5))
				self.table.setItem(0,6,QTableWidgetItem(sub6))

			
			if un=='adminit':
				

				self.table.insertRow(0)
				self.table.setItem(0,0,QTableWidgetItem('Username'))
				self.table.setItem(0,1,QTableWidgetItem('sem'))
				self.table.setItem(0,2,QTableWidgetItem('branch'))
				self.table.setItem(0,3,QTableWidgetItem('Date'))
				self.table.setItem(0,4,QTableWidgetItem(sub1))
				self.table.setItem(0,5,QTableWidgetItem(sub2))
				self.table.setItem(0,6,QTableWidgetItem(sub3))
				self.table.setItem(0,7,QTableWidgetItem(sub4))
				self.table.setItem(0,8,QTableWidgetItem(sub5))
				self.table.setItem(0,9,QTableWidgetItem(sub6))

				query='select username,sem,dept,date,sub1,sub2,sub3,sub4,sub5,sub6 from attrecord where dept=%s'
				cursor=conn.cursor()
				cursor.execute(query,('it',))
				result=cursor.fetchall()
				
				for row_no,row_data in enumerate(result):
					row_no+=1


					self.table.insertRow(row_no)
					for column_no,data in enumerate(row_data):
						
						self.table.setItem(row_no,column_no,QTableWidgetItem(str(data)))
				self.stackedWidget.setCurrentIndex(7)

			if un=='admincs':
				self.table.insertRow(0)
				self.table.setItem(0,0,QTableWidgetItem('Username'))
				self.table.setItem(0,1,QTableWidgetItem('sem'))
				self.table.setItem(0,2,QTableWidgetItem('branch'))
				self.table.setItem(0,3,QTableWidgetItem('Date'))
				self.table.setItem(0,4,QTableWidgetItem(sub1))
				self.table.setItem(0,5,QTableWidgetItem(sub2))
				self.table.setItem(0,6,QTableWidgetItem(sub3))
				self.table.setItem(0,7,QTableWidgetItem(sub4))
				self.table.setItem(0,8,QTableWidgetItem(sub5))
				self.table.setItem(0,9,QTableWidgetItem(sub6))
				query='select username,sem,dept,date,sub1,sub2,sub3,sub4,sub5,sub6 from attrecord where dept=%s'
				cursor=conn.cursor()
				cursor.execute(query,('cmpn',))
				result=cursor.fetchall()
				
				for row_no,row_data in enumerate(result):
					row_no+=1

					self.table.insertRow(row_no)
					for column_no,data in enumerate(row_data):
						self.table.setItem(row_no,column_no,QTableWidgetItem(str(data)))
				self.stackedWidget.setCurrentIndex(7)



			if un!='adminit' and un!='admincs':
					query='select date,sub1,sub2,sub3,sub4,sub5,sub6 from attrecord where username=%s'
					cursor=conn.cursor()
					cursor.execute(query,(un,))
					result=cursor.fetchall()
					sub1total=0
					sub2total=0
					sub3total=0
					sub4total=0
					sub5total=0
					sub6total=0
					for lecs in result:
						sub1total+=lecs[1]
						sub2total+=lecs[2]
						sub3total+=lecs[3]
						sub4total+=lecs[4]
						sub5total+=lecs[5]
						sub6total+=lecs[6]
					row_no=0
			
			

					for row_no,row_data in enumerate(result):
						row_no+=1

						self.table.insertRow(row_no)
						for column_no,data in enumerate(row_data):
							self.table.setItem(row_no,column_no,QTableWidgetItem(str(data)))
					row_no=row_no+1
					column_no=0
					self.table.setItem(row_no,column_no,QTableWidgetItem(str('Total')))

			
				
			
					self.table.setItem(row_no,1,QTableWidgetItem(str(sub1total)))
					self.table.setItem(row_no,2,QTableWidgetItem(str(sub2total)))
					self.table.setItem(row_no,3,QTableWidgetItem(str(sub3total)))
					self.table.setItem(row_no,4,QTableWidgetItem(str(sub4total)))
					self.table.setItem(row_no,5,QTableWidgetItem(str(sub5total)))
					self.table.setItem(row_no,6,QTableWidgetItem(str(sub6total)))
					self.stackedWidget.setCurrentIndex(7)
			

	def viewbackbtn(self):

		self.viewback.clicked.connect(self.onviewbackbtn)

	def onviewbackbtn(self):
		self.table.clearContents()
		self.stackedWidget.setCurrentIndex(5)

	def filebtn(self):
		self.file.clicked.connect(self.onfilebtn)

	def onfilebtn(self):

		conn=connect(host='localhost',database='attendance',user='root',password='')
		un=self.usernameview.text()
		path='C:\\Users\\hp\\Desktop\\'+str(un)+'.csv'
		fp1=open(path,mode='w')
		query1='select * from sem4 where dept in(select dept from studentdetails where username=%s)'
		cur=conn.cursor()
		cur.execute(query1,(un,))
		subs=cur.fetchall()
		if un=='adminit' or un=='admincs':
			sub=sub='Username'+','+'Date'+','+str(subs[0][1])+','+str(subs[0][2])+','+str(subs[0][3])+','+str(subs[0][4])+','+str(subs[0][5])+','+str(subs[0][6])
		else:
			sub='Date'+','+str(subs[0][1])+','+str(subs[0][2])+','+str(subs[0][3])+','+str(subs[0][4])+','+str(subs[0][5])+','+str(subs[0][6])
		fp1.write(sub)
		fp1.write('\n')
	

		
		
		
		if un=='adminit' or un=='admincs':
			query='select username,date,sub1,sub2,sub3,sub4,sub5,sub6,sub1lec,sub2lec,sub3lec,sub4lec,sub5lec,sub6lec from attrecord where dept in (select dept from studentdetails where username=%s)order by username'
			cursor=conn.cursor()
			cursor.execute(query,(un,))
			result=cursor.fetchall()
			for lecs in result:
				st=str(lecs[0])+','+str(lecs[1])+','+str(lecs[2])+'::'+str(lecs[8])+','+str(lecs[3])+'::'+str(lecs[9])+','+str(lecs[4])+'::'+str(lecs[10])+','+str(lecs[5])+'::'+str(lecs[11])+','+str(lecs[6])+'::'+str(lecs[12])+','+str(lecs[7])+'::'+str(lecs[13])
				fp1.write(st)
				fp1.write('\n')	
			fp1.close()
			self.showmessagebox('info','file generated')

		else:
			query='select date,sub1,sub2,sub3,sub4,sub5,sub6,sub1lec,sub2lec,sub3lec,sub4lec,sub5lec,sub6lec from attrecord where username=%s'
			cursor=conn.cursor()
			cursor.execute(query,(un,))
			result=cursor.fetchall()
			
		
			sub1total=0
			sub2total=0
			sub3total=0
			sub4total=0
			sub5total=0
			sub6total=0
			sub1l=0
			sub2l=0
			sub3l=0
			sub4l=0
			sub5l=0
			sub6l=0
			for lecs in result:
				sub1total+=lecs[1]
				sub2total+=lecs[2]
				sub3total+=lecs[3]
				sub4total+=lecs[4]
				sub5total+=lecs[5]
				sub6total+=lecs[6]
				sub1l+=lecs[7]
				sub2l+=lecs[8]
				sub3l+=lecs[9]
				sub4l+=lecs[10]
				sub5l+=lecs[11]
				sub6l+=lecs[12]

	
			
			
				st=str(lecs[0])+','+str(lecs[1])+'::'+str(lecs[7])+','+str(lecs[2])+'::'+str(lecs[8])+','+str(lecs[3])+'::'+str(lecs[9])+','+str(lecs[4])+'::'+str(lecs[10])+','+str(lecs[5])+'::'+str(lecs[11])+','+str(lecs[6])+'::'+str(lecs[12])
				fp1.write(st)

	
				fp1.write('\n')
			endline='Total'+','+str(sub1total)+'::'+str(sub1l)+','+str(sub2total)+'::'+str(sub2l)+','+str(sub3total)+'::'+str(sub3l)+','+str(sub4total)+'::'+str(sub4l)+','+str(sub5total)+'::'+str(sub5l)+','+str(sub6total)+'::'+str(sub6l)
			fp1.write(endline)
		

			self.showmessagebox('info','file generated')

			fp1.close()

	def analysisbtn(self):
		self.analysis.clicked.connect(self.onanalysis)
	def onanalysis(self):
		name=self.usernameview.text()
		conn=connect(host='localhost',database='attendance',user='root',password='')
		query1='select * from sem4 where dept in(select dept from studentdetails where username=%s)'
		cur=conn.cursor()
		cur.execute(query1,(name,))
		row1=cur.fetchone()
		subl=[]
		for i in row1:
			subl.append(i)
		if name=='adminit' or name=='admincs':
			query='select * from attrecord where dept in(select dept from studentdetails where username=%s)'
		else:
			query='select * from attrecord where username=%s'
		cursor=conn.cursor()
		cursor.execute(query,(name,))
		result=cursor.fetchall()
		
		sub1total=0
		sub2total=0
		sub3total=0
		sub4total=0
		sub5total=0
		sub6total=0
		sub1l=0
		sub2l=0
		sub3l=0
		sub4l=0
		sub5l=0
		sub6l=0
		for lecs in result:
			sub1total+=lecs[4]
			sub2total+=lecs[5]
			sub3total+=lecs[6]
			sub4total+=lecs[7]
			sub5total+=lecs[8]
			sub6total+=lecs[9]
			sub1l+=lecs[10]
			sub2l+=lecs[11]
			sub3l+=lecs[12]
			sub4l+=lecs[13]
			sub5l+=lecs[14]
			sub6l+=lecs[15]
		subdict={subl[1]:[sub1total,sub1l],subl[2]:[sub2total,sub2l],subl[3]:[sub3total,sub3l],subl[4]:[sub4total,sub4l],subl[5]:[sub5total,sub5l],subl[6]:[sub6total,sub6l]}
		#sublist=[sub1total,sub2total,sub3total,sub4total,sub5total,sub6total,subl]
		d1=DataFrame(subdict,index=['attended','total'])
		d1=d1.transpose()
		d1[['attended','total']].plot(kind='bar')

	
		plt.show()

	def calculatebtn(self):
		self.calculate.clicked.connect(self.oncalculate)

	def oncalculate(self):
		user=self.un.text()
		dept=self.dept_2.text()
		
		self.caluser.setText(user)
		self.deptcal.setText(dept)
		self.stackedWidget.setCurrentIndex(9)

	def backcalbtn(self):
		self.backcal.clicked.connect(self.onbackcalbtn)

	def onbackcalbtn(self):
		self.stackedWidget.setCurrentIndex(5)

	def submitcalbtn(self):
		self.calsubmit.clicked.connect(self.onsubmitcalbtn)

	def onsubmitcalbtn(self):
		datefrom=self.cal1.selectedDate().toPyDate()
		dateto=self.cal2.selectedDate().toPyDate()
		self.fromd.setText(str(datefrom))
		self.tod.setText(str(dateto))
		usr=self.caluser.text()
		dept=self.deptcal.text()
		conn=connect(host='localhost',database='attendance',user='root',password='')
		query='select * from attrecord where date>=%s and date<=%s and username =%s and dept =%s '
		data=(datefrom,dateto,usr,dept)
		cursor=conn.cursor()
		cursor.execute(query,data)
		result=cursor.fetchall()
		
		sub1=0
		sub2=0
		sub3=0
		sub4=0
		sub5=0
		sub6=0
		sub1lec=0
		sub2lec=0
		sub3lec=0
		sub4lec=0
		sub5lec=0
		sub6lec=0
		
		for att in result:
			sub1+=att[4]
			sub2+=att[5]
			sub3+=att[6]
			sub4+=att[7]
			sub5+=att[8]
			sub6+=att[9]
			sub1lec+=att[10]
			sub2lec+=att[11]
			sub3lec+=att[12]
			sub4lec+=att[13]
			sub5lec+=att[14]
			sub6lec+=att[15]
		while sub1lec==0 or sub2lec==0 or sub3lec==0 or sub4lec==0 or sub5lec==0 or sub6lec==0:   #code fr 0 div

			try:
				sub1p=sub1/sub1lec
				self.sub1sh.setText(str(sub1)+'/'+str(sub1lec)+'='+str(round((sub1/sub1lec*100),3)))
				sub2p=sub2/sub2lec
				self.sub2sh.setText(str(sub2)+'/'+str(sub2lec)+'='+str(round((sub2/sub2lec*100),3)))
				sub3p=sub3/sub3lec
				self.sub3sh.setText(str(sub3)+'/'+str(sub3lec)+'='+str(round((sub3/sub3lec*100),3)))
				sub4p=sub4/sub4lec
				self.sub4sh.setText(str(sub4)+'/'+str(sub4lec)+'='+str(round((sub4/sub4lec*100),3)))
				sub5p=sub5/sub5lec
				self.sub5sh.setText(str(sub5)+'/'+str(sub5lec)+'='+str(round((sub5/sub5lec*100),3)))
				sub6p=sub6/sub6lec
				self.sub6sh.setText(str(sub6)+'/'+str(sub6lec)+'='+str(round((sub6/sub6lec*100),3)))
			except:
				if sub1lec==0:
					self.sub1sh.setText(str(sub1)+'/'+str(sub1lec)+'='+'0')
					sub1lec=-1
				if sub2lec==0:
					self.sub2sh.setText(str(sub2)+'/'+str(sub2lec)+'='+'0')
					sub2lec=-1
				if sub3lec==0:
					self.sub3sh.setText(str(sub3)+'/'+str(sub3lec)+'='+'0')
					sub3lec=-1
				if sub4lec==0:
					self.sub4sh.setText(str(sub4)+'/'+str(sub4lec)+'='+'0')
					sub4lec=-1
				if sub5lec==0:
					self.sub5sh.setText(str(sub5)+'/'+str(sub5lec)+'='+'0')
					sub5lec=-1
				if sub6lec==0:
					self.sub6sh.setText(str(sub6)+'/'+str(sub6lec)+'='+'0')
					sub6lec=-1

		if sub1lec>0 and sub2lec>0 and sub3lec>0 and sub4lec>0 and sub5lec>0 and sub6lec>0:
			self.sub1sh.setText(str(sub1)+'/'+str(sub1lec)+'='+str(round((sub1/sub1lec*100),3)))
			self.sub2sh.setText(str(sub2)+'/'+str(sub2lec)+'='+str(round((sub2/sub2lec*100),3)))
			self.sub3sh.setText(str(sub3)+'/'+str(sub3lec)+'='+str(round((sub3/sub3lec*100),3)))
			self.sub4sh.setText(str(sub4)+'/'+str(sub4lec)+'='+str(round((sub4/sub4lec*100),3)))
			self.sub5sh.setText(str(sub5)+'/'+str(sub5lec)+'='+str(round((sub5/sub5lec*100),3)))
			self.sub6sh.setText(str(sub6)+'/'+str(sub6lec)+'='+str(round((sub6/sub6lec*100),3)))
		

        
		avgatt=round((sub1/sub1lec*100),3)+round((sub2/sub2lec*100),3)+round((sub3/sub3lec*100),3)+round((sub4/sub4lec*100),3)+round((sub5/sub5lec*100),3)+round((sub6/sub6lec*100),3)
		avgattd=round((avgatt/6),3)

		self.attcalsh.setText(str(avgattd))

		query1='select * from sem4 where dept=%s'
		cursor.execute(query1,(dept,))
		subs=cursor.fetchone()
		self.sub1s.setText(subs[1])
		self.sub2s.setText(subs[2])
		self.sub3s.setText(subs[3])
		self.sub4s.setText(subs[4])
		self.sub5s.setText(subs[5])
		self.sub6s.setText(subs[6])
		self.attshowname.setText(usr)
		self.attshowdept.setText(dept)


		self.stackedWidget.setCurrentIndex(10)

	def backcalshowbtn(self):
		self.backcalshow.clicked.connect(self.onbackcalshowbtn)

	def onbackcalshowbtn(self):
		self.stackedWidget.setCurrentIndex(5)



		


if __name__=='__main__':
	application=QApplication([])
	
	att=Attendance()
	att.show()

	application.exec_()