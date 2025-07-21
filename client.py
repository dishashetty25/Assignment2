import sys
import socket
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("logs.txt", mode='a'),
        logging.StreamHandler()
    ]
)

def send_to_server(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 12345))
            s.send(message.encode())
            response = s.recv(1024).decode()
            return response
    except Exception as e:
        return f"FAILURE: {str(e)}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py \"Number|TABLENAME|Parameters\"")
        print("Example:")
        print("  python client.py \"1|Books|101\"")
        print("  python client.py \"2|Books|BookID=105, Title=ABC, Author=XYZ, Genre=Tech, YearPublished=2022\"")
        return

    message = sys.argv[1]
    response = send_to_server(message)
    logging.info(response)

if __name__ == "__main__":
    main()

