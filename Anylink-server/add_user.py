from config import Configuration
if __name__ == "__main__":
    config = Configuration("/home/orikeidar01/config.json", "anylink")
    config.database.add_user("testusr@icloud.com",
                             "$6$uBE1saOxQ7JWCNH2$7h6J7n9cF0O5h6/.6EcoEF0iYE3JepfLQsN5Ldm3XiRPxuGNsmMlS/gq0sBCgAg.ShL37Q4on4/FMw6bUnz1A1","anylink")