import flet as flet
from flet import *
import sqlite3
conn = sqlite3.connect('db/userdb.db', check_same_thread=False)

tb=DataTable(
    columns=[
        DataColumn(Text("id")),
        DataColumn(Text("name")),
        DataColumn(Text("email")),
        DataColumn(Text("password")),
    ],
    rows=[]
)

id_edit = Text()
name_edit = TextField(label="Nome")
email_edit = TextField(label="Email")
password_edit = TextField(label="Senha")

def hidedlg(e):
    dlg.visible = False
    dlg.update()

def saveedit(e):
    try:
        myid = id_edit.value
        c =conn.cursor()
        c.execute("UPDATE users SET name=?, email=?, password=? WHERE id=?", (name_edit.value, email_edit.value, password_edit.value, myid))
        conn.commit()
        print("Dados atualizados com sucesso!")
        tb.rows.clear()
        calldb()
        dlg.visible = False
        dlg.update()
        tb.update()
    except Exception as e:
        print("Erro ao atualizar dados:", e)

def showdelete(e):
    try:
        myid = int(e.control.data)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (myid,))
        conn.commit()
        print("Dados deletados com sucesso!")
        tb.rows.clear()
        calldb()
        tb.update()
    except Exception as e:
        print("Erro ao deletar dados:", e)

dlg = Container(
    bgcolor="green",
    padding=10,
    content=Column([
        Row([
            Text("Editar dados", size=20, weight="bold"),
            IconButton(icon="Sair", on_click=hidedlg)
        ]),
        name_edit,
        email_edit,
        password_edit,
        ElevatedButton("Salvar", on_click=saveedit)
    ])
)

def showedit(e):
    data_edit = e.control.data
    id_edit = data_edit['id']
    name_edit = data_edit['name']
    email_edit = data_edit['email']
    password_edit = data_edit['password']
    

def calldb():
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    print(users)
    
    if not users =="":
        keys = ["id", "name", "email", "password"]
        
        result = [dict(zip(keys, values)) for values in users]
        for x in result:
            tb.rows.append(
                DataRow(
                cells=[
                    DataCell(Row([
                        IconButton(icon="Editar", icon_color="green",
                                   data=x["id"],
                                   on_click=showedit
                                   ),
                        
                        IconButton(icon="Deletar", icon_color="red",
                                   data=x["id"],
                                   on_click=showdelete
                                   ),
                    ])),
                    DataCell(Text(x['id'])),
                    DataCell(Text(x['name'])),
                    DataCell(Text(x['email'])),
                    DataCell(Text(x['password'])),
                ]
                )
            )
calldb()

dlg.visible = False            
mytable = Column([
    dlg,
    Row([tb], scroll="always"),
])

