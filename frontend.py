import tkinter as tk
from tkinter import messagebox, filedialog
from backend import *
import os

class AppJuego:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.ventana.title(" Akinator ")
        self.ventana.geometry("1000x500")
        self.ventana.resizable(False, False) # Evita que se deforme la ventana
        
        # Paleta de Colores: Estilo Claro, Limpio y Profesional (Light Mode)
        self.fondo_claro_general = "#f8fafc"   # Gris casi blanco muy limpio (slate-50)
        self.fondo_blanco_tarjeta = "#ffffff"  # Blanco puro para que resalten los cuadros
        self.borde_suave = "#e2e8f0"           # Gris claro para los bordes de los cuadros
        
        self.color_azul_botones = "#2563eb"    # Azul rey profesional para botones de acción
        self.color_azul_hover = "#1d4ed8"      # Azul más oscuro para cuando se presiona
        
        self.color_verde_si = "#16a34a"        # Verde amigable para el botón SÍ
        self.color_rojo_no = "#dc2626"         # Rojo suave para el botón NO y Salir
        
        self.color_texto_oscuro = "#0f172a"   # Gris oscuro casi negro para letras principales
        self.color_texto_gris = "#64748b"     # Gris medio para subtítulos secundarios

        self.ventana.configure(bg=self.fondo_claro_general)

        # Instancia del árbol lógico (Backend)
        self.arbol_logico = ArbolDecision()
        
        # SOLUCIÓN DE RUTA DINÁMICA: Detecta la carpeta donde corre este script
        self.ruta = os.path.dirname(os.path.abspath(__file__))
        
        # Nombre del archivo por defecto unificado a .json
        self.archivo_guardado_automatico = os.path.join(self.ruta, "arbol_progreso.json")

        # --- SISTEMA DE PERSISTENCIA INICIAL ---
        # Si ya hay un progreso guardado anteriormente, se carga; si no, se crea el base de una vez
        if os.path.exists(self.archivo_guardado_automatico):
            self.arbol_logico.cargar_desde_archivo(self.archivo_guardado_automatico)
        else:
            self.arbol_logico.guardar_en_archivo(self.archivo_guardado_automatico)

        # Variables de control de recorrido
        self.nodo_actual = None
        self.nodo_padre_actual = None
        self.el_ultimo_paso_fue_si = True

        # Contenedor principal dinámico
        self.contenedor_pantallas = tk.Frame(self.ventana, bg=self.fondo_claro_general)
        self.contenedor_pantallas.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)

        # Mostrar menú de inicio al arrancar
        self.mostrar_menu_inicio()

    def limpiar_pantalla(self):
        """Borra los componentes visuales anteriores para redibujar."""
        for componente in self.contenedor_pantallas.winfo_children():
            componente.destroy()

    def mostrar_menu_inicio(self):
        self.limpiar_pantalla()

        # Título del juego elegante y minimalista
        etiqueta_titulo = tk.Label(
            self.contenedor_pantallas, text=" AKINATOR ", 
            font=("Segoe UI", 26, "bold"), bg=self.fondo_claro_general, fg=self.color_texto_oscuro
        )
        etiqueta_titulo.pack(pady=(30, 5))

        etiqueta_subtitulo = tk.Label(
            self.contenedor_pantallas, text="Pensá en algo y la Inteligencia Artificial intentará adivinar.", 
            font=("Segoe UI", 11), bg=self.fondo_claro_general, fg=self.color_texto_gris
        )
        etiqueta_subtitulo.pack(pady=(0, 40))

        # Botón para empezar a jugar
        boton_jugar = tk.Button(
            self.contenedor_pantallas, text="🎮 EMPEZAR A JUGAR", font=("Segoe UI", 12, "bold"),
            bg=self.color_azul_botones, fg="white", activebackground=self.color_azul_hover, activeforeground="white",
            relief="flat", width=24, bd=0, cursor="hand2", pady=12, command=self.iniciar_partida
        )
        boton_jugar.pack(pady=8)

        # Zona horizontal para botones de archivos (.json)
        fila_botones_archivos = tk.Frame(self.contenedor_pantallas, bg=self.fondo_claro_general)
        fila_botones_archivos.pack(pady=20)

        boton_cargar = tk.Button(
            fila_botones_archivos, text="📂 Cargar Árbol", font=("Segoe UI", 10, "bold"),
            bg=self.fondo_blanco_tarjeta, fg=self.color_texto_oscuro, 
            activebackground=self.borde_suave, activeforeground=self.color_texto_oscuro,
            relief="solid", bd=1, highlightthickness=0, width=14, cursor="hand2", pady=8, command=self.presionar_boton_cargar
        )
        boton_cargar.config(highlightbackground=self.borde_suave)
        boton_cargar.pack(side=tk.LEFT, padx=10)

        boton_guardar = tk.Button(
            fila_botones_archivos, text="💾 Guardar Como", font=("Segoe UI", 10, "bold"),
            bg=self.fondo_blanco_tarjeta, fg=self.color_texto_oscuro, 
            activebackground=self.borde_suave, activeforeground=self.color_texto_oscuro,
            relief="solid", bd=1, highlightthickness=0, width=14, cursor="hand2", pady=8, command=self.presionar_boton_guardar
        )
        boton_guardar.config(highlightbackground=self.borde_suave)
        boton_guardar.pack(side=tk.LEFT, padx=10)

        # Separador visual sutil
        linea_decorativa = tk.Label(self.contenedor_pantallas, text="─────────────────────────────", font=("Arial", 10), bg=self.fondo_claro_general, fg=self.borde_suave)
        linea_decorativa.pack(pady=5)

        # Botón para salir exigido por las pautas
        boton_salir = tk.Button(
            self.contenedor_pantallas, text="🚪 Salir del Sistema", font=("Segoe UI", 11, "bold"),
            bg=self.color_rojo_no, fg="white", activebackground="#b91c1c", activeforeground="white",
            relief="flat", width=24, bd=0, cursor="hand2", pady=8, command=self.ventana.quit
        )
        boton_salir.pack(pady=15)

    def iniciar_partida(self):
        """Reinicia los punteros a la raíz del árbol para empezar de cero."""
        self.nodo_actual = self.arbol_logico.raiz
        self.nodo_padre_actual = None
        self.el_ultimo_paso_fue_si = True
        self.mostrar_pantalla_pregunta_o_sospecha()

    def mostrar_pantalla_pregunta_o_sospecha(self):
        self.limpiar_pantalla()

        # Si el nodo actual es una pregunta, continúa haciendo preguntas
        if self.nodo_actual.es_pregunta:
            etiqueta_estado = tk.Label(self.contenedor_pantallas, text="PREGUNTA DEL SISTEMA", font=("Segoe UI", 9, "bold"), bg=self.fondo_claro_general, fg=self.color_azul_botones)
            etiqueta_estado.pack(pady=(10, 0))

            tarjeta_pregunta = tk.Frame(self.contenedor_pantallas, bg=self.fondo_blanco_tarjeta, bd=1, relief="solid", highlightbackground=self.borde_suave)
            tarjeta_pregunta.pack(expand=True, fill=tk.BOTH, pady=25, padx=10)

            texto_pregunta = tk.Label(
                tarjeta_pregunta, text=self.nodo_actual.texto, 
                font=("Segoe UI", 18, "bold"), bg=self.fondo_blanco_tarjeta, fg=self.color_texto_oscuro, wraplength=480
            )
            texto_pregunta.pack(expand=True, padx=35, pady=35)

            fila_respuestas = tk.Frame(self.contenedor_pantallas, bg=self.fondo_claro_general)
            fila_respuestas.pack(pady=(0, 20))

            boton_si = tk.Button(
                fila_respuestas, text="SÍ, CLARO", font=("Segoe UI", 11, "bold"),
                bg=self.color_verde_si, fg="white", activebackground="#15803d", activeforeground="white",
                relief="flat", width=14, bd=0, cursor="hand2", pady=12,
                command=self.responder_con_si
            )
            boton_si.pack(side=tk.LEFT, padx=15)

            boton_no = tk.Button(
                fila_respuestas, text="NO, TOTAL", font=("Segoe UI", 11, "bold"),
                bg=self.color_rojo_no, fg="white", activebackground="#b91c1c", activeforeground="white",
                relief="flat", width=14, bd=0, cursor="hand2", pady=12,
                command=self.responder_con_no
            )
            boton_no.pack(side=tk.LEFT, padx=15)
        else:
            # Si el nodo es hoja, la IA intenta adivinar el objeto
            self.mostrar_pantalla_adivinacion_final()

    def responder_con_si(self):
        self.nodo_padre_actual = self.nodo_actual
        self.nodo_actual = self.nodo_actual.si
        self.el_ultimo_paso_fue_si = True
        self.mostrar_pantalla_pregunta_o_sospecha()

    def responder_con_no(self):
        self.nodo_padre_actual = self.nodo_actual
        self.nodo_actual = self.nodo_actual.no
        self.el_ultimo_paso_fue_si = False
        self.mostrar_pantalla_pregunta_o_sospecha()

    def mostrar_pantalla_adivinacion_final(self):
        self.limpiar_pantalla()

        etiqueta_estado = tk.Label(self.contenedor_pantallas, text="PREDICCIÓN FINAL", font=("Segoe UI", 9, "bold"), bg=self.fondo_claro_general, fg=self.color_azul_botones)
        etiqueta_estado.pack(pady=(10, 0))

        tarjeta_sospecha = tk.Frame(self.contenedor_pantallas, bg=self.fondo_blanco_tarjeta, bd=1, relief="solid", highlightbackground=self.borde_suave)
        tarjeta_sospecha.pack(expand=True, fill=tk.BOTH, pady=25, padx=10)

        texto_sospecha = tk.Label(
            tarjeta_sospecha, text=f"¿Estás pensando en...\n\n {self.nodo_actual.texto.upper()}? ", 
            font=("Segoe UI", 18, "bold"), bg=self.fondo_blanco_tarjeta, fg=self.color_texto_oscuro, wraplength=480
        )
        texto_sospecha.pack(expand=True, padx=35, pady=35)

        fila_botones_veredicto = tk.Frame(self.contenedor_pantallas, bg=self.fondo_claro_general)
        fila_botones_veredicto.pack(pady=(0, 20))

        boton_correcto = tk.Button(
            fila_botones_veredicto, text="¡Sí, correcto! 🎉", font=("Segoe UI", 11, "bold"),
            bg=self.color_verde_si, fg="white", activebackground="#15803d", activeforeground="white",
            relief="flat", width=16, bd=0, cursor="hand2", pady=12, command=self.procesar_victoria_ia
        )
        boton_correcto.pack(side=tk.LEFT, padx=15)

        boton_incorrecto = tk.Button(
            fila_botones_veredicto, text="No, fallaste ❌", font=("Segoe UI", 11, "bold"),
            bg=self.color_rojo_no, fg="white", activebackground="#b91c1c", activeforeground="white",
            relief="flat", width=16, bd=0, cursor="hand2", pady=12, command=self.mostrar_pantalla_aprendizaje
        )
        boton_incorrecto.pack(side=tk.LEFT, padx=15)

    def procesar_victoria_ia(self):
        messagebox.showinfo("🎉🎉", "¡FELICIDADES A MÍ! He adivinado correctamente.")
        
        querer_otra_partida = messagebox.askyesno("Nueva partida", "¿Querés iniciar otra partida inmediatamente?")
        if querer_otra_partida:
            self.iniciar_partida()
        else:
            self.mostrar_menu_inicio()

    def mostrar_pantalla_aprendizaje(self):
        self.limpiar_pantalla()

        tk.Label(
            self.contenedor_pantallas, text="El sistema falló. Ayúdanos a aprender", 
            font=("Segoe UI", 14, "bold"), bg=self.fondo_claro_general, fg=self.color_texto_oscuro
        ).pack(pady=(5, 15))
        
        tarjeta_formulario = tk.Frame(self.contenedor_pantallas, bg=self.fondo_blanco_tarjeta, bd=1, relief="solid", highlightbackground=self.borde_suave)
        tarjeta_formulario.pack(expand=True, fill=tk.BOTH, pady=5, padx=10)

        # Entrada para el nuevo objeto
        tk.Label(tarjeta_formulario, text="¿En qué estabas pensando realmente?", font=("Segoe UI", 9, "bold"), bg=self.fondo_blanco_tarjeta, fg=self.color_texto_gris).pack(anchor=tk.W, padx=30, pady=(15, 2))
        self.entrada_nuevo_objeto = tk.Entry(tarjeta_formulario, font=("Segoe UI", 11), bg=self.fondo_claro_general, fg=self.color_texto_oscuro, highlightthickness=1, highlightbackground=self.borde_suave, relief="flat", bd=4)
        self.entrada_nuevo_objeto.pack(fill=tk.X, padx=30, pady=2)

        # Entrada para la nueva pregunta
        tk.Label(tarjeta_formulario, text=f"Escribe una pregunta para diferenciar tu objeto de '{self.nodo_actual.texto}':", font=("Segoe UI", 9, "bold"), bg=self.fondo_blanco_tarjeta, fg=self.color_texto_gris).pack(anchor=tk.W, padx=30, pady=(15, 2))
        self.entrada_nueva_pregunta = tk.Entry(tarjeta_formulario, font=("Segoe UI", 11), bg=self.fondo_claro_general, fg=self.color_texto_oscuro, highlightthickness=1, highlightbackground=self.borde_suave, relief="flat", bd=4)
        self.entrada_nueva_pregunta.pack(fill=tk.X, padx=30, pady=2)

        # Configuración de respuesta Sí o No
        fila_seleccion_respuesta = tk.Frame(tarjeta_formulario, bg=self.fondo_blanco_tarjeta)
        fila_seleccion_respuesta.pack(fill=tk.X, padx=30, pady=15)

        tk.Label(fila_seleccion_respuesta, text="Para tu objeto, la respuesta es:", font=("Segoe UI", 9, "bold"), bg=self.fondo_blanco_tarjeta, fg=self.color_texto_oscuro).pack(side=tk.LEFT, pady=5)
        
        self.variable_seleccion_si_no = tk.StringVar(value="Sí")
        menu_desplegable = tk.OptionMenu(fila_seleccion_respuesta, self.variable_seleccion_si_no, "Sí", "No")
        menu_desplegable.config(font=("Segoe UI", 10, "bold"), width=6, bg=self.fondo_claro_general, fg=self.color_azul_botones, activebackground=self.fondo_claro_general, activeforeground=self.color_azul_botones, relief="flat", bd=0, highlightthickness=0)
        menu_desplegable["menu"].config(bg=self.fondo_blanco_tarjeta, fg=self.color_texto_oscuro, font=("Segoe UI", 10), bd=0)
        menu_desplegable.pack(side=tk.LEFT, padx=15)

        # Botón para registrar el aprendizaje
        boton_guardar_conocimiento = tk.Button(
            self.contenedor_pantallas, text="💾 GUARDAR CONOCIMIENTO", font=("Segoe UI", 12, "bold"),
            bg=self.color_azul_botones, fg="white", activebackground=self.color_azul_hover, activeforeground="white",
            relief="flat", width=26, bd=0, cursor="hand2", pady=10, command=self.ejecutar_registro_aprendizaje
        )
        boton_guardar_conocimiento.pack(pady=(15, 5))

    def ejecutar_registro_aprendizaje(self):
        objeto_usuario = self.entrada_nuevo_objeto.get().strip().lower()
        pregunta_usuario = self.entrada_nueva_pregunta.get().strip()

        if objeto_usuario == "" or pregunta_usuario == "":
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")
            return

        if not pregunta_usuario.startswith("¿"): pregunta_usuario = "¿" + pregunta_usuario
        if not pregunta_usuario.endswith("?"): pregunta_usuario = pregunta_usuario + "?"

        respuesta_es_si = self.variable_seleccion_si_no.get() == "Sí"

        self.arbol_logico.aprender(
            self.nodo_padre_actual,
            self.el_ultimo_paso_fue_si,
            objeto_usuario,
            pregunta_usuario,
            respuesta_es_si
        )

        self.arbol_logico.guardar_en_archivo(self.archivo_guardado_automatico)
        messagebox.showinfo("Aprendizaje Completo", "¡Conocimiento guardado automáticamente!")

        # Esto es lo que faltaba
        jugar_de_nuevo = messagebox.askyesno("Nueva partida", "¿Querés jugar otra partida con el conocimiento nuevo?")
        if jugar_de_nuevo:
            self.iniciar_partida()
        else:
            self.mostrar_menu_inicio()

    def presionar_boton_cargar(self):
        carpeta = os.path.normpath(self.ruta)
        # Filtro estricto para archivos .json (RF-02)
        ruta_archivo = filedialog.askopenfilename(title="Cargar árbol de decisiones", filetypes=[("Archivos JSON", "*.json")], initialdir=carpeta)
        if ruta_archivo:
            if self.arbol_logico.cargar_desde_archivo(ruta_archivo):
                self.archivo_guardado_automatico = ruta_archivo
                messagebox.showinfo("Éxito", "Árbol cargado de manera correcta")
            else:
                # Tolerancia a fallos: se levanta el árbol por defecto si está corrupto o vacío
                messagebox.showerror("Error", "Archivo corrupto, vacío o formato inválido. Se cargará el árbol por defecto.")
                self.arbol_logico = ArbolDecision()

    def presionar_boton_guardar(self):
        carpeta = os.path.normpath(self.ruta)
        # Filtro estricto para guardar como .json
        ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar árbol como...", 
            defaultextension=".json", 
            filetypes=[("Archivos JSON", "*.json")],
            initialdir=carpeta  
        )
        
        if ruta_archivo:
            if self.arbol_logico.guardar_en_archivo(ruta_archivo):
                self.archivo_guardado_automatico = ruta_archivo
                messagebox.showinfo("Éxito", "Árbol respaldado en disco de forma segura.")
            else:
                messagebox.showerror("Error", "Error crítico al intentar escribir en el archivo.")

if __name__ == "__main__":
    raiz_tk = tk.Tk()
    aplicacion = AppJuego(raiz_tk)
    raiz_tk.mainloop()