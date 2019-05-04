from client import Client


def main():
    client = Client(("35.237.82.70",8822))
    client.connect("testusr@gmail.com","abc")
    client.start_client()
if __name__ == "__main__":
    main()