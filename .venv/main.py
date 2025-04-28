import user_controller
import db

while True:
    print("🌟 WELCOME TO THE TWITTER APP 🌟")
    print(f"Enter the option:\n1-SignUp\n2-Login\n3-Exit\n")
    option = int(input('choice: '))
    if option == 1:
        while True:
            print('You can press e for exit menu')
            username = input("Enter your username: ")
            if username == 'e':
                break
            if  len(username) > 2:
                break
        while True:
            print('You can press e for exit menu')
            password = input("Enter your password: ")
            b = user_controller.strong_password(password)
            if password == 'e':
                break
            elif b:
                break
            else:
                print("Wrong format of password!")

        while True:
            print('You can press e for exit menu')
            name = input("Enter your name: ")
            if name == 'e':
                break
            elif len(name) > 2:
                break
            else:
                print("Wrong format of name!")

        while True:
            print('You can press e for exit menu')
            email = input("Enter your email: ")
            b = user_controller.valid_email(email)
            if email == 'e':
                break
            elif b:
                break
            else:
                print("Wrong format of email!")

        while True:
            print('You can press e for exit menu')
            age_input = input("Enter your age: ")
            if age_input == 'e':
                break
            try:
                age = int(age_input)
                if age > 17:
                    break
                else:
                    print("Your age must be at least 18 years old")
            except ValueError:
                print("Please enter a valid number.")

        while True:
            d = ['male', 'female']
            print('You can press e for exit menu')
            gender = input("Enter your gender: ")
            if gender == 'e':
                break
            elif gender.lower() in d:
                break
            else:
                print("Wrong format of gender!")
        # Register in database
        try:
            user_controller.sign_up(username, password, name, email, age, gender, bio="")
        except:
            print("Something went wrong!")
            print()

    elif option == 2:
        username = input('Enter your Username: ')
        password = input('Enter your Password: ')
        user_controller.log_in(username, password)
    elif option == 3:
        print("Goodbye")
        break
    else:
        print("Invalid option")