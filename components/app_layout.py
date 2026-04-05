import flet as ft

# 🎨 Paleta
BACKGROUND = ft.Colors.BLUE_GREY_900
CARD = ft.Colors.BLUE_GREY_800
PRIMARY = ft.Colors.BLUE_400
TEXT = ft.Colors.WHITE
SUBTEXT = ft.Colors.WHITE_70


def app_layout(page: ft.Page, title: str, content: ft.Control, go_to_menu):

    return ft.Container(
        expand=True,
        bgcolor=BACKGROUND,
        padding=ft.Padding.only(top=30, left=15, right=15, bottom=15),
        content=ft.Column(
            expand=True,
            spacing=10,
            controls=[

                # 🔝 HEADER
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.TextButton(
                            content=ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(ft.Icons.ARROW_BACK, color=PRIMARY),
                                    ft.Text("Menú", color=PRIMARY)
                                ]
                            ),
                            on_click=lambda e: go_to_menu()
                        ),

                        ft.Text(
                            title,
                            size=18,
                            weight="bold",
                            color=TEXT
                        ),

                        ft.Container(width=40)
                    ]
                ),

                # 📦 CONTENIDO SCROLLEABLE
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=True,
                                controls=[
                                ft.Container(
                                    width=min(360, page.width * 0.92),
                                    bgcolor=CARD,
                                    border_radius=20,
                                    padding=20,
                                    expand=True,  # 👈 CLAVE
                                    content=content
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )
)