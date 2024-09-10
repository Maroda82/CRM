from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import filedialog

# Definición de la clase Ventana que hereda de Tk (la ventana principal de Tkinter)
class Ventana(tb.Window):
    def __init__(self):  # Constructor de Ventana
        super().__init__()  # Llama al constructor de la clase base (Tk)
        self.ventana_login()  # Llama al método ventana_login para configurar la interfaz de login
      
    def centrar_ventana(self,ventana,ancho,alto):
        #obtener dimensiones de la pantalla
        pantalla_ancho=self.winfo_screenwidth()
        pantalla_alto=self.winfo_screenheight()
        #calcular las coordenadas para centrar la ventana:
        x=(pantalla_ancho-ancho)//2
        y=(pantalla_alto-alto)//2
        #Establecer las coordenadas de la ventana
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        
    def ventana_login(self):
        # Crear un frame dentro de la ventana principal
        self.grid_columnconfigure(1,weight=1)
        self.frame_login = Frame(master=self)
        self.frame_login.grid(row=0, column=1, sticky=NSEW)  # Coloca el frame en la ventana principal

        # Crear un LabelFrame dentro del frame de login con el texto 'Acceso'
        lblframe_login = tb.LabelFrame(master=self.frame_login, text='Acceso')
        lblframe_login.pack(padx=10, pady=35)  # Añade padding alrededor del LabelFrame


        # Crear un Label dentro del LabelFrame con el texto 'Inicio de Sesión'
        lbl_titulo = tb.Label(master=lblframe_login, text='Inicio de Sesión', font=('Calibri',18))
        lbl_titulo.pack(padx=10, pady=35)  # Añade padding alrededor del Label

        self.ent_usuario=tb.Entry(master=lblframe_login, width=40, justify=CENTER)
        self.ent_usuario.pack(padx=10,pady=10)

        self.ent_clave=tb.Entry(master=lblframe_login, width=40, justify=CENTER)
        self.ent_clave.pack(padx=10,pady=10)
        self.ent_clave.config(show='*')


        btn_acceso=tb.Button(master=lblframe_login, width=38, text='Login', bootstyle='success', command=self.logueo_usuarios)
        btn_acceso.pack(padx=10,pady=10)
        self.ent_usuario.focus()        
    def ventana_menu(self):
        self.frame_left=Frame(master=self,width=200)
        self.frame_left.grid(row=0,column=0,sticky=NSEW)

        self.frame_center=Frame(master=self,width=200)
        self.frame_center.grid(row=0,column=1,sticky=NSEW)

        self.ventana_busqueda_detalle_venta()

       
        btn_usuarios=Button(master=self.frame_left,text='Usuario', width=15, height=2,command=self.ventana_lista_usuarios)
        btn_usuarios.grid(row=0,column=0,padx=10, pady=10)

        btn_productos=Button(master=self.frame_left,text='Productos', width=15, height=2,command=self.ventana_lista_productos)
        btn_productos.grid(row=1,column=0,padx=10, pady=10)

        btn_ventas=Button(master=self.frame_left,text='Ventas', width=15, height=2,command=self.ventana_detalle_venta)
        btn_ventas.grid(row=2,column=0,padx=10, pady=10)
    
        btn_informes=Button(master=self.frame_left,text='Informes', width=15, height=2,command=self.ventana_reportes)
        btn_informes.grid(row=3,column=0,padx=10, pady=10)
    def ventana_lista_usuarios(self):
        self.borrar_frames()
        self.frame_lista_usuarios=Frame(master=self.frame_center)
        self.frame_lista_usuarios.grid(row=0, column=1, columnspan=2, sticky=NSEW)
        lblframe_botones_lista_usuarios=tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_botones_lista_usuarios.grid(row=0,column=0,sticky=NSEW, padx=5, pady=5)

        btn_nuevo_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Nuevo',width=15,bootstyle='success',command=self.ventana_nuevo_usuario)
        btn_nuevo_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)

        btn_modificar_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Modificar',width=15,bootstyle='warning',command=self.ventana_modificar_usuario)
        btn_modificar_lista_usuarios.grid(row=0,column=1,padx=10,pady=10)

        btn_eliminar_lista_usuarios=tb.Button(master=lblframe_botones_lista_usuarios,text='Eliminar',width=15,bootstyle='danger',command=self.eliminar_usuarios)
        btn_eliminar_lista_usuarios.grid(row=0,column=2,padx=10,pady=10)

        lblframe_busqueda_lista_usuarios=tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_busqueda_lista_usuarios.grid(row=1,column=0,padx=5,pady=5, sticky=NSEW)

        self.ent_buscar_lista_usuarios=tb.Entry(master=lblframe_busqueda_lista_usuarios, width=98)
        self.ent_buscar_lista_usuarios.grid(row=0,column=0,padx=10,pady=10)
        self.ent_buscar_lista_usuarios.bind('<Key>',self.buscar_usuarios)

        
        lblframe_tree_lista_usuarios=tb.LabelFrame(master=self.frame_lista_usuarios)
        lblframe_tree_lista_usuarios.grid(row=2,column=0,padx=5,pady=5, sticky=NSEW)

        #CREACIÓN DE COLUMNAS

        columnas=("codigo", "nombre", "clave", "rol")

        #crear el treeview o tabla

        self.tree_lista_usuarios=tb.Treeview(master=lblframe_tree_lista_usuarios, height=17, columns=columnas,show='headings', bootstyle='success')
        self.tree_lista_usuarios.grid(row=0, column=0, padx=10, pady=10,)

        #creando encabezados o cabeceras

        self.tree_lista_usuarios.heading('codigo', text='Codigo', anchor=W)
        self.tree_lista_usuarios.heading('nombre', text='Nombre', anchor=W)
        self.tree_lista_usuarios.heading('clave', text='Clave', anchor=W)
        self.tree_lista_usuarios.heading('rol', text='Rol', anchor=W)

        #configurar las columnas que quiero que se muestren

        self.tree_lista_usuarios['displaycolumns']=('codigo','nombre','rol')

        #Ancho de las columnas, para que no los dé por defecto la tabla

        self.tree_lista_usuarios.column('codigo',width=100)
        self.tree_lista_usuarios.column('nombre',width=300)
        self.tree_lista_usuarios.column('clave',width=100)
        self.tree_lista_usuarios.column('rol',width=200)

        #Crear el Scrollbar o barra de scroll

        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_usuarios,bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=5, pady=10)

        #Configurar el Scrollbar

        tree_scroll.config(command=self.tree_lista_usuarios.yview)

        self.buscar_usuarios('')
        #la propiedad focus es para que se me marque el campo de texto de color
        self.ent_buscar_lista_usuarios.focus()
    def buscar_usuarios(self,event):
        try:

            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            #limpiar nuestro treeview o tabla
            #el método .get_children() nos trae todos los registros
            registro=self.tree_lista_usuarios.get_children()
            for elementos in registro: 
                self.tree_lista_usuarios.delete(elementos)

            #creamos la consulta para buscar el usuario, con condición donde el nombre sea parecido a lo que pasemos por parámetro
            #el % hace una búsqueda amplia
            mi_cursor.execute("SELECT * FROM Usuarios WHERE Nombre LIKE ?",(self.ent_buscar_lista_usuarios.get()+'%',))
            datos_usuarios=mi_cursor.fetchall()
            #instertar las filas al treeview o tabla
            for fila in datos_usuarios:
                self.tree_lista_usuarios.insert('',0,fila[0],values=(fila[0], fila[1], fila[2], fila[3]))
            #aplicar cambios
            mi_conexion.commit()
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Buscar Usuarios', 'Ocurrió un error')
    def logueo_usuarios(self):

        try:


            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            con_usuario=self.ent_usuario.get()
            con_clave=self.ent_clave.get()


            #creamos la consulta. Desde usuarios donde nombre sea igual a lo que le pasemos en nombre y clave (nombre=?)
            mi_cursor.execute("SELECT * FROM Usuarios WHERE nombre=? AND Clave=?",(con_usuario,con_clave))
            datos_logueo=mi_cursor.fetchall()
            #si los datos de logueo son diferentes a vacío....entonces:
            if datos_logueo!='':
                for fila in datos_logueo:
                    self.codigo_usuario_logueado=fila[0]
                    self.nombre_usuario_logueado=fila[1]
                    clave_usuario_logueado=fila[2]
                if(self.nombre_usuario_logueado==self.ent_usuario.get()and clave_usuario_logueado==self.ent_clave.get()):
                    
                    self.ventana_menu()
                    self.frame_login.destroy()
            
            #aplicar cambios
            mi_conexion.commit()
            #cerrar la conexion
            mi_conexion.close()

        except:
            messagebox.showwarning('Logueo','el usuario o la clave son incorrectas')
    def ventana_nuevo_usuario(self):
        #poner una ventana flotante por encima de ventana de lista de usuarios
        self.frame_nuevo_usuario=Toplevel(master=self)
        self.frame_nuevo_usuario.title('Nuevo Usuario')
        self.centrar_ventana(self.frame_nuevo_usuario,400,350)
        #grab.set es una propiedad que impide que no se puede crear ninguna acción hasta que no se cierre la ventana
        self.frame_nuevo_usuario.grab_set()

        #colocamos el label frame en la ventana de nuevo usuario

        lblframen_nuevo_usuario=tb.LabelFrame(master=self.frame_nuevo_usuario, text='Nuevo Usuario') 
        lblframen_nuevo_usuario.pack(padx=15,pady=10)

        lbl_codigo_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Código')
        lbl_codigo_nuevo_usuario.grid(row=0,column=0,padx=10,pady=10)
        self.ent_codigo_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_codigo_nuevo_usuario.grid(row=0,column=1,padx=10,pady=10) 

        lbl_nombre_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Nombre')
        lbl_nombre_nuevo_usuario.grid(row=1,column=0,padx=10,pady=10)
        self.ent_nombre_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_nombre_nuevo_usuario.grid(row=1,column=1,padx=10,pady=10)

        lbl_clave_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Clave')
        lbl_clave_nuevo_usuario.grid(row=2,column=0,padx=10,pady=10)
        self.ent_clave_nuevo_usuario=tb.Entry(master=lblframen_nuevo_usuario,width=40)
        self.ent_clave_nuevo_usuario.grid(row=2,column=1,padx=10,pady=10)
        self.ent_clave_nuevo_usuario.config(show='*')         

        lbl_rol_nuevo_usuario=Label(master=lblframen_nuevo_usuario,text='Rol')
        lbl_rol_nuevo_usuario.grid(row=3,column=0,padx=10,pady=10)
        #elige nuevo usuario
        self.cbo_rol_nuevo_usuario=tb.Combobox(master=lblframen_nuevo_usuario, width=38, values=['Administrador','Bodega', 'Vendedor'])
        self.cbo_rol_nuevo_usuario.grid(row=3,column=1,padx=10,pady=10)
        #por defecto nos aparece la posición cero que sería el administrador
        self.cbo_rol_nuevo_usuario.current(0)
        self.cbo_rol_nuevo_usuario.config(state='readonly')

        btn_guardar_usuario=tb.Button(master=lblframen_nuevo_usuario,text='Guardar', width=38,bootstyle='success',command=self.guardar_usuarios)
        btn_guardar_usuario.grid(row=4,column=1,padx=10,pady=10)
        self.correlativo_usuarios()
        self.ent_nombre_nuevo_usuario.focus()
    def guardar_usuarios(self):
        if(self.ent_codigo_nuevo_usuario.get()==''or self.ent_nombre_nuevo_usuario.get()==''or self.ent_clave_nuevo_usuario.get()=='' or self.cbo_rol_nuevo_usuario.get()==''):
            messagebox.showerror('Guardando Usuarios', 'Por favor, llene todos los campos')
            return
        try:
            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            guardar_datos_usuarios=(self.ent_codigo_nuevo_usuario.get(), self.ent_nombre_nuevo_usuario.get(), self.ent_clave_nuevo_usuario.get(), self.cbo_rol_nuevo_usuario.get())



            #creamos la consulta. AQUÍ LOS INTERROGANTES ? SON CADA UNO DE LOS CAMPOS QUE SE GUARDAN: código o ID, Nombre, Clave, Rol etc
            mi_cursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)",(guardar_datos_usuarios))
            
            #aplicar cambios
            mi_conexion.commit()
            messagebox.showinfo('Guardando Usuarios', 'Registro guardado correctamente')
            #cerrar la ventana
            self.frame_nuevo_usuario.destroy()
            #refrescar la lista de usuarios
            self.buscar_usuarios('')
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Guardando usuarios','Ocurrió un Error')

        #validación para que los campos no queden vacíos
    def ventana_modificar_usuario(self):

        #Almacenamos el valor de lista de usuarios
        #pongo otra variable para extraer los datos del valor seleccionado
        self.usuario_seleccionado=self.tree_lista_usuarios.focus()
        self.valor_usuario_seleccionado=self.tree_lista_usuarios.item(self.usuario_seleccionado,'values')
        
        #condición si el valor de usuario es diferente o = a vacío:
        if self.valor_usuario_seleccionado!='':
        
            #poner una ventana flotante por encima de ventana de lista de usuarios
            self.frame_modificar_usuario=Toplevel(master=self)
            self.frame_modificar_usuario.title('Mofidicar Usuario')
            self.centrar_ventana(self.frame_modificar_usuario,400,350)
            #grab.set es una propiedad que impide que no se puede crear ninguna acción hasta que no se cierre la ventana
            self.frame_modificar_usuario.grab_set()

            #colocamos el label frame en la ventana de nuevo usuario

            lblframen_modificar_usuario=tb.LabelFrame(master=self.frame_modificar_usuario, text='Modificar Usuario') 
            lblframen_modificar_usuario.pack(padx=15,pady=10)

            lbl_codigo_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Código')
            lbl_codigo_modificar_usuario.grid(row=0,column=0,padx=10,pady=10)
            self.ent_codigo_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_codigo_modificar_usuario.grid(row=0,column=1,padx=10,pady=10) 

            lbl_nombre_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Nombre')
            lbl_nombre_modificar_usuario.grid(row=1,column=0,padx=10,pady=10)
            self.ent_nombre_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_nombre_modificar_usuario.grid(row=1,column=1,padx=10,pady=10)

            lbl_clave_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Clave')
            lbl_clave_modificar_usuario.grid(row=2,column=0,padx=10,pady=10)
            self.ent_clave_modificar_usuario=tb.Entry(master=lblframen_modificar_usuario,width=40)
            self.ent_clave_modificar_usuario.grid(row=2,column=1,padx=10,pady=10)
            self.ent_clave_modificar_usuario.config(show='*')         

            lbl_rol_modificar_usuario=Label(master=lblframen_modificar_usuario,text='Rol')
            lbl_rol_modificar_usuario.grid(row=3,column=0,padx=10,pady=10)
            #elige nuevo usuario
            self.cbo_rol_modificar_usuario=tb.Combobox(master=lblframen_modificar_usuario, width=38, values=['Administrador','Bodega', 'Vendedor'])
            self.cbo_rol_modificar_usuario.grid(row=3,column=1,padx=10,pady=10)
            #por defecto nos aparece la posición cero que sería el administrador

            btn_modificar_usuario=tb.Button(master=lblframen_modificar_usuario,text='Guardar', width=38,bootstyle='warning',command=self.modificar_usuarios)
            btn_modificar_usuario.grid(row=4,column=1,padx=10,pady=10) 

            self.llenar_entrys_modificar_usuarios()  
    #llenar los entrys con los valores que hemos seleccionado
    def llenar_entrys_modificar_usuarios(self):
        #borrar los datos de cada entry en el combobox para que no se se sobreescriba algo que hayamos introducido
        self.ent_codigo_modificar_usuario.delete(0,END)
        self.ent_nombre_modificar_usuario.delete(0,END)
        self.ent_clave_modificar_usuario.delete(0,END)
        self.cbo_rol_modificar_usuario.delete(0,END)

        self.ent_codigo_modificar_usuario.insert(0,self.valor_usuario_seleccionado[0])
        self.ent_codigo_modificar_usuario.config(state='readonly')
        self.ent_nombre_modificar_usuario.insert(0,self.valor_usuario_seleccionado[1])
        self.ent_clave_modificar_usuario.insert(0,self.valor_usuario_seleccionado[2])
        self.cbo_rol_modificar_usuario.insert(0,self.valor_usuario_seleccionado[3])
        self.cbo_rol_modificar_usuario.config(state='readonly')
    def modificar_usuarios(self):

        if(self.ent_codigo_modificar_usuario.get()==''or self.ent_nombre_modificar_usuario.get()==''or self.ent_clave_modificar_usuario.get()=='' or self.cbo_rol_modificar_usuario.get()==''):
            messagebox.showerror('Modificando Usuarios', 'Por favor, llene todos los campos')
            return
        try:
            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            modificar_datos_usuarios=( self.ent_nombre_modificar_usuario.get(), self.ent_clave_modificar_usuario.get(), self.cbo_rol_modificar_usuario.get())



            #creamos la consulta. AQUÍ LOS INTERROGANTES ? SON CADA UNO DE LOS CAMPOS QUE SE GUARDAN: código o ID, Nombre, Clave, Rol etc
            mi_cursor.execute("UPDATE Usuarios SET Nombre=?, Clave=?, Rol=? WHERE Codigo="+self.ent_codigo_modificar_usuario.get(),(modificar_datos_usuarios))
            
            #aplicar cambios
            mi_conexion.commit()
            messagebox.showinfo('Modificando Usuarios', 'Registro modificado correctamente')

            #refrescar la lista de usuarios
            self.valor_usuario_seleccionado=self.tree_lista_usuarios.item(self.usuario_seleccionado,text='', values=(self.ent_codigo_modificar_usuario.get(),self.ent_nombre_modificar_usuario.get(),self.ent_clave_modificar_usuario.get(), self.cbo_rol_modificar_usuario.get()))           
            
            #cerrar la ventana
            self.frame_modificar_usuario.destroy()
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Modificando usuarios','Ocurrió un Error')
    def eliminar_usuarios(self):
        #obtener el valor del usuario a eliminar de la lista de usuarios treeview
        #1/obtener foco
        usuario_seleccionado_eliminar=self.tree_lista_usuarios.focus()
        valor_usuario_seleccionado_eliminar=self.tree_lista_usuarios.item(usuario_seleccionado_eliminar,'values')
        #colocar capturador de errores

        try:

            #si el valor del usuario seleccionado es diferente o vacío entonces
            if valor_usuario_seleccionado_eliminar!='':
                respuesta=messagebox.askquestion('Eliminando Usuario','¿Está seguro de que quiere eliminar el usuario?')
                if respuesta=='yes':

                #conexion a la base de datos
                    mi_conexion=sqlite3.connect('Ventas.db')
                    #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
                    mi_cursor=mi_conexion.cursor()

                
                    #creamos la consulta
                    mi_cursor.execute("DELETE FROM Usuarios WHERE Codigo="+ str(valor_usuario_seleccionado_eliminar[0]))
                
                    #aplicar cambios
                    mi_conexion.commit()
                    messagebox.showinfo('Eliminando Usuarios','Registro elminado correctamente')
                    #que me muestre la lista de usuarios para refrescar treeview
                    self.buscar_usuarios('')
                    #cerrar la conexion
                    mi_conexion.close()
                else:
                    messagebox.showerror('Eliminando Usuario', 'Eliminación Cancelada')
        except:
            messagebox.showerror('Eliminando Usuario','Ocurrió un error')      
    def correlativo_usuarios(self):
        try:

            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            #creamos la consulta para buscar el usuario, con condición donde el nombre sea parecido a lo que pasemos por parámetro
            #el % hace una búsqueda amplia
            mi_cursor.execute("SELECT MAX(Codigo) FROM Usuarios")
            #coloco al final fetchone porque sólo necesito que me dé un dato
            correlativo_usuarios=mi_cursor.fetchone()
            for datos in correlativo_usuarios:
                #si no hay datos creo un nuevo correlativo de usuario
                if datos==None:
                    self.nuevo_correlativo_usuario=(int(1))
                    self.ent_codigo_nuevo_usuario.config(state=NORMAL)
                    #empezar correlativod desde posición 0, pasarle la variable nuevo correlativo usuario
                    self.ent_codigo_nuevo_usuario.insert(0,self.nuevo_correlativo_usuario)
                    #paso al final a estado sólo de lectura, para que no se modifique
                    self.ent_codigo_nuevo_usuario.state(state='readonly')
                else:
                    #si ya tuviera datos en la tabla, empezaría en los datos (4) y le sumaría 1=5
                    self.nuevo_correlativo_usuario=(int(datos)+1)
                    self.ent_codigo_nuevo_usuario.config(state=NORMAL)
                    #empezar correlativod desde posición 0, pasarle la variable nuevo correlativo usuario
                    self.ent_codigo_nuevo_usuario.insert(0,self.nuevo_correlativo_usuario)
                    #paso al final a estado sólo de lectura, para que no se modifique
                    self.ent_codigo_nuevo_usuario.config(state='readonly')

        
            #aplicar cambios
            mi_conexion.commit()
            #cerrar la conexion
            mi_conexion.close()

        except:
            messagebox.showerror('Correlativo Usuarios', 'Ocurrió un error')

