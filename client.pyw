from tkinter import *
import customtkinter as ct
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.messagebox import askretrycancel, askyesnocancel
import socket, threading, string, queue, sys
import os, time, random
from customtkinter import *
from flask import send_from_directory
from regex import T 
from CTkMessagebox import CTkMessagebox

# ===================== CONFIG =====================

SERVER_ADDRESS = "localhost"
SERVER_PORT = 5000
bgColor = "black"

# ===================== RANDOM NAME =====================

# ===================== GUI =====================

ct.set_appearance_mode("dark")
ct.set_default_color_theme("themes\\green.json")

root = ct.CTk()
root.title("ChatRoom")
root.geometry("500x620+450+100")
root.configure(fg_color=bgColor)

# ===================== AVATAR =====================

if not os.path.exists("sources"):
    os.makedirs("sources")

avatar_file = "sources\\loadAvator.txt"
if not os.path.exists(avatar_file):
    with open(avatar_file, "w") as f:
        f.write("avatar\\avatar (1).png")



with open(avatar_file, "r") as f:
    # avatar_path = f.read().strip()
    image = ["avatar\\avatar (1).png", "avatar\\avatar (2).png", "avatar\\avatar (3).png"]
    avatar_path = random.choice(image)

# ===================== CHAT APP =====================

def generate_guestname():
    chars = string.ascii_letters + string.digits
    return "Guest_" + "".join(random.choice(chars) for _ in range(6))

guestname = generate_guestname()

class LoginPage:
    """Typewriter welcome text, then reveal the login UI with a slide animation."""
    def __init__(self, root, text: str = "Welcome to ChatApp", speed: int = 60):
        self.root = root
        self.root.configure(fg_color="black")
        self.root.overrideredirect(False)
        self.root.geometry("1000x600+200+40")
        set_default_color_theme("dark-blue")
        self.root.resizable(False, False)
        self.root.title("Login Page")
        self.text = text
        self.speed = speed
        self.idx = 0

        # white text on black background (no red)
        self.label = CTkLabel(root, text="", font=("monospace", 48, "bold"),
                              text_color="white", fg_color="black")
        self.label.place(relx=0.5, rely=0.20, anchor="center")

        self.root.after(300, self._type)

    def _type(self):
        if self.idx < len(self.text):
            current = self.label.cget("text") + self.text[self.idx]
            self.label.configure(text=current)
            self.idx += 1
            self.root.after(self.speed, self._type)
        else:
            self.root.after(450, self._reveal_login)

    def _reveal_login(self):
        # Keep the welcome title fixed at top, then show staged credential inputs.
        # Don't destroy the label — resize/reposition it to top.
        try:
            self.label.place_configure(relx=0.5, rely=0.12)
            self.label.configure(font=("monospace", 36, "bold"))
        except Exception:
            pass
        # start the email->password staged flow

        flow = EmailPasswordFlow(self.root, title_label=self.label)
        flow.show_email_stage()

