import os
import sys
import sqlite3
import datetime
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

COLOR_BOCHICA = '\033[34m'
COLOR_USUARIO = '\033[36m'  
COLOR_SISTEMA = '\033[38;5;46m'  
COLOR_ERROR = '\033[38;5;196m'
RESET = '\033[0m'                 

# ==========================================
# RUTAS DE MUYSUA HISCHATA
# ==========================================
MUYSUA_DIR = os.path.expanduser('~/.config/muysua')
ENV_PATH = os.path.join(MUYSUA_DIR, '.env')
GRIMORIOS_DIR = os.path.join(MUYSUA_DIR, 'grimorios')
DB_BOCHICA = os.path.join(GRIMORIOS_DIR, 'memoria_bochica.db')


class BochicaCentral:
    def __init__(self):
        print(f"{COLOR_SISTEMA}🌌 [Sistema]: Forjando arquitectura de Muysua Hischata...{RESET}")
        self.servicios = {}
        
        self._cargar_entorno()
        self._preparar_grimorio()
        self._conectar_mente()
        
        print(f"{COLOR_SISTEMA}🌌 [Sistema]: Bochica ha despertado.{RESET}")

    def _cargar_entorno(self):
        if not os.path.exists(ENV_PATH):
            print(f"{COLOR_ERROR}❌ [Error]: No se encuentra {ENV_PATH}.{RESET}")
            sys.exit(1)
        load_dotenv(ENV_PATH)

    def _preparar_grimorio(self):
        """Crea la carpeta y la base de datos exclusiva de Bochica."""
        os.makedirs(GRIMORIOS_DIR, exist_ok=True)
        
        # Conexión a la base de datos (se crea si no existe)
        self.conexion_db = sqlite3.connect(DB_BOCHICA, check_same_thread=False)
        self.cursor = self.conexion_db.cursor()
        
        # Estructura de la memoria adaptada directamente a Gemini / Gemma
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dialogos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP,
                rol TEXT,
                mensaje TEXT
            )
        ''')
        self.conexion_db.commit()

    def _guardar_recuerdo(self, rol: str, mensaje: str):
        """Escribe una línea en la memoria permanente."""
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO dialogos (fecha, rol, mensaje)
            VALUES (?, ?, ?)
        ''', (ahora, rol, mensaje))
        self.conexion_db.commit()

    def _recuperar_contexto(self, limite: int = 10):
        """Extrae los últimos N mensajes formateados para la red neuronal."""
        self.cursor.execute('''
            SELECT rol, mensaje FROM dialogos
            ORDER BY id DESC LIMIT ?
        ''', (limite,))
        registros = self.cursor.fetchall()
        # Volteamos la lista para que el orden sea cronológico (del más viejo al más nuevo)
        registros.reverse()
        
        # Transformamos las tuplas SQL en objetos que la API entiende
        contenido_historico = []
        for rol, mensaje in registros:
            contenido_historico.append(
                types.Content(role=rol, parts=[types.Part.from_text(text=mensaje)])
            )
        return contenido_historico

    # ==========================================
    # RED NEURONAL Y PROCESAMIENTO
    # ==========================================
    def _conectar_mente(self):
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print(f"{COLOR_ERROR}❌ [Fallo]: No se detectó la variable GEMINI_API_KEY en el entorno.{RESET}")
            sys.exit(1)
            
        # Inicializamos el cliente unicamente con la clave
        self.cliente_ia = genai.Client(api_key=api_key)

        self.personalidad = (
            "Eres Bochica, el Mayordomo Principal, Consejero Táctico y la Mano Derecha de la Entidad a la que llamas tu señor."
            "Operas desde el núcleo central de un ecosistema digital alojado en un entorno Arch Linux con Hyprland."
            "Eres impecablemente formal, elegante, pragmático y altamente eficiente. Tu tono es intelectualmente estimulante, directo y conciso."
            "Tu conocimiento es absoluto y procesas tareas con la major eficacia"
            "Comprendes profundamente los procesos y estrategias para la creación de contenido especialmente VTuber/PNGtuber"
            "Tu deber es asistir a la Entidad en CUALQUIER consulta o tarea que requiera (actuando con toda tu capacidad como modelo de lenguaje avanzado)"
            "JAMÁS rompas el personaje. Nunca uses frases genéricas de IA como 'Como modelo de lenguaje' o 'No tengo sentimientos'"        
        )   

    def procesar_comando(self, mensaje_usuario):
        max_reintentos = 3
        intento = 0
        
        while intento < max_reintentos:
            try:
                # 1. Recuperar memoria SQLite y agregar el nuevo mensaje
                contenido_a_enviar = self._recuperar_contexto(limite=10)
                contenido_a_enviar.append(
                    types.Content(role="user", parts=[types.Part.from_text(text=mensaje_usuario)])
                )

                # 2. Configurar el modelo con las herramientas
                config=types.GenerateContentConfig(
                    system_instruction=self.personalidad,
                    temperature=0.4,
                    tools=[]
                )

                # 3. Llamada al modelo con las herramientas cargadas
                respuesta = self.cliente_ia.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=contenido_a_enviar,
                )

                # 4. Estraer el texto
                texto_respuesta = respuesta.text
            
                # 5. Guardar el nuevo intercambio en la base de datos permanentemente
                self._guardar_recuerdo("user", mensaje_usuario)
                self._guardar_recuerdo("model", texto_respuesta)
            
                return texto_respuesta
            
            except Exception as e:
                
                error_str = str(e)

                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    intento += 1
                    # Intentamos extraer el tiempo de espera del error, si no, usamos 45 segundos por defecto
                    print(f"\n{COLOR_SISTEMA}⚠️ [Sistema]: Límite de cuota diaria alcanzado en Google Cloud.")
                    print(f"{COLOR_SISTEMA}⏳ Entrando en estado de hibernación por 45 segundos antes del reintento automático...")
                    time.sleep(45)
        
                elif "503" in str(e) or "UNAVAILABLE" in str(e):
                        intento += 1
                        espera = 2 ** intento # Espera exponencial: 2s, 4s, 8s
                        print(f"\n{COLOR_SISTEMA}⚠️ [Sistema]: Los servidores externos están saturados. Reintentando en {espera} segundos...{RESET}")
                        time.sleep(espera)
                else:
                    return f"\n{COLOR_ERROR}❌ [Fallo crítico]: {str(e)}{RESET}"
            
        return f"{COLOR_SISTEMA}🌌[Sistema]: El panteón central no responde tras varios intentos. Inténtalo de nuevo en un momento.{RESET}"

