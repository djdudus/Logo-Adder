import os
from tkinter import ttk, filedialog
import tkinter as tk
from PIL import Image


def remove_background(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if (
            item[0] > 135 and item[1] > 135 and item[2] > 135
        ):  # Sprawdzanie białych pikseli
            new_data.append((255, 255, 255, 0))  # Ustawienie piksela na przezroczysty
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def select_destination_directory():
    root.dest_dir = filedialog.askdirectory(
        initialdir="", title="Wybierz folder docelowy"
    )
    ttk.Label(frm, text=f"folder docelowy: {root.dest_dir}").grid(column=1, row=2)


def select_directory():
    root.srcFileName = filedialog.askdirectory(initialdir="", title="Wybierz folder")
    ttk.Label(frm, text=f"folder źródłowy: {root.srcFileName}").grid(column=1, row=1)


def select_logo():
    root.filename = filedialog.askopenfilename(
        initialdir="",
        title="Wybierz plik z logo",
        filetypes=(("Pliki png", "*.png"), ("Wszystkie pliki", "*.*")),
    )
    ttk.Label(frm, text=f"logo: {root.filename}").grid(column=1, row=3)


def add_logo():
    try:
        size = (int(width_var.get()), int(height_var.get()))

        # Sprawdzanie, czy folder źródłowy, folder docelowy i plik z logo zostały wybrane
        if (
            not hasattr(root, "srcFileName")
            or not hasattr(root, "dest_dir")
            or not hasattr(root, "filename")
        ):
            raise ValueError("Nie wybrano wszystkich wymaganych plików/folderów.")

        width, height = size
        logo_size = (
            int(size[0] // 4.5),
            size[1] // 10,
        )  # dostosowanie rozmiaru logo do procentowej wartości
        src_dir = root.srcFileName
        dest_dir = root.dest_dir
        logo_file = root.filename
        os.makedirs(dest_dir, exist_ok=True)

        logo_image = Image.open(logo_file, "r").convert("RGBA").resize(logo_size)

        # usunięcie tła
        if remove_bg_var.get():
            # Tworzenie obrazu bez tła na podstawie kanału alpha
            logo_image = remove_background(logo_image)

        logo_width, logo_height = logo_image.size
        os.makedirs(f"{src_dir}zdjeciazlogo", exist_ok=True)
        for filename in os.listdir(src_dir):
            try:
                if not (filename.endswith(".png") or filename.endswith(".jpg")):
                    # funkcja pomija pliki o rozszerzeniach innych niż .png i .jpg
                    continue
                background = (
                    Image.open(os.path.join(src_dir, filename), "r")
                    .convert("RGBA")
                    .resize(size, Image.LANCZOS)
                )
                text_img = Image.new("RGBA", background.size, (0, 0, 0, 0))
                text_img.paste(background, (0, 0))
                text_img.paste(
                    logo_image,
                    (width - logo_width - 15, height - logo_height - 10),
                    logo_image,
                )
                output_filename = f"{os.path.splitext(filename)[0]}_logo.webp"
                text_img.save(
                    os.path.join(dest_dir, output_filename),
                    format="webp",
                    optimize=True,
                    quality=int(quality_scale.get()),
                )
            except Exception as e:
                ttk.Label(
                    frm,
                    text=f"Błąd przy przetwarzaniu {filename}: {e}",
                    foreground="red",
                ).grid(column=1, row=10 + i)
            i += 1
    except ValueError as e:
        ttk.Label(frm, text=f"Błąd: {e}", foreground="red").grid(column=1, row=9)


root = tk.Tk()
frm = ttk.Frame(root, padding="20p", width="600p", height="300p")
frm.grid()
ttk.Button(frm, text="Wyjdź", command=root.quit).grid(column=1, row=8)
ttk.Button(frm, text="Wybierz folder ze zdjęciami", command=select_directory).grid(
    column=0, row=1
)
ttk.Button(frm, text="Wybierz plik z logo", command=select_logo).grid(column=0, row=3)
ttk.Button(
    frm, text="Wybierz folder docelowy", command=select_destination_directory
).grid(column=0, row=2)
ttk.Button(frm, text="dodaj logo", command=add_logo).grid(column=0, row=8)
# ustawianie docelowej szerokości i wysokości zdjęcia
ttk.Label(frm, text="Szerokość:").grid(column=0, row=4)
width_var = tk.StringVar(value="640")  # wartość domyślna
width_entry = ttk.Entry(frm, textvariable=width_var).grid(column=1, row=4)

ttk.Label(frm, text="Wysokość:").grid(column=0, row=5)
height_var = tk.StringVar(value="427")  # wartość domyślna
height_entry = ttk.Entry(frm, textvariable=height_var).grid(column=1, row=5)

# suwak do ustawienia jakości
ttk.Label(frm, text="Jakość:").grid(column=0, row=6)
quality_scale = tk.Scale(frm, from_=1, to_=100, orient=tk.HORIZONTAL)
quality_scale.set(85)  # wartość domyślna
quality_scale.grid(column=1, row=6)
# checkbox do usunięcia tła
remove_bg_var = tk.BooleanVar()
remove_bg_check = ttk.Checkbutton(frm, text="Usuń tło z logo", variable=remove_bg_var)
remove_bg_check.grid(column=0, row=7)


root.mainloop()
