from config import Configuration
if __name__ == "__main__":
    config = Configuration("/home/orikeidar01/config.json", "anylink")
    config.database.add_user("test@icloud.com",
                             "ECD71870D1963316A97E3AC3408C9835AD8CF0F3C1BC703527C30265534F75AE","anylink")