class EmailPasswordFlow:
    """Shows an email input stage, then a password stage with sliding animations.
    On password submit it shows a brief progress then opens MainPage.
    """
    def __init__(self, root, title_label: CTkLabel = None):
        self.root = root
        self.title_label = title_label
        self.email_frame = None
        self.password_frame = None
        self.email_var = StringVar()
        self.pass_var = StringVar()

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.eyes_icon_open = ct.CTkImage(Image.open(os.path.join(image_path, "eyes_open.png")), size=(20, 20))
        self.eyes_icon_closed =  ct.CTkImage(Image.open(os.path.join(image_path, "eyes_closed.png")), size=(20, 20))
        # self.gen_image =  ct.CTkImage(Image.open(os.path.join(image_path, "magic-wand.png")), size=(20, 20))
        self.gen_image =  ct.CTkImage(Image.open(os.path.join(image_path, "innovation.png")), size=(32, 32))


    def _slide(self, widget, start_x, end_x, steps=20, delay=12):
        # animate widget's x position (absolute pixels) using place_info
        def step(i):
            if i > steps:
                widget.place_configure(x=end_x)
                return
            x = int(start_x + (end_x - start_x) * (i / steps))
            widget.place_configure(x=x)
            self.root.after(delay, lambda: step(i + 1))

        step(0)

    def show_email_stage(self):
        w = self.root.winfo_width() or 1000
        h = self.root.winfo_height() or 600
        # center position
        cx = int(w / 2)
        cy = int(h * 0.45)

        # desired frame size
        fw = 480
        fh = 160
        Height = 22
        Width = 380

        # create frame for email input (pass width/height to constructor)
        self.email_frame = CTkFrame(self.root, fg_color="#111", corner_radius=12, width=fw, height=fh)

        CTkLabel(self.email_frame, text="Username", font=("monospace", 20, "bold"), text_color="white").pack(pady=(20, 6), anchor="nw", padx=(20, 0))

        self.email_entry = CTkEntry(self.email_frame, placeholder_text="Email or username", font=("monospace", 18, "bold"), 
                                         height=Height, width=Width, text_color="#dedede", fg_color="#0A0A0A", border_width=0, textvariable=self.email_var)
        self.email_entry.pack(padx=20, pady=(4, 4), ipady=10, ipadx=105)

        self.generate_eyes = ct.CTkButton(self.email_frame, text="", image=self.gen_image, width=0, font=("consolas", 100), fg_color="transparent", hover_color="#202124", command=self.generate_guest_name)
        self.generate_eyes.pack(padx=(0, 20), pady=(0, 0), side="right", anchor="e")
        
        self.submit_btn = CTkButton(self.email_frame, text="Next", command=self._on_email_submit, width=0, font=("monospace", 18, "bold"))
        self.submit_btn.pack(pady=(10, 16), ipadx=40, ipady=5)

        start_x = w + 20
        end_x = cx - int(fw / 2)
        place_y = cy - int(fh / 2) - 40
        self.email_frame.place(x=start_x, y=place_y)
        self._slide(self.email_frame, start_x, end_x-80, steps=18, delay=12)

    def _on_email_submit(self):
        email = self.email_var.get().strip()
        if not email:
            CTkMessagebox(title="Error", message="Please enter your email.", icon="cancel")
            return
        # slide email frame left and then show password
        w = self.root.winfo_width() or 1000
        fw = self.email_frame.winfo_width()
        start_x = self.email_frame.winfo_x()
        target_x = -fw - 50
        self._slide(self.email_frame, start_x, target_x, steps=18, delay=12)
        # after slide, create password frame coming from right
        global guestname, user_name
        guestname = email
        user_name = email

        self.root.after(350, self.show_password_stage)

    def show_password_stage(self):
        w = self.root.winfo_width() or 1000
        h = self.root.winfo_height() or 600
        cx = int(w / 2)
        cy = int(h * 0.45)

        # desired frame size
        fw = 480
        fh = 160

        # match email frame styles: same inner entry sizing/padding and submit layout
        Height = 22
        Width = 380

        self.password_frame = CTkFrame(self.root, fg_color="#111", corner_radius=12, width=fw, height=fh)
        CTkLabel(self.password_frame, text="Password", font=("monospace", 20, "bold"), text_color="white").pack(pady=(20, 6), anchor="nw", padx=(20, 0))

        pass_entry = CTkEntry(self.password_frame, textvariable=self.pass_var, placeholder_text="Password",
                              font=("monospace", 18, "bold"), height=Height, width=Width,
                              text_color="#dedede", fg_color="#0A0A0A", border_width=0, show="*")
        pass_entry.pack(padx=20, pady=(4, 4), ipady=10, ipadx=105)


        # show-password checkbox (keep functionality but keep visual spacing compact)
        def toggle_show():
            if pass_entry.cget("show") == "":
                pass_entry.configure(show="*")
                self.icon_eyes.configure(image=self.eyes_icon_closed)
            else:
                pass_entry.configure(show="")
                self.icon_eyes.configure(image=self.eyes_icon_open)
        show_var = BooleanVar(value=False)

        self.icon_eyes = ct.CTkButton(self.password_frame, text="", image=self.eyes_icon_closed, width=0, font=("consolas", 100), fg_color="transparent", hover_color="#202124", command=toggle_show)
        self.icon_eyes.pack(padx=(0, 20), pady=(0, 0), side="right", anchor="e")
        
        self.submit_btn = CTkButton(self.password_frame, text="Next", command=self._on_password_submit, width=0, font=("monospace", 18, "bold"))
        self.submit_btn.pack(pady=(10, 16), ipadx=40, ipady=5)

        start_x = w + 20
        end_x = cx - int(fw / 2)
        place_y = cy - int(fh / 2) - 40
        self.password_frame.place(x=start_x, y=place_y)
        # slide to the same visual final offset as the email stage
        self._slide(self.password_frame, start_x, end_x-80, steps=18, delay=12)

    def _on_password_submit(self):
        self.submit_btn.configure(state="disabled")
        pwd = self.pass_var.get().strip()
        if not pwd:
            CTkMessagebox(title="Error", message="Please enter your password.", icon="cancel")
            return

        # Ensure geometry info is up-to-date
        self.root.update_idletasks()

        # Create four large dots placed bottom-center, blink one-by-one (left->right)
        # We'll use a container so the group stays centered and visible.
        dots_frame = CTkFrame(self.root, fg_color="transparent")
        dots_frame.place(relx=0.5, rely=0.92, anchor="center")
        dots_frame.lift()

        dot_font = ("monospace", 48, "bold")
        dots = []
        for i in range(4):
            lbl = CTkLabel(dots_frame, text="●", font=dot_font, text_color="#4a4a4a", fg_color="transparent")
            lbl.pack(side=LEFT, padx=8)
            dots.append(lbl)

        duration = 5.0  # seconds to run the animation
        start_time = time.time()

        def tick(counter=0):
            elapsed = time.time() - start_time
            if elapsed >= duration:
                # finish: open MainPage
                global user_name
                user_name = self.email_var.get().strip()
                for w in self.root.winfo_children():
                    w.destroy()
                AvatorPage(self.root)
                return

            # determine active dot (0..3) and update visual state
            active = counter % 4
            for idx, d in enumerate(dots):
                if idx == active:
                    d.configure(text="●", text_color="#FFFFFF")
                else:
                    # dim the inactive dots so active one stands out
                    d.configure(text="●", text_color="#4a4a4a")

            # schedule next frame (~350ms for a clear sequential blink)
            self.root.after(350, lambda: tick(counter + 1))

        # start animation loop
        tick(0)

    def generate_guest_name(self):
        new_name = generate_guestname()
        self.email_var.set(new_name)
        self.email_entry.delete(0, END)
        self.email_entry.insert(0, new_name)  # insert into entry for easy copying

