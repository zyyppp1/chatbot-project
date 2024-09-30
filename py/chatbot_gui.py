import tkinter as tk
from tkinter import scrolledtext
from chatbot_logic import process_input

def send_message():
    user_input = user_input_entry.get()
    response = process_input(user_input)
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    chat_history.insert(tk.END, "Bot: " + response + "\n")
    chat_history.config(state=tk.DISABLED)
    user_input_entry.delete(0, tk.END)

# 创建主窗口
root = tk.Tk()
root.title("Chatbot")

# 创建一个滚动文本区域，用于显示聊天历史
chat_history = scrolledtext.ScrolledText(root, state='disabled', width=70, height=20)
chat_history.grid(row=0, column=0, columnspan=2)

# 创建一个输入框
user_input_entry = tk.Entry(root, width=70)
user_input_entry.grid(row=1, column=0)

# 创建一个发送按钮
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1)

root.mainloop()