#=======================PRODUCTOS==============================================

    def ventana_lista_productos(self):
        self.borrar_frames()
        self.frame_lista_productos=Frame(master=self.frame_center)
        self.frame_lista_productos.grid(row=0, column=1, columnspan=2, sticky=NSEW)
        lblframe_botones_lista_productos=tb.LabelFrame(master=self.frame_lista_productos)
        lblframe_botones_lista_productos.grid(row=0,column=0,sticky=NSEW, padx=5, pady=5)

        btn_nuevo_lista_productos=tb.Button(master=lblframe_botones_lista_productos,text='Nuevo',width=15,bootstyle='success', command=self.ventana_nuevo_producto)
        btn_nuevo_lista_productos.grid(row=0,column=0,padx=10,pady=10)

        btn_modificar_lista_productos=tb.Button(master=lblframe_botones_lista_productos,text='Modificar',width=15,bootstyle='warning',command=self.ventana_modificar_producto)
        btn_modificar_lista_productos.grid(row=0,column=1,padx=10,pady=10)

        btn_eliminar_lista_productos=tb.Button(master=lblframe_botones_lista_productos,text='Eliminar',width=15,bootstyle='danger', command=self.eliminar_producto)
        btn_eliminar_lista_productos.grid(row=0,column=2,padx=10,pady=10)

        lblframe_busqueda_lista_productos=tb.LabelFrame(master=self.frame_lista_productos)
        lblframe_busqueda_lista_productos.grid(row=1,column=0,padx=5,pady=5, sticky=NSEW)

        self.ent_buscar_lista_productos = tb.Entry(master=lblframe_busqueda_lista_productos, width=98)
        self.ent_buscar_lista_productos.grid(row=0, column=0, padx=10, pady=10)
        self.ent_buscar_lista_productos.bind('<KeyRelease>', self.buscar_productos)


        
        lblframe_tree_lista_productos=tb.LabelFrame(master=self.frame_lista_productos)
        lblframe_tree_lista_productos.grid(row=2,column=0,padx=5,pady=5, sticky=NSEW)

        #CREACIÓN DE COLUMNAS

        #el mínimo es para crear informes de inventario bajo

        columnas=("codigo", "nombre", "laboratorio", "coste", "precio","stock","minimo")

        #crear el treeview o tabla

        self.tree_lista_productos=tb.Treeview(master=lblframe_tree_lista_productos, height=17, columns=columnas,show='headings', bootstyle='success')
        self.tree_lista_productos.grid(row=0, column=0, padx=10, pady=10,)

        #creando encabezados o cabeceras

        self.tree_lista_productos.heading('codigo', text='Codigo', anchor=W)
        self.tree_lista_productos.heading('nombre', text='Descripción', anchor=W)
        self.tree_lista_productos.heading('laboratorio', text='Laboratorio', anchor=W)
        self.tree_lista_productos.heading('coste', text='Coste', anchor=W)
        self.tree_lista_productos.heading('precio', text='Precio', anchor=W)
        self.tree_lista_productos.heading('stock', text='Stock', anchor=W)
        self.tree_lista_productos.heading('minimo', text='Mínimo', anchor=W)


        #configurar las columnas que quiero que se muestren

        self.tree_lista_productos['displaycolumns']=('codigo','nombre','laboratorio','precio')

        #Ancho de las columnas, para que no los dé por defecto la tabla

        self.tree_lista_productos.column('codigo',width=100)
        self.tree_lista_productos.column('nombre',width=300)
        self.tree_lista_productos.column('laboratorio',width=200)
        self.tree_lista_productos.column('coste',width=100)
        self.tree_lista_productos.column('precio',width=100)
        self.tree_lista_productos.column('stock',width=100)
        self.tree_lista_productos.column('minimo',width=100)



        #Crear el Scrollbar o barra de scroll

        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_productos,bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=5, pady=10)

        #Configurar el Scrollbar

        tree_scroll.config(command=self.tree_lista_productos.yview)

        self.buscar_productos('')
        #la propiedad focus es para que se me marque el campo de texto de color
        self.ent_buscar_lista_productos.focus()
    def ventana_nuevo_producto(self):
        # Crear una ventana flotante por encima de la ventana de lista de usuarios
        self.frame_nuevo_producto = Toplevel(master=self)
        self.frame_nuevo_producto.title('Nuevo Producto')
        self.centrar_ventana(self.frame_nuevo_producto,400, 450)
        self.frame_nuevo_producto.grab_set()

        # Colocamos el label frame en la ventana de nuevo producto
        lblframen_nuevo_producto = tb.LabelFrame(master=self.frame_nuevo_producto, text='Nuevo Producto')
        lblframen_nuevo_producto.pack(padx=15, pady=15)

        # Código del producto
        lbl_codigo_nuevo_producto = Label(master=lblframen_nuevo_producto, text='Código')
        lbl_codigo_nuevo_producto.grid(row=0, column=0, padx=10, pady=10)
        self.ent_codigo_nuevo_producto = tb.Entry(master=lblframen_nuevo_producto, width=40)
        self.ent_codigo_nuevo_producto.grid(row=0, column=1, padx=10, pady=10)

        # Descripción del producto
        lbl_nombre_nuevo_producto = Label(master=lblframen_nuevo_producto, text='Descripción')
        lbl_nombre_nuevo_producto.grid(row=1, column=0, padx=10, pady=10)
        self.ent_nombre_nuevo_producto = tb.Entry(master=lblframen_nuevo_producto, width=40)
        self.ent_nombre_nuevo_producto.grid(row=1, column=1, padx=10, pady=10)

        # Laboratorio
        lbl_laboratorio_nuevo_producto = Label(master=lblframen_nuevo_producto, text='Laboratorio')
        lbl_laboratorio_nuevo_producto.grid(row=2, column=0, padx=10, pady=10)
        self.ent_laboratorio_nuevo_producto = tb.Entry(master=lblframen_nuevo_producto, width=40)
        self.ent_laboratorio_nuevo_producto.grid(row=2, column=1, padx=10, pady=10)

        # Coste
        lbl_coste_nuevo_producto = Label(master=lblframen_nuevo_producto, text='Coste')
        lbl_coste_nuevo_producto.grid(row=3, column=0, padx=10, pady=10)
        self.ent_coste_nuevo_producto = tb.Entry(master=lblframen_nuevo_producto, width=40)
        self.ent_coste_nuevo_producto.grid(row=3, column=1, padx=10, pady=10)

        # Precio
        lbl_precio_nuevo_producto = Label(master=lblframen_nuevo_producto, text='Precio')
        lbl_precio_nuevo_producto.grid(row=4, column=0, padx=10, pady=10)
        self.ent_precio_nuevo_producto = tb.Entry(master=lblframen_nuevo_producto, width=40)
        self.ent_precio_nuevo_producto.grid(row=4, column=1, padx=10, pady=10)

        # Stock
        lbl_stock_nuevo_producto = Label(master=lblframen_nuevo_producto, text='Stock')
        lbl_stock_nuevo_producto.grid(row=5, column=0, padx=10, pady=10)
        self.ent_stock_nuevo_producto = tb.Entry(master=lblframen_nuevo_producto, width=40)
        self.ent_stock_nuevo_producto.grid(row=5, column=1, padx=10, pady=10)

        # Mínimo
        lbl_minimo_nuevo_producto = Label(master=lblframen_nuevo_producto, text='Mínimo')
        lbl_minimo_nuevo_producto.grid(row=6, column=0, padx=10, pady=10)
        self.ent_minimo_nuevo_producto = tb.Entry(master=lblframen_nuevo_producto, width=40)
        self.ent_minimo_nuevo_producto.grid(row=6, column=1, padx=10, pady=10)

        # Botón para guardar el producto
        btn_guardar_producto = tb.Button(master=lblframen_nuevo_producto, text='Guardar', width=38, bootstyle='success',command=self.guardar_productos)
        btn_guardar_producto.grid(row=7, column=1, padx=10, pady=10)
        self.correlativo_productos()
        self.ent_nombre_nuevo_producto.focus()
    def guardar_productos(self):

        if(self.ent_codigo_nuevo_producto.get()==''or self.ent_nombre_nuevo_producto.get()==''or self.ent_laboratorio_nuevo_producto.get()=='' 
           or self.ent_coste_nuevo_producto.get()=='' or self.ent_precio_nuevo_producto.get()=='' or self.ent_stock_nuevo_producto.get()=='' or self.ent_minimo_nuevo_producto.get()==''):

            messagebox.showerror('Guardando Productos', 'Por favor, llene todos los campos')
            return
        try:
            float(self.ent_coste_nuevo_producto.get())
            float(self.ent_precio_nuevo_producto.get())
            int(self.ent_stock_nuevo_producto.get())
            int(self.ent_minimo_nuevo_producto.get())
            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            guardar_datos_productos=(self.ent_codigo_nuevo_producto.get(), self.ent_nombre_nuevo_producto.get(), self.ent_laboratorio_nuevo_producto.get(), self.ent_precio_nuevo_producto.get(),
            self.ent_precio_nuevo_producto.get(), self.ent_stock_nuevo_producto.get(),self.ent_minimo_nuevo_producto.get())



            #creamos la consulta. AQUÍ LOS INTERROGANTES ? SON CADA UNO DE LOS CAMPOS QUE SE GUARDAN: código o ID, Nombre, Clave, Rol etc
            mi_cursor.execute("INSERT INTO Productos VALUES(?,?,?,?,?,?,?)",(guardar_datos_productos))
            
            #aplicar cambios
            mi_conexion.commit()
            messagebox.showinfo('Guardando Productos', 'Producto guardado correctamente')
            #cerrar la ventana
            self.frame_nuevo_producto.destroy()
            #refrescar la lista de usuarios
            self.buscar_productos('')
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Guardando Productos','Ocurrió un Error')
    def buscar_productos(self,event):
        
        try:

            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            #limpiar nuestro treeview o tabla
            #el método .get_children() nos trae todos los registros
            registro=self.tree_lista_productos.get_children()
            for elementos in registro: 
                self.tree_lista_productos.delete(elementos)

            #creamos la consulta para buscar el usuario, con condición donde el nombre sea parecido a lo que pasemos por parámetro
            #el % hace una búsqueda amplia
            mi_cursor.execute("SELECT * FROM Productos WHERE Nombre LIKE ?",(self.ent_buscar_lista_productos.get()+'%',))
            datos_productos=mi_cursor.fetchall()
            #instertar las filas al treeview o tabla
            for fila in datos_productos:
                self.tree_lista_productos.insert('',0,fila[0],values=(fila[0], fila[1],fila[2],fila[3],fila[4],fila[5],fila[6],))
            #aplicar cambios
            mi_conexion.commit()
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Buscar Productos', 'Ocurrió un error')
    def correlativo_productos(self):
        
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Consulta para obtener el máximo valor de Codigo
            mi_cursor.execute("SELECT MAX(Codigo) FROM Productos")
            correlativo_productos = mi_cursor.fetchone()

            # Verificamos el resultado de la consulta
            if correlativo_productos[0] is None:
                self.nuevo_correlativo_producto = 1
            else:
                self.nuevo_correlativo_producto = int(correlativo_productos[0]) + 1

            # Configurar el Entry para mostrar el nuevo correlativo
            self.ent_codigo_nuevo_producto.config(state=NORMAL)
            self.ent_codigo_nuevo_producto.delete(0, 'end')
            self.ent_codigo_nuevo_producto.insert(0, self.nuevo_correlativo_producto)
            self.ent_codigo_nuevo_producto.config(state='readonly')

            # Aplicar cambios y cerrar la conexión
            mi_conexion.commit()
            mi_conexion.close()

        except Exception as e:
            messagebox.showerror('Correlativo Productos', f'Ocurrió un error: {e}')
    def ventana_modificar_producto(self):
        
        self.producto_seleccionado=self.tree_lista_productos.focus()
        self.valor_producto_seleccionado=self.tree_lista_productos.item(self.producto_seleccionado,'values')
        
        #condición si el valor de usuario es diferente o = a vacío:
        if self.valor_producto_seleccionado!='':
            # Crear una ventana flotante por encima de la ventana de lista de usuarios
            self.frame_modificar_producto = Toplevel(master=self)
            self.frame_modificar_producto.title('Modificar Producto')
            self.centrar_ventana(self.frame_modificar_producto,400, 450)
            self.frame_modificar_producto.grab_set()

            # Colocamos el label frame en la ventana de nuevo producto
            lblframen_modificar_producto = tb.LabelFrame(master=self.frame_modificar_producto, text='Modificar Producto')
            lblframen_modificar_producto.pack(padx=15, pady=15)

            # Código del producto
            lbl_codigo_modificar_producto = Label(master=lblframen_modificar_producto, text='Código')
            lbl_codigo_modificar_producto.grid(row=0, column=0, padx=10, pady=10)
            self.ent_codigo_modificar_producto = tb.Entry(master=lblframen_modificar_producto, width=40)
            self.ent_codigo_modificar_producto.grid(row=0, column=1, padx=10, pady=10)

            # Descripción del producto
            lbl_nombre_modificar_producto = Label(master=lblframen_modificar_producto, text='Descripción')
            lbl_nombre_modificar_producto.grid(row=1, column=0, padx=10, pady=10)
            self.ent_nombre_modificar_producto = tb.Entry(master=lblframen_modificar_producto, width=40)
            self.ent_nombre_modificar_producto.grid(row=1, column=1, padx=10, pady=10)

            # Laboratorio
            lbl_laboratorio_modificar_producto = Label(master=lblframen_modificar_producto, text='Laboratorio')
            lbl_laboratorio_modificar_producto.grid(row=2, column=0, padx=10, pady=10)
            self.ent_laboratorio_modificar_producto = tb.Entry(master=lblframen_modificar_producto, width=40)
            self.ent_laboratorio_modificar_producto.grid(row=2, column=1, padx=10, pady=10)

            # Coste
            lbl_coste_modificar_producto = Label(master=lblframen_modificar_producto, text='Coste')
            lbl_coste_modificar_producto.grid(row=3, column=0, padx=10, pady=10)
            self.ent_coste_modificar_producto = tb.Entry(master=lblframen_modificar_producto, width=40)
            self.ent_coste_modificar_producto.grid(row=3, column=1, padx=10, pady=10)

            # Precio
            lbl_precio_modificar_producto = Label(master=lblframen_modificar_producto, text='Precio')
            lbl_precio_modificar_producto.grid(row=4, column=0, padx=10, pady=10)
            self.ent_precio_modificar_producto = tb.Entry(master=lblframen_modificar_producto, width=40)
            self.ent_precio_modificar_producto.grid(row=4, column=1, padx=10, pady=10)

            # Stock
            lbl_stock_modificar_producto = Label(master=lblframen_modificar_producto, text='Stock')
            lbl_stock_modificar_producto.grid(row=5, column=0, padx=10, pady=10)
            self.ent_stock_modificar_producto = tb.Entry(master=lblframen_modificar_producto, width=40)
            self.ent_stock_modificar_producto.grid(row=5, column=1, padx=10, pady=10)

            # Mínimo
            lbl_minimo_modificar_producto = Label(master=lblframen_modificar_producto, text='Mínimo')
            lbl_minimo_modificar_producto.grid(row=6, column=0, padx=10, pady=10)
            self.ent_minimo_modificar_producto = tb.Entry(master=lblframen_modificar_producto, width=40)
            self.ent_minimo_modificar_producto.grid(row=6, column=1, padx=10, pady=10)

            # Botón para modificar el producto
            btn_modificar_producto = tb.Button(master=lblframen_modificar_producto, text='Modificar', width=38, bootstyle='warning',command=self.modificar_producto)
            btn_modificar_producto.grid(row=7, column=1, padx=10, pady=10)
            self.llenar_entrys_modificar_productos()
            self.ent_nombre_modificar_producto.focus()
    def llenar_entrys_modificar_productos(self):
        #borrar los datos de cada entry en el combobox para que no se se sobreescriba algo que hayamos introducido
        self.ent_codigo_modificar_producto.delete(0,END)
        self.ent_nombre_modificar_producto.delete(0,END)
        self.ent_laboratorio_modificar_producto.delete(0,END)
        self.ent_coste_modificar_producto.delete(0,END)
        self.ent_precio_modificar_producto.delete(0,END)
        self.ent_stock_modificar_producto.delete(0,END)
        self.ent_minimo_modificar_producto.delete(0,END)

        #llamamos entre paréntesis al valor del producto seleccionado
        self.ent_codigo_modificar_producto.config(state=NORMAL)
        self.ent_codigo_modificar_producto.insert(0,self.valor_producto_seleccionado[0])
        self.ent_codigo_modificar_producto.config(state='readonly')
        self.ent_nombre_modificar_producto.insert(0,self.valor_producto_seleccionado[1])
        self.ent_laboratorio_modificar_producto.insert(0,self.valor_producto_seleccionado[2])
        self.ent_coste_modificar_producto.insert(0,self.valor_producto_seleccionado[3])
        self.ent_precio_modificar_producto.insert(0,self.valor_producto_seleccionado[4])
        self.ent_stock_modificar_producto.config(state=NORMAL)
        self.ent_stock_modificar_producto.insert(0,self.valor_producto_seleccionado[5])
        self.ent_stock_modificar_producto.config(state='readonly')
        self.ent_minimo_modificar_producto.insert(0,self.valor_producto_seleccionado[6])
    def modificar_producto(self):
       
        try:
            float(self.ent_coste_modificar_producto.get())
            float(self.ent_precio_modificar_producto.get())
            int(self.ent_stock_modificar_producto.get())
            int(self.ent_minimo_modificar_producto.get())
            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()

            modificar_datos_productos=(self.ent_nombre_modificar_producto.get(), self.ent_laboratorio_modificar_producto.get(), self.ent_coste_modificar_producto.get(),
            self.ent_precio_modificar_producto.get(), self.ent_stock_modificar_producto.get(),self.ent_minimo_modificar_producto.get())



            #creamos la consulta. AQUÍ LOS INTERROGANTES ? SON CADA UNO DE LOS CAMPOS QUE SE GUARDAN: código o ID, Nombre, Clave, Rol etc
            mi_cursor.execute("UPDATE Productos SET Nombre=?, Laboratorio=?, Coste=?, Precio=?, Stock=?, Minimo=? WHERE Codigo="+self.ent_codigo_modificar_producto.get(),(modificar_datos_productos))
            
            #aplicar cambios
            mi_conexion.commit()
            messagebox.showinfo('Modificando Productos', 'Producto modificado correctamente')

            #refrescar la lista de productos
            self.valor_producto_seleccionado=self.tree_lista_productos.item(self.producto_seleccionado,text='', values=(self.ent_codigo_modificar_producto.get(), self.ent_nombre_modificar_producto.get(), self.ent_laboratorio_modificar_producto.get(), self.ent_coste_modificar_producto.get(),
            self.ent_precio_modificar_producto.get(), self.ent_stock_modificar_producto.get(),self.ent_minimo_modificar_producto.get()))           
            
            #cerrar la ventana
            self.frame_modificar_producto.destroy()
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Modificando usuarios','Ocurrió un Error')
    def eliminar_producto(self):

        #obtener el valor del usuario a eliminar de la lista de usuarios treeview
        #1/obtener foco
        producto_seleccionado_eliminar=self.tree_lista_productos.focus()
        valor_producto_seleccionado_eliminar=self.tree_lista_productos.item(producto_seleccionado_eliminar,'values')
        #colocar capturador de errores

        try:

            #si el valor del usuario seleccionado es diferente o vacío entonces
            if valor_producto_seleccionado_eliminar!='':
                respuesta=messagebox.askquestion('Eliminando Producto','¿Está seguro de que quiere eliminar el producto?')
                if respuesta=='yes':

                #conexion a la base de datos
                    mi_conexion=sqlite3.connect('Ventas.db')
                    #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
                    mi_cursor=mi_conexion.cursor()

                
                    #creamos la consulta
                    mi_cursor.execute("DELETE FROM Productos WHERE Codigo="+ str(valor_producto_seleccionado_eliminar[0]))
                
                    #aplicar cambios
                    mi_conexion.commit()
                    messagebox.showinfo('Eliminando Productos','Producto elminado correctamente')
                    #que me muestre la lista de usuarios para refrescar treeview
                    self.buscar_productos('')
                    #cerrar la conexion
                    mi_conexion.close()
                else:
                    messagebox.showerror('Eliminando Producto', 'Eliminación Cancelada')
        except:
            messagebox.showerror('Eliminando Producto','Ocurrió un error')
    
