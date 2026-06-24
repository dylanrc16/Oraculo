import json
import os

class NodoDecision:
    def __init__(self, texto, es_pregunta=True):
        self.texto = texto
        self.es_pregunta = es_pregunta
        self.si = None  # Hijo izquierdo (Si el usuario dice SÍ)
        self.no = None  # Hijo derecho (Si el usuario dice NO)


class ArbolDecision:
    def __init__(self):
        # Árbol base inicial por defecto exigido por el cartel
        self.raiz = NodoDecision("¿Es un animal?", es_pregunta=True)
        self.raiz.si = NodoDecision("Perro", es_pregunta=False)
        self.raiz.no = NodoDecision("Computadora", es_pregunta=False)

    def _nodo_a_diccionario(self, nodo):
        """Función auxiliar para convertir el árbol en un diccionario mapeable a JSON."""
        if nodo is None:
            return None
        
        # Si es un objeto/animal (nodo hoja), guardamos su texto
        if not nodo.es_pregunta:
            return {"texto": nodo.texto, "es_pregunta": False}
        
        # Si es pregunta, guardamos sus hijos de forma recursiva
        return {
            "texto": nodo.texto,
            "es_pregunta": True,
            "si": self._nodo_a_diccionario(nodo.si),
            "no": self._nodo_a_diccionario(nodo.no)
        }

    def _diccionario_a_nodo(self, datos):
        """Función auxiliar para reconstruir el árbol desde el diccionario estructurado."""
        if datos is None:
            return None
        
        # VERIFICACIÓN: Validar que el diccionario tenga las llaves obligatorias (RF-14)
        if not isinstance(datos, dict) or "texto" not in datos or "es_pregunta" not in datos:
            raise ValueError("Formato de nodo inválido")
            
        nodo = NodoDecision(datos["texto"], datos["es_pregunta"])
        if datos["es_pregunta"]:
            # Validar que una pregunta tenga declaradas sus ramas hijas
            if "si" not in datos or "no" not in datos:
                raise ValueError("Pregunta sin ramas definidas")
            nodo.si = self._diccionario_a_nodo(datos["si"])
            nodo.no = self._diccionario_a_nodo(datos["no"])
            
        return nodo

    def guardar_en_archivo(self, ruta_archivo):
        """Guarda el árbol en un archivo JSON válido."""
        try:
            diccionario_completo = self._nodo_a_diccionario(self.raiz)
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(diccionario_completo, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False

    def cargar_desde_archivo(self, ruta_archivo):
        """Carga el árbol desde un archivo JSON validando su integridad (RF-02)."""
        if not os.path.exists(ruta_archivo):
            return False
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                # Reconstruimos y verificamos la estructura completa
                nueva_raiz = self._diccionario_a_nodo(datos)
                if nueva_raiz is None:
                    return False
                self.raiz = nueva_raiz
            return True
        except (json.JSONDecodeError, ValueError, KeyError):
            # Captura archivos vacíos, dañados o con formato incorrecto de árbol
            return False