from turtle import st
from unicodedata import name

from numpy import save
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mysql.connector
import json
import re
import secrets
import json
import smtplib

from fastapi.middleware.cors import CORSMiddleware
origins = ['*']



app = FastAPI(
    title="RETANTIVE API",
    description="Having the right-minded people in your team always reflects the company culture and values. So retaining those loyal people are also crucial for organizational improvement",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#user authentication

# app = FastAPI()
class Item(BaseModel):
    id: str
    value: str



# model 
class Message(BaseModel):
    message: str

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check(email):
    if(re.fullmatch(regex, email)):
        return "Valid Email"
    else:
        return "Invalid Email"


@app.get(
    "/user_creation/",
    tags=["user"],
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                                "fullname": "John doe",
                                "email": "John@gmail.com",
                                "EmployeeId": "451",
                                "Department": "information technology",
                                "Designation": "software developer",
                                "DOJ": "1655278054",
                                "password": "John@12",
                                "message": "All detail recorded successfully"
                                }
                }
            },
        },
    },
)

async def read_item(Fullname: str,EmployeeId:str,Department:str,Designation:str,timeslot:str,password:str,email:str):
    
    # if check(Email)=='Valid Email': 
    
    generated_key = secrets.token_urlsafe(20)
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tgtech@1234"
    )
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tgtech@1234",
    database="hrbot"
    )

    #cursor
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM users")
    myresult = mycursor.fetchall()

    #insert data into table

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("retentive.hrm@gmail.com", "hrtrqpxfqjyyklld")

    subject = "Welcome to Retentive - Registration Successful."
    body = f"Hi {Fullname},\nThank you for registering and becoming a part of Retentive HR.\n\nWe will guide you through certain activities and events daily. Hope we will help you to make your work days enjoyable.\n\nThanks & Regards\nTeam Retentive HR\n"
    message="Subject:{}\n\n{}".format(subject,body)
    s.sendmail("retentive.hrm@gmail.com", email,message)
    s.quit()
    sql = "INSERT INTO users (Fullname, EmployeeId,Department,Designation,timeslot,password,email) VALUES (%s, %s,%s,%s, %s,%s,%s)"
    val = (Fullname,EmployeeId,Department,Designation,timeslot,password,email)
    mycursor.execute(sql, val)

    mydb.commit()

    return JSONResponse(status_code=200, content={"fullname": Fullname,"EmployeeId":EmployeeId,"Department":Department,"Designation":Designation,"timeslot":timeslot,"password":password,"email":email,"message":"All detail recorded successfully"})
   

@app.get(
    "/login/",
    tags=["user"],
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": { "message":"you are successfully logedin" }
                }
            },
        },
    },
)
async def read_item(EmployeeId:str,password:str):  
    mydb = mysql.connector.connect( 
    host="localhost",
    user="root",
    password="Tgtech@1234"
    )
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tgtech@1234",
    database="hrbot"
    )

    #cursor
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM users")
    myresult = mycursor.fetchall()
    for i in range(len(myresult)):
        try:
            while EmployeeId==myresult[i][2] and password==myresult[i][-3]:
                return JSONResponse(status_code=200, content={"message":"you are successfully logedin","fullname":myresult[i][1],"EmployeeID":myresult[i][2],"email":myresult[i][-1]})
        except:
            return JSONResponse(status_code=404, content={"message":"enter correct details","err":i})

    





#end of authentication Api 


@app.get(
    "/get_users/",
    tags=["user"],
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                                'user': ['Nitesh kanojia', 'sneha', 'milind', 'brahma'],
                                'employee Id': ['451', '784', '789', '786']
                                
                                }
                }
            },
        },
    },
)

async def users():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tgtech@1234"
    )

    # print(mydb)

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tgtech@1234",
    database="hrbot"
    )

    #cursor
    mycursor = mydb.cursor()
    mycursor.execute("Show tables;")

    myresult = mycursor.fetchall()
    tables=[]
    ulist=[]
    elist=[]
    tlist=[]
    emlist=[]
    for x in myresult:
        tables.append(x)
    mycursor.execute(f"SELECT * FROM users")
    myresult = mycursor.fetchall()
    for i in range(len(myresult)):
        ulist.append(myresult[i][1])
        elist.append(myresult[i][2])
        tlist.append(myresult[i][-2])
        emlist.append(myresult[i][-1])
    return JSONResponse(status_code=200, content={"user":ulist,"employeeId":elist, "time":tlist,"email":emlist})
    

##############################################################################
# satisfaction survey
##############################################################################
abc=[]


#conn string


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tgtech@1234")

# print(mydb)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tgtech@1234",
  database="hrbot")

#cursor
mycursor = mydb.cursor()
mycursor.execute("Show tables;")
 