#=======================VENTAS=========================================================   
    
    
    def ventana_detalle_venta(self):
        self.borrar_frames()
        self.frame_detalle_venta=Frame(master=self.frame_center)
        self.frame_detalle_venta.grid(row=0, column=1, sticky=NSEW)
        
        lblframe_botones_detalle_venta=tb.LabelFrame(master=self.frame_detalle_venta)
        lblframe_botones_detalle_venta.grid(row=0,column=0,sticky=NSEW, padx=5, pady=5)

        btn_detalle=tb.Button(master=lblframe_botones_detalle_venta,text='Detalle',width=15,bootstyle='info',command=self.ventana_listado_ventas)
        btn_detalle.grid(row=0,column=0,padx=10,pady=10)

        btn_cantidad=tb.Button(master=lblframe_botones_detalle_venta,text='Cantidad',width=15,bootstyle='warning',command=self.ventana_modificar_cantidad)
        btn_cantidad.grid(row=0,column=1,padx=10,pady=10)

        btn_borrar=tb.Button(master=lblframe_botones_detalle_venta,text='Borrar',width=15,bootstyle='danger',command=self.borrar_producto_detalle_venta)
        btn_borrar.grid(row=0,column=2,padx=10,pady=10)

        btn_descuento=tb.Button(master=lblframe_botones_detalle_venta,text='Descuento',width=15,bootstyle='success',command=self.ventana_descuento)
        btn_descuento.grid(row=0,column=3,padx=10,pady=10)

        btn_cobrar=tb.Button(master=lblframe_botones_detalle_venta,text='Cobrar',width=15,bootstyle='warning',command=self.ventana_contado)
        btn_cobrar.grid(row=0,column=4,padx=10,pady=10)

        btn_credito=tb.Button(master=lblframe_botones_detalle_venta,text='Crédito',width=15,bootstyle='danger')
        btn_credito.grid(row=0,column=5,padx=10,pady=10)
       
       
        self.busqueda_codigo()
        self.busqueda_descripcion()
        
        lblframe_tree_lista_detalle_venta=tb.LabelFrame(master=self.frame_detalle_venta)
        lblframe_tree_lista_detalle_venta.grid(row=2,column=0,padx=5,pady=5, sticky=NSEW)

        #CREACIÓN DE COLUMNAS

        #el mínimo es para crear informes de inventario bajo

        columnas=("numero", "codigo", "descripcion", "coste", "precio","cantidad","stock", "descuento", "subtotal", "existencias")

        #crear el treeview o tabla

        self.tree_detalle_venta=tb.Treeview(master=lblframe_tree_lista_detalle_venta, height=40, columns=columnas,show='headings', bootstyle='success')
        self.tree_detalle_venta.grid(row=0, column=0, padx=10, pady=10,)

        #creando encabezados o cabeceras

        self.tree_detalle_venta.heading('numero', text='No', anchor=W)
        self.tree_detalle_venta.heading('codigo', text='Codigo', anchor=W)   
        self.tree_detalle_venta.heading('descripcion', text='Descripción', anchor=W)
        self.tree_detalle_venta.heading('coste', text='Coste', anchor=W)
        self.tree_detalle_venta.heading('precio', text='Precio', anchor=W)
        self.tree_detalle_venta.heading('cantidad', text='Cant', anchor=W)
        self.tree_detalle_venta.heading('stock', text='Stock', anchor=W)
        self.tree_detalle_venta.heading('descuento', text='Desc', anchor=W)
        self.tree_detalle_venta.heading('subtotal', text='Subtotal', anchor=W)
        self.tree_detalle_venta.heading('existencias', text='Exist', anchor=W)



        #configurar las columnas que quiero que se muestren

        self.tree_detalle_venta['displaycolumns']=('codigo', 'descripcion','precio','cantidad', 'subtotal','existencias')

        #Ancho de las columnas, para que no los dé por defecto la tabla

        self.tree_detalle_venta.column('numero',width=70)
        self.tree_detalle_venta.column('codigo',width=70)
        self.tree_detalle_venta.column('descripcion',width=300)
        self.tree_detalle_venta.column('coste',width=100)
        self.tree_detalle_venta.column('precio',width=100)
        self.tree_detalle_venta.column('cantidad',width=100)
        self.tree_detalle_venta.column('stock',width=100)
        self.tree_detalle_venta.column('descuento',width=100)
        self.tree_detalle_venta.column('subtotal',width=100)
        self.tree_detalle_venta.column('existencias',width=100)





        #Crear el Scrollbar o barra de scroll

        tree_scroll=tb.Scrollbar(master=lblframe_tree_lista_detalle_venta,bootstyle='success-round')
        tree_scroll.grid(row=0, column=1, padx=5, pady=10)

        #Configurar el Scrollbar

        tree_scroll.config(command=self.tree_detalle_venta.yview)
        
        #TOTAL DETALLE VENTAS
        
        lblframe_total_detalle_venta = tb.LabelFrame(master=self.frame_detalle_venta)
        lblframe_total_detalle_venta.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)

        # Hacer que el Entry ocupe el 100% del ancho del LabelFrame
        self.ent_total_detalle_venta = tb.Entry(master=lblframe_total_detalle_venta, font=('calibri', 18), justify=RIGHT)
        self.ent_total_detalle_venta.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        # Configurar la columna para expandirse
        lblframe_total_detalle_venta.grid_rowconfigure(0, weight=1)
        lblframe_total_detalle_venta.grid_columnconfigure(0, weight=1)

        #self.buscar_productos('')
        #la propiedad focus es para que se me marque el campo de texto de color
        self.ent_buscar_detalle_venta.focus()
        self.ventana_busqueda_detalle_venta()
        self.mostrar_producto_detalle_venta()
        #como este método recibe unos parámetros se le colocan las comillas
        self.buscar_productos_detalle_venta('')
        self.total_detalle_venta()
        self.correlativo_ventas()
    def busqueda_descripcion(self):
       
        lblframe_busqueda_detalle_venta=tb.LabelFrame(master=self.frame_detalle_venta)
        lblframe_busqueda_detalle_venta.grid(row=1,column=0,padx=5,pady=5, sticky=NSEW)

        self.btn_busqueda_descripcion = tb.Button(master=lblframe_busqueda_detalle_venta, width=10, text='abc', bootstyle='success-outline',command=self.busqueda_codigo)
        self.btn_busqueda_descripcion.grid(row=0,column=0,padx=10, pady=10)

        self.ent_buscar_detalle_venta = tb.Entry(master=lblframe_busqueda_detalle_venta, font=14, width=61)
        self.ent_buscar_detalle_venta.grid(row=0, column=1, padx=10, pady=10)


        self.ent_buscar_detalle_venta.bind('<KeyRelease>', self.buscar_productos_detalle_venta)
    def busqueda_codigo(self):
        
        lblframe_busqueda_detalle_venta=tb.LabelFrame(master=self.frame_detalle_venta)
        lblframe_busqueda_detalle_venta.grid(row=1,column=0,padx=5,pady=5, sticky=NSEW)

        self.btn_busqueda_codigo= tb.Button(master=lblframe_busqueda_detalle_venta,width=10, text='#id', bootstyle='success-outline', command=self.busqueda_descripcion)
        self.btn_busqueda_codigo.grid(row=0,column=0,padx=10, pady=10)

        self.ent_buscar_codigo_detalle_venta = tb.Entry(master=lblframe_busqueda_detalle_venta, font=14, width=61)
        self.ent_buscar_codigo_detalle_venta.grid(row=0, column=1, padx=10, pady=10)
        self.ent_buscar_codigo_detalle_venta.bind('<Return>',self.producto_encontrado_detalle_venta)
    #scroll frame. Frame del lado derecho, donde están todos los productos
    def ventana_busqueda_detalle_venta(self):
        self.frame_busqueda_detalle_venta=ScrolledFrame(master=self, width=600, autohide=True)
        self.frame_busqueda_detalle_venta.grid(row=0,column=2,padx=10,pady=10,sticky=NSEW)
        #NSEW es sticky a los cuatro lados   
    #Busca una serie de productos en la base de datos y los muestra en el scroll frame
    def buscar_productos_detalle_venta(self,event):
        try:

            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()
            #limpiar nuestro scrollframe con ciclo 'for' recorriendo los widgets que tenga ese scrollframe dentro
            for wid in self.frame_busqueda_detalle_venta.winfo_children():
                wid.destroy()
            # Crear la consulta para buscar productos cuyo nombre se parezca al texto ingresado
            mi_cursor.execute("SELECT * FROM Productos WHERE Nombre LIKE ?",(self.ent_buscar_detalle_venta.get()+'%',))
            datos_productos_detalle_venta=mi_cursor.fetchall()
            #variable para almacenar el código del producto
            codigo_busqueda_detalle_venta=StringVar()
            contador=0
            filas=2

            #me va a poner dos botones por cada fila
            #quiero que me traiga el nombre, que está en la fila 1, el valor que le vamos a pasar al radio button será el código en fila 0 
            for fila in datos_productos_detalle_venta:
                radbuton=Radiobutton(master=self.frame_busqueda_detalle_venta,text=fila[1]+'\n'+ fila[2]+'\n'+'\n'+str(f'{fila[4]:,.2f}€ IVA inc'),value=fila[0]
                ,variable=codigo_busqueda_detalle_venta, indicator=0, width=37, height=5, command=lambda:self.pasar_codigo_detalle_venta(codigo_busqueda_detalle_venta.get()))
                radbuton.grid(row=contador//filas,column=contador%filas)
                contador+= 1
            #aplicar cambios
            mi_conexion.commit()
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Buscar Productos', 'Ocurrió un error')
    #Esta función inserta el código del producto seleccionado en el campo de entrada correspondiente # y llama a la función para procesar los productos seleccionados
    def pasar_codigo_detalle_venta(self, codigo_seleccionado_detalle_venta):
         self.ent_buscar_codigo_detalle_venta.insert(0,codigo_seleccionado_detalle_venta)
         self.producto_encontrado_detalle_venta('')   
    # busca el producto y prepara los datos para su inserción a DetalleVentaT si tiene stock. Por último, llama a las funciones de agregar y mostrar el producto en la TABLA DE DETALLES VENTA
    def productos_seleccionados_detalle_venta(self):
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Consulta para buscar el producto en la tabla Productos
            mi_cursor.execute("SELECT * FROM Productos WHERE Codigo = ?", (self.ent_buscar_codigo_detalle_venta.get(),))
            datos_productos_seleccionados = mi_cursor.fetchall()

            if datos_productos_seleccionados:
                # Guardar las filas en una variable para guardar y agregar en tabla DetalleVentaT
                for fila in datos_productos_seleccionados:
                    self.datos_guardar_producto_detalle_venta = (int(self.nuevo_correlativo_ventas), fila[0], fila[1], fila[3], fila[4], '1', fila[5], '0')
                # Agregar a DetalleVentaT
                self.agregar_producto_detalle_venta()
                self.mostrar_producto_detalle_venta()

            # Aplicar cambios
            mi_conexion.commit()
        except sqlite3.Error as e:
            messagebox.showerror('Producto Seleccionado', f'Ocurrió un error en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Producto Seleccionado', f'Ocurrió un error: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()
    #agrega productos a la tabla de DetalleVentaT, PERO NO SE VISUALIZA EN LA TABLA
    def agregar_producto_detalle_venta(self):
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Comprobar que datos_guardar_producto_detalle_venta es una tupla con el número correcto de elementos
            if len(self.datos_guardar_producto_detalle_venta) == 8:
                # Insertar los datos en DetalleVentaT
                mi_cursor.execute("INSERT INTO DetalleVentaT VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                self.datos_guardar_producto_detalle_venta)
                
                # Aplicar cambios
                mi_conexion.commit()
                messagebox.showinfo('Agregando Productos Detalle Venta', 'Registro agregado correctamente')
            else:
                messagebox.showwarning('Datos Incorrectos', 'Los datos para agregar el producto no son válidos.')

        except sqlite3.IntegrityError as e:
            messagebox.showerror('Error de Integridad', f'Error de integridad en la base de datos: {e}')
        except sqlite3.OperationalError as e:
            messagebox.showerror('Error de Operación', f'Error de operación en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Agregando Productos Detalle Venta', f'Ocurrió un error: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()
    #Actualiza la interfaz Detalles de Venta de usuario con los datos de DetalleVentaT.
    def mostrar_producto_detalle_venta(self):
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Limpiar el treeview o tabla
            registro = self.tree_detalle_venta.get_children()
            for elementos in registro:
                self.tree_detalle_venta.delete(elementos)

            # Consulta para obtener los datos de DetalleVentaT
            mi_cursor.execute("SELECT * FROM DetalleVentaT")
            self.datos_productos_detalle_venta = mi_cursor.fetchall()

            # Insertar las filas en el treeview o tabla
            for fila in self.datos_productos_detalle_venta:
                # Calcular el subtotal y la existencia
                subtotal = float(fila[4] * fila[5])
                existencia = int(fila[6] - fila[5])
                self.tree_detalle_venta.insert('', 'end', text=fila[0], values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], subtotal, existencia))

            # Cerrar la conexión
            mi_conexion.close()
        except sqlite3.Error as e:
            messagebox.showerror('Buscar Productos Detalle Venta', f'Ocurrió un error en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Buscar Productos Detalle Venta', f'Ocurrió un error: {e}')
    #Maneja la lógica para verificar si un producto está disponible en DetalleVentaT y Productos, y decide si debe agregar el producto a DetalleVentaT o simplemente actualizar la cantidad existente.
    def producto_encontrado_detalle_venta(self,event):
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            codigo = self.ent_buscar_codigo_detalle_venta.get()

            # Consulta para encontrar el producto en DetalleVentaT
            mi_cursor.execute("SELECT * FROM DetalleVentaT WHERE Codigo = ?", (codigo,))
            producto_encontrado = mi_cursor.fetchall()

            if producto_encontrado:
                for fila in producto_encontrado:
                    cantidad_actual = fila[5]
                    stock_actual = fila[6]
                    existencia = int(stock_actual - cantidad_actual)
                    if existencia == 0:
                        messagebox.showwarning('Existencias', 'Producto sin Existencias')
                        self.ent_buscar_codigo_detalle_venta.delete(0, END)
                        return
                # Si el producto está en DetalleVentaT y tiene existencia, sumar uno
                self.sumar_uno_detalle_venta()
            else:
                # Consulta para encontrar el stock del producto en Productos
                mi_cursor.execute("SELECT Stock FROM Productos WHERE Codigo = ?", (codigo,))
                producto_no_encontrado = mi_cursor.fetchall()
                if producto_no_encontrado:
                    for fila in producto_no_encontrado:
                        stock = fila[0]
                        if stock == 0:
                            messagebox.showwarning('Existencias', 'Producto sin Existencias')
                            self.ent_buscar_codigo_detalle_venta.delete(0, END)
                            return
                    # Si el producto tiene stock, agregar a DetalleVentaT
                    self.productos_seleccionados_detalle_venta()
                    self.total_detalle_venta()
                else:
                    messagebox.showerror('Producto', 'Producto no encontrado en la base de datos principal')

            # Aplicar cambios
            mi_conexion.commit()
        except sqlite3.Error as e:
            messagebox.showerror('Producto', f'Ocurrió un error en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Producto', f'Ocurrió un error: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()
            self.ent_buscar_codigo_detalle_venta.delete(0, END)
            self.total_detalle_venta()
    def sumar_uno_detalle_venta(self):
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Obtener el código del producto
            codigo = self.ent_buscar_codigo_detalle_venta.get()

            # Consulta para actualizar la cantidad del producto en DetalleVentaT
            mi_cursor.execute("UPDATE DetalleVentaT SET Cantidad = Cantidad + 1 WHERE Codigo = ?", (codigo,))

            # Aplicar cambios
            mi_conexion.commit()
            self.mostrar_producto_detalle_venta()
        except sqlite3.Error as e:
            messagebox.showerror('Sumar uno detalle de venta', f'Ocurrió un error en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Sumar uno detalle de venta', f'Ocurrió un error: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()
    def borrar_producto_detalle_venta(self):
        #obtener el valor del usuario a eliminar de la lista de usuarios treeview
        #1/obtener foco
        producto_seleccionado_eliminar=self.tree_detalle_venta.focus()
        valor_producto_seleccionado_eliminar=self.tree_detalle_venta.item(producto_seleccionado_eliminar,'values')
        #colocar capturador de errores

        if valor_producto_seleccionado_eliminar!='':
 
            try:

                    #conexion a la base de datos
                    mi_conexion=sqlite3.connect('Ventas.db')
                    #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
                    mi_cursor=mi_conexion.cursor()

                
                    #creamos la consulta. Eliminamos el valor del producto venta con el 1, QUE ES EL PRODUCTO. El 0 no, porque es el número de venta
                    mi_cursor.execute("DELETE FROM DetalleVentaT WHERE Codigo="+ str(valor_producto_seleccionado_eliminar[1]))
                
                    #aplicar cambios
                    mi_conexion.commit()
                    messagebox.showinfo('Eliminando Producto Detalle Venta','Registro elminado correctamente')
                    #que me muestre la lista de productos detalle venta para refrescar treeview
                    self.mostrar_producto_detalle_venta()
                    self.total_detalle_venta()
                    #cerrar la conexion
                    mi_conexion.close()
           
            except:
                messagebox.showerror('Eliminando Producto','Ocurrió un error')    
    def total_detalle_venta(self):
        #variable que colocamos en 0. Para fila en el tree de detalle venta, pasamos la propiedad al tree 'get_children' para que pase por sus hijos
        self.total=0
        for fila in self.tree_detalle_venta.get_children():
        #al total le incrementamos lo que tenga nuestros datos del tree detalle venta, le pasamos el valor de la fila 8, que es subtotal
        #establecemos el total de la suma de la fila 8
            self.total+=float(self.tree_detalle_venta.item(fila,'values')[8])

        self.ent_total_detalle_venta.config(state=NORMAL)
        self.ent_total_detalle_venta.delete(0,END)
        self.ent_total_detalle_venta.insert(0,f'{self.total:,.2f}€ IVA Inc.')
        self.ent_total_detalle_venta.config(state='readonly')
    def ventana_modificar_cantidad(self):

        #Almacenamos el valor de lista de usuarios
        #pongo otra variable para extraer los datos del valor seleccionado
        self.cantidad_seleccionada=self.tree_detalle_venta.focus()
        self.valor_cantidad_seleccionada=self.tree_detalle_venta.item(self.cantidad_seleccionada,'values')
        
        #condición si el valor de usuario es diferente o = a vacío:
        if self.valor_cantidad_seleccionada!='':
        
            #poner una ventana flotante por encima de ventana de lista de usuarios
            self.frame_modificar_cantidad=Toplevel(master=self)
            self.frame_modificar_cantidad.title('Mofidicar Cantidad')
            self.centrar_ventana(self.frame_modificar_cantidad,350,350)
            #grab.set es una propiedad que impide que no se puede crear ninguna acción hasta que no se cierre la ventana
            self.frame_modificar_cantidad.grab_set()

            #generamos una variable y guardarmos el valor de la cantidad seleccionada           
            variable_descripcion=(self.valor_cantidad_seleccionada[2])

            lbl_descripcion_cantidad=tb.Label(master=self.frame_modificar_cantidad,text='Producto', font=('Calibri', 16),bootstyle='success')
            lbl_descripcion_cantidad.pack(padx=10,pady=35)
            #aquí USAMOS LA VARIABLE CREADA ARRIBA Y LE VAMOS A PASAR EL TEXT CON VARIABLE DESCRIPCIÓN, PARA ALMACENAR LA DESCRIPCIÓN
            lbl_descripcion_cantidad.config(text=variable_descripcion)

            lbl_cantidad_modificar=Label(master=self.frame_modificar_cantidad,text='Cantidad',font=14)
            lbl_cantidad_modificar.pack(padx=10,pady=5)

            self.ent_cantidad_modificar_detalle=tb.Entry(master=self.frame_modificar_cantidad,justify=CENTER,font=14)
            self.ent_cantidad_modificar_detalle.pack(padx=10,pady=15)
            self.ent_cantidad_modificar_detalle.insert(0,self.valor_cantidad_seleccionada[5])
            self.ent_cantidad_modificar_detalle.bind('<Return>',self.modificar_cantidad_detalle_venta)

            self.ent_cantidad_modificar_detalle.focus()      
    def modificar_cantidad_detalle_venta(self,event):
        
        
        try:    

            int(self.ent_cantidad_modificar_detalle.get())
            
            if self.ent_cantidad_modificar_detalle.get()==0:
                messagebox.showerror('Modificando Cantidad', 'La cantidad no es válida')
                return
            #generamos otra condición por la cual si la cantidad que introduzco es mayor al valor de cantidad del producto seleccionado
            if int(self.ent_cantidad_modificar_detalle.get())>int(self.valor_cantidad_seleccionada[6]):
                messagebox.showerror('Modificando Cantidad', 'Existencia insuficiente')
                return


            #conexion a la base de datos
            mi_conexion=sqlite3.connect('Ventas.db')
            #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
            mi_cursor=mi_conexion.cursor()


            #creamos la consulta. AQUÍ LOS INTERROGANTES ? SON CADA UNO DE LOS CAMPOS QUE SE GUARDAN: código de producto [1] y el campo de entrada para modificar cantidad conseguir todos
            mi_cursor.execute("UPDATE DetalleVentaT SET Cantidad=? WHERE Codigo="+self.valor_cantidad_seleccionada[1],(self.ent_cantidad_modificar_detalle.get()))
            
            #aplicar cambios
            mi_conexion.commit()

            #float para decimales e int para enteros. Calcular subtotal y existencias

            subtotal=float(self.valor_cantidad_seleccionada[4])*float(self.ent_cantidad_modificar_detalle.get())
            existencia=int(self.valor_cantidad_seleccionada[6])-int(self.ent_cantidad_modificar_detalle.get())


            #refrescar la lista de usuarios
            self.valor_cantidad_seleccionada=self.tree_detalle_venta.item(self.cantidad_seleccionada,text='', values=(self.valor_cantidad_seleccionada[0],self.valor_cantidad_seleccionada[1],self.valor_cantidad_seleccionada[2], self.valor_cantidad_seleccionada[3],
            self.valor_cantidad_seleccionada[4],self.ent_cantidad_modificar_detalle.get(),self.valor_cantidad_seleccionada[6],self.valor_cantidad_seleccionada[7],subtotal,existencia))
                     
            
            #cerrar la ventana
            self.frame_modificar_cantidad.destroy()
            self.total_detalle_venta()
            #cerrar la conexion
            mi_conexion.close()
        except:
            messagebox.showerror('Modificando Cantidad Detalle Venta','Ocurrió un Error')          
    def ventana_descuento(self):
         #Almacenamos el valor de lista de usuarios
        #pongo otra variable para extraer los datos del valor seleccionado
        self.descuento_seleccionado=self.tree_detalle_venta.focus()
        self.valor_descuento_seleccionado=self.tree_detalle_venta.item(self.descuento_seleccionado,'values')
        
        #condición si el valor de usuario es diferente o = a vacío:
        if self.valor_descuento_seleccionado!='':

            self.buscar_precio_descuento()
        
            #poner una ventana flotante por encima de ventana de lista de usuarios
            self.frame_descuento=Toplevel(master=self)
            self.frame_descuento.title('Aplicar Descuento')
            self.centrar_ventana(self.frame_descuento,350,300)
            #grab.set es una propiedad que impide que no se puede crear ninguna acción hasta que no se cierre la ventana
            self.frame_descuento.grab_set()

            #generamos una variable y guardarmos el valor de la cantidad seleccionada           
            descripcion_descuento=(self.valor_descuento_seleccionado[2])
            coste_descuento=(self.valor_descuento_seleccionado[3])
            #precio_descuento=(self.valor_descuento_seleccionado[4])
            precio_descuento=(self.precio_aplicar_descuento)

            lbl_descripcion_descuento=tb.Label(master=self.frame_descuento,text='Producto', font=('Calibri', 16),bootstyle='success')
            lbl_descripcion_descuento.pack(padx=10,pady=15)
            #aquí USAMOS LA VARIABLE CREADA ARRIBA Y LE VAMOS A PASAR EL TEXT CON VARIABLE DESCRIPCIÓN, PARA ALMACENAR LA DESCRIPCIÓN
            lbl_descripcion_descuento.config(text=descripcion_descuento)


            lbl_coste_descuento=tb.Label(master=self.frame_descuento,text='Coste', font=('Calibri', 16))
            lbl_coste_descuento.pack(padx=10,pady=5)
            #aquí USAMOS LA VARIABLE CREADA ARRIBA Y LE VAMOS A PASAR EL TEXT CON VARIABLE DESCRIPCIÓN, PARA ALMACENAR LA DESCRIPCIÓN
            lbl_coste_descuento.config(text=f'Coste: {coste_descuento}')

            lbl_precio_descuento=tb.Label(master=self.frame_descuento,text='Precio', font=('Calibri', 16))
            lbl_precio_descuento.pack(padx=10,pady=5)
            #aquí USAMOS LA VARIABLE CREADA ARRIBA Y LE VAMOS A PASAR EL TEXT CON VARIABLE DESCRIPCIÓN, PARA ALMACENAR LA DESCRIPCIÓN
            lbl_precio_descuento.config(text=f'Precio: {precio_descuento}')

            lbl_nuevo_precio=tb.Label(master=self.frame_descuento,text='Nuevo Precio',bootstyle='warning', font=('Calibri', 16))
            lbl_nuevo_precio.pack(padx=10,pady=5)
            #aquí USAMOS LA VARIABLE CREADA ARRIBA Y LE VAMOS A PASAR EL TEXT CON VARIABLE DESCRIPCIÓN, PARA ALMACENAR LA DESCRIPCIÓN
            self.ent_nuevo_precio=tb.Entry(master=self.frame_descuento,justify=CENTER,font=14)
            self.ent_nuevo_precio.pack(padx=10,pady=15)
            self.ent_nuevo_precio.insert(0,self.valor_descuento_seleccionado[4])
            self.ent_nuevo_precio.bind('<Return>',self.aplicar_descuento_detalle_venta)

            self.ent_nuevo_precio.focus()           
    def aplicar_descuento_detalle_venta(self, event):
        try:
            # Obtener y convertir el nuevo precio a float
            nuevo_precio = float(self.ent_nuevo_precio.get())
            # Obtener y convertir el coste y el precio actual a float
            coste = float(self.valor_descuento_seleccionado[3])
            precio_actual = float(self.precio_aplicar_descuento)

            # Imprimir para depuración
            print(f"Nuevo Precio: {nuevo_precio}, Coste: {coste}, Precio Actual: {precio_actual}")

            # Verificar si el nuevo precio es menor que el coste
            if nuevo_precio < coste:
                messagebox.showerror('Aplicando Descuento', 'El nuevo precio está por debajo del coste')
                return

            # Verificar si el nuevo precio es mayor que el precio actual
            if nuevo_precio > precio_actual:
                messagebox.showerror('Aplicando Descuento', 'No está haciendo ningún descuento, precio ingresado mayor al precio actual')
                return

            # Calcular el descuento unitario
            descuento_unitario = precio_actual - nuevo_precio

            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Consulta SQL usando parámetros
            mi_cursor.execute("UPDATE DetalleVentaT SET Precio=?, Descuento=? WHERE Codigo=?", 
                            (nuevo_precio, descuento_unitario, self.valor_descuento_seleccionado[1]))

            # Aplicar cambios
            mi_conexion.commit()

            # Calcular subtotal y existencia
            subtotal = float(self.valor_descuento_seleccionado[5]) * nuevo_precio
            existencia = int(self.valor_descuento_seleccionado[6]) - int(self.valor_descuento_seleccionado[5])

            # Refrescar la lista de usuarios
            self.valor_descuento_seleccionado = self.tree_detalle_venta.item(self.descuento_seleccionado, 
                text='', 
                values=(self.valor_descuento_seleccionado[0], 
                        self.valor_descuento_seleccionado[1], 
                        self.valor_descuento_seleccionado[2], 
                        self.valor_descuento_seleccionado[3],
                        nuevo_precio, 
                        self.valor_descuento_seleccionado[5], 
                        self.valor_descuento_seleccionado[6], 
                        descuento_unitario, 
                        subtotal, 
                        existencia))

            # Cerrar la ventana y la conexión
            self.frame_descuento.destroy()
            self.total_detalle_venta()
            mi_conexion.close()
            
        except Exception as e:
            messagebox.showerror('Aplicando Descuento', f'Ocurrió un Error: {e}')
    def buscar_precio_descuento(self):
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Crear la consulta para buscar el precio del producto por código
            query = "SELECT Precio FROM Productos WHERE Codigo = ?"
            mi_cursor.execute(query, (self.valor_descuento_seleccionado[1],))
            datos_precio_descuento = mi_cursor.fetchall()

            # Verificar si se obtuvieron datos
            if datos_precio_descuento:
                # Asignar el precio del primer resultado
                self.precio_aplicar_descuento = datos_precio_descuento[0][0]
            else:
                # Manejo si no se encuentran resultados
                self.precio_aplicar_descuento = None
                messagebox.showwarning('Buscar Productos', 'No se encontró el producto')

            # Cerrar la conexión
            mi_conexion.close()

        except sqlite3.Error as e:
            messagebox.showerror('Buscar Productos', f'Ocurrió un error: {e}')
    #Ventana de Cobro
    def ventana_contado(self):
        #si cualquier dato en el treeview es mayor a cero entonces: 
        if len(self.tree_detalle_venta.get_children())>0:

            #ESTABLECER VARIABLES PARA FECHA Y HORA
            fecha_actual=datetime.now()
            self.fecha_venta_contado=(fecha_actual.strftime('%d/%m/%Y'))
            self.hora_venta_contado=(fecha_actual.strftime('%H:%M:%S'))


            self.frame_contado = Toplevel(master=self)
            self.frame_contado.title('Cobrar Venta al Contado')
            self.centrar_ventana(self.frame_contado,475,350)
            self.frame_contado.grab_set()

            # Frame para el total de la venta
            self.lblframe_total = tb.LabelFrame(master=self.frame_contado)
            self.lblframe_total.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

            lbl_total_contado = tb.Label(master=self.lblframe_total, text='Total Venta', font=('Calibri', 22), bootstyle='info')
            lbl_total_contado.pack()

            lbl_total_venta = tb.Label(master=self.lblframe_total, text='Total', font=('Calibri', 22))
            lbl_total_venta.pack()
            lbl_total_venta.config(text=f'{self.total:,.2f}€ IVA Inc.')

            # Frame para el efectivo y el cambio
            self.lblframe_cambio = tb.LabelFrame(master=self.frame_contado)
            self.lblframe_cambio.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

            lbl_efectivo = tb.Label(master=self.lblframe_cambio, text='Efectivo', font=('Calibri', 22), bootstyle='warning')
            lbl_efectivo.grid(row=0, column=0, padx=10, pady=10)

            # Cambiado Label por Entry para permitir la entrada de efectivo
            self.ent_efectivo = tb.Entry(master=self.lblframe_cambio, justify=CENTER, font=('Calibri', 22))
            self.ent_efectivo.grid(row=0, column=1, pady=10, padx=10)
            self.ent_efectivo.insert(0, self.total)
            self.ent_efectivo.bind('<KeyRelease>',self.calcular_cambio)

            lbl_cambio = tb.Label(master=self.lblframe_cambio, text='Cambio', font=('Calibri', 22), bootstyle='warning')
            lbl_cambio.grid(row=1, column=0, padx=10, pady=10)

            self.lbl_calculo_cambio = tb.Label(master=self.lblframe_cambio, text='0.00€', font=('Calibri', 22))
            self.lbl_calculo_cambio.grid(row=1, column=1, padx=10, pady=10)  # Añadido grid() correctamente

            btn_cobro_contado = tb.Button(master=self.lblframe_cambio, text='Cobrar', width=45, bootstyle='success',command=self.guardar_venta)
            btn_cobro_contado.grid(row=2, column=1, padx=10, pady=10)

            self.ent_efectivo.focus()
    #le ponemos un evento a calcular_cambio (al lado de self, como parámetro), porque lo vamos a llamar desde la ventana contado
    def calcular_cambio(self,event):
        if self.ent_efectivo.get()=='':
            self.lbl_calculo_cambio.config(text='0.00€')
            return
        try:
            float(self.ent_efectivo.get())
            Cambio=0
            #almacenamos la venta llamando a total
            Venta=(self.total)
            Efectivo=(self.ent_efectivo.get())
            Cambio=float(Efectivo)-float(Venta)
            self.lbl_calculo_cambio.config(text=f'{Cambio:,.2f}€ IVA Inc.')
            

        except:
            messagebox.showerror('Calcular Cambio', 'Algun dato no es válido')
    def correlativo_ventas(self):
        
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Consulta para obtener el máximo valor de Codigo
            mi_cursor.execute("SELECT MAX(No) FROM Ventas")
            correlativo_ventas = mi_cursor.fetchone()

            # Verificamos el resultado de la consulta
            if correlativo_ventas[0] is None:
                self.nuevo_correlativo_ventas = 1
            else:
                self.nuevo_correlativo_ventas = int(correlativo_ventas[0]) + 1

            # Aplicar cambios y cerrar la conexión
            mi_conexion.commit()
            mi_conexion.close()

        except Exception as e:
            messagebox.showerror('Correlativo Ventas', f'Ocurrió un error: {e}')
    #Guarda la venta en la tabla correspondiente de la base de datos, EN ESTE CASO ES VENTAS
    def guardar_venta(self):
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            datos_ventas=(self.nuevo_correlativo_ventas,self.fecha_venta_contado,self.hora_venta_contado,
            self.codigo_usuario_logueado, self.nombre_usuario_logueado,'1','CONSUMIDOR FINAL',self.total,
            'Factura Emitida','Contado')

            # Comprobar que datos_guardar_producto_detalle_venta es una tupla con el número correcto de elementos
            if len(datos_ventas) == 10:
                # Insertar los datos en tabla VENTAS
                mi_cursor.execute("INSERT INTO Ventas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(datos_ventas))
                
                # Aplicar cambios
                mi_conexion.commit()
                messagebox.showinfo('Guardando Ventas', 'Venta de contado agregada con éxito')
                self.guardar_detalle_ventas()
                self.eliminar_detalle_ventaT()
                self.frame_contado.destroy()
                #vuelvo a llamar a la ventana detalle de venta, para que me cargue la ventanita vacía
                self.ventana_detalle_venta()
            else:
                messagebox.showwarning('Datos Incorrectos', 'Los datos para agregar el producto no son válidos.')

        except sqlite3.IntegrityError as e:
            messagebox.showerror('Error de Integridad', f'Error de integridad en la base de datos: {e}')
        except sqlite3.OperationalError as e:
            messagebox.showerror('Error de Operación', f'Error de operación en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Guardando Ventas', f'Ocurrió un error: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()        
    #Guarda los datos en la tabla detalle de VENTA
    def guardar_detalle_ventas(self):
        self.mostrar_producto_detalle_venta()
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()
            
            datos_detalle_venta = self.datos_productos_detalle_venta
            # Recorremos todos los elementos del treeview y colocamos cada elemento
            for elementos in datos_detalle_venta:
                # Comprobar que cada elementos es una tupla con el número correcto de elementos
                if len(elementos) == 8:
                    # Insertar los datos en DetalleVenta
                    mi_cursor.execute("INSERT INTO DetalleVenta VALUES (?, ?, ?, ?, ?, ?, ?, ?)", elementos)
                else:
                    messagebox.showwarning('Datos Incorrectos', 'Los datos para agregar el producto no son válidos.')
            
            # Aplicar cambios
            mi_conexion.commit()
            self.actualizar_stock()  # Mover fuera del bucle

        except sqlite3.IntegrityError as e:
            messagebox.showerror('Error de Integridad', f'Error de integridad en la base de datos: {e}')
        except sqlite3.OperationalError as e:
            messagebox.showerror('Error de Operación', f'Error de operación en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Guardando Productos Detalle Venta', f'Ocurrió un error: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()

    def eliminar_detalle_ventaT(self):
 
            try:

                #conexion a la base de datos
                mi_conexion=sqlite3.connect('Ventas.db')
                #crear el cursor. Un cursor es un objeto que permite ejecutar comandos SQL y obtener resultados de consultas. 
                mi_cursor=mi_conexion.cursor()

            
                #creamos la consulta. Eliminamos el valor del producto venta con el 1, QUE ES EL PRODUCTO. El 0 no, porque es el número de venta
                mi_cursor.execute("DELETE FROM DetalleVentaT")
            
                #aplicar cambios
                mi_conexion.commit()
                #cerrar la conexion
                mi_conexion.close()
           
            except:
                messagebox.showerror('Eliminando Detalle de VentaT','Ocurrió un error')     
    def actualizar_stock(self):
        self.mostrar_producto_detalle_venta()
        
        try:
            # Conexión a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()
            
            datos_stock = self.datos_productos_detalle_venta
            
            # Recorremos todos los elementos del treeview y actualizamos el stock
            for fila in datos_stock:
                # Comprobar que cada elemento es una tupla con el número correcto de elementos
                if len(fila) == 8:  # O el número de elementos que corresponda
                    mi_cursor.execute("UPDATE Productos SET Stock = Stock - ? WHERE Codigo = ?", (fila[5], fila[1]))
                else:
                    messagebox.showwarning('Datos Incorrectos', 'Los datos para actualizar el stock no son válidos.')
            
            # Aplicar cambios
            mi_conexion.commit()
        
        except sqlite3.IntegrityError as e:
            messagebox.showerror('Error de Integridad', f'Error de integridad en la base de datos: {e}')
        except sqlite3.OperationalError as e:
            messagebox.showerror('Error de Operación', f'Error de operación en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Actualizando Stock', f'Ocurrió un error: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()
    def ventana_listado_ventas(self):
        self.borrar_frames()

        self.frame_listado_venta=Frame(master=self.frame_center)
        self.frame_listado_venta.grid(row=0,column=1,sticky=NSEW)

        #=====================FRAME DEL BUSCADOR====================================

        lblframe_busqueda_listado_venta=tb.LabelFrame(master=self.frame_listado_venta)
        lblframe_busqueda_listado_venta.grid(row=0,column=0,sticky=NSEW)

        lbl_fecha_listado_venta=tb.Label(master=lblframe_busqueda_listado_venta,bootstyle='info',
        text='Ventas de Fecha:', font=('Calibri',14))
        lbl_fecha_listado_venta.grid(row=0,column=0,padx=5,pady=5)
        self.ent_fecha_listado_venta=tb.DateEntry(master=lblframe_busqueda_listado_venta)
        self.ent_fecha_listado_venta.grid(row=0,column=1,padx=5,pady=5)
        btn_buscar_venta_fecha=tb.Button(master=lblframe_busqueda_listado_venta,text='Buscar',width=20,
        bootstyle='success',command=self.mostrar_listado_ventas)
        btn_buscar_venta_fecha.grid(row=0,column=2,padx=5,pady=5)


        #TÍTULO LISTADO VENTA

        lblframe_titulo_listado_venta=tb.LabelFrame(master=self.frame_listado_venta)
        lblframe_titulo_listado_venta.grid(row=1,column=0,sticky=NSEW)
        lbl_titulo_listado_venta=tb.Label(master=lblframe_titulo_listado_venta,bootstyle='success',
        text='LISTA DE VENTAS DEL DÍA DE MI NEGOCIO O EMPRESA', font=('Calibri',14))
        lbl_titulo_listado_venta.grid(row=0,column=0)

        #TREE DE LISTADO VENTA
        lblframe_tree_listado_venta=tb.LabelFrame(master=self.frame_listado_venta)
        lblframe_tree_listado_venta.grid(row=2,column=0,sticky=NSEW)
        #CREAMOS LAS COLUMNAS
        columnas=("no","fecha","hora","codusu","usuario","codcli","cliente","monto","estado","tipo")
        #CREAMOS EL TREEVIEW
        self.tree_listado_venta=tb.Treeview(master=lblframe_tree_listado_venta,height=30, columns=columnas,
        show='headings',bootstyle='success')
        self.tree_listado_venta.grid(row=0,column=0)

        #CREAMOS CABECERAS
        self.tree_listado_venta.heading('no',text='No', anchor=W)
        self.tree_listado_venta.heading('fecha',text='Fecha', anchor=W)
        self.tree_listado_venta.heading('hora',text='Hora', anchor=W)
        self.tree_listado_venta.heading('codusu',text='Código Usuario', anchor=W)
        self.tree_listado_venta.heading('usuario',text='Usuario', anchor=W)
        self.tree_listado_venta.heading('codcli',text='Código Cliente', anchor=W)
        self.tree_listado_venta.heading('cliente',text='Cliente', anchor=W)
        self.tree_listado_venta.heading('monto',text='Monto', anchor=W)
        self.tree_listado_venta.heading('estado',text='Estado', anchor=W)
        self.tree_listado_venta.heading('tipo',text='Tipo', anchor=W)

        #configurar las columnas que quiero que se muestren

        self.tree_listado_venta['displaycolumns']=('no','fecha','hora','cliente','monto','tipo')

        #Ancho de columnas
        self.tree_listado_venta.column('no',width=50)
        self.tree_listado_venta.column('fecha',width=100)
        self.tree_listado_venta.column('hora',width=100)
        self.tree_listado_venta.column('cliente',width=200)
        self.tree_listado_venta.column('monto',width=75)
        self.tree_listado_venta.column('tipo',width=75)

        #crear el Scrollbar
        tree_scroll=tb.Scrollbar(master=self.frame_listado_venta,bootstyle='success_round')
        tree_scroll.grid(row=2,column=2,pady=10)

        #configuración de Scrollbar
        tree_scroll.config(command=self.tree_listado_venta.yview)

        #Total de ventas en el día
        self.lbl_total_listado_venta=tb.Label(master=self.frame_listado_venta,font=('Calibri',24),
        justify=RIGHT)
        self.lbl_total_listado_venta.grid(row=3,column=0,sticky=E)

        self.tree_listado_venta.bind('<<TreeviewSelect>>',self.venta_seleccionada)


        #=========================lISTADO DETALLE DE VENTAS===============================

        lblframe_datos_detalle_venta=tb.LabelFrame(master=self.frame_listado_venta)
        lblframe_datos_detalle_venta.grid(row=0,column=3,sticky=NSEW)

        lbl_numero=tb.Label(master=lblframe_datos_detalle_venta,text='Venta:',bootstyle='info',font=
        ('Calibri',14))
        lbl_numero.grid(row=0,column=0,padx=5,pady=5)
        #AQUÍ SE INSTANCIA A SELF, porque se va a llamar a otra función y tiene que marcar el texto que se encuentra vacío por defecto
        self.lbl_no_venta=Label(master=lblframe_datos_detalle_venta,text='')
        self.lbl_no_venta.grid(row=0,column=1,padx=5,pady=5,sticky=W)

        lbl_cliente=tb.Label(master=lblframe_datos_detalle_venta,text='Cliente:',bootstyle='info',font=('Calibri',14))
        lbl_cliente.grid(row=1,column=0,padx=5,pady=5)
        #AQUÍ SE INSTANCIA A SELF, porque se va a llamar a otra función y tiene que marcar el texto que se encuentra vacío por defecto
        self.lbl_cliente_venta=Label(master=lblframe_datos_detalle_venta,text='')
        self.lbl_cliente_venta.grid(row=1,column=1,padx=5,pady=5,sticky=W)

        lblframe_botones_listado_detalle_venta=tb.LabelFrame(master=self.frame_listado_venta)
        lblframe_botones_listado_detalle_venta.grid(row=1,column=3,sticky=NSEW)

        self.btn_devolucion_contado=tb.Button(master=lblframe_botones_listado_detalle_venta,
        text='Devolucion-Contado',width=20,bootstyle='warning',command=self.ventana_devolucion_contado)
        self.btn_devolucion_contado.grid(row=0,column=0,padx=5,pady=2)
        
        self.btn_devolucion_credito=tb.Button(master=lblframe_botones_listado_detalle_venta,
        text='Devolucion-Crédito',width=20,bootstyle='danger')
        self.btn_devolucion_credito.grid(row=0,column=1,padx=5,pady=2)

        self.btn_imprimir_venta=tb.Button(master=lblframe_botones_listado_detalle_venta,
        text='Imprimir-Venta',width=20,bootstyle='info',command=self.imprimir_venta_pdf)
        self.btn_imprimir_venta.grid(row=0,column=2,padx=5,pady=2)

        #Contenedor del TREEVIEW DE LISTADO VENTA

        lblframe_tree_listado_detalle_venta=tb.LabelFrame(master=self.frame_listado_venta)
        lblframe_tree_listado_detalle_venta.grid(row=2,column=3,sticky=NSEW)

        #CREAMOS LAS COLUMNAS
        columnas=("no","codigo","descripcion","costo","precio","cantidad","stock","descuento","subtotal")
        #CREAMOS EL TREEVIEW
        self.tree_listado_detalle_venta=tb.Treeview(master=lblframe_tree_listado_detalle_venta,height=30, columns=columnas,
        show='headings',bootstyle='success',selectmode='extended')
        self.tree_listado_detalle_venta.grid(row=0,column=0)

        #CREAMOS CABECERAS
        self.tree_listado_detalle_venta.heading('no',text='No', anchor=W)
        self.tree_listado_detalle_venta.heading('codigo',text='Codigo', anchor=W)
        self.tree_listado_detalle_venta.heading('descripcion',text='Descripción', anchor=W)
        self.tree_listado_detalle_venta.heading('costo',text='Costo', anchor=W)
        self.tree_listado_detalle_venta.heading('precio',text='Precio', anchor=W)
        self.tree_listado_detalle_venta.heading('cantidad',text='Cantidad', anchor=W)
        self.tree_listado_detalle_venta.heading('stock',text='Stock', anchor=W)
        self.tree_listado_detalle_venta.heading('descuento',text='Descuento', anchor=W)
        self.tree_listado_detalle_venta.heading('subtotal',text='Subtotal', anchor=W)

        #configurar las columnas que quiero que se muestren

        self.tree_listado_detalle_venta['displaycolumns']=('codigo','descripcion','precio','cantidad','subtotal')

        #Ancho de columnas
        self.tree_listado_detalle_venta.column('codigo',width=75)
        self.tree_listado_detalle_venta.column('descripcion',width=200)
        self.tree_listado_detalle_venta.column('precio',width=75)
        self.tree_listado_detalle_venta.column('cantidad',width=75)
        self.tree_listado_detalle_venta.column('subtotal',width=100)

        #crear el Scrollbar
        tree_scroll=tb.Scrollbar(master=self.frame_listado_venta,bootstyle='success_round')
        tree_scroll.grid(row=2,column=4,pady=10)

        #configuración de Scrollbar
        tree_scroll.config(command=self.tree_listado_detalle_venta.yview)

        #Total de ventas en el día
        self.lbl_total_listado_detalle_venta=tb.Label(master=self.frame_listado_venta,font=('Calibri',24),
        justify=RIGHT)
        self.lbl_total_listado_detalle_venta.grid(row=3,column=3,sticky=E)
        self.mostrar_listado_ventas()
    def mostrar_listado_ventas(self):
        # Limpiar el listado de detalle de ventas al abrir o seleccionar una fecha
        self.limpiar_listado_detalle_ventas()
        
        try:
            # Conectar a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Limpiar el TreeView o tabla de ventas
            registros = self.tree_listado_venta.get_children()
            for registro in registros:
                self.tree_listado_venta.delete(registro)

            # Obtener el patrón de búsqueda desde el entry de fecha
            patron = self.ent_fecha_listado_venta.entry.get()

            # Consultar las ventas en la base de datos según el patrón de fecha
            mi_cursor.execute("SELECT * FROM Ventas WHERE Fecha LIKE ?", ('%' + patron + '%',))
            datos_listado_ventas = mi_cursor.fetchall()

            # Insertar las filas en el TreeView
            for fila in datos_listado_ventas:
                self.tree_listado_venta.insert('',0, text=fila[0], values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], 
                fila[6],fila[7],fila[8],fila[9]))

            # Confirmar los cambios y cerrar la conexión
            mi_conexion.commit()
            mi_conexion.close()

            # Actualizar el total de ventas
            self.total_listado_ventas()
        
        except Exception as e:
            # Mostrar un mensaje de error si ocurre alguna excepción
            messagebox.showerror('Buscar Listado de Ventas', f'Ocurrió un error: {e}')

    def total_listado_ventas(self):
        try:
            # Conectar a la base de datos
            with sqlite3.connect('Ventas.db') as mi_conexion:
                mi_cursor = mi_conexion.cursor()
                
                # Calcular el total de ventas
                mi_cursor.execute("SELECT SUM(Montante) FROM Ventas")
                total_ventas = mi_cursor.fetchone()[0] or 0.0  # Obtener el total calculado, o 0 si es None

                # Actualizar la etiqueta o campo correspondiente en la interfaz de usuario
                if hasattr(self, 'lbl_total_listado_venta'):
                    self.lbl_total_listado_venta.config(text=f"Total Ventas: {total_ventas:.2f}€ IVA inc.")
                else:
                    raise AttributeError("lbl_total_listado_venta no ha sido inicializada.")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al actualizar el total de ventas: {e}")

    #recibe un evento
    def venta_seleccionada(self,event):
        venta_seleccionada=self.tree_listado_venta.focus()
        self.valor_venta_seleccionada=self.tree_listado_venta.item(venta_seleccionada,'values')
        if self.valor_venta_seleccionada!="":
            #almacenamiento de los valores número de venta y clientes en las etiquetas correspondientes
            self.lbl_no_venta.config(text=self.valor_venta_seleccionada[0])
            self.lbl_cliente_venta.config(text=self.valor_venta_seleccionada[6])
            self.mostrar_listado_detalle_venta()
    def mostrar_listado_detalle_venta(self):
        try:
            # Conectar a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Limpiar el TreeView o tabla de detalles
            registro = self.tree_listado_detalle_venta.get_children()
            for elementos in registro:
                self.tree_listado_detalle_venta.delete(elementos)

            # Consultar los detalles de la venta
            mi_cursor.execute("SELECT * FROM DetalleVenta WHERE No = ?", (self.valor_venta_seleccionada[0],))
            datos_listado_detalle_ventas = mi_cursor.fetchall()

            # Insertar las filas en el TreeView
            for fila in datos_listado_detalle_ventas:
                subtotal = float(fila[4]) * float(fila[5])
                self.tree_listado_detalle_venta.insert('', '0', text=fila[0], values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], subtotal))

            # Cerrar la conexión
            mi_conexion.commit()
            mi_conexion.close()
            self.total_listado_detalle_ventas()

        except Exception as e:
            messagebox.showwarning('Mostrar listado detalle ventas', f'Ocurrió un error: {e}')

    def total_listado_detalle_ventas(self):
            self.total_lista_detalle_ventas=0
            #establecemos el recorrido
            for fila in self.tree_listado_detalle_venta.get_children():
                #el [8] es el subtotal dentro del treeview lista detalle ventas
                self.total_lista_detalle_ventas+=float(self.tree_listado_detalle_venta.item(fila,'values')[8])
            self.lbl_total_listado_detalle_venta.config(text=f'{self.total_lista_detalle_ventas:,.2f}€')
    def limpiar_listado_detalle_ventas(self):
        # Limpiar etiquetas número de venta y número de cliente
        self.lbl_no_venta.config(text='')
        self.lbl_cliente_venta.config(text='')
        
        # Limpiar total detalle venta
        self.lbl_total_listado_detalle_venta.config(text='0.00€')
        
        # Recorrer y eliminar todas las filas en el Treeview
        datos = self.tree_listado_detalle_venta.get_children()
        for fila in datos:
            self.tree_listado_detalle_venta.delete(fila)  # Aquí se pasa la fila a eliminar
    def ventana_devolucion_contado(self):
        try:
            self.producto_listado_seleccionado = self.tree_listado_detalle_venta.focus()

            if not self.producto_listado_seleccionado:
                messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para devolver.")
                return

            self.valor_producto_seleccionado = self.tree_listado_detalle_venta.item(self.producto_listado_seleccionado, 'values')

            if self.valor_producto_seleccionado:
                # Crear ventana de devolución
                self.frame_devolucion = Toplevel(master=self)
                self.frame_devolucion.title('Aplicar Devolución')
                self.centrar_ventana(self.frame_devolucion, 350, 300)
                self.frame_devolucion.grab_set()

                # Configurar el grid
                self.frame_devolucion.columnconfigure(0, weight=1)
                self.frame_devolucion.columnconfigure(1, weight=1)
                self.frame_devolucion.columnconfigure(2, weight=1)

                # Mostrar detalles del producto seleccionado
                codigo_devolucion = self.valor_producto_seleccionado[1]
                descripcion_devolucion = self.valor_producto_seleccionado[2]
                cantidad_devolucion = self.valor_producto_seleccionado[5]
                subtotal_devolucion = self.valor_producto_seleccionado[8]

                lbl_codigo_devolucion = tb.Label(
                    master=self.frame_devolucion, text='Producto', font=('Calibri', 16), bootstyle='success'
                )
                lbl_codigo_devolucion.grid(row=0, column=1, padx=10, pady=15)
                lbl_codigo_devolucion.config(text=codigo_devolucion)

                lbl_descripcion_devolucion = tb.Label(
                    master=self.frame_devolucion, text='Descripción', font=('Calibri', 16), bootstyle='success'
                )
                lbl_descripcion_devolucion.grid(row=1, column=1, padx=10, pady=15)
                lbl_descripcion_devolucion.config(text=descripcion_devolucion)

                lbl_cantidad_devolucion = tb.Label(
                    master=self.frame_devolucion, text='Cantidad', font=('Calibri', 16)
                )
                lbl_cantidad_devolucion.grid(row=2, column=1, padx=10, pady=5)
                lbl_cantidad_devolucion.config(text=cantidad_devolucion)

                lbl_subtotal_devolucion = tb.Label(
                    master=self.frame_devolucion, text='Subtotal', font=('Calibri', 16)
                )
                lbl_subtotal_devolucion.grid(row=3, column=1, padx=10, pady=5)
                lbl_subtotal_devolucion.config(text=f'Precio: {subtotal_devolucion}€')

                lblframe_boton_devolucion = tb.LabelFrame(master=self.frame_devolucion)
                lblframe_boton_devolucion.grid(row=4, column=0, columnspan=3, sticky=NSEW, padx=10, pady=5)

                lblframe_boton_devolucion.columnconfigure(0, weight=1)

                self.btn_devolucion = tb.Button(
                    master=lblframe_boton_devolucion,
                    text='Devolución-Contado',
                    width=20,
                    bootstyle='warning',
                    command=self.procesar_devolucion_contado
                )
                self.btn_devolucion.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
            else:
                messagebox.showwarning("Advertencia", "No se pudo obtener información del producto seleccionado.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error: {e}")
    def procesar_devolucion_contado(self):
        try:
            # Actualizar el stock después de la devolución
            self.actualizar_stock_devolucion()

            # Obtener el subtotal del producto antes de eliminarlo
            subtotal_producto = float(self.valor_producto_seleccionado[8])

            # Eliminar el producto seleccionado
            self.eliminar_producto_seleccionado()

            # Eliminar los registros de DetalleVenta en la base de datos
            self.eliminar_detalle_venta_en_db()

            # Obtener el id de la venta actual
            id_venta = self.lbl_no_venta.cget('text')

            # Actualizar el monto total de la venta
            self.actualizar_monto_venta(id_venta)

            # Verificar si la venta aún tiene productos asociados
            self.verificar_y_eliminar_venta()

            # Actualizar el total de ventas y detalle de ventas
            self.total_listado_ventas()  # Recalcular total de ventas
            self.total_listado_detalle_ventas()  # Recalcular total de detalle de ventas

            # Actualizar el listado de ventas en la interfaz de usuario
            self.actualizar_listado_ventas()  # Asegúrate de que esta función refleje los cambios

            # Cerrar la ventana de devolución
            self.frame_devolucion.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al procesar la devolución: {e}")


    def actualizar_stock_devolucion(self):
        mi_conexion = None  # Inicializar mi_conexion aquí para asegurar que esté definida en el bloque finally
        try:
            # Verificar si la conexión a la base de datos se realiza correctamente
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()
            
            # Obtener los datos del producto seleccionado
            datos_devolucion = self.valor_producto_seleccionado 

            # Verificar que los datos del producto seleccionado son válidos
            if datos_devolucion and len(datos_devolucion) > 5:
                codigo_producto = datos_devolucion[1]  # Código del producto en columna 1
                cantidad_a_reponer = datos_devolucion[5]  # Stock a reponer en columna 5
                
                print(f"Reponiendo stock para el producto con código: {codigo_producto}")
                print(f"Cantidad a reponer: {cantidad_a_reponer}")
                
                # Actualizar el stock en la base de datos
                mi_cursor.execute("UPDATE Productos SET Stock = Stock + ? WHERE Codigo = ?", (cantidad_a_reponer, codigo_producto))
            
                # Aplicar cambios
                mi_conexion.commit()
                messagebox.showinfo("Éxito", "Stock actualizado correctamente.")
            else:
                messagebox.showwarning('Datos Incorrectos', 'No se seleccionó ningún producto para actualizar o los datos son incompletos.')

        except sqlite3.IntegrityError as e:
            messagebox.showerror('Error de Integridad', f'Error de integridad en la base de datos: {e}')
        except sqlite3.OperationalError as e:
            messagebox.showerror('Error de Operación', f'Error de operación en la base de datos: {e}')
        except sqlite3.DatabaseError as e:  # Capturar errores específicos de la base de datos
            messagebox.showerror('Error en la Base de Datos', f'Error en la base de datos: {e}')
        except Exception as e:
            messagebox.showerror('Actualizando Stock', f'Ocurrió un error inesperado: {e}')
        finally:
            # Cerrar la conexión
            if mi_conexion:
                mi_conexion.close()    

    def eliminar_producto_seleccionado(self):
        try:
            self.tree_listado_detalle_venta.delete(self.producto_listado_seleccionado)
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al eliminar el producto seleccionado: {e}")

    def verificar_y_eliminar_venta(self):
        try:
            # Conectar a la base de datos usando el contexto `with`
            with sqlite3.connect('Ventas.db') as mi_conexion:
                mi_cursor = mi_conexion.cursor()

                no_venta = self.lbl_no_venta.cget('text')

                # Verificar si hay productos asociados a esta venta
                mi_cursor.execute("SELECT COUNT(*) FROM DetalleVenta WHERE No = ?", (no_venta,))
                count = mi_cursor.fetchone()[0]

                if count == 0:
                    # No hay productos restantes, eliminar la venta
                    mi_cursor.execute("DELETE FROM Ventas WHERE No = ?", (no_venta,))
                    
                    # También eliminar la venta del TreeView de ventas
                    venta_seleccionada = self.tree_listado_venta.selection()
                    if venta_seleccionada:
                        self.tree_listado_venta.delete(venta_seleccionada)

                # Confirmar los cambios
                mi_conexion.commit()

        except sqlite3.DatabaseError as db_error:
            # Manejo específico para errores de base de datos
            messagebox.showerror("Error", f"Se produjo un error de base de datos: {db_error}")
        except Exception as e:
            # Manejo general para otros errores
            messagebox.showerror("Error", f"Se produjo un error al verificar o eliminar la venta: {e}")



    def eliminar_detalle_venta_en_db(self):
        try:
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()
            
            no_venta = self.lbl_no_venta.cget('text')
            codigo_producto = self.valor_producto_seleccionado[1]

            mi_cursor.execute("DELETE FROM DetalleVenta WHERE No = ? AND Codigo = ?", (no_venta, codigo_producto))
            
            mi_conexion.commit()
            mi_conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al eliminar el detalle de venta en la base de datos: {e}")

    def actualizar_listado_ventas(self):
        try:
            # Conectar a la base de datos
            mi_conexion = sqlite3.connect('Ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Limpiar el TreeView de ventas actual
            registros = self.tree_listado_venta.get_children()
            for registro in registros:
                self.tree_listado_venta.delete(registro)

            # Obtener el patrón de búsqueda desde el entry de fecha
            patron = self.ent_fecha_listado_venta.entry.get()

            # Consultar las ventas en la base de datos según el patrón de fecha
            mi_cursor.execute("SELECT * FROM Ventas WHERE Fecha LIKE ?", ('%' + patron + '%',))
            datos_listado_ventas = mi_cursor.fetchall()

            # Insertar las filas en el TreeView
            for fila in datos_listado_ventas:
                self.tree_listado_venta.insert('', 0, text=fila[0], values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], 
                                                                            fila[6], fila[7], fila[8], fila[9]))

            # Confirmar los cambios y cerrar la conexión
            mi_conexion.commit()
            mi_conexion.close()

            # Actualizar el total de ventas
            self.total_listado_ventas()
        
        except Exception as e:
            messagebox.showerror('Actualizar Listado de Ventas', f'Ocurrió un error: {e}')
    def actualizar_monto_venta(self, id_venta):
        try:
            with sqlite3.connect('Ventas.db') as mi_conexion:
                mi_cursor = mi_conexion.cursor()
                
                # Calcular el nuevo monto total sumando (Precio * Cantidad) para todos los detalles de la venta
                mi_cursor.execute("""
                    SELECT SUM(Precio * Cantidad) 
                    FROM DetalleVenta 
                    WHERE No = ?
                """, (id_venta,))
                
                nuevo_total = mi_cursor.fetchone()[0] or 0.0  # Obtener el total calculado, o 0 si es None

                # Actualizar el monto total en la base de datos
                mi_cursor.execute("UPDATE Ventas SET Montante = ? WHERE No = ?", (nuevo_total, id_venta))

        except Exception as e:
            messagebox.showerror('Actualizar Monto Venta', f'Ocurrió un error al actualizar el monto: {e}')


    def imprimir_venta_pdf(self):
        try:
            # Obtener detalles de la venta
            venta_id = self.lbl_no_venta.cget('text')
            cliente_nombre = self.lbl_cliente_venta.cget('text')

            # Crear una ventana emergente para guardar el PDF
            archivo_pdf = filedialog.asksaveasfilename(defaultextension='.pdf',
                                                    filetypes=[("Archivo PDF", "*.pdf")],
                                                    title="Guardar Venta como PDF")
            if not archivo_pdf:
                return  # Si el usuario cancela, salir de la función

            # Crear el PDF usando reportlab
            pdf = canvas.Canvas(archivo_pdf, pagesize=A4)
            pdf.setTitle(f"Venta No {venta_id}")
            pdf.setFont("Helvetica", 12)

            # Reducimos el margen izquierdo y ajustamos las posiciones
            margen_izquierdo = 50  # Puedes ajustar este valor según necesites

            # Título de la Venta
            pdf.drawString(margen_izquierdo, 800, f"Detalles de la Venta No {venta_id}")
            pdf.drawString(margen_izquierdo, 780, f"Cliente: {cliente_nombre}")

            # Encabezado de tabla
            pdf.drawString(margen_izquierdo, 750, "Código Producto")
            pdf.drawString(margen_izquierdo + 100, 750, "Descripción")
            pdf.drawString(margen_izquierdo + 250, 750, "Cantidad")
            pdf.drawString(margen_izquierdo + 350, 750, "Precio Unitario")
            pdf.drawString(margen_izquierdo + 450, 750, "Subtotal")

            # Variables de posición para ir bajando las filas
            y_position = 730

            # Obtener los productos del TreeView
            for fila in self.tree_listado_detalle_venta.get_children():
                datos_producto = self.tree_listado_detalle_venta.item(fila, 'values')

                pdf.drawString(margen_izquierdo, y_position, str(datos_producto[1]))  # Código
                pdf.drawString(margen_izquierdo + 100, y_position, str(datos_producto[2]))  # Descripción
                pdf.drawString(margen_izquierdo + 250, y_position, str(datos_producto[5]))  # Cantidad
                pdf.drawString(margen_izquierdo + 350, y_position, f"{float(datos_producto[4]):,.2f} €")  # Precio
                pdf.drawString(margen_izquierdo + 450, y_position, f"{float(datos_producto[8]):,.2f} €")  # Subtotal

                y_position -= 20  # Mover hacia abajo para la siguiente fila

            # Total de la venta
            pdf.drawString(margen_izquierdo, y_position - 20, f"Total Venta: {self.total_lista_detalle_ventas:,.2f} € IVA inc.")

            # Guardar el PDF
            pdf.save()
            messagebox.showinfo("Éxito", "La venta ha sido guardada como PDF correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al generar el PDF: {e}")



#=================================INFORMES===========================================
    def ventana_reportes(self):
        self.borrar_frames()
        
        self.frame_reportes=Frame(master=self.frame_center)
        #va a la segunda columna, la columna 1, la primera es la 0
        self.frame_reportes.grid(row=0,column=1,sticky=NSEW)
        
        lblframe_reportes=tb.LabelFrame(master=self.frame_reportes,text='Lista de Reportes')
        lblframe_reportes.grid(row=0,column=0,padx=10,pady=10)
        
        btn_cuadre_contado=tb.Button(master=lblframe_reportes,text='Cuadre Contado',width=20,
        bootstyle='success',command=self.ventana_cuadre_contado)
        btn_cuadre_contado.grid(row=0,column=0,padx=10,pady=10)
        
        btn_cuadre_credito=tb.Button(master=lblframe_reportes,text='Cuadre Crédito',width=20,
        bootstyle='success')
        btn_cuadre_credito.grid(row=1,column=0,padx=10,pady=10)
    def ventana_cuadre_contado(self):
        self.borrar_frames()
        
        # Creación del frame principal
        self.frame_cuadre_contado = Frame(master=self.frame_center)
        self.frame_cuadre_contado.grid(row=0, column=1, sticky=NSEW)
        
        # LabelFrame para la búsqueda
        lblframe_busqueda_cuadre_contado = tb.LabelFrame(master=self.frame_cuadre_contado, text='Búsqueda')
        lblframe_busqueda_cuadre_contado.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        
        # Label y DateEntry para la fecha
        lbl_fecha_cuadre_contado = tb.Label(master=lblframe_busqueda_cuadre_contado, text='Fecha', bootstyle='info', font=('Calibri', 14))
        lbl_fecha_cuadre_contado.grid(row=0, column=0, pady=10, padx=10, sticky=W)  # Alineación a la izquierda
        
        self.ent_fecha_cuadre_contado = tb.DateEntry(master=lblframe_busqueda_cuadre_contado)
        self.ent_fecha_cuadre_contado.grid(row=0, column=1, pady=10, padx=10, sticky=W)
        
        # Botón para buscar
        btn_buscar_cuadre_contado = tb.Button(master=lblframe_busqueda_cuadre_contado, text='Buscar', width=15, bootstyle='success',command=self.mostrar_cuadre_contado)
        btn_buscar_cuadre_contado.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        
        # LabelFrame para mostrar detalles
        lblframe_cuadre_contado = tb.LabelFrame(master=self.frame_cuadre_contado, text='Detalle')
        lblframe_cuadre_contado.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)
        
        # Label y valor para Ventas
        lbl_venta_contado = tb.Label(master=lblframe_cuadre_contado, text='Ventas', bootstyle='primary', font=('Calibri', 14))
        lbl_venta_contado.grid(row=0, column=0, pady=10, padx=10, sticky=W)  # Alineación a la izquierda
        
        self.lbl_total_contado = tb.Label(master=lblframe_cuadre_contado, text='0.00€', bootstyle='primary', font=('Calibri', 14))
        self.lbl_total_contado.grid(row=0, column=1, pady=10, padx=10, sticky=E)  # Alineación a la derecha
        
        # Label y valor para Utilidad
        lbl_utilidad_contado = tb.Label(master=lblframe_cuadre_contado, text='Utilidad', bootstyle='success', font=('Calibri', 14))
        lbl_utilidad_contado.grid(row=1, column=0, pady=10, padx=10, sticky=W)  # Alineación a la izquierda
        
        self.lbl_utilidad_total = tb.Label(master=lblframe_cuadre_contado, text='0.00€', bootstyle='success', font=('Calibri', 14))
        self.lbl_utilidad_total.grid(row=1, column=1, pady=10, padx=10, sticky=E)  # Alineación a la derecha
        
        # Label y valor para Descuento
        lbl_descuento_contado = tb.Label(master=lblframe_cuadre_contado, text='Descuento', bootstyle='danger', font=('Calibri', 14))
        lbl_descuento_contado.grid(row=2, column=0, pady=10, padx=10, sticky=W)  # Alineación a la izquierda
        
        self.lbl_descuento_total = tb.Label(master=lblframe_cuadre_contado, text='0.00€', bootstyle='danger', font=('Calibri', 14))
        self.lbl_descuento_total.grid(row=2, column=1, pady=10, padx=10, sticky=E)  # Alineación a la derecha
        self.mostrar_cuadre_contado()        
    def mostrar_cuadre_contado(self):
        try:
            # Conexión a la base de datos con 'with'
            with sqlite3.connect('Ventas.db') as mi_conexion:
                mi_cursor = mi_conexion.cursor()

                # Crear variable fecha para almacenar la fecha
                fecha = self.ent_fecha_cuadre_contado.entry.get()

                # Consulta SQL para obtener los datos
                mi_cursor.execute("""
                    SELECT SUM(DetalleVenta.Precio * DetalleVenta.Cantidad) AS Venta,
                        SUM(DetalleVenta.Precio * DetalleVenta.Cantidad) - SUM(DetalleVenta.Coste * DetalleVenta.Cantidad) AS Utilidad,
                        SUM(DetalleVenta.Descuento * DetalleVenta.Cantidad) AS Descuentos
                    FROM Ventas 
                    INNER JOIN DetalleVenta ON Ventas.No = DetalleVenta.No 
                    WHERE Ventas.Fecha LIKE ? AND Ventas.Tipo = 'Contado'
                """, ("%"+fecha+"%",))

                datos_cuadre_contado = mi_cursor.fetchall()

                # Verificar si no hay ventas en el día
                if datos_cuadre_contado == [(None, None, None)]:
                    messagebox.showinfo('Sin Ventas', 'No existen ventas del día')
                    self.limpiar_cuadre_contado()
                    return

                # Inicializar acumuladores
                total_venta_contado = 0.00
                total_utilidad_contado = 0.00
                total_descuento_contado = 0.00

                # Procesar los resultados y actualizar las etiquetas
                for fila in datos_cuadre_contado:
                    total_venta_contado += float(fila[0] or 0)
                    total_utilidad_contado += float(fila[1] or 0)
                    total_descuento_contado += float(fila[2] or 0)

                self.lbl_total_contado.config(text=f"{total_venta_contado:,.2f}€")
                self.lbl_utilidad_total.config(text=f"{total_utilidad_contado:,.2f}€")
                self.lbl_descuento_total.config(text=f"{total_descuento_contado:,.2f}€")

        except Exception as e:
            messagebox.showerror('Cuadre Ventas de Contado', f'Ocurrió un error: {e}')
            self.limpiar_cuadre_contado()

    def limpiar_cuadre_contado(self):
        #etiquetas labell Llamo a config para reinicializar
        self.lbl_total_contado.config(text='0.00 €')
        self.lbl_utilidad_total.config(text='0.00 €')
        self.lbl_descuento_total.config(text='0.00 €')





#=================================BORRAR FRAMES===========================================
    def borrar_frames(self):
        for frames in self.frame_center.winfo_children():
            frames.destroy()
        self.frame_busqueda_detalle_venta.grid_forget()


# Función principal que configura y ejecuta la ventana
def main():
    app = Ventana()  # Crea una instancia de la clase Ventana
    app.title('Sistema de Ventas')  # Establece el título de la ventana
    app.state('zoomed')  # Abre la ventana en modo maximizado
    tb.Style('solar')
    app.mainloop()  # Inicia el bucle principal de la aplicación

# Ejecuta la función main solo si el script se ejecuta directamente
if __name__ == '__main__':
    main()

    