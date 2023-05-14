import sqlite3  
from internet import check_internet_connection 

# Veritabanı bağlantısını oluşturur
def create_connection():
    connection = sqlite3.connect('C:/Users/svimu/Desktop/asistant/memory.db')  
    return connection

# Soruları ve cevapları veritabanından alır
def get_questions_and_answers():
    con = create_connection()  
    cur = con.cursor()  
    cur.execute('SELECT * FROM questionsAndAnswer') 
    return cur.fetchall() 

# Bir soru ve cevabı veritabanına ekler
def insert_question_and_answer(question, answer):
    con = create_connection() 
    cur = con.cursor()  
    query = "INSERT INTO questionsAndAnswer VALUES ('" + question + "', '" + answer + "')"  
    cur.execute(query)  
    con.commit()  



def get_answer_from_memory(question):
    rows = get_questions_and_answers()  
    answer = ""  
    for row in rows:  
        if row[0] in question:  
            answer = row[1] 
            break  
    return answer 

def get_name():
    con = create_connection()  
    cur = con.cursor() 
    query = "SELECT value FROM memory WHERE name = 'assistant_name'"  
    cur.execute(query)  
    return cur.fetchall()[0][0]  

def update_name(new_name):
    con = create_connection() 
    cur = con.cursor()  #
    query = "UPDATE memory SET value = '" + new_name + "' WHERE name = 'assistant_name'" 
    cur.execute(query)  
    con.commit()  # Değişiklikleri veritabanına kaydeder



def update_last_seen(last_seen_date):
    con = create_connection()  
    cur = con.cursor()  
    query = "UPDATE memory SET value = '" + str(last_seen_date) + "' WHERE name = 'last_seen_date'"  
    cur.execute(query) 
    con.commit()  

def get_last_seen():
    con = create_connection() 
    cur = con.cursor()  
    query = "SELECT value FROM memory WHERE name = 'last_seen_date'" 
    cur.execute(query)  
    return str(cur.fetchall()[0][0]) 

def update_last_modify(last_modify):
    con = create_connection()  
    cur = con.cursor()  
    query = "UPDATE memory SET value = '" + str(last_modify) + "' WHERE name = 'last_modify'" 
    cur.execute(query)  
    con.commit() 

def get_last_modify():
    con = create_connection()  
    cur = con.cursor()  
    query = "SELECT value FROM memory WHERE name = 'last_modify'"  
    cur.execute(query)  
    return str(cur.fetchall()[0][0])  



def turn_on_speech():
    if check_internet_connection: 
        con = create_connection()  
        cur = con.cursor()  
        query = "UPDATE memory SET value='on' WHERE name='speech'" 
        cur.execute(query) 
        con.commit() 
        return "Konuşuyorum. "  
    else:
        return "Hey, İnternet bağlatını kontrol et."  

def turn_off_speech():
    con = create_connection()  
    cur = con.cursor() 
    query = "UPDATE memory SET value='off' WHERE name='speech'" 
    cur.execute(query)  
    con.commit()  
    return "Tamamm... "  

def speak_is_on():
    con = create_connection()
    cur = con.cursor()  
    query = "SELECT value FROM memory WHERE name='speech'" 
    cur.execute(query)  
    ans = str(cur.fetchall()[0][0])  
    if ans == "on":
        return True  
    else:
        return False  

def turn_on_listen():
    if check_internet_connection:  
        con = create_connection()  
        cur = con.cursor()  
        query = "UPDATE memory SET value='on' WHERE name='listen'"  
        cur.execute(query) 
        con.commit()  
        return "Dinliyorum..." 
    else:
        return "Hey, İnternet bağlatını kontrol et." 

def turn_off_listen():
    con = create_connection()  
    cur = con.cursor()  
    query = "UPDATE memory SET value='off' WHERE name='listen'" 
    cur.execute(query) 
    con.commit()  
    return "Lütfen talimatları yazın"  

def listen_is_on():
    con = create_connection()  
    cur = con.cursor()  
    query = "SELECT value FROM memory WHERE name='listen'" 
    cur.execute(query)  
    ans = str(cur.fetchall()[0][0])  
    if ans == "on":
        return True 
    else:
        return False  

def get_name_from_memory():
    con = create_connection()  
    cur = con.cursor() 
    cur.execute('SELECT * FROM emailId')  
    return cur.fetchall()  

def insert_emailId(name, emailId):
    con = create_connection()  
    cur = con.cursor() 
    query = "INSERT INTO emailId VALUES ('" + name + "', '" + emailId + "')" 
    cur.execute(query) 
    con.commit()  

def get_emailId(name):
    rows = get_name_from_memory()  
    answer = ""
    for row in rows:
        if row[0] in name: 
            answer = row[1]  
            return answer
    return "0"  