class AvatorPage:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color="black")
        self.root.geometry("1000x650+500+100")
        self.root.resizable(False, False)
        set_default_color_theme("dark-blue")

        self.imgSize_big = (400, 400)
        self.imgSize_small = (40, 40)

        self.selected_avatar = None
        self.avatars = []

        # MAIN FRAME
        self.mainFrame = ct.CTkFrame(self.root, fg_color="black")
        self.mainFrame.pack(fill=BOTH, expand=True)

        # ================= BIG AVATAR (TOP CENTER) =================
        self.previewFrame = ct.CTkFrame(self.mainFrame, fg_color="black")
        self.previewFrame.pack(pady=50)

        self.previewLabel = tk.Label(self.previewFrame, bg="black")
        self.previewLabel.pack()

        # container for avatars
        self.avatarBar = ct.CTkFrame(self.mainFrame, fg_color="transparent")
        self.avatarBar.pack(side=BOTTOM, fill=X, padx=70, pady=10)
        self.avatarBar.pack_propagate(False)

        self.avatarBar.configure(width=700, height=60)

        # load avatars 1–10
        for i in range(1, 15):
            img_path = f"avatar\\avatar ({i}).png"

            img = Image.open(img_path)

            # small_img = ImageTk.PhotoImage(img.resize(self.imgSize_small))
            big_img = ImageTk.PhotoImage(img.resize(self.imgSize_big))
            # hover_img = ImageTk.PhotoImage(img.resize((50, 50)))
            # normal_img = ImageTk.PhotoImage(img.resize((40, 40)))
            hover_img = ImageTk.PhotoImage(img.resize((60, 60)))
            normal_img = ImageTk.PhotoImage(img.resize((50, 50)))

            self.avatars.append((normal_img, hover_img, big_img))
            btn = ct.CTkButton(
                self.avatarBar,
                text="",
                image=normal_img,
                fg_color="transparent",
                hover_color="#222", width=70, height=70,
                command=lambda idx=i-1, p=img_path: self.selectAvatar(idx, p)
            )
            btn.pack(side=LEFT, padx=1)
            btn.bind("<Enter>", lambda e, b=btn, i=hover_img: b.configure(image=i))
            btn.bind("<Leave>", lambda e, b=btn, i=normal_img: b.configure(image=i))

        # ================= NEXT BUTTON =================
        self.nextButton = ct.CTkButton(
            self.root,
            text="Next", text_color="white",
            font=("Lucida Console", 18),
            state="disabled",
            command=self.getChatApp)

        self.nextButton.pack(side=BOTTOM, anchor="center", pady=10, padx=10, ipadx=2, ipady=8)

    # ================= SELECT AVATAR =================
    def selectAvatar(self, idx, path):
        self.selected_avatar = path
        img = Image.open(path)

            # small_img = ImageTk.PhotoImage(img.resize(self.imgSize_small))
        big_img = ImageTk.PhotoImage(img.resize(self.imgSize_big))

        # update big preview
        # big_img = self.avatars[idx][1]
        self.previewLabel.configure(image=big_img)
        self.previewLabel.image = big_img

        # enable next
        self.nextButton.configure(state="normal")

        # save
        with open("sources\\avatorFileName.txt", "w") as f:
            f.write(path)

        global avatar_path
        avatar_path = path

    def getChatApp(self):
        self.mainFrame.destroy()
        self.nextButton.destroy()
        ChatApp(self.root)
