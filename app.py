import flet as flet
from flet import *
from user_table import create_table
from datatable import mytable
import sqlite3
conn = sqlite3.connect('db/userdb.db', check_same_thread=False)

def main(page: Page):
    create_table()
    page.scroll = "auto"

    def showinput(e):
        inputcontent.offset = transform.Offset(0, 0)
        page.update()

    def hideinput(e):
        inputcontent.offset = transform.Offset(0, 0)
        page.update()

    def savedata(e):
        with sqlite3.connect('db/userdb.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name.value, email.value, password.value))
            conn.commit()

        page.snack_bar = SnackBar(Text("Sucesso"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    name = TextField(label="Nome")
    email = TextField(label="Email")
    password = TextField(label="Senha")

    inputcontent = Card(
        offset=transform.Offset(2, 0),
        animate_offset=animation.Animation(600, curve="easeIn"),
        elevation=30,
        content=Container([
            Row([
                Text("add dados", size=20, weight="bold"),
                IconButton(icon="Sair", icon_size=30, on_click=hideinput),
                name,
                email,
                password,
                FilledButton("Cadastrar", on_click=savedata),
            ])
        ]),
    )

    page.add(
        Column([
            Text("Cadastro de Usuário", size=30, weight="bold"),
            ElevatedButton("Cadastro", on_click=showinput),
            mytable,
            inputcontent,
        ])
    )

flet.app(target=main)