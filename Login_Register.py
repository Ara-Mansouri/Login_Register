import os
import json
import hashlib
import re

User_Info="Users.json"
print("📁 Saving/reading file from:", os.path.abspath(User_Info))

def Load_Users():
    if os.path.exists(User_Info):
        with open(User_Info,"r") as file:
            try:
                Users=json.load(file)
                Users.setdefault("Users",[])
                return Users
            except json.JSONDecodeError: 
                   print("⚠ Error: user file is corrupted. Resetting it.")
                   Users=initialize_users_file()
    else:
        Users=initialize_users_file()
       
    return Users
def initialize_users_file():
          Users={"Users":[]}
          Save_user(Users)
          return Users
def Save_user(Users):
     with open(User_Info,"w") as file:
         json.dump(Users,file,indent=4)
def Password_Checker(Password):
    if len(Password)<8:
        print("❌ Password must be at least 8 characters long.")
        return False
    if not re.search(r"[a-z]",Password):
        print("❌ Password must contain at least one lowercase letter.")
        return False
    if not re.search(r"[A-Z]",Password):
        print("❌ Password must contain at least one uppercase  letter.")
        return False
    if not re.search(r"[0-9]", Password):
        print("❌ Password must contain at least one digit.")
        return False
    if not re.search(r"[!@#$%^&*()\-_=+]", Password):
        print("❌ Password must contain at least one special character (!@#$%^&*()-_+=).")
        return False
    return True
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def Register(Users):
   Name= input("Enter Your Name:")
   while True:
     Password=input("Enter Your Password:")
     if Password_Checker(Password):
       break
   hashpassword=hash_password(Password)
   User_Entry={"Name":Name,"Password":hashpassword,"State":0}
   if Register_Validator(Users,User_Entry):
        Users["Users"].append(User_Entry)
        Save_user(Users)

def Register_Validator(Users,User_Entry):
    if Users["Users"]:
        for user in Users["Users"]:
            if ( user["Name"]==User_Entry["Name"] and user["Password"]==User_Entry["Password"]):
                
                print("User Already Exists! please Login")
                return 0
        print("User Registered Successfuly!")
        return 1   
    else:
        print("User Registered Successfuly!")
        return 1
def Login(Users):
    Name= input("Enter Your Name:")
    Password=input("Enter Your Password:")
    hashpassword=hash_password(Password)
    for User in Users["Users"]:
        User["State"]=0
    for user in Users["Users"]:
        if user["Name"] == Name and user["Password"] == hashpassword:
                 user["State"] = 1  
                 Save_user(Users)
                 print(f"✅ Login under the name '{Name}' completed.")
                 return

    print("User Not Found Register First")           
def Show_users(Users):
    if Users["Users"]:
        print("Users Using This System are:")
        for User in Users["Users"]:
            print(f"{User['Name']}")
    else:
        print("❌ No users found.")
def login_Checker(Users):
    for user in Users["Users"]:
        if user["State"]==1:
            print(f"Login Under Name {user['Name']}")
            choice=input("Enter 1 if you want to Logout:")
            if choice=="1":
                Logout(user['Name'],user['Password'],Users)
                return 1
            else:
                login_Checker(Users)
    return 1
def Logout(name,password,Users):
    for user in Users['Users']:
        if user['Name']==name and user['Password']==password:
            user['State']=0
            print(f"Logout Under name {user['Name']} Successful")
            Save_user(Users)
   
def main(): 
    
    Users=Load_Users()
    while True:
            if login_Checker(Users):
                print("\n🔐 User System Menu")
                print("1. Register")
                print("2. Login")
                print("3. Show All existing Accounts")
                print("4. Exit")
                choice=input("Enter Your Choice:").strip()
                if choice=="1":
                   Register(Users)
                elif choice=="2":
                   Login(Users)
                elif choice=="3":
                     Show_users(Users)
                elif choice=="4":
                   break
                else:
                    print("⚠ Invalid Choice. Please enter a valid number.")


    
if __name__ == "__main__":
    main()
