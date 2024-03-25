from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import re

import telebot
chat_id=0
# Replace 'YOUR_TOKEN' with your actual bot token obtained from BotFather
TOKEN = '###'

# Initialize the bot
bot = telebot.TeleBot(TOKEN)
key=0
def get_db_connection():
    print("database connecting")
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



@bot.message_handler(commands=['start'])
def handle_start(message):
    print(message)
    bot.reply_to(message, "Hello! I'm a Themis.Are you the one we were looking for \n type secret:")
    print("Chat ID:", message.chat.id)
    global chat_id 

    chat_id = message.chat.id
# @bot.message_handler(commands=['problem'])
# def handle_start(message):

#     bot.reply_to(message, "WORKING TO GIVE YOU PROBLEMS")
#     conn = get_db_connection()
    
#     problem= conn.execute('SELECT id1 , complaint FROM user WHERE your_column < 4 ORDER BY RANDOM() LIMIT 5;',(key,)).fetchone()
    
#     conn.commit()
#     conn.close()
#     print("Chat ID:", message.chat.id)
#     global chat_id 

#     chat_id = message.chat.id

@bot.message_handler(commands=['problem'])
def handle_start(message):
    bot.reply_to(message, "WORKING TO GIVE YOU PROBLEMS")
    conn = get_db_connection()
    
    # Select rows where 'your_column' is less than 4 and limit the result to 5 rows
    problems = conn.execute('SELECT id1, complaint FROM users WHERE count < 4 ORDER BY RANDOM() LIMIT 3;').fetchall()
    #problems = conn.execute('SELECT id1, complaint FROM users ;').fetchall()
    print(problems)
    conn.close()
    
    # Iterate over each row and send the 'id1' and 'complaint' as messages
    for problem in problems:
        id1, complaint = problem
        bot.send_message(chat_id=message.chat.id, text=f"ID: {id1}\nComplaint: {complaint}")

# Start the bot








@bot.message_handler(commands=['advice'])
def handle_start(message):

    bot.reply_to(message, "WORKING TO GIVE YOU PROBLEMS")
    conn = get_db_connection()
    
    problem= conn.execute('SELECT id1 , complaint  FROM user WHERE count < 4  ORDER BY RANDOM() LIMIT 4;',(key,)).fetchone()
    # for i in problem
    conn.commit()

    print("Chat ID:", message.chat.id)
    global chat_id 

    chat_id = message.chat.id

@bot.message_handler(func=lambda message: message.text[0:5]=="help:")
def handle_name(message):
    bot.send_message(chat_id=chat_id,text="getting answers of other students")
    
    conn = get_db_connection()
    helps=conn.execute('SELECT advices from users where id1=?',(message.text[5:],)).fetchone()
    #bot.send_message(chat_id=message.chat.id, text=helps)

    conn.commit()
    conn.close()
    if helps:
        helps_text = helps[0]
        parts = re.split(r'(\d+)', helps_text)  # Split at every occurrence of a numeric digit
        for part in parts:
            bot.send_message(chat_id=message.chat.id, text=part)




@bot.message_handler(func=lambda message: message.text[0:4]=="ans:")
def handle_name(message):
    bot.send_message(chat_id=chat_id,text="giving your  advices in the format ans:[key][advice]")
    answer = message.text[4:]
    count=0
    print(answer)
    # for i in answer:
    #     if type(i)!=int:
    #         break
    #     count=count+1
    # print(answer[count:])
    for i in answer:
        if not isinstance(i, int):
            break
    count += 1
    print(answer[:count])
    print(answer[count:])
    conn = get_db_connection()

    
    update = conn.execute('UPDATE users SET advices = advices ||  ?' ' || ? WHERE id1=?;',(key,answer[count:],answer[:count]))
    increment_stmt = 'UPDATE users SET count = count + 1 WHERE id1=?;'
    conn.execute(increment_stmt,(answer[:count],))    
    conn.commit()
    conn.close()
    
    
    # chat_id = message.chat.id
    #conn = get_db_connection()
    #tasks = conn.execute('SELECT * FROM tasks').fetchall()
    #lawStudents = conn.execute('SELECT * FROM law WHERE key=?',(key,)).fetchone()
    #law=conn.execute('INSERT INTO law VALUES(2,"ADDSF","SDSDF","SDFSD")')
    #conn.execute('INSERT INTO law (key, Name, Year, Organization) VALUES (?, ?, ?, ?)', (3, "ADDSF", "SDSDF", "SDFSD"))
    #conn.commit()
    #print(lawStudents)
    # if lawStudents:
    #     bot.send_message(chat_id=chat_id,text="You are registered")
    # else:
    #     bot.send_message(chat_id=chat_id,text="authentication failed")

    # conn.close()
    # print(key)


@bot.message_handler(func=lambda message: message.text[0:7]=="secret:")
def handle_name(message):
    bot.send_message(chat_id=chat_id,text="entering key: ")
    global key
    key = message.text[7:]
    print(key)
    # chat_id = message.chat.id
    conn = get_db_connection()
    #tasks = conn.execute('SELECT * FROM tasks').fetchall()
    lawStudents = conn.execute('SELECT * FROM law WHERE key=?',(key,)).fetchone()
    #law=conn.execute('INSERT INTO law VALUES(2,"ADDSF","SDSDF","SDFSD")')
    #conn.execute('INSERT INTO law (key, Name, Year, Organization) VALUES (?, ?, ?, ?)', (3, "ADDSF", "SDSDF", "SDFSD"))
    conn.commit()
    print(lawStudents)
    if lawStudents:
        bot.send_message(chat_id=chat_id,text="You are registered")
    else:
        bot.send_message(chat_id=chat_id,text="authentication failed")

    conn.close()
    print(key)
    #user_data[chat_id] = {'name': name}
    #bot.reply_to(message, f"Hi {name}! Now please enter your content.")

@bot.message_handler(func=lambda message: message.text=="content")
def handle_content(message):
    conn = get_db_connection()
    #tasks = conn.execute('SELECT * FROM tasks').fetchall()

    conn.close()

    print("contenting")
    chat_id = message.chat.id
    content = message.text
    user_id = message.from_user.id
    # name = user_data[chat_id]['name']
    
    # # Store name and content in responses dictionary
    # if user_id not in responses:
    #     responses[user_id] = []
    # responses[user_id].append({'name': name, 'content': content})
    
    # Ask for next content
    bot.reply_to(message, "Thanks! Please enter your next content or type /done to finish.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Print the chat ID
    bot.reply_to(message, message.text[0:6])
    bot.send_message(chat_id=chat_id, text="Bot is now running.")


# Define a command handler for the '/start' command
#bot.send_message(chat_id="YOUR_CHAT_ID", text="Bot is now running.")

# Define a message handler for normal messages
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)
print("hi")
# Start the bot
bot.polling()
