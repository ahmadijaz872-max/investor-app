import os
import requests
import urllib.parse
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.fitimage import FitImage

KV = '''
MDScreen:
    md_bg_color: 0.07, 0.08, 0.1, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(12)

        MDLabel:
            text: "INVESTOR TRADER PANEL"
            font_style: "H6"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 0.9, 1, 1
            size_hint_y: None
            height: self.texture_size[1]

        # Gold Card
        MDCard:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(80)
            padding: dp(10)
            radius: [12]
            md_bg_color: 0.11, 0.13, 0.17, 1
            line_color: 1, 0.84, 0, 1

            MDLabel:
                text: "GOLD (XAU/USD) REAL-TIME"
                font_style: "Caption"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.6, 0.65, 0.7, 1

            MDLabel:
                id: gold_price_lbl
                text: "$2,400.00"
                font_style: "H5"
                bold: True
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 0.84, 0, 1

        # Data Metrics List
        MDScrollView:
            MDBoxLayout:
                id: metrics_box
                orientation: 'vertical'
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

        # Action Buttons
        MDBoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            MDRaisedButton:
                text: "➕ Add Funds"
                md_bg_color: 0.3, 0.69, 0.31, 1
                size_hint_x: 0.5
                on_release: app.show_deposit_dialog()

            MDRaisedButton:
                text: "📜 Rules PDF"
                md_bg_color: 0, 0.9, 1, 1
                text_color: 0, 0, 0, 1
                size_hint_x: 0.5
                on_release: app.open_rules_pdf()

        # Footer Instruction
        MDCard:
            size_hint_y: None
            height: dp(75)
            padding: dp(8)
            radius: [8]
            md_bg_color: 0.07, 0.08, 0.1, 1

            MDLabel:
                text: "⚠️ IMPORTANT INSTRUCTIONS:\\n• Equity updates automatically from MT5 core server.\\n• Withdrawals processed within 24 business hours."
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.45, 0.48, 0.52, 1

        MDLabel:
            text: "⚡ Design by Ahmsxtrade"
            font_style: "Caption"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 0.84, 0, 1
            size_hint_y: None
            height: self.texture_size[1]
'''

class InvestorApp(MDApp):
    dialog = None
    deposit_address = "0xfeff2067ef...971debbd"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        self.populate_metrics()
        Clock.schedule_interval(self.update_gold_price, 5)

    def populate_metrics(self):
        items = [
            ("Current Amount", "$10,500.00", [0.3, 0.69, 0.31, 1]),
            ("Deposit Amount", "$8,000.00", [0.13, 0.59, 0.95, 1]),
            ("Live Equity", "$11,250.50", [0, 0.9, 1, 1]),
            ("Live Withdrawal", "$2,500.00", [1, 0.6, 0, 1]),
        ]
        container = self.root.ids.metrics_box
        for title, val, color in items:
            card = Builder.load_string(f'''
MDCard:
    size_hint_y: None
    height: dp(60)
    padding: dp(10)
    radius: [10]
    md_bg_color: 0.13, 0.15, 0.19, 1

    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: "{title}"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.56, 0.59, 0.64, 1
        MDLabel:
            text: "{val}"
            font_style: "Subtitle1"
            bold: True
            theme_text_color: "Custom"
            text_color: {color}
''')
            container.add_widget(card)

    def update_gold_price(self, dt):
        try:
            import random
            price = 2400.00 + random.uniform(-2.5, 3.5)
            self.root.ids.gold_price_lbl.text = f"${price:,.2f}"
        except Exception:
            pass

    def show_deposit_dialog(self):
        content = MDBoxLayout(orientation='vertical', spacing='12dp', size_hint_y=None, height='220dp')
        
        # Load Image if available
        qr_file = "qr_code.png" if os.path.exists("qr_code.png") else "qr_code.jpg"
        if os.path.exists(qr_file):
            img = FitImage(source=qr_file, size_hint=(None, None), size=('120dp', '120dp'), pos_hint={'center_x': 0.5})
            content.add_widget(img)
        else:
            lbl = MDLabel(text="[ Place qr_code.png in folder ]", halign="center", theme_text_color="Hint")
            content.add_widget(lbl)

        addr_lbl = MDLabel(text=self.deposit_address, font_style="Caption", halign="center")
        content.add_widget(addr_lbl)

        self.dialog = MDDialog(
            title="DEPOSIT FUNDS",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="COPY ADDRESS", theme_text_color="Custom", text_color=(0, 0.9, 1, 1), on_release=self.copy_addr),
                MDFlatButton(text="CLOSE", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def copy_addr(self, instance):
        Clipboard.copy(self.deposit_address)

    def open_rules_pdf(self):
        pdf_file = "rules.pdf"
        if os.path.exists(pdf_file):
            import webbrowser
            webbrowser.open(os.path.abspath(pdf_file))

if __name__ == "__main__":
    InvestorApp().run()
