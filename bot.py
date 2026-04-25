import os
import django
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from recipes.models import Recipe, UserQuery

TOKEN = "7949444632:AAHHs5Q2AFQ7a3eGkehgrvyd2U0lqsBz-wQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn1 = KeyboardButton("Show recipes")
    btn2 = KeyboardButton("Categories")
    btn3 = KeyboardButton("Quick recipes")
    btn4 = KeyboardButton("Search by ingredient")
    
    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Welcome to Recipe Bot! 🍳\nChoose a command from the menu below:",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: message.text == "Show recipes")
def show_recipes(message):
    recipes = Recipe.objects.all()
    if recipes.exists():
        text = "Recipes in the database:\n"
        for r in recipes:
            text += f"- {r.name} ({r.time})\n"
    else:
        text = "The database is empty."
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "Quick recipes")
def quick_recipes(message):
    recipes = Recipe.objects.filter(quick=True)
    if recipes.exists():
        text = "Quick recipes (under 10 minutes):\n"
        for r in recipes:
            text += f"⚡ {r.name} ({r.time})\n"
    else:
        text = "No quick recipes found."
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "Categories")
def show_categories(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🥐 Breakfast", callback_data="cat_Breakfast")
    btn2 = InlineKeyboardButton("🍲 Soup", callback_data="cat_Soup")
    btn3 = InlineKeyboardButton("🍝 Main Course", callback_data="cat_Main")
    btn4 = InlineKeyboardButton("🥗 Salad", callback_data="cat_Salad")
    btn5 = InlineKeyboardButton("🍰 Dessert", callback_data="cat_Dessert")
    btn6 = InlineKeyboardButton("🥪 Snack", callback_data="cat_Snack")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    bot.send_message(message.chat.id, "Choose a category:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def handle_category(call):
    category_name = call.data.split('_')[1]
    recipes = Recipe.objects.filter(category=category_name)
    
    if recipes.exists():
        text = f"Recipes in '{category_name}':\n\n"
        for r in recipes:
            text += f"🍳 {r.name} ({r.time})\n"
    else:
        text = f"Sorry, no recipes found in '{category_name}'."
        
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "Search by ingredient")
def ask_for_ingredient(message):
    msg = bot.send_message(message.chat.id, "Enter ingredient (e.g., egg, chicken):")
    bot.register_next_step_handler(msg, process_ingredient_step)

def process_ingredient_step(message):
    user_text = message.text.lower()
    
    
    UserQuery.objects.create(chat_id=message.chat.id, query_text=user_text)
    
    recipes = Recipe.objects.filter(ingredients__icontains=user_text)
    
    if recipes.exists():
        text = f"Found {recipes.count()} recipes with '{user_text}':\n\n"
        for r in recipes:
            text += f"📌 Name: {r.name} ({r.time})\n"
            text += f"🛒 Ingredients: {r.ingredients}\n"
            text += f"📖 Steps:\n{r.steps}\n\n"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, f"No recipes found with '{user_text}'.")

@bot.message_handler(func=lambda message: True)
def handle_any_text(message):
    user_text = message.text.lower()
    
    
    UserQuery.objects.create(chat_id=message.chat.id, query_text=user_text)
    
    recipes = Recipe.objects.filter(ingredients__icontains=user_text)
    
    if recipes.exists():
        text = f"Found {recipes.count()} recipes with '{user_text}':\n\n"
        for r in recipes:
            text += f"📌 Name: {r.name} ({r.time})\n"
            text += f"🛒 Ingredients: {r.ingredients}\n"
            text += f"📖 Steps:\n{r.steps}\n\n"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, f"I don't know this command, or no recipes found with '{user_text}'. Try to use the menu!")

print("Bot is running! Press Ctrl+C to stop.")
bot.infinity_polling()