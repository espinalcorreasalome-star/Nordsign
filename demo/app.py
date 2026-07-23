import os

import customtkinter as ctk
from PIL import Image

from tema import(
    COLOR_FONDO,
    COLOR_BARRA_SUPERIOR,
    COLOR_PANEL_LATERAL,
    COLOR_CONTENEDOR_CAMARA,
    COLOR_FONDO_CAMARA,
    COLOR_PANEL_RESULTADO,
    COLOR_BOTON_INICIAR,
    COLOR_BOTON_INICIAR_HOVER,
    COLOR_BOTON_FINALIZAR,
    COLOR_BOTON_FINALIZAR_HOVER,
    COLOR_TEXTO_OSCURO,
    COLOR_TEXTO_CLARO,
    COLOR_TEXTO_SEGUNDARIO,
    COLOR_TEXTO_ESPERA,
    ANCHO_VENTANA,
    ALTO_VENTANA,
    ANCHO_MINIMO,
    ALTO_MINIMO,
    RADIO_PANEL,
    RADIO_BOTON,
    RADIO_CAMARA,
    RADIO_RESULTADO,
    FUENTE_TITULO,
    FUENTE_DESCRIPCION,
    FUENTE_BOTON,
    FUENTE_RESULTADO_TITULO,
    FUENTE_RESULTADO,
    FUENTE_ESTADO,
    TITULO_APLICACION,
    DESCRIPCION_PROYECTO,
    TEXTO_INICIAR,
    TEXTO_FINALIZAR,
    TEXTO_RESULTADO,
    TEXTO_ESPERANDO,
    TEXTO_CAMARA_APAGADA,
    TEXTO_LISTO
)

#rutas

DEMO_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RECURSOS_DIR = os.path.join(
    DEMO_DIR,
    "recursos"
)

ARCHIVO_LOGO = os.path.join(
    RECURSOS_DIR,
    "logo_lasic_circular.png"
)

#configuracion general 
ctk.set_appearance_mode(
    "dark"
)

ctk.set_default_color_theme(
    "blue"
)