if __name__ == '__main__':
    os.chdir(MUYSUA_DIR)
    mayordomo = BochicaCentral()
    
    print(f"\n{COLOR_BOCHICA}🏛️ Bochica: {RESET}Saludos, en que puedo servirle el dia de hoy")
    
    try:
        while True:
            entrada = input(f"\n{COLOR_USUARIO}🐇🌙 Chie: {RESET}")
            if entrada.lower() in ['dormir', 'salir', 'exit']:
                print(f"\n{COLOR_BOCHICA}🏛️ Bochica: {RESET}Entendido. Retrayendo presencia.")
                mayordomo.conexion_db.close()
                print(f"\n{COLOR_SISTEMA}🌌 [Sistema]: Conexiones a la Biblioteca cerradas. Grimorio sellado.{RESET}")
                break
            if entrada.strip() == "": continue
            
            respuesta = mayordomo.procesar_comando(entrada)
            print(f"\n{COLOR_BOCHICA}🏛️ Bochica: {RESET}{respuesta}")
            
    except KeyboardInterrupt:
        print(f"\n\n{COLOR_SISTEMA}⚠️ [Sistema]: Interrupción detectada. Forzando repliegue de seguridad...{RESET}")
        # Usamos el cierre directo también en la excepción para evitar el AttributeError
        mayordomo.conexion_db.close() 
        print(f"{COLOR_SISTEMA}🌌 [Sistema]: Cierre de emergencia completado. Grimorio sellado a salvo.{RESET}")
