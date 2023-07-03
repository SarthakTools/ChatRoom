from tkinter import *
import customtkinter as ct
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.messagebox import askretrycancel, askyesnocancel
import socket
import threading
import os
import time
import random, cProfile

root = ct.CTk()
root.title("ChatRoom")
ct.set_appearance_mode("dark")
ct.set_default_color_theme("themes\\green.json")
bgColor = "black"
root.configure(fg_color=bgColor)

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectToServer():
    try:
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    except:
        server = askretrycancel("Server Offline", "Server is currently offline")
        if server == True:
            connectToServer()
        else:
            quit()

connectToServer()

# Create GUI

avatorFileName = "sources\\loadAvator.txt"
if os.path.exists(avatorFileName):
    pass
else:
    os.makedirs("sources")
    with open(avatorFileName, "x") as f:
        pass

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry(f"700x650+{random.randint(100, 200)}+100")
        self.root.resizable(False, False)
        self.root.configure(fg_color="black")

        self.loginframe = ct.CTkFrame(self.root, fg_color="#333", corner_radius=15)

        self.loginLabel = ct.CTkLabel(self.loginframe, text="Login", font=("game of squids", 50), text_color="white")
        self.loginLabel.pack(side=TOP, pady=30)

        self.usernameInput = ct.CTkEntry(self.loginframe, placeholder_text="Username", font=("consolas", 20), 
                                         height=20, width=450, text_color="cyan", fg_color="#333")
        self.usernameInput.pack(side=TOP, pady=15, ipady=15)

        self.passwordInput = ct.CTkEntry(self.loginframe, placeholder_text="Password", font=("consolas", 20), 
                                         height=20, width=450, text_color="cyan", show="*")
        self.passwordInput.pack(side=TOP, pady=15, ipady=15)

        self.loginBtn = ct.CTkButton(self.loginframe, text="Login", text_color="white", font=("consolas", 25), command=self.destoryLoginPage)
        self.loginBtn.pack(side=TOP, pady=15, ipadx=185, ipady=8)

        self.loginframe.pack(side=TOP, ipady=50, ipadx=50, pady=100, padx=20)

    def destoryLoginPage(self):
        if len(self.usernameInput.get()) > 3:
            if len(self.passwordInput.get()) > 3:
                print("Moving to AvatorPage")
                global guestname
                guestname = self.usernameInput.get()
                self.loginframe.destroy()
                AvatorPage(root)

