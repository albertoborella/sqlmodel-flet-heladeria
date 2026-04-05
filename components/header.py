import flet as ft

def header(title: str, go_to_menu):
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.TextButton(
                "← Menú",
                on_click=lambda e: go_to_menu()
            ),
            ft.Text(title, size=20, weight="bold", color="white"),
        ]
    )