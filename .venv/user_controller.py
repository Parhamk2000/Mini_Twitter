import db
from db import users_col, tweets_col
from datetime import datetime
import re


def strong_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    return bool(re.match(pattern, password))

def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def sign_up(username, password, name, email, age, gender, bio=""):
    if users_col.find_one({'username': username}):
        print("Username already exists")
        return

    if not strong_password(password):
        print("❌ Password must be at least 8 characters long and contain:")
        print("   - At least one lowercase letter")
        print("   - At least one uppercase letter")
        print("   - At least one digit")
        return

    if not valid_email(email):
        print("❌ Invalid email address.")
        return

    users_col.insert_one({
        "username": username,
        "password": password,
        "name": name,
        "age": age,
        "gender": gender,
        "email": email,
        "bio": bio,
        "created_at": datetime.utcnow()
    })
    print("✅ Signup successful!")

def log_in(username, password):
    user = users_col.find_one({'username': username})
    if not user:
        print("❌ Username not found.")
        return None
    if user['password'] != password:
        print("❌ Incorrect password.")
        return None
    while True:
        print(f"\n🎉 ✅ Welcome back, {user['name']}!\n")
        print("👇 What would you like to do?")
        print(" 1️⃣  Tweet something new")
        print(" 2️⃣  Go to your profile panel")
        print(" 3️⃣  See all tweets")
        print(" 4️⃣  Exit to main menu\n")
        ans = input("Choice: ")

        if ans == "1":
            print("\n📝 What's on your mind?")
            tweet = input("✍️  Enter your tweet: ")
            db.tweets_col.insert_one({
                "tweet": tweet,
                "created_at": datetime.utcnow(),
                "username": username,
                "name": user['name'],
            })
            print("\n✅ Your tweet has been posted successfully!")
            print("🚀 Check your profile to see it live!\n")

        elif ans == "2":
            print(f"Name: {user['name']}\nEmail: {user['email']}")
            print(40 * "-")
            tweets = tweets_col.find({'username': username})
            for tweet in tweets:
                print(f'Tweet: {tweet["tweet"]} at {tweet["created_at"]}')
            print()

            while True:
                choice = input('1.Edit Profile\n2.View Profile\n3.Edit Tweets\n4.Exit\n')

                if choice == "1":
                    update_user(username)

                elif choice == "2":
                    users = users_col.find({'username': username})
                    tweets = len(list(db.tweets_col.find({'username': username})))
                    print("-"*20,"Profile","-"*20)
                    for user in users:
                        print(f'Name: {user["name"]}\nEmail: {user["email"]}\nAge: {user["age"]}\n'
                              f'Gender: {user["gender"]}\nBio: {user["bio"]}\nTweets count: {tweets}')
                        print(40 * "-")

                elif choice == "3":
                    tweets = list(tweets_col.find({'username': username}))
                    if not tweets:
                        print('No tweets found.')
                    else:
                        for idx, tweet in enumerate(tweets):
                            print(f'{idx + 1} - Tweet: {tweet["tweet"]} at {tweet["created_at"]}')
                        ans = input('Which tweet number do you want to edit? ')
                        try:
                            ans = int(ans)
                            if 1 <= ans < len(tweets) + 1:
                                selected_tweet = tweets[ans]
                                new_tweet = input('Enter new tweet content: ')
                                tweets_col.update_one(

                                    {'_id': selected_tweet['_id']},

                                    {'$set': {'tweet': new_tweet}}

                                )
                                print('Tweet updated successfully ✅')
                            else:
                                print('Invalid tweet number ❌')
                        except ValueError:

                            print('Please enter a valid number.')

                elif choice == "4":
                    break

                else:
                    print('Please enter a valid number.')

        elif ans == "3":
            tweets = list(tweets_col.find())
            if not tweets:
                print('No tweets found.')
            else:
                for tweet in tweets:
                    print(f'Tweet: {tweet["tweet"]} at {tweet["created_at"]}\nWriter: {tweet["username"]}')
                    print(40 * "-")
        elif ans == "4":
            break

        else:
            print('Invalid choice.')

def update_user(username):
    user = users_col.find_one({'username': username})
    if user:
        print("\n(Press 'e' at any time to cancel updating)\n")
        # Name
        while True:
            name = input("Enter your name: ")
            if name.lower() == 'e':
                print('Operation canceled ❌')
                return
            if len(name) > 2:
                break
            else:
                print("❗ Wrong format of name (at least 3 characters)!")
        # Age
        while True:
            age_input = input("Enter your age: ")
            if age_input.lower() == 'e':
                print('Operation canceled ❌')
                return
            try:
                age = int(age_input)
                if age > 17:
                    break
                else:
                    print("❗ Your age must be at least 18 years old.")
            except ValueError:
                print("❗ Please enter a valid number.")
        # Gender
        while True:
            d = ['male', 'female']
            gender = input("Enter your gender (male/female): ")
            if gender.lower() == 'e':
                print('Operation canceled ❌')
                return
            if gender.lower() in d:
                gender = gender.lower()
                break
            else:
                print("❗ Wrong format of gender! (Only 'male' or 'female')")
        # Bio
        bio = input("Enter your bio (optional): ")
        if bio.lower() == 'e':
            print('Operation canceled ❌')
            return
        update_data = {
            'name': name,
            'age': age,
            'gender': gender,
            'bio': bio
        }
        users_col.update_one(
            {'username': username},
            {'$set': update_data}
        )
        print('✅ Updated Successfully!')
    else:
        print('❌ User not found.')

