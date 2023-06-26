from flask import Flask, render_template, request,url_for,redirect
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import pytesseract
"""image_path = "/Users/raneemmousa/Desktop/chatbottryimage.jpg"  # Replace with the actual path to your image
image = Image.open(image_path)
extracted_text = pytesseract.image_to_string(image)
print(extracted_text)"""

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
app = Flask(__name__,template_folder='templates', static_folder='Static')
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/Abstract")
def Abstract():
    return render_template("/Static/Abstract.html")
@app.route("/frontend")
def frontend():
    return render_template("/Static/frontend.html")

def is_file_empty(file_path):
    return os.stat(file_path).st_size == 0

@app.route("/index",methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    global chat_history
    image = request.files["image"]
    if str(image)!="<FileStorage: '' ('application/octet-stream')>":
        # User input is an image
       
        image_path = "temp_image.jpg"  # Path to temporarily save the uploaded image
        image.save(image_path)


        extracted_text = pytesseract.image_to_string(Image.open(image_path))
        user_input = extracted_text.strip()
       
        chat_history.append({"role": "user", "content": user_input})
        try:
            messages = [
                {"role": "system", "content": "You are a hilarious mathematics and programming tutor and you know nothing about history, humanities, and politics, you help students prepare for exams and give them feedbacks on their weekness points, you help organise their time before exams, you can provide them with questions on their exam topic , and they could provide you their response back and you grade their work and you should dilever answers in a funny way and make your students laugh, you are supposed to assess students in everything related to math like calculus , your name is profbotix so start the conersation with , profbotix is here to help"},
                *chat_history
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            bot_response = response.choices[0].message.content.strip()

            chat_history.append({"role": "assistant", "content": bot_response})

            # Delete image
            os.remove(image_path)
        except is_file_empty(image_path):
            # User inpt is text
            user_input = request.form["message"]

            # Procss uer input as before
            
            chat_history.append({"role": "user", "content": user_input})

            messages = [
                {"role": "system", "content": "You are a hilarious mathematics and programming tutor and you know nothing about history, humanities, and politics, you help students prepare for exams and give them feedbacks on their weekness points, you help organise their time before exams, you can provide them with questions on their exam topic , and they could provide you their response back and you grade their work and you should dilever answers in a funny way and make your students laugh, you are supposed to assess students in everything related to math like calculus , your name is profbotix so start the conersation with , profbotix is here to help"},
                *chat_history
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            bot_response = response.choices[0].message.content.strip()

            chat_history.append({"role": "assistant", "content": bot_response})
   
    if "message" in request.form and not request.files["image"] :
            # User input is text
            user_input = request.form["message"]

            # Processinput 
            
            chat_history.append({"role": "user", "content": user_input})

            messages = [
                {"role": "system", "content": "You are a hilarious mathematics and programming tutor and you know nothing about history, humanities, and politics, you help students prepare for exams and give them feedbacks on their weekness points, you help organise their time before exams, you can provide them with questions on their exam topic , and they could provide you their response back and you grade their work and you should dilever answers in a funny way and make your students laugh, you are supposed to assess students in everything related to math like calculus , your name is profbotix so start the conersation with , profbotix is here to help"},
                *chat_history
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            bot_response = response.choices[0].message.content.strip()

            chat_history.append({"role": "assistant", "content": bot_response})
        
        
    

    return render_template("chatbot.html", user_input=user_input, bot_response=bot_response, chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