#aplicacion principal :)
class AplicacionLasic(ctk.CTk):

    def __init__(self):
        super().__init__()

        self._configurar_ventana()
        self._configurar_cuadricula()
        self._crear_barra_superior()
        self._crear_panel_lateral()
        self._crear_panel_derecho()

    def _configurar_ventana(self):
        self.title(
            TITULO_APLICACION
        )

        self.geometry(
            f"{ANCHO_VENTANA}x{ALTO_VENTANA}"
        )

        self.minsize(
            ANCHO_MINIMO,
            ALTO_MINIMO
        )

        self.configure(
            fg_color=COLOR_FONDO
        )

   
        self.title(
            TITULO_APLICACION
        )

        self.geometry(
            f"{ANCHO_VENTANA}x{ALTO_VENTANA}"
        )

        self.minsize(
            ANCHO_MINIMO,
            ALTO_MINIMO
        )

        self.configure(
            fg_color = COLOR_FONDO
        )

    def _configurar_cuadricula(self):
        # Fila 0: barra superior
        # Fila 1: contenido principal
        self.grid_rowconfigure(
            0,
            weight=0
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # Una sola columna principal
        self.grid_columnconfigure(
            0,
            weight=1
        )

    def _crear_barra_superior(self):
        self.barra_superior = ctk.CTkFrame(
            self,
            height=68,
            corner_radius=0,
            fg_color=COLOR_BARRA_SUPERIOR
        )

        self.barra_superior.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=22,
            pady=(20, 8)
        )

        self.barra_superior.grid_columnconfigure(
            0,
            weight=1
        )

        self.titulo = ctk.CTkLabel(
            self.barra_superior,
            text=TITULO_APLICACION,
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO_CLARO,
            anchor="w"
        )

        self.titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=22,
            pady=10
        )

    def _crear_panel_lateral(self):
        self.contenedor_principal = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.contenedor_principal.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=22,
            pady=(8, 22)
        )

        self.contenedor_principal.grid_rowconfigure(
            0,
            weight=1
        )

        self.contenedor_principal.grid_columnconfigure(
            0,
            weight=0,
            minsize=300
        )

        self.contenedor_principal.grid_columnconfigure(
            1,
            weight=1
        )

        self.panel_lateral = ctk.CTkFrame(
            self.contenedor_principal,
            width=300,
            corner_radius=RADIO_PANEL,
            fg_color=COLOR_PANEL_LATERAL
        )

        self.panel_lateral.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 14)
        )

        self.panel_lateral.grid_columnconfigure(
            0,
            weight=1
        )

        self.panel_lateral.grid_rowconfigure(
            4,
            weight=1
        )

        self._crear_logo()
        self._crear_descripcion()
        self._crear_botones()
        self._crear_estado()

    def _crear_logo(self):
        if os.path.exists(ARCHIVO_LOGO):
            imagen_logo = Image.open(
                ARCHIVO_LOGO
            )

            self.logo = ctk.CTkImage(
                light_image=imagen_logo,
                dark_image=imagen_logo,
                size=(190, 190)
            )

            self.logo_label = ctk.CTkLabel(
                self.panel_lateral,
                text="",
                image=self.logo
            )

        else:
            self.logo_label = ctk.CTkLabel(
                self.panel_lateral,
                text="LASIC",
                font=FUENTE_TITULO,
                text_color=COLOR_TEXTO_CLARO
            )

        self.logo_label.grid(
            row=0,
            column=0,
            padx=25,
            pady=(28, 12)
        )

    def _crear_descripcion(self):
        self.descripcion = ctk.CTkLabel(
            self.panel_lateral,
            text=DESCRIPCION_PROYECTO,
            font=FUENTE_DESCRIPCION,
            text_color=COLOR_TEXTO_SEGUNDARIO,
            justify="center",
            wraplength=235
        )

        self.descripcion.grid(
            row=1,
            column=0,
            padx=26,
            pady=(4, 25)
        )

    def _crear_botones(self):
        self.boton_iniciar = ctk.CTkButton(
            self.panel_lateral,
            text=TEXTO_INICIAR,
            height=52,
            corner_radius=RADIO_BOTON,
            fg_color=COLOR_BOTON_INICIAR,
            hover_color=COLOR_BOTON_INICIAR_HOVER,
            text_color=COLOR_TEXTO_CLARO,
            font=FUENTE_BOTON,
            command=self._prueba_iniciar
        )

        self.boton_iniciar.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=28,
            pady=(5, 12)
        )

        self.boton_finalizar = ctk.CTkButton(
            self.panel_lateral,
            text=TEXTO_FINALIZAR,
            height=52,
            corner_radius=RADIO_BOTON,
            fg_color=COLOR_BOTON_FINALIZAR,
            hover_color=COLOR_BOTON_FINALIZAR_HOVER,
            text_color=COLOR_TEXTO_OSCURO,
            font=FUENTE_BOTON,
            command=self._prueba_finalizar
        )

        self.boton_finalizar.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=28,
            pady=(0, 12)
        )

    def _crear_estado(self):
        self.estado_label = ctk.CTkLabel(
            self.panel_lateral,
            text=TEXTO_LISTO,
            font=FUENTE_ESTADO,
            text_color=COLOR_TEXTO_SEGUNDARIO
        )

        self.estado_label.grid(
            row=5,
            column=0,
            padx=20,
            pady=(10, 22)
        )

    def _crear_panel_derecho(self):
        self.panel_derecho = ctk.CTkFrame(
            self.contenedor_principal,
            fg_color="transparent"
        )

        self.panel_derecho.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.panel_derecho.grid_columnconfigure(
            0,
            weight=1
        )

        self.panel_derecho.grid_rowconfigure(
            0,
            weight=4
        )

        self.panel_derecho.grid_rowconfigure(
            1,
            weight=2
        )

        self._crear_panel_camara()
        self._crear_panel_resultado()

    def _crear_panel_camara(self):
        self.contenedor_camara = ctk.CTkFrame(
            self.panel_derecho,
            corner_radius=RADIO_CAMARA,
            fg_color=COLOR_CONTENEDOR_CAMARA
        )

        self.contenedor_camara.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 14)
        )

        self.contenedor_camara.grid_rowconfigure(
            0,
            weight=1
        )

        self.contenedor_camara.grid_columnconfigure(
            0,
            weight=1
        )

        self.vista_camara = ctk.CTkLabel(
            self.contenedor_camara,
            text=TEXTO_CAMARA_APAGADA,
            font=FUENTE_DESCRIPCION,
            text_color=COLOR_TEXTO_OSCURO,
            fg_color=COLOR_FONDO_CAMARA,
            corner_radius=RADIO_CAMARA
        )

        self.vista_camara.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

    def _crear_panel_resultado(self):
        self.panel_resultado = ctk.CTkFrame(
            self.panel_derecho,
            corner_radius=RADIO_RESULTADO,
            fg_color=COLOR_PANEL_RESULTADO
        )

        self.panel_resultado.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.panel_resultado.grid_columnconfigure(
            0,
            weight=1
        )

        self.panel_resultado.grid_rowconfigure(
            1,
            weight=1
        )

        self.resultado_titulo = ctk.CTkLabel(
            self.panel_resultado,
            text=TEXTO_RESULTADO,
            font=FUENTE_RESULTADO_TITULO,
            text_color=COLOR_TEXTO_OSCURO
        )

        self.resultado_titulo.grid(
            row=0,
            column=0,
            pady=(18, 4)
        )

        self.resultado_label = ctk.CTkLabel(
            self.panel_resultado,
            text=TEXTO_ESPERANDO,
            font=FUENTE_RESULTADO,
            text_color=COLOR_TEXTO_ESPERA
        )

        self.resultado_label.grid(
            row=1,
            column=0,
            pady=(0, 20)
        )

    def _prueba_iniciar(self):
        self.estado_label.configure(
            text="Botón iniciar presionado"
        )

        self.resultado_label.configure(
            text="A"
        )

    def _prueba_finalizar(self):
        self.estado_label.configure(
            text=TEXTO_LISTO
        )

        self.resultado_label.configure(
            text=TEXTO_ESPERANDO
        )

if __name__ == "__main__":
    app = AplicacionLasic()
    app.mainloop()