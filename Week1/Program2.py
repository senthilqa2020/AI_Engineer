# Program2_PasswordRetry.py


def password_retry():
    # Step 1: Store the correct password
    correct_password = "openAI123"

    # Step 2: Allow the user 3 attempts
    for attempt in range(1, 4):  # 1 to 3
        entered_password = input(f"Attempt {attempt} - Enter password: ")

        # Step 3: Check if entered password is correct
        if entered_password == correct_password:
            print("Login Successful")
            break  # Exit the loop if correct
        else:
            print("Incorrect password.")

    # Step 4: If all 3 attempts fail → Account Locked
    else:  # This else belongs to the for loop
        print("Account Locked")


# Main program execution
if __name__ == "__main__":
    password_retry()