myresult = mycursor.fetchall()
tables=[] 
for x in myresult:
    tables.append(x)

class satisfactionidgen(BaseModel):
    qid: str
    question:str
    batch:str
    designation:str
    name:str
    uid:str
    code:str


@app.get(
    "/satisfaction_id_gen/{pos}",
    tags=["satisfaction survey"],
    response_model=satisfactionidgen,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                                "qid": "1",
                                "question": "How satisfied are you with the access to the equipment necessary for performing your tasks",
                                "batch": "1",
                                "designation": "data analyst",
                                "name": "nitesh",
                                "uid": "87851202"
                                }
                }
            },
        },
    },
)

# fubnction for satisfaction
async def satisfactiongen(posibility: str,batch:int,designation:str,name:str,uid:str):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tgtech@1234"
    )

    # print(mydb)

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tgtech@1234",
    database="hrbot"
    )

    #cursor
    mycursor = mydb.cursor()
    mycursor.execute("Show tables;")
    
    myresult = mycursor.fetchall()
    tables=[] 
    for x in myresult:
        tables.append(x)
    mycursor.execute(f"SELECT * FROM hrbot.satisfactionqn where question not in ( select question from hrbot.feedback where uid={uid}) ORDER BY RAND() LIMIT 20;")
    myresult = mycursor.fetchall()

    fdkq=[]
    code=[]
    for x in myresult:
        fdkq.append(list(x))
    designations=designation
    batchs=batch
    dfdkq=[]
    dfdkc=[]
    for item in fdkq:
        dfdkq.append(item[1])
        dfdkc.append(item[2])
        code.append(item[6])

    # using list comprehension
    n = 4
    fdk1 = [dfdkq[0:96][i:i + n] for i in range(0, len(dfdkq[0:96]), n)]
    fdk2=[dfdkc[0:96][i:i + n] for i in range(0, len(dfdkc[0:96]), n)] 
    fdk3= [code[0:96][i:i + n] for i in range(0, len(code[0:96]), n)]
    fdk1.insert(0,[])
    fdk3.insert(0,[]) 
    if posibility == "yes":
        res="Please choose from the below activity. Let's go for it:"
        qn=fdk1[batchs][0]
        fdk3=fdk3[batchs][0]  
        dictionary ={"qid": 1, "question":qn,"batch":batchs,"designation":designations,"name":name,"uid":uid,"code":fdk3}
        json_object = json.dumps(dictionary, indent = 4)
        with open(f"{uid}stbk.json", "w") as outfile:
            outfile.write(json_object)
        return {"qid": 1, "question":qn,"batch":batchs,"designation":designations,"name":name,"uid":uid,"code":fdk3}
    if posibility == "no":
        res="Please provide you avilibility"
        return {"qid": "", "value": res,"question":"","batch":batchs,"designation":designations,"name":name,"uid":uid,"code":fdk3}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})



class satisfactionqstn(BaseModel):
    nxtid: str
    quote: str
    question:str
    batch:str
    designation:str
    name:str
    uid:str
    code:str

