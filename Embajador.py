import threading
import re
import socket
import pickle

class Embajador:
    def __init__(self):
        self.word_fragments = {}  # Diccionario para almacenar los fragmentos de palabras con su estado
        self.available_nodes = {}  # Diccionario para hacer seguimiento de los nodos disponibles
        self.lock = threading.Lock()

    def separate_text(self, text):
        words = re.findall(r'\b\w+\b', text.lower())  # Encontrar todas las palabras en el texto
        chunk_size = len(words) // 3  # Dividir el texto en 3 fragmentos
        chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]
        return chunks

    def assign_word_fragments(self, fragments):
        with self.lock:
            for i, fragment in enumerate(fragments):
                fragment_id = f"A{i}"  # Asignar identificador al fragmento
                self.word_fragments[fragment_id] = {'state': 'A', 'data': fragment}  # A = Disponible

    def handle_new_node(self, node_id):
        with self.lock:
            self.available_nodes[node_id] = True

    def handle_node_exit(self, node_id):
        with self.lock:
            del self.available_nodes[node_id]

    def handle_load_balancing(self):
        pass  # Implementar lógica de equilibrio de carga aquí

    def merge_results(self):
        word_counts = {}
        for fragment_info in self.word_fragments.values():
            words = fragment_info['data']
            for word in words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
        return word_counts

    def handle_circuit_breaker_data(self, text):
        word_fragments = self.separate_text(text)
        self.assign_word_fragments(word_fragments)

    def start(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(('127.0.0.1', 5555))
        servidor.listen(4)
        print("El Embajador está escuchando en el puerto 5555")
        while True:
            conn, addr = servidor.accept()
            print("Conexión establecida con el Circuit Breaker")
            with conn:
                data = conn.recv(4096)
                text = pickle.loads(data)
                self.handle_circuit_breaker_data(text)
                word_counts = self.merge_results()
                
                conn.sendall(pickle.dumps(word_counts))
                print("Recuento de palabras enviado al Circuit Breaker.")

if __name__ == "__main__":
    embajador = Embajador()
    embajador.start()

