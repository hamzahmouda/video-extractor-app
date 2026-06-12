import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from extractor.youtube_extractor import extract_video_info
from excel.excel_writer import save_to_excel
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser


FILE_PATH = "data/videos.xlsx"


# ✅ Ajouter vidéo
def add_video():
    url = entry.get()

    if not url:
        messagebox.showwarning("⚠️ Erreur", "Veuillez entrer un lien")
        return

    try:
        data = extract_video_info(url)
        save_to_excel(data)

        load_table()
        entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("❌ Erreur", str(e))

def open_video():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("⚠️", "Sélectionnez une ligne")
        return

    try:
        df = pd.read_excel(FILE_PATH)
        index = table.index(selected)
        row = df.iloc[index]

        url = row.get("URL", "")

        if not url:
            messagebox.showerror("Erreur", "Aucune URL trouvée")
            return

        webbrowser.open(url)

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# ✅ Charger tableau
def load_table():
    for row in table.get_children():
        table.delete(row)

    try:
        df = pd.read_excel(FILE_PATH)

        for _, row in df.iterrows():
            description = "" if pd.isna(row.get('Description')) else str(row['Description'])
            short_desc = description[:50] + "..." if len(description) > 50 else description

            table.insert("", tk.END, values=(
                row.get("Titre"),
                row.get("Durée"),
                row.get("Chaîne"),
                row.get("Date"),
                row.get("Vues"),
                short_desc
            ))

    except:
        pass

def load_thumbnail(url):
    try:
        response = requests.get(url)
        img_data = response.content

        image = Image.open(BytesIO(img_data))
        image = image.resize((320, 180))  # taille thumbnail

        return ImageTk.PhotoImage(image)

    except:
        return None


# ✅ Recherche (corrigée)
def search():
    keyword = search_entry.get().lower()

    for row in table.get_children():
        table.delete(row)

    try:
        df = pd.read_excel(FILE_PATH)

        filtered = df[df.apply(lambda r: keyword in str(r.values).lower(), axis=1)]

        for _, row in filtered.iterrows():
            description = "" if pd.isna(row.get('Description')) else str(row['Description'])
            short_desc = description[:50] + "..." if len(description) > 50 else description

            table.insert("", tk.END, values=(
                row.get("Titre"),
                row.get("Durée"),
                row.get("Chaîne"),
                row.get("Date"),
                row.get("Vues"),
                short_desc
            ))

    except Exception as e:
        messagebox.showerror("❌ Erreur", str(e))


# ✅ Supprimer ligne
def delete_selected():
    selected_item = table.selection()

    if not selected_item:
        messagebox.showwarning("⚠️", "Sélectionnez une ligne")
        return

    confirm = messagebox.askyesno("Confirmation", "Supprimer cette ligne ?")
    if not confirm:
        return

    try:
        df = pd.read_excel(FILE_PATH)

        index = table.index(selected_item)
        df = df.drop(index=index).reset_index(drop=True)

        df.to_excel(FILE_PATH, index=False)

        load_table()

    except Exception as e:
        messagebox.showerror("❌ Erreur", str(e))


# ✅ Double clic → détails complets
def show_details(event):
    selected = table.selection()
    if not selected:
        return

    try:
        df = pd.read_excel(FILE_PATH)
        index = table.index(selected)
        row = df.iloc[index]

        titre = row.get("Titre", "")
        chaine = row.get("Chaîne", "")
        duree = row.get("Durée", row.get("Durée (sec)", ""))
        date = row.get("Date", "")
        vues = row.get("Vues", "")

        description = "" if pd.isna(row.get('Description')) else str(row['Description'])
        tags = "" if pd.isna(row.get('Tags')) else str(row['Tags'])
        thumbnail_url = row.get("Thumbnail", "")

        # ✅ popup
        window = tk.Toplevel(root)
        window.title("📄 Détails vidéo")
        window.geometry("800x600")

        # ✅ image
        img = load_thumbnail(thumbnail_url)
        if img:
            img_label = tk.Label(window, image=img)
            img_label.image = img
            img_label.pack(pady=10)

        # ✅ texte
        text = tk.Text(window, wrap="word")
        text.pack(fill="both", expand=True)

        text.insert(tk.END, f"🎬 Titre: {titre}\n\n")
        text.insert(tk.END, f"📺 Chaîne: {chaine}\n\n")
        text.insert(tk.END, f"⏱ Durée: {duree}\n\n")
        text.insert(tk.END, f"📅 Date: {date}\n\n")
        text.insert(tk.END, f"👁 Vues: {vues}\n\n")
        text.insert(tk.END, f"📝 Description:\n{description}\n\n")
        text.insert(tk.END, f"🏷 Tags:\n{tags}\n")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))
# ✅ UI
root = tk.Tk()
root.title("🎬 Video Extractor PRO")
root.geometry("1100x650")

# 🔗 URL input
label = tk.Label(root, text="🔗 Entrer URL vidéo :", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root, width=100)
entry.pack(pady=5)

# ✅ boutons ligne
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Button(top_frame, text="➕ Ajouter", command=add_video, bg="green", fg="white").grid(row=0, column=0, padx=5)
tk.Button(top_frame, text="🗑 Supprimer", command=delete_selected, bg="red", fg="white").grid(row=0, column=1, padx=5)
tk.Button(top_frame, text="🔄 Rafraîchir", command=load_table).grid(row=0, column=1, padx=5)
tk.Button(top_frame,text="🎥 Ouvrir vidéo",command=open_video,bg="purple",fg="white").grid(row=0, column=2, padx=5)

# ✅ recherche
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

search_entry = tk.Entry(search_frame, width=50)
search_entry.grid(row=0, column=0, padx=5)

tk.Button(search_frame, text="🔍 Rechercher", command=search).grid(row=0, column=1)

# ✅ tableau
columns = ("Titre", "Durée", "Chaîne", "Date", "Vues","Description")

table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)

table.pack(fill="both", expand=True)

# ✅ double click bind
table.bind("<Double-1>", show_details)

# ✅ chargement initial
load_table()

root.mainloop()