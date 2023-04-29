import re

USERS = {}


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Key doesn't exist"
        except ValueError:
            return 'Check the number or name please'
        except IndexError:
            return 'Element is not present'

    return inner


def hello_message():
    return "Hello! How can I help you?"


PHONE_PATTERN = re.compile(r'^\+?\d{10,12}$')


@input_error
def add_user(name, phone):
    if not name.isalpha() or not PHONE_PATTERN.match(phone):
        return 'Please enter the correct number or contact name'

    if name in USERS:
        return f'User {name} already exists'
    elif phone in USERS.values():
        return f'Phone number {phone} already exists'
    else:
        USERS[name] = phone
        return f'User {name} added!'


@input_error
def change_phone(name, phone):
    if name not in USERS:
        return "There is no such contact!"
    if not PHONE_PATTERN.match(phone):
        return "Check if the number is correct!"
    else:
        USERS[name] = phone
        return f'User {name} changed!'


@input_error
def show_all():
    if not USERS:
        return 'There are no saved contacts yet'
    message = ''
    for name, phone in USERS.items():
        message += f'Name: {name} phone: {phone}\n'
    return message


@input_error
def show_phone(name):
    for n, p in USERS.items():
        if n.lower() == name.lower():
            return f"{name}'s phone number is {p}"

    return f'No contact found for {name}'


def unknown_command(*_):
    return """Please select one of the commands:
            add user: add
            change user: change
            show all contacts: show all
            show user's phone: phone 'name''"""


def help_command(*_):
    return """Please select one of the commands:    
            add user: add
            change user: change
            show all contacts: show all
            show user's phone: phone 'name'"""


def exit_message():
    return None


HANDLERS = {
    'hello': hello_message,
    'add': add_user,
    'change': change_phone,
    'show all': show_all,
    'phone': show_phone,
    'help': help_command,
    'exit': exit_message,
    'goodbye': exit_message,
    'close': exit_message,
}


def main():
    while True:
        user_input = input('Please enter Command: ')
        command, *args = user_input.split()
        command = command.lstrip()

        try:
            handler = HANDLERS[command.lower()]
        except KeyError:
            if args:
                command = command + ' ' + args[0]
                args = args[1:]
            handler = HANDLERS.get(command.lower(), unknown_command)

        result = handler(*args)

        if not result:
            break
        print(result)

    print('Good bye!')


if __name__ == "__main__":
    main()


