# import flet as ft
# from controllers.user_controller import login_user
# from config import cargar_config

# # 🎨 Paleta consistente
# BACKGROUND = ft.Colors.BLUE_GREY_900
# CARD = ft.Colors.BLUE_GREY_800
# PRIMARY = ft.Colors.BLUE_400
# TEXT = ft.Colors.WHITE
# SUBTEXT = ft.Colors.WHITE_70


# def login_view(page: ft.Page, on_login_success):

#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

#     username_input = ft.TextField(
#         hint_text="Username",
#         prefix_icon=ft.Icons.VERIFIED_USER,
#         width=300,
#         bgcolor=ft.Colors.BLUE_GREY_700,
#         border_radius=10,
#         border_color="transparent",
#         color=TEXT
#     )

#     password_input = ft.TextField(
#         hint_text="Contraseña",
#         prefix_icon=ft.Icons.LOCK,
#         password=True,
#         width=300,
#         bgcolor=ft.Colors.BLUE_GREY_700,
#         border_radius=10,
#         border_color="transparent",
#         color=TEXT
#     )

#     result_text = ft.Text("", color=ft.Colors.RED_300)

#     def handle_login(e):
#         username = username_input.value
#         password = password_input.value

#         success, result = login_user(username, password)

#         if success:
#             page.user = result.username
#             page.is_admin = result.is_admin
#             on_login_success()
#         else:
#             result_text.value = result
#             page.update()

#     config = cargar_config()
#     nombre = config.get("nombre_heladeria", "Mi Heladería")

#     return ft.Container(
#         expand=True,
#         bgcolor=BACKGROUND,
#         content=ft.Column(
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             controls=[

#                 # 📦 CARD LOGIN
#                 ft.Container(
#                     width=360,
#                     bgcolor=CARD,
#                     border_radius=20,
#                     padding=30,
#                     content=ft.Column(
#                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                         spacing=20,
#                         controls=[

#                             # 🔥 TÍTULO
#                             ft.Column(
#                                 controls=[
#                                     ft.Text(f"Bienvenido a {nombre}", size=20, color="white"),
#                                     username_input,
#                                     password_input,
#                                     boton_login
#                                 ]
#                             ),

#                             ft.Text(
#                                 "Iniciá sesión para continuar",
#                                 size=14,
#                                 color=SUBTEXT
#                             ),

#                             # 📩 INPUTS
#                             username_input,
#                             password_input,

#                             # 🔘 BOTÓN
#                             ft.Container(
#                                 width=300,
#                                 height=45,
#                                 content=ft.FilledButton(
#                                     content=ft.Text("Ingresar", size=16, weight="bold"),
#                                     style=ft.ButtonStyle(
#                                         bgcolor=PRIMARY,
#                                         shape=ft.RoundedRectangleBorder(radius=10)
#                                     ),
#                                     on_click=handle_login
#                                 )
#                             ),

#                             result_text
#                         ]
#                     )
#                 )
#             ]
#         )
#     )

import flet as ft
from controllers.user_controller import login_user
from config import cargar_config

# 🎨 Paleta consistente
BACKGROUND = ft.Colors.BLUE_GREY_900
CARD = ft.Colors.BLUE_GREY_800
PRIMARY = ft.Colors.BLUE_400
TEXT = ft.Colors.WHITE
SUBTEXT = ft.Colors.WHITE_70


def login_view(page: ft.Page, on_login_success):

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    username_input = ft.TextField(
        hint_text="Username",
        prefix_icon=ft.Icons.VERIFIED_USER,
        width=300,
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        border_color="transparent",
        color=TEXT
    )

    password_input = ft.TextField(
        hint_text="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        width=300,
        bgcolor=ft.Colors.BLUE_GREY_700,
        border_radius=10,
        border_color="transparent",
        color=TEXT
    )

    result_text = ft.Text("", color=ft.Colors.RED_300)

    def handle_login(e):
        username = username_input.value
        password = password_input.value

        success, result = login_user(username, password)

        if success:
            page.user = result.username
            page.is_admin = result.is_admin
            on_login_success()
        else:
            result_text.value = result
            page.update()

    # 🔹 Nombre dinámico de la heladería
    config = cargar_config()
    nombre = config.get("nombre_heladeria", "Mi Heladería")

    return ft.Container(
        expand=True,
        bgcolor=BACKGROUND,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                ft.Container(
                    width=360,
                    bgcolor=CARD,
                    border_radius=20,
                    padding=30,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[

                            ft.Image(
                                src="logo.png",
                                width=120,
                                height=120,
                                fit="contain"
                            ),

                            ft.Text(
                                nombre,
                                size=22,
                                weight="bold",
                                color="white"
                            ),

                            ft.Text(
                                "Iniciá sesión para continuar",
                                size=14,
                                color=SUBTEXT
                            ),

                            # 📩 INPUTS
                            username_input,
                            password_input,

                            # 🔘 BOTÓN
                            ft.Container(
                                width=300,
                                height=45,
                                content=ft.FilledButton(
                                    content=ft.Text("Ingresar", size=16, weight="bold"),
                                    style=ft.ButtonStyle(
                                        bgcolor=PRIMARY,
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    ),
                                    on_click=handle_login
                                )
                            ),

                            # ⚠️ RESULTADO
                            result_text
                        ]
                    )
                )
            ]
        )
    )