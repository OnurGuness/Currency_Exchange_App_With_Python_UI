import customtkinter as ctk
import requests
import threading

# --- Ayarlar ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CurrencyMaster(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Pencere Ayarları ---
        self.title("Kur Radarı Pro v4")
        self.geometry("400x600")
        self.resizable(False, True) 
        
        # Değişkenler
        self.mini_mode = False
        self.all_rates = {}
        self.favorites = set()  # Favori döviz birimleri için set
        self.base_currency = "TRY"
        self.api_url = f"https://api.exchangerate-api.com/v4/latest/{self.base_currency}"

        # --- NORMAL MOD BAŞLIK ALANI ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.header_frame.pack(pady=(15, 5), padx=10, fill="x")

        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Canlı Kur Piyasası", 
                                      font=("Roboto", 20, "bold"))
        self.lbl_title.pack(side="left", padx=5)

        # Normal Mod Switch'i
        self.switch_mini = ctk.CTkSwitch(self.header_frame, text="Mini Mod", 
                                           command=self.toggle_mode, onvalue=True, offvalue=False)
        self.switch_mini.pack(side="right")

        # --- MİNİ MOD BAŞLIK ALANI (Başlangıçta Gizli) ---
        self.mini_header = ctk.CTkFrame(self, height=35, fg_color="#1a1a1a", corner_radius=0)
        
        # Mini moddan çıkış butonu (Switch yerine Buton daha kararlı çalışır)
        self.btn_return = ctk.CTkButton(self.mini_header, text="⤢ Normale Dön", 
                                        command=self.return_to_normal,
                                        width=120, height=25,
                                        fg_color="#424242", hover_color="#616161")
        self.btn_return.pack(side="top", pady=5)

        # --- ARAMA ve YENİLEME ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(pady=5, padx=10, fill="x")

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_list)
        
        self.entry_search = ctk.CTkEntry(self.controls_frame, placeholder_text="Ara (USD, EUR)...", 
                                         textvariable=self.search_var, height=35)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_refresh = ctk.CTkButton(self.controls_frame, text="⟳", width=40, height=35, 
                                         command=self.start_update_thread)
        self.btn_refresh.pack(side="right")

        # --- LİSTE ALANI ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.scroll_frame.pack(pady=(5, 10), padx=10, fill="both", expand=True)

        # Veriyi Çek
        self.start_update_thread()

    def fetch_data(self):
        try:
            response = requests.get(self.api_url)
            data = response.json()
            raw_rates = data["rates"]

            self.all_rates = {}
            for code, rate in raw_rates.items():
                if rate > 0:
                    self.all_rates[code] = 1 / rate

            self.update_ui_list(self.search_var.get())
            self.btn_refresh.configure(fg_color="#43A047") 
            
        except Exception as e:
            print(f"Hata: {e}")
            self.btn_refresh.configure(fg_color="#D32F2F")

    def update_ui_list(self, filter_text=""):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Filtrele ve sırala: Favoriler önce, sonra alfabetik
        all_keys = list(self.all_rates.keys())
        filtered_keys = [code for code in all_keys if filter_text.upper() in code or filter_text in code]
        sorted_keys = sorted(filtered_keys, key=lambda c: (0 if c in self.favorites else 1, c))

        for code in sorted_keys:
            if code == "TRY": continue

            rate = self.all_rates[code]

            pady_val = 1 if self.mini_mode else 3
            card = ctk.CTkFrame(self.scroll_frame, fg_color="#2b2b2b", corner_radius=6)
            card.pack(pady=pady_val, padx=2, fill="x")

            # Favori butonu
            fav_text = "★" if code in self.favorites else "☆"
            btn_fav = ctk.CTkButton(card, text=fav_text, width=30, height=25, 
                                    fg_color="transparent", hover_color="#616161",
                                    command=lambda c=code: self.toggle_fav(c))
            btn_fav.pack(side="left", padx=5, pady=5)

            lbl_code = ctk.CTkLabel(card, text=code, font=("Arial", 13, "bold"), width=35, anchor="w")
            lbl_code.pack(side="left", padx=3, pady=5)

            if rate < 0.1: val_text = f"{rate:.4f} ₺"
            elif rate > 1000: val_text = f"{rate:.0f} ₺"
            else: val_text = f"{rate:.2f} ₺"
                
            lbl_val = ctk.CTkLabel(card, text=val_text, font=("Consolas", 13), text_color="white")
            lbl_val.pack(side="right", padx=8)

            if not self.mini_mode:
                if rate < 20: bar_color = "#66BB6A"
                elif rate < 60: bar_color = "#FFA726"
                else: bar_color = "#EF5350"

                bar_val = min(rate / 60, 1.0)
                prog = ctk.CTkProgressBar(card, width=90, height=6, progress_color=bar_color)
                prog.set(bar_val)
                prog.pack(side="right", padx=5)

    def toggle_fav(self, code):
        if code in self.favorites:
            self.favorites.remove(code)
        else:
            self.favorites.add(code)
        self.update_ui_list(self.search_var.get())

    def filter_list(self, *args):
        self.update_ui_list(self.search_var.get())

    def start_update_thread(self):
        self.btn_refresh.configure(state="disabled")
        threading.Thread(target=self.fetch_data, daemon=True).start()
        self.after(2000, lambda: self.btn_refresh.configure(state="normal"))

    def toggle_mode(self):
        """Switch'e tıklandığında çalışır."""
        if self.switch_mini.get() == 1:
            self.go_to_mini_mode()
        else:
            self.return_to_normal()

    def go_to_mini_mode(self):
        """Mini moda geçer."""
        self.mini_mode = True
        
        # 1. Normal UI Gizle
        self.header_frame.pack_forget()
        self.controls_frame.pack_forget()
        
        # 2. Mini UI Göster
        self.mini_header.pack(side="top", fill="x", pady=0)
        
        # 3. Pencere Ayarları
        self.geometry("250x300")
        self.attributes('-topmost', True)
        
        # 4. Scroll Frame Ayarı
        self.scroll_frame.pack_forget()  # Geçici olarak forget et
        self.scroll_frame.configure(corner_radius=0)
        self.scroll_frame.pack(pady=0, padx=0, fill="both", expand=True)
        
        self.update_ui_list(self.search_var.get())

    def return_to_normal(self):
        """Normal moda döner."""
        self.mini_mode = False
        
        # 1. Mini UI Gizle
        self.mini_header.pack_forget()
        
        # 2. Scroll Frame'i geçici forget et
        self.scroll_frame.pack_forget()
        
        # 3. Normal UI Göster (before olmadan sırayla pack et)
        self.header_frame.pack(pady=(15, 5), padx=10, fill="x")
        self.controls_frame.pack(pady=5, padx=10, fill="x")
        
        # 4. Scroll Frame Ayarı
        self.scroll_frame.configure(corner_radius=10)
        self.scroll_frame.pack(pady=(5, 10), padx=10, fill="both", expand=True)
        
        # 5. Pencere Ayarları
        self.geometry("400x600")
        self.attributes('-topmost', False)
        
        # 6. Switch'i Manuel Olarak Kapat (Senkronizasyon Sorununu Çözer)
        self.switch_mini.deselect()
        
        self.update_ui_list(self.search_var.get())

if __name__ == "__main__":
    app = CurrencyMaster()
    app.mainloop()