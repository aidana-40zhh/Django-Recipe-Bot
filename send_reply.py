import telebot
TOKEN = "7949444632:AAHHs5Q2AFQ7a3eGkehgrvyd2U0lqsBz-wQ"
bot = telebot.TeleBot(TOKEN)

user_chat_id = "" 

reply_text = "Здравствуйте! Вы просили добавить рецепт салата — мы это сделали. Приятного аппетита!"

bot.send_message(user_chat_id, reply_text)

print("Сообщение успешно отправлено пользователю!")