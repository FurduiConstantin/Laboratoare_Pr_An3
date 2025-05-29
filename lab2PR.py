import socket
import threading

# Configurare rețea
MULTICAST_GROUP = "224.0.0.1"
MULTICAST_PORT = 5000
BUFFER_SIZE = 1024

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            print(f"\nMesaj primit de la {addr[0]}: {message}")
        except Exception as e:
            print(f"Eroare la primirea mesajului: {e}")
            break

def main():
    # Creare socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Asociază socket-ul la portul multicast
    sock.bind(("", MULTICAST_PORT))
    
    # Alăturare la grupul multicast
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = group + socket.inet_aton("0.0.0.0")
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    # Pornire fir de execuție pentru recepția mesajelor
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    
    print("\nChat UDP pornit! Scrie 'exit' pentru a ieși.")
    
    while True:
        try:
            message = input("\n> ")
            if message.lower() == "exit":
                break
            
            # Mesaj privat
            if message.startswith("@"):  
                parts = message.split(" ", 1)
                if len(parts) < 2:
                    print("Format greșit! Folosește: @IP mesaj")
                    continue
                target_ip, private_msg = parts[0][1:], parts[1]
                try:
                    sock.sendto(private_msg.encode("utf-8"), (target_ip, MULTICAST_PORT))
                    print(f"Mesaj privat trimis către {target_ip}")
                except Exception as e:
                    print(f"Eroare la trimiterea mesajului privat: {e}")
            else:
                # Mesaj public
                sock.sendto(message.encode("utf-8"), (MULTICAST_GROUP, MULTICAST_PORT))
        except Exception as e:
            print(f"Eroare la transmiterea mesajului: {e}")
            break
    
    # Închidere socket
    try:
        sock.close()
        print("Chat închis.")
    except Exception as e:
        print(f"Eroare la închiderea socket-ului: {e}")
    
if __name__ == "__main__":
    main()