# ===================== SOCKET =====================

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg_queue = queue.Queue()


def connect():
    try:
        global user_name
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        client_socket.send(guestname.encode("utf-8"))
    except:
        if askretrycancel("Server Offline", "Server is offline"):
            connect()
        else:
            sys.exit()

connect()

# ===================== RECEIVE THREAD (STARTS EARLY) =====================

def socket_listener():
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            msg_queue.put(msg.decode("utf-8"))
        except:
            break

threading.Thread(target=socket_listener, daemon=True).start()

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x620+450+100")

        image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
        avatar_ = os.path.join(os.path.dirname(os.path.relpath(__file__)), "avatar")
        send_image = CTkImage(Image.open(os.path.join(image_path, "send.png")), size=(30, 30))

        top = Frame(root, bg="black")
        top.pack(fill=X, pady=10)

        global avatar_path
        
        icon = CTkImage(Image.open(os.path.join(avatar_, avatar_path.split("\\")[-1])), size=(40, 40))

        self.icon = ct.CTkLabel(top, image=icon, text="")
        self.icon.image = icon
        self.icon.pack(side=LEFT, padx=5)

        global guestname
        ct.CTkLabel(top, text=guestname, font=("consolas", 20)).pack(side=LEFT)

        # ---- Chat area
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.frame = Frame(self.canvas, bg="black")
        self.frame.pack(fill=BOTH, expand=True)

        self.scroll = ct.CTkScrollbar(root, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)

        # 👇 IMPORTANT: store canvas window
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor="nw"
        )

        self.canvas.pack(side=TOP, fill=BOTH, expand=True)
        self.scroll.pack(side=RIGHT, fill=Y)

        # 👇 IMPORTANT: auto-resize frame to canvas width
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width-30))

        # 👇 IMPORTANT: update scroll region
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # # ---- Input
        bottom = CTkFrame(root, fg_color="#222")
        bottom.pack(side=BOTTOM, fill=X, padx=10 , pady=10)

        self.entry = ct.CTkEntry(bottom, placeholder_text="Type message...", font=("Poppins", 18), fg_color="transparent", border_color="#222")
        self.entry.pack(side=LEFT, fill=X, expand=True, padx=10, pady=7)

        CTkButton(bottom, text="", image=send_image, fg_color="transparent", hover_color="#333", width=0, command=lambda : self.send()).pack(side=RIGHT, padx=3)

        self.root.bind("<Return>", lambda e: self.send())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.after(30, self.process_messages)

    # ===================== UI SAFE MESSAGE HANDLER =====================

    def process_messages(self):
        while not msg_queue.empty():
            msg = msg_queue.get()

            message = msg.split("|", 1)[1] if len(msg.split(":", 1)) > 1 else msg
            sender_image = msg.split("|", 1)[0] if len(msg.split(":", 1)) > 1 else sender_image

            frame = ct.CTkFrame(self.frame, fg_color="black")
            frame.pack(anchor="w", padx=10, pady=2, ipady=10)

            time_label = ct.CTkLabel(frame, text=time.strftime("%H:%M"), fg_color="transparent", font=("Poppins", 13), text_color="white")
            time_label.pack(side=TOP, anchor="nw", padx=42)
            
            image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "avatar")
            s_image = CTkImage(Image.open(os.path.join(image_path, sender_image.split("\\")[1])), size=(40, 40))
            sender_icon = ct.CTkLabel(frame, image=s_image, text="",)
            sender_icon.pack(side=LEFT, padx=0, pady=2)

            label = ct.CTkLabel(frame, text=message, fg_color="#2A2C40", corner_radius=6, wraplength=260, font=("Poppins", 20))
            label.pack(padx=10, pady=2, ipady=4, ipadx=5)

            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1.0)

        self.root.after(30, self.process_messages)

    # ===================== SEND =====================

    def send(self):
        msg = self.entry.get().strip()
        if not msg:
            return
        data = f"{avatar_path}|{msg}"

        frame = ct.CTkFrame(self.frame, fg_color="transparent")
        frame.pack(anchor="ne", padx=5, pady=2, ipady=10)

        time_label = ct.CTkLabel(frame, text=time.strftime("%H:%M"), fg_color="transparent", font=("Poppins", 13), text_color="white")
        time_label.pack(side=TOP, anchor="ne", padx=42)
        
        image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "avatar")
        my_image = CTkImage(Image.open(os.path.join(image_path, avatar_path.split("\\")[1])), size=(30, 30))

        my_icon = ct.CTkLabel(frame, image=my_image, text="",)
        my_icon.pack(side=RIGHT, padx=0, pady=2)

        label = ct.CTkLabel(frame, text=msg, fg_color="#3737A4", corner_radius=6, wraplength=260, font=("Poppins", 20))
        label.pack(anchor="e", padx=10, pady=2, ipady=4, ipadx=5)

        client_socket.send(data.encode("utf-8"))
        self.entry.delete(0, END)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def on_close(self):
        # if askyesnocancel("Exit", "Leave chat?"):
        #     client_socket.close()
            # self.root.destroy()
        self.root.destroy()
    
    

# ===================== START =====================

# ChatApp(root)

LoginPage(root)

# AvatorPage(root)

root.mainloop()