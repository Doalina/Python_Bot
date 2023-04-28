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


def hello_message(*_):
    return "Hello! How can I help you?"


PHONE_PATTERN = re.compile(r'^\+?\d{10,12}$')


@input_error
def add_user(args):
    if not args[0].isalpha() or not PHONE_PATTERN.match(args[1]):
        return 'Please enter the correct number or contact name'

    name, phone = args[0], args[1]

    if name in USERS:
        return f'User {name} already exists'
    elif phone in USERS.values():
        return f'Phone number {phone} already exists'
    else:
        USERS[name] = phone
        return f'User {name} added!'


@input_error
def change_phone(name, number):
    if name not in USERS:
        return "There is no such contact!"
    name, phone = name, number
    if not PHONE_PATTERN.match(phone):
        return "Check if the number is correct!"
    else:
        USERS[name] = phone
        return f'User {name} changed!'


@input_error
def show_all(*_):
    if not USERS:
        return 'There are no saved contacts yet'
    message = ''
    for name, phone in USERS.items():
        message += f'Name: {name} phone: {phone}\n'
    return message


@input_error
def show_phone(args):
    if args and len(args) == 1:
        query = args[0]
        for name, phone in USERS.items():
            if name.lower() == query.lower() or phone == query:
                return f'{name}: {phone}'
        return f'No contact found for {query}'
    else:
        return 'Please enter a valid contact query'


def unknown_command(*_):
    return """Please select one of the commands:
            add user: add
            change user: change
            show all contacts: show all
            show user's phone: phone 'name'
            show user name: phone 'phone'"""


def help_command(*_):
    return """Please select one of the commands:    
            add user: add
            change user: change
            show all contacts: show all
            show user's phone: phone 'name'
            show user name: phone 'phone'"""


def exit_message(*_):
    # print('Good bye!')
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

        if handler == change_phone:
            result = handler(*args)
        else:
            result = handler(args)

        if not result:
            break
        print(result)

    print('Good bye!')


if __name__ == "__main__":
    main()


