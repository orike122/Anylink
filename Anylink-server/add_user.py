from config import Configuration
if __name__ == "__main__":
    config = Configuration("/home/orikeidar01/config.json", "anylink")
    config.database.add_user("testusr@gmail.com",
                             "$6$/bPljc0H0oOo11nW$eE4vy9BMrHgKvPT//4wiTh7r2YtYTOLrm43qu5h.GyJ1ZrgN2f9lwNrVq6HxSZ6ysjCdIRGgUqXWSW6YSLq4B/","anylink")