class AvatorPage:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color="black")
        self.root.geometry("1000x650+500+100")
        self.root.resizable(False, False)
        # All avator images code logic

        self.imgHeight = 180
        self.imgWidth = 180
        self.imgHeightOnHover = 185
        self.imgWidthOnHover = 185
        self.avator1_src = Image.open("images\\avator2.png")
        self.avator1 = ImageTk.PhotoImage(self.avator1_src.resize((self.imgWidth, self.imgHeight)))
        self.avator2_src = Image.open("images\\man.png")
        self.avator2 = ImageTk.PhotoImage(self.avator2_src.resize((self.imgWidth, self.imgHeight)))
        self.avator3_src = Image.open("images\\grownup.png")
        self.avator3 = ImageTk.PhotoImage(self.avator3_src.resize((self.imgWidthOnHover, self.imgHeightOnHover)))
        self.avator4_src = Image.open("images\\womanavt.png")
        self.avator4 = ImageTk.PhotoImage(self.avator4_src.resize((self.imgWidthOnHover, self.imgHeightOnHover)))
        self.avator5_src = Image.open("images\\man3.png")
        self.avator5 = ImageTk.PhotoImage(self.avator5_src.resize((self.imgWidthOnHover, self.imgHeightOnHover)))

        # All avator images code logic ends here
        self.avatorFrame = ct.CTkFrame(self.root, height=500, width=650, fg_color="#222")

        # self.choseAvatorLabel = ct.CTkLabel(self.avatorFrame, text="Select your Avator", font=("consolas", 35), text_color="white")
        # self.choseAvatorLabel.pack(side=TOP, pady=15, anchor="nw", padx=40)

        self.avatorImageButton = ct.CTkFrame(self.avatorFrame, fg_color="#222")
        self.manAvtButton = ct.CTkButton(self.avatorImageButton, text="", image=self.avator1, fg_color="#222", hover_color="#333", 
                                        command=lambda: self.configBtnBgOnClick("images\\avator2.png"))
        self.womanAvtButton = ct.CTkButton(self.avatorImageButton, text="", image=self.avator2, fg_color="#222", hover_color="#333", 
                                        command=lambda: self.configBtnBgOnClick("images\\man.png"))
        self.avator2Img = ct.CTkButton(self.avatorImageButton, text="", image=self.avator3, fg_color="#222", hover_color="#333", 
                                        command=lambda: self.configBtnBgOnClick("images\\grownup.png"))
        self.womanAvtButton3 = ct.CTkButton(self.avatorImageButton, text="", image=self.avator4, fg_color="#222", hover_color="#333", 
                                        command=lambda: self.configBtnBgOnClick("images\\womanavt.png"))
        self.avator3Img = ct.CTkButton(self.avatorImageButton, text="", image=self.avator5, fg_color="#222", hover_color="#333", 
                                        command=lambda: self.configBtnBgOnClick("images\\man3.png"))

        self.manAvtButton.pack(side=LEFT, anchor="ne", padx=15, pady=50)
        self.womanAvtButton.pack(side=LEFT, anchor="ne", padx=15, pady=50)
        self.avator2Img.pack(side=LEFT, anchor="ne", padx=15, pady=50)
        self.womanAvtButton3.pack(side=LEFT, anchor="ne", padx=15, pady=50)
        self.avator3Img.pack(side=LEFT, anchor="ne", padx=15, pady=50)
        self.avatorImageButton.pack(side=TOP, anchor="sw", pady=100, fill=X, ipadx=40)
        self.avatorFrame.pack(side=TOP, fill=BOTH, expand=True, ipadx=300, pady=32, ipady=10)

        self.nextButton = ct.CTkButton(self.root, text="Next", font=("Lucida Console", 20), width=0
                                       ,command=self.getChatApp, state="disabled")
        self.nextButton.pack(side=BOTTOM, anchor="se", pady=15, ipady=15, ipadx=50, padx=25)

    def getChatApp(self):
        self.avatorFrame.destroy()
        self.nextButton.destroy()
        ChatApp(root)
        
    def configBtnBgOnClick(self, filename):
        self.filename = filename
        with open(avatorFileName, "w") as f:
            f.write(self.filename)
            self.nextButton.configure(state="normal")
            print("Written in the file successfully...")

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(True, True)
        self.root.geometry("500x620+450+100")

        # Create a frame to hold the labels
        self.optionFram = Frame(root, bg="black")

        # All imagas for chatfram code

        manIconSrc2 = Image.open("images\\man1.png")
        manIconImage2 = ImageTk.PhotoImage(manIconSrc2.resize((40, 40)))
        submitIconSrc = Image.open("images\\send2.png")
        submitIconImage = ImageTk.PhotoImage(submitIconSrc.resize((40, 40)))
        messageIconSrc = Image.open("images\\message.png")
        messageIconImage = ImageTk.PhotoImage(messageIconSrc.resize((40, 40)))
        chatIconSrc = Image.open("images\\chat.png")
        chatIconImage = ImageTk.PhotoImage(chatIconSrc.resize((35, 35)))

        # All imagas for chatfram code ends here

        self.messageIcon = ct.CTkButton(self.optionFram, text="",image=messageIconImage, width=0, bg_color=bgColor, fg_color=bgColor)
        self.messageIcon.pack(side=RIGHT, anchor="nw", padx=5, pady=5)

        self.manIcon2 = ct.CTkButton(self.optionFram, text="",image=manIconImage2, height=1, width=1, bg_color=bgColor, fg_color=bgColor,
                                corner_radius=20)
        self.manIcon2.pack(side=LEFT, anchor="ne")

        self.username = ct.CTkLabel(self.optionFram, text=guestname, font=("consolas", 20), text_color="#d8d8df")
        self.username.pack(side=LEFT, padx=5, pady=7, anchor="ne")
        self.optionFram.pack(side=TOP, fill=X, anchor="n")

        self.canvasFrame = Frame(root)
        self.canvasFrame.pack(fill=BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvasFrame, bg="black", highlightthickness=0)

        self.label_frame = tk.Frame(self.canvas, bg="black")
        self.label_frame.pack(side="left", fill="both", expand=True)

        self.scrollable_window = self.canvas.create_window((0, 0), window=self.label_frame, anchor="nw")

        # self.emoji_frame = ct.CTkScrollableFrame(self.canvas)
        # self.emoji_frame.pack(side=BOTTOM, anchor="nw")

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label_frame.bind("<Configure>", self.configure_scroll_region)

        self.scrollbar = ct.CTkScrollbar(self.canvas, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.yview_moveto(1.0)

        self.scrollbar.pack(side="right", fill=Y)

        self.canvas.bind("<Configure>", self.resize_frame)
        self.canvas.pack(side=TOP, fill=BOTH)

        bgColorChatFram = "#080420"
        self.chatFram = Frame(root, bg=bgColorChatFram)

        self.chatIcon = ct.CTkButton(self.chatFram, text="",image=chatIconImage, width=20, bg_color=bgColorChatFram, fg_color=bgColorChatFram)
        self.chatIcon.pack(side=LEFT, padx=5)

        self.msgInput = ct.CTkEntry(self.chatFram, placeholder_text="Type your message here...", height=40, font=("consolas", 18))
        self.msgInput.pack(side=LEFT, pady=10, padx=0, fill=X, expand=True)

        self.submitBtn = ct.CTkButton(self.chatFram, text="", image=submitIconImage, bg_color=bgColorChatFram, fg_color=bgColorChatFram, height=40, width=20, hover_color=bgColorChatFram)
        self.submitBtn.pack(side=LEFT, padx=0, pady=8)
        self.submitBtn.configure(command=self.sendMessage)

        self.chatFram.pack(side=BOTTOM, fill=X, ipady=5)

        self.root.bind("<Return>", lambda event: self.sendMessage())
        self.root.protocol("WM_DELETE_WINDOW", self.onWindowClosing)


        with open(avatorFileName, "r") as imageName:
            self.avatorImageFile = imageName.read()

        self.my_avator = self.avatorImageFile

    def configure_scroll_region(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def resize_frame(self, e):
        self.canvas.itemconfigure(self.scrollable_window, width=e.width-30)
        
    def receive_messages(self):
        while True:
            try:
                self.incoming_message_recv = client_socket.recv(1024).decode('utf-8')
                self.ip_address, self.recieved_message = self.incoming_message_recv.split(":")
                self.formatted_message = self.recieved_message.strip()
                if self.incoming_message_recv:
                    self.bot_frame = ct.CTkFrame(self.label_frame, fg_color="black")
                    self.bot_frame.pack(side=TOP, anchor="nw", padx=10)
                    self.bot_image_src = Image.open(self.my_avator)
                    self.bot_image = ImageTk.PhotoImage(self.bot_image_src.resize((40, 40)))
                    self.incoming_message = ct.CTkLabel(self.bot_frame, text=self.formatted_message, font=("Poppins", 14), fg_color="#444", corner_radius=6, wraplength=250)
                    self.incoming_message.pack(side=RIGHT, anchor="ne", padx=10, pady=10, ipady=8, ipadx=10)
                    self.bot_image_label = ct.CTkLabel(self.bot_frame, text="", image=self.bot_image, fg_color="black")
                    self.bot_image_label.pack(side=TOP, pady=13)
                    self.canvas.update_idletasks()
                    self.canvas.yview_moveto(1.0)
                else:
                    print("No clients found")
            except:
                break
        
    def sendMessage(self):
        self.message = self.msgInput.get()
        if self.message:
            self.user_frame = ct.CTkFrame(self.label_frame, fg_color="black")
            self.user_frame.pack(side=TOP, anchor="ne")
            self.user_image_src = Image.open(self.my_avator)
            self.user_image = ImageTk.PhotoImage(self.user_image_src.resize((40, 40)))        
            self.user_label = ct.CTkLabel(self.user_frame, text=self.message, font=("Poppins", 15), fg_color="#419f5b", corner_radius=4, wraplength=250)
            self.user_label.pack(side=LEFT, anchor="nw", pady=10, ipadx=10, ipady=6, padx=10)
            user_image_label = ct.CTkLabel(self.user_frame, text="", image=self.user_image, fg_color="black")
            user_image_label.pack(side=TOP, pady=13)
            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1.0)
            client_socket.send(self.message.encode('utf-8'))
            self.msgInput.delete(0, END)

        # self.receive_thread.start()
        # self.receive_thread = threading.Thread(target=self.receive_messages)
        self.root.after(1, threading.Thread(target=self.receive_messages).start())

    def onWindowClosing(self):
        confirm = askyesnocancel("Chat Room", "Are you sure ???")
        if confirm == True:
            client_socket.close()
            self.root.destroy()
        else:
            pass

LoginPage(root)
# AvatorPage(root)
# ChatApp(root)
cProfile.run("root.mainloop()")