import os
import time
import eth_utils
import flet as ft
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
from transactions import get_last_5


load_dotenv()

alchemy_url = os.getenv('URL')
web3 = Web3(HTTPProvider(alchemy_url))


class ETHValidator(ft.UserControl):
    loader = ft.Container(
        bgcolor=ft.colors.WHITE38,
        content=ft.ProgressRing(
            width=50,
            height=50,
            stroke_width=5,
        ), 
        alignment=ft.alignment.center
    )
    def __init__(self):
        self.title = ft.Text(
            "Validate your ETH wallet.",
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.colors.BLACK54,
            opacity=1,
            animate_opacity=500,
            offset=ft.transform.Offset(0, 0),
            animate_offset=500
        )
        self.validation_box = ft.Container(
            content=self.title,
            width=250, 
            height=70,
            bgcolor=ft.colors.WHITE,
            border_radius=5,
            animate=ft.animation.Animation(
                500, ft.AnimationCurve.EASE_OUT_BACK
            ),
            on_click=self.expand_validation_box,
            alignment=ft.alignment.center,
        )
        self.input_title = ft.Text(
            "Verify Your Etherium Address Here",
            color=ft.colors.BLACK87,
            weight=ft.FontWeight.W_600,
            opacity=0,
            animate_opacity=500
        )
        self.eth_address_input = ft.TextField(
            width=350,
            height=50,
            border=ft.InputBorder.UNDERLINE,
            text_size=12,
            content_padding=3,
            cursor_color=ft.colors.BLACK,
            cursor_width=1,
            color=ft.colors.BLACK,
            opacity=0,
            animate_opacity=500,
            offset=ft.transform.Offset(0.05, 0),
            autofocus=True,
        )
        self.validation_status = ft.Container(
            opacity=0,
            offset=ft.transform.Offset(2.5, 0),
            animate_opacity=ft.animation.Animation(
                500, ft.AnimationCurve.EASE
            ),
            animate_offset=ft.animation.Animation(
                500, ft.AnimationCurve.EASE
            ),
            shape=ft.BoxShape.CIRCLE,
            alignment=ft.alignment.center,
            width=25,
            height=25,
            scale=ft.Scale(0.75),
            content=ft.Icon(ft.icons.CIRCLE)
        )
        self.submit_adress = ft.ElevatedButton(
            'Validate',
            width=350,
            height=50,
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=10)}
            ),
            on_click=self.validate_address
        )
        super().__init__()
    
    def expand_validation_box(self, e):
        self.title.opacity = 0
        self.title.offset = ft.transform.Offset(0, -1)
        self.title.update()
        time.sleep(0.5)

        self.validation_box.content = None
        self.validation_box.width = 500
        self.validation_box.update()
        time.sleep(0.5)

        self.validation_box.height = 250
        self.validation_box.border_radius = 10
        self.validation_box.update()
        time.sleep(0.25)
        
        self.add_input()
    
    def add_input(self):
        self.validation_box.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                self.input_title,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[self.eth_address_input, self.validation_status]
                ),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                self.submit_adress
            ]
        )
        self.validation_box.update()

        self.input_title.opacity = 1
        self.input_title.update()

        self.eth_address_input.opacity = 1
        self.eth_address_input.update()
    
    def clear_validation_status(self):
        self.validation_status.opacity = 0
        self.validation_status.offset = ft.transform.Offset(2.5, 0)
        self.validation_status.content.value = False
        self.validation_status.update()
        time.sleep(0.5)
    
    def validation_status_success(self):
        self.validation_status.content = ft.Icon(ft.icons.CHECK_CIRCLE)
        self.validation_status.content.color = ft.colors.TEAL_600
        self.validation_status.opacity = 1
        self.validation_status.offset = ft.transform.Offset(1, 0)
        self.validation_status.update()
        time.sleep(0.5)
        self.validation_status.content.value = True
        self.validation_status.update()
    
    def validation_status_failed(self):
        self.validation_status.content = ft.Icon(ft.icons.CIRCLE)
        self.validation_status.content.color = ft.colors.RED
        self.validation_status.update()
        self.validation_status.opacity = 1
        self.validation_status.offset = ft.transform.Offset(1, 0)
        self.validation_status.update()
        time.sleep(0.5)

    def validate_address(self, e):
        eth_address = self.eth_address_input.value

        self.clear_validation_status()

        if eth_utils.address.is_address(eth_address):
            self.page.overlay.append(self.loader)
            self.page.update()
            balance = web3.eth.get_balance(eth_address)
            balance = web3.from_wei(balance, 'ether')
            text = (
                f"{eth_address} is a valid ETH address."
                f"\nCurrent balance: {balance:.3f} ETH"
            )
            snack_content = ft.Column(
                controls=[
                    ft.Text(
                        value=text,
                        color=ft.colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value='Last 10 transactions:',
                        size=16,
                        color=ft.colors.BLACK87,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value=get_last_5(eth_address),
                        color=ft.colors.BLACK87,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            big_snack = ft.SnackBar(
                bgcolor=ft.colors.WHITE,
                elevation=25,
                content=snack_content,
                duration=120000,
                show_close_icon=True,
                close_icon_color=ft.colors.BLACK38,
            )
            self.page.snack_bar = big_snack
            self.page.overlay.pop()
            self.validation_status_success()
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.validation_status_failed()
    
    def build(self):
        return ft.Container(
            ft.Card(content=self.validation_box, elevation=15),
            alignment=ft.alignment.center,
        )


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    background_img = ft.Image('assets/img/hero.webp', scale=1.35)
    validator = ETHValidator()
    stack = ft.Stack([background_img, validator])
    
    page.add(stack)

ft.app(main)