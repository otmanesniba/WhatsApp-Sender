import pywhatkit
import re
import time
from colorama import Fore, Style, init
from pyfiglet import Figlet

# Initialize colorama
init(autoreset=True)

# ASCII Banner
def show_banner():
    f = Figlet(font='slant')
    print(Fore.CYAN + f.renderText('WA Sender Pro'))
    print(Fore.GREEN + "=" * 60)
    print(Fore.YELLOW + "⚡ Created by Otmane Sniba 7 | Safe WhatsApp Messaging Tool ⚡")
    print(Fore.GREEN + "=" * 60 + Style.RESET_ALL + "\n")

def validate_moroccan_number(number):
    """Check if the number matches Morocco's WhatsApp format (+212[67]XXXXXXXX)"""
    pattern = r'^\+212[67]\d{8}$'
    return re.match(pattern, number) is not None

def get_valid_number(prompt):
    """Keep asking until a valid Moroccan number is entered"""
    while True:
        num = input(Fore.CYAN + prompt + Style.RESET_ALL)
        if validate_moroccan_number(num):
            return num
        print(Fore.RED + "Invalid format! Use +212 followed by 9 digits starting with 6/7 (e.g., +212612345678)")

def send_messages():
    show_banner()
    print(Fore.YELLOW + "WhatsApp Message Sender Pro")
    print(Fore.BLUE + "1. Send to one person")
    print(Fore.BLUE + "2. Send to multiple people\n")
    
    # Get user choice
    while True:
        choice = input(Fore.MAGENTA + "Choose an option (1/2): " + Style.RESET_ALL)
        if choice in ['1', '2']:
            break
        print(Fore.RED + "Invalid choice. Please enter 1 or 2")

    if choice == '1':
        # Single recipient
        number = get_valid_number("Enter recipient's number (+212612345678): ")
        message = input(Fore.CYAN + "Enter your message: " + Style.RESET_ALL)
        recipients = [number]
        messages = [message]
    else:
        # Multiple recipients
        while True:
            try:
                count = int(input(Fore.CYAN + "\nHow many people do you want to send to? " + Style.RESET_ALL))
                if count > 0:
                    break
                print(Fore.RED + "Please enter a number greater than 0")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number")
        
        recipients = []
        for i in range(count):
            prompt = f"Enter number {i+1}/{count} (+212612345678): "
            recipients.append(get_valid_number(prompt))

        # Message type selection
        print(Fore.YELLOW + "\n" + "═"*40)
        while True:
            msg_choice = input(Fore.MAGENTA + "Choose message type:\n1. Same message for all\n2. Different message for each\nEnter (1/2): " + Style.RESET_ALL)
            if msg_choice in ['1', '2']:
                break
            print(Fore.RED + "Invalid choice. Please enter 1 or 2")

        # Collect messages based on choice
        if msg_choice == '1':
            message = input(Fore.CYAN + "\nEnter message to send to all: " + Style.RESET_ALL)
            messages = [message] * len(recipients)
        else:
            messages = []
            for idx, number in enumerate(recipients, 1):
                msg = input(Fore.CYAN + f"\nEnter message for recipient {Fore.YELLOW}{idx}/{len(recipients)} {Fore.CYAN}({number}): " + Style.RESET_ALL)
                messages.append(msg)

    # Send messages with progress tracking
    print(Fore.GREEN + "\n" + "═"*40 + " SENDING MESSAGES " + "═"*40)
    success_count = 0
    for idx, (number, message) in enumerate(zip(recipients, messages), 1):
        try:
            print(Fore.BLUE + f"\n📤 Sending to {number} ({idx}/{len(recipients)})..." + Style.RESET_ALL)
            pywhatkit.sendwhatmsg_instantly(
                phone_no=number,
                message=message,
                wait_time=15,
                tab_close=True
            )
            success_count += 1
            print(Fore.GREEN + "✅ Message sent successfully!")
            time.sleep(4)  # Delay between messages
        except Exception as e:
            print(Fore.RED + f"❌ Failed to send to {number}: {str(e)}")
    
    print(Fore.GREEN + "\n" + "═"*40 + " SUMMARY " + "═"*40)
    print(Fore.YELLOW + f"\nMessage sending completed! Success: {Fore.GREEN}{success_count}{Fore.YELLOW}/{Fore.CYAN}{len(recipients)}" + Style.RESET_ALL)
    print(Fore.GREEN + "\n" + "═"*40 + " Thank you for using WA Sender Pro! " + "═"*40 + "\n")

if __name__ == "__main__":
    send_messages()