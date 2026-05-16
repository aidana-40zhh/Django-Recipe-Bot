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
    btn5 = KeyboardButton("Contact Admin")  
    
    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn4)
    keyboard.add(btn5)

    bot.send_message(
        message.chat.id,
        "Welcome to Recipe Bot! 🍳\nChoose a command from the menu below:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == "Show recipes")
def show_recipes(message):
    try:
        recipes = Recipe.objects.all()
        if recipes.exists():
            markup = InlineKeyboardMarkup()
            for r in recipes:
                
                markup.add(InlineKeyboardButton(f"🍱 {r.name}", callback_data=f"rec_{r.id}"))
            bot.send_message(message.chat.id, "Select a recipe to view details:", reply_markup=markup)
        else:
            
            bot.send_message(message.chat.id, "Error: The recipe database is currently empty.")
    except Exception:
        
        bot.send_message(message.chat.id, "Connection error: Unable to reach the database. Please try again later.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('rec_'))
def handle_recipe_detail(call):
    try:
        recipe_id = call.data.split('_')[1]
        r = Recipe.objects.get(id=recipe_id)
        text = f"📌 Name: {r.name} ({r.time})\n\n"
        text += f"🛒 Ingredients: {r.ingredients}\n\n"
        text += f"📖 Steps:\n{r.steps}"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text)
    except Recipe.DoesNotExist:
        
        bot.send_message(call.message.chat.id, "Error: This recipe no longer exists.")
    except Exception:
        bot.send_message(call.message.chat.id, "Connection error occurred.")

@bot.message_handler(func=lambda message: message.text == "Quick recipes")
def quick_recipes(message):
    try:
        recipes = Recipe.objects.filter(quick=True)
        if recipes.exists():
            text = "Quick recipes (under 10 minutes):\n"
            for r in recipes:
                text += f"⚡ {r.name} ({r.time})\n"
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "No quick recipes found in the database.")
    except Exception:
        bot.send_message(message.chat.id, "Connection error: Database is offline.")

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
    try:
        category_name = call.data.split('_')[1]
        recipes = Recipe.objects.filter(category=category_name)
        
        if recipes.exists():
            text = f"Recipes in '{category_name}':\n\n"
            for r in recipes:
                text += f"🍴 {r.name} ({r.time})\n"
        else:
            text = f"Sorry, no recipes found in '{category_name}'."
            
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text)
    except Exception:
        bot.send_message(call.message.chat.id, "Connection error.")

@bot.message_handler(func=lambda message: message.text == "Search by ingredient")
def ask_for_ingredient(message):
    msg = bot.send_message(message.chat.id, "Enter ingredient (e.g., egg, chicken):")
    bot.register_next_step_handler(msg, process_ingredient_step)

def process_ingredient_step(message):

    if not message.text or message.text.strip() == "":
        bot.send_message(message.chat.id, "Error: Empty input is not allowed. Please enter a valid ingredient.")
        return

    user_text = message.text.strip().lower()
    
    try:
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
    except Exception:
        bot.send_message(message.chat.id, "Connection error: Failed to complete search.")

@bot.message_handler(func=lambda message: message.text == "Contact Admin")
def contact_admin_start(message):
    msg = bot.send_message(message.chat.id, "Please write your message or question for the administrator:")
    bot.register_next_step_handler(msg, process_admin_message)

def process_admin_message(message):
    
    if not message.text or message.text.strip() == "":
        box_msg = bot.send_message(message.chat.id, "Error: Message cannot be empty. Please try again:")
        bot.register_next_step_handler(box_msg, process_admin_message)
        return

    user_text = message.text.strip()
    try:
        UserQuery.objects.create(chat_id=message.chat.id, query_text=f"[FEEDBACK]: {user_text}")
        bot.send_message(message.chat.id, "Thank you! Your message has been sent to the administrator's dashboard.")
    except Exception:
        bot.send_message(message.chat.id, "Connection error: Failed to send message.")

@bot.message_handler(func=lambda message: True)
def handle_any_text(message):
    user_text = message.text.strip().lower() if message.text else ""
    if user_text == "":
        bot.send_message(message.chat.id, "Error: Invalid input.")
        return

    try:
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
            bot.send_message(message.chat.id, "I don't know this command, or no recipes found with this ingredient. Try to use the menu!")
    except Exception:
        bot.send_message(message.chat.id, "Connection error.")

print("Bot is running! Press Ctrl+C to stop.")
bot.infinity_polling()