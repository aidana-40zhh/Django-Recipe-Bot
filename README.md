# 🍳 Recipe Bot (Hybrid Chatbot)

## 1. Project Title and Description
**Recipe Bot** is a hybrid Telegram chatbot designed to automate the search for food recipes by ingredients or categories. 

The main feature of this project is its hybrid architecture (Telegram Interface + Web Admin Panel + Database). All recipes are stored in an SQLite database and managed through the Django web administration panel. The bot also collects user query analytics (message history) and stores them in the database for further analysis.

## 2. Technologies Used
* **Programming Language:** Python 3
* **Web Framework:** Django (ORM, Admin Panel)
* **Telegram API:** pyTelegramBotAPI (Telebot)
* **Database:** SQLite
* **Architecture Type:** Hybrid chatbot (Python + Web + Database)

## 3. Installation Guide
To deploy this project locally, follow these steps:

1. Clone the repository or download the project archive.
2. Open a terminal in the project directory and create a virtual environment:
   ```bash
   python -m venv venv