@app.get(
    "/feedback_question/{qid}/{answer}",
    tags=["360 feedback"],
    response_model=satisfactionqstn,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def feedbacktest(qid:str,answer:str,uid:str):
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tgtech@1234"
        )


        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tgtech@1234",
        database="hrbot"
        )

        #cursor
        mycursor = mydb.cursor()
        mycursor.execute("Show tables;")
        
        myresult = mycursor.fetchall()
        tables=[] 
        for x in myresult:
            tables.append(x)
        mycursor.execute(f" SELECT * FROM hrbot.satisfactionqn where question not in ( select question from hrbot.feedback where uid={uid}) ORDER BY RAND() LIMIT 20;")
        myresult = mycursor.fetchall()
        # Opening JSON file
        with open(f'{uid}stbk.json', 'r') as openfile:
        
            # Reading from json file
            json_object = json.load(openfile)
        qstn=json_object['question']
        batchsz=json_object['batch']
        dsgn=json_object['designation']
        nme=json_object['name']
        designations=dsgn
        batchs=batchsz
        fdkq=[]
        code=[]
        dfdkq=[]
        dfdkc=[]
        for x in myresult:
            fdkq.append(list(x))
        
        for item in fdkq:
            dfdkq.append(item[1])
            dfdkc.append(item[2])
            code.append(item[6])
        # using list comprehension
        n = 4
        fdk1 = [dfdkq[0:96][i:i + n] for i in range(0, len(dfdkq[0:96]), n)]
        fdk2=[dfdkc[0:96][i:i + n] for i in range(0, len(dfdkc[0:96]), n)] 
        fdk3= [code[0:96][i:i + n] for i in range(0, len(code[0:96]), n)]
        fdk1.insert(0,[])
        fdk3.insert(0,[])  
        print(fdk1[1][1])
        def insrtqr(txtques):
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tgtech@1234",
            database="hrbot"
            )
            mycursor = mydb.cursor()
            sql = "INSERT INTO feedback (name,question,answer,uid) VALUES (%s, %s,%s,%s)"
            val = (nme,txtques,answers,uid)
            mycursor.execute(sql, val)
            mydb.commit()


        def nxtQue(qid):
            try:
                nxtque=int(qid)
                if(nxtque==1):
                    txtques=fdk3[batchs][0]
                    coding=fdk3[batchs][0]
                    insrtqr(qstn)
                elif(nxtque==2):
                    txtques=f"{fdk1[batchs][1]}"
                    coding=fdk3[batchs][1]
                    insrtqr(txtques)
                elif(nxtque==3):
                    txtques=f"{fdk1[batchs][2]}"
                    coding=fdk3[batchs][2]
                    insrtqr(txtques)
                elif(nxtque==4):
                    txtques=f"{fdk1[batchs][3]}"
                    coding=fdk3[batchs][3]
                    insrtqr(txtques)
                else:
                    txtques=f"question out of range"
                    coding="false"
                return txtques,coding
            except:
                txtques=f"question out of range"
                coding="false"
                return txtques,coding
        answers=answer
        
        quee=int(qid)
        if(answers==""):
            txtwarn="Please select appropriate"
    
        else:
            # mydb = mysql.connector.connect(
            # host="localhost",
            # user="root",
            # password="Tgtech@1234",
            # database="hrbot"
            # )
            # mycursor = mydb.cursor()
            # sql = "INSERT INTO feedback (name,question,answer,uid) VALUES (%s, %s,%s,%s)"
            txtnxtvalue=nxtQue(qid) 
            print("question",txtnxtvalue[0])
            # val = (nme,txtnxtvalue[0],answers,uid)
            # mycursor.execute(sql, val)
            # mydb.commit()

            txtwarn="This is your question...."
            
            
        return {"nxtid":quee+1,"quote":txtwarn,"question":txtnxtvalue[0],"batch":batchsz,"designation":dsgn,"name":nme,"uid":uid,"code":txtnxtvalue[1]}
    except:
        return JSONResponse(status_code=404, content={"message":"somwthing went wrong!"})



class updateshecdule(BaseModel):
    uid:str
    msg:str
    name:str
    email:str
@app.get(
    "/update_shecdule/{qid}/{answer}",
    tags=["update_shecdule"],
    response_model=updateshecdule,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def updatetime(msg:str,uid:str,name:str,email:str):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tgtech@1234",
        database="hrbot")

    mycursor = mydb.cursor()

    sql = f"UPDATE users SET timeslot = '{msg}' WHERE EmployeeId ='{uid}'"

    mycursor.execute(sql)

    mydb.commit()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("retentive.hrm@gmail.com", "hrtrqpxfqjyyklld")

    subject = f"Rescheduling Successful @{msg}."
    body = f"Hi {name},\n\nThank you for rescheduling your slot. Please use the below link:\nhttp://www.thinkgestalt.com/\n\nPlease make sure you complete your daily grind before your closing time.\n\nGreetings and best wishes for the day ahead!\n\nThanks & Regards\nTeam Retentive HR\n"
    message="Subject:{}\n\n{}".format(subject,body)
    s.sendmail("retentive.hrm@gmail.com", email,message)
    s.quit()
    return JSONResponse(status_code=200, content={"empid":uid,"message":msg,"name":name,"email":email})


    #save responses to database




# class save_responses(BaseModel):
#     uid:str
#     qid:str
#     msg:str
# @app.get(
#     "/save_responses/{qid}/{answer}",
#     tags=["save_responses"],
#     response_model=save_responses,
#     responses={
#         404: {"model": Message, "description": "The item was not found"},
#         200: {
#             "description": "Item requested by ID",
#             "content": {
#                 "application/json": {
#                     "example": {"id": "bar", "value": "The bar tenders"}
#                 }
#             },
#         },
#     },
# )
# # async def save_responses(name:str,uid:str,msg:str,quid:str):
# #     mydb = mysql.connector.connect(
# #     host="localhost",
# #     user="root",
# #     password="Tgtech@1234",
# #     database="hrbot"
# #     )
# #     mycursor = mydb.cursor()
# #     sql = "INSERT INTO feedback (name,question,answer,uid) VALUES (%s, %s,%s,%s)"
# #     val = (name,quid,msg,uid)
# #     mycursor.execute(sql, val)
# #     mydb.commit()



    
