import pandas as pd
import bcrypt

user_file = "users.csv"
users_df = pd.read_csv(user_file)

def is_hashed(pw):
    return pw.startswith("$2b$") or pw.startswith("$2a$")  # bcrypt hashes start like this

for i, row in users_df.iterrows():
    if not is_hashed(row["Password"]):
        hashed = bcrypt.hashpw(row["Password"].encode('utf-8'), bcrypt.gensalt())
        users_df.at[i, "Password"] = hashed.decode('utf-8')

users_df.to_csv(user_file, index=False)
print("✅ All plaintext passwords have been hashed.")
