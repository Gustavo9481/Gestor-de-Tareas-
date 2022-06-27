# ---- GESTOR DE TAREAS ----    | ---- TASK MANAGER ---- 
# - Agregar nuevas tareas       | - Add new tasks
# - Modificar tareas anteriores | - Modify previus tasks
# - Marcar tareas finalizadas   | - Mark finished tasks
# - Eliminar tareas             | - Delete tasks


from tkinter import *
import sqlite3

root = Tk()
root.title('Tareas')
root.geometry('500x500')
root.config(bg='#001D3D')


# BBDD base de datos --------------------------------------------------------------------
conex = sqlite3.connect('tareas.db')  # conexión a base de datos / BBDD conexion
c = conex.cursor()  # creación del cursor / cursor creation

# creación de la tabla de BBDD ----- BBDD table creation
c.execute("""
  CREATE TABLE if not exists tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT NOT NULL,
    completado BOOLEAN NOT NULL
  );
""")
# campo 1 => identificador del registro en la BBDD [tarea]
# campo 2 => creación, fecha de creación de la tarea, capta momento exacto
# campo 3 => descripción, texto que introduce user explicando la tarea
# campo 4 => completado, booleano que mostrará status de la tarea

conex.commit() # ejecución de la instrucción c.execute
completado = ''
color = '#FFFFFF'
# FUNCIONES ----------- FUNCTIONS -----------
# eliminar tareas ----- delete tasks -----
def remove1(id):
  def remove2():
    c.execute("DELETE FROM tareas WHERE id = ?", (id, ))
    conex.commit()
    mostrar()
  return remove2


# tareas completadas ----- mark finished tasks -----
def marcados1(id):
  def marcados2():
    tarea = c.execute("SELECT * FROM tareas WHERE id = ?", (id,)).fetchone()
    c.execute("UPDATE tareas SET completado = ? WHERE id = ?", (not tarea[3], id))
    conex.commit()
    mostrar()
  return marcados2
# currying => retrasar la ejecución de una función anidandola dentro de otra

# renderizar las tareas [mostrar todas] ----- render tasks -----
def mostrar():
  global completado
  global color
  rows = c.execute("SELECT * FROM tareas").fetchall() # genera lista de tuplas
  for widget in frame.winfo_children():  # elimina los elementos de la pantalla 
    widget.destroy()
  for i in range(0, len(rows)):
    id = rows[i][0]
    completado = rows[i][3] # en la tupla indice 3
    descripcion = rows[i][2]
    color = '#8E8E99' if completado else '#FFFFFF'
    l = Checkbutton(frame, text=descripcion, fg=color, width=60, anchor='w', bg='#001D3D', command=marcados1(id))
    l.grid(row=i, column=0, sticky='w')
    be = Button(frame, text='⌫', bg='#001D3D', fg='white', bd=0, padx=5, command=remove1(id))
    be.grid(row=i, column=1)
    l.select() if completado else l.deselect()

# agregar nueva tarea ----- add a new task -----
def agregar_tarea():
  tarea = e.get()
  if tarea:
    c.execute("""
      INSERT INTO tareas (descripcion, completado) VALUES (?,?)""", (tarea, False))
    conex.commit()
    e.delete(0, END)
    mostrar()
  else:
    pass



# INTERFAZ GRÁFICA ------------- GRAPHICAL INTERFACE -----------------
l = Label(root, text='Tarea >', fg='white', bg='#001D3D', padx=3)
l.grid(row=0, column=0, padx=3, pady=3)

e = Entry(root, width=64, bg='#001D3D', fg='white', insertbackground="white", bd=1)
e.grid(row=0, column=1, padx=3, pady=3)
# insertbackground da color al cursor de escritura

b = Button(root, text='✚', bg='#FF5F00', fg='#ffffff', bd=0, padx=3, command=agregar_tarea)
b.grid(row=0, column=2, padx=3, pady=3)

frame = LabelFrame(root, text='Mis tareas', bg='#001D3D', fg='white', pady=5, padx=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)



e.focus() # coloca el cursor automáticamente en el entry / cursor on entry
root.bind('<Return>', lambda x: agregar_tarea())
# bind permite usar el intro por teclado para agregar una tarea
mostrar()
root.mainloop()
