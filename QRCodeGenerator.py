import customtkinter as ctk
import qrcode
from PIL import Image
from tkinter import filedialog
import os

# App style
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

logo_path = None
qr_img = None

# 25 color presets
colors = [
"black","white","gray","silver",
"red","crimson","firebrick","darkred",
"blue","navy","royalblue","skyblue",
"green","limegreen","forestgreen",
"orange","darkorange","gold",
"yellow","khaki",
"purple","indigo","violet",
"pink","deeppink"
]

def choose_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(
        filetypes=[("Images","*.png *.jpg *.jpeg")]
    )
    if logo_path:
        logo_label.configure(text=os.path.basename(logo_path))

def generate_qr():

    global qr_img

    data = entry.get()

    if data == "":
        status.configure(text="Enter a link or text first")
        return

    qr_color = qr_color_menu.get()
    bg_color = bg_color_menu.get()

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color=qr_color,
        back_color=bg_color
    ).convert("RGB")

    if logo_path:

        logo = Image.open(logo_path)

        qr_width, qr_height = qr_img.size

        logo_size = qr_width // 4

        logo = logo.resize((logo_size, logo_size))

        pos = (
            (qr_width - logo_size) // 2,
            (qr_height - logo_size) // 2
        )

        qr_img.paste(logo, pos)

    qr_img.show()

    status.configure(text="QR generated successfully")

def save_qr():

    global qr_img

    if qr_img:

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG","*.png")]
        )

        if path:
            qr_img.save(path)
            status.configure(text="QR saved successfully")

app = ctk.CTk()

app.geometry("520x560")

app.title("Advanced QR Code Generator")

title = ctk.CTkLabel(
    app,
    text="QR Code Generator",
    font=("Arial",30)
)

title.pack(pady=20)

entry = ctk.CTkEntry(
    app,
    width=380,
    placeholder_text="Enter link or text"
)

entry.pack(pady=10)

qr_color_label = ctk.CTkLabel(app,text="QR Color")
qr_color_label.pack()

qr_color_menu = ctk.CTkOptionMenu(
    app,
    values=colors
)

qr_color_menu.set("black")
qr_color_menu.pack(pady=5)

bg_color_label = ctk.CTkLabel(app,text="Background Color")
bg_color_label.pack()

bg_color_menu = ctk.CTkOptionMenu(
    app,
    values=colors
)

bg_color_menu.set("white")
bg_color_menu.pack(pady=5)

logo_button = ctk.CTkButton(
    app,
    text="Add Logo Image",
    command=choose_logo
)

logo_button.pack(pady=12)

logo_label = ctk.CTkLabel(
    app,
    text="No logo selected"
)

logo_label.pack()

generate_button = ctk.CTkButton(
    app,
    text="Generate QR Code",
    command=generate_qr
)

generate_button.pack(pady=18)

save_button = ctk.CTkButton(
    app,
    text="Save QR Code",
    command=save_qr
)

save_button.pack(pady=8)

status = ctk.CTkLabel(
    app,
    text=""
)

status.pack(pady=10)

app.mainloop()