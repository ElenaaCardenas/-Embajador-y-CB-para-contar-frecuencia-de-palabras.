import socket
import pickle

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 5555))
    print("Conectado al Embajador")
    
    # Enviamos datos al Embajador
    texto = """Hola, mundo. Esto es una cadena, se supone que debe tener varias palabras pues 
    vamos a realizar un conteo de frecuencia de las mismas usando el lenguaje de programación Python. 
    Ya no sé qué escribir pero sigo escribiendo para que poco a poco la cadena sea más larga y el 
    ejercicio de programación sea demostrable. Creo que con todo esto que he escrito es suficiente"""
    
    cliente.sendall(pickle.dumps(texto))

    # Recibimos el recuento de palabras del Embajador
    try:
        data = cliente.recv(4096)
        word_counts = pickle.loads(data)
        print("Recuento de palabras recibido del Embajador:")
        for palabra, frecuencia in word_counts.items():
            print(f"La palabra '{palabra}' tiene una frecuencia de {frecuencia}")
    except Exception as e:
        print("Error al recibir el recuento de palabras:", e)
    finally:
        cliente.close()

if __name__ == "__main__":
    main()
