from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
from kivy.clock import Clock
import os
import webbrowser

class InvestorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        self.main_box = MDBoxLayout(orientation='vertical', padding=15, spacing=15)
        self.show_dashboard()
        return self.main_box

    def show_dashboard(self):
        self.main_box.clear_widgets()
        
        # Title
        title = MDLabel(
            text="INVESTOR TRADER PANEL", 
            halign="center", 
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 0.7, 1, 1)
        )
        self.main_box.add_widget(title)
        
        # Gold Card
        gold_card = MDCard(orientation='vertical', padding=10, size_hint=(1, None), height="80dp", md_bg_color=(0.1, 0.1, 0.1, 1))
        gold_title = MDLabel(text="GOLD (XAU/USD) REAL-TIME", halign="center", theme_text_color="Secondary")
        self.gold_price = MDLabel(text="$2,401.66", halign="center", bold=True, theme_text_color="Custom", text_color=(1, 0.8, 0, 1))
        gold_card.add_widget(gold_title)
        gold_card.add_widget(self.gold_price)
        self.main_box.add_widget(gold_card)

        # 1. MINE BUTTON
        mine_btn = MDButton(
            MDButtonText(text="MINE (30s CHART)"),
            size_hint=(1, None), 
            height="50dp",
            on_release=self.start_mining_screen
        )
        self.main_box.add_widget(mine_btn)

        # Stats Rows
        self.add_stat_row("Current Amount", "$10,500.00")
        self.add_stat_row("Deposit Amount", "$8,000.00")
        self.add_stat_row("Live Equity", "$11,250.50")
        self.add_stat_row("Live Withdrawal", "$2,500.00")

        # Bottom Buttons
        btn_box = MDBoxLayout(spacing=10, size_hint=(1, None), height="50dp")
        
        add_funds_btn = MDButton(MDButtonText(text="Add Funds"), size_hint=(0.5, 1), on_release=self.show_qr_popup)
        rules_btn = MDButton(MDButtonText(text="Rules & Legal PDF"), size_hint=(0.5, 1), on_release=self.open_pdf_file)
        
        btn_box.add_widget(add_funds_btn)
        btn_box.add_widget(rules_btn)
        self.main_box.add_widget(btn_box)

    def add_stat_row(self, label_text, amount_text):
        card = MDCard(padding=10, size_hint=(1, None), height="50dp", md_bg_color=(0.15, 0.15, 0.18, 1))
        box = MDBoxLayout()
        lbl = MDLabel(text=label_text, theme_text_color="Secondary")
        val = MDLabel(text=amount_text, halign="right", bold=True, theme_text_color="Custom", text_color=(0, 0.8, 0.4, 1))
        box.add_widget(lbl)
        box.add_widget(val)
        card.add_widget(box)
        self.main_box.add_widget(card)

    # 2. Add Funds Image/QR Fix
    def show_qr_popup(self, instance):
        img_path = os.path.join(os.path.dirname(__file__), 'qr_code.jpeg')
        if os.path.exists(img_path):
            content = Image(source=img_path)
        else:
            content = MDLabel(text="qr_code.jpeg file not found in folder!", halign="center")
            
        dialog = MDDialog(
            type="custom",
            content_cls=content,
        )
        dialog.open()

    # 3. Rules PDF Opener Fix
    def open_pdf_file(self, instance):
        pdf_path = os.path.join(os.path.dirname(__file__), 'rules.pdf')
        if os.path.exists(pdf_path):
            webbrowser.open(pdf_path)
        else:
            print("rules.pdf file not found!")

    # 4. Mining Screen Logic (30 Seconds Timer)
    def start_mining_screen(self, instance):
        self.main_box.clear_widgets()
        self.timer_seconds = 30
        
        self.status_label = MDLabel(
            text="LIVE CANDLESTICK CHART MINING IN PROGRESS...", 
            halign="center", 
            theme_text_color="Custom",
            text_color=(0, 0.8, 1, 1)
        )
        self.timer_label = MDLabel(
            text=f"Time Remaining: {self.timer_seconds}s", 
            halign="center", 
            bold=True
        )
        
        self.main_box.add_widget(self.status_label)
        self.main_box.add_widget(self.timer_label)
        
        self.mining_event = Clock.schedule_interval(self.update_mining_timer, 1)

    def update_mining_timer(self, dt):
        self.timer_seconds -= 1
        self.timer_label.text = f"Time Remaining: {self.timer_seconds}s"
        
        if self.timer_seconds <= 0:
            Clock.unschedule(self.mining_event)
            self.show_mining_success()

    def show_mining_success(self):
        self.main_box.clear_widgets()
        
        success_label = MDLabel(
            text="SUCCESS!\nYou Have Successfully Made $1", 
            halign="center", 
            bold=True,
            theme_text_color="Custom",
            text_color=(0, 1, 0, 1)
        )
        
        back_btn = MDButton(
            MDButtonText(text="Back to Dashboard"),
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.show_dashboard()
        )
        
        self.main_box.add_widget(success_label)
        self.main_box.add_widget(back_btn)

if __name__ == '__main__':
    InvestorApp().run()
