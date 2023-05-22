from classes import Name, Phone, Record, AddressBook


USERS = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Key doesn't exist"
        except ValueError:
            return 'Check the number or name, please'
        except IndexError:
            return 'Element is not present'

    return inner


def hello_message() -> str:
    return "Hello! How can I help you?"


def help_command() -> str:
    return ("Please select one of the commands:\n"
            "add user: add\n"
            "change user: change\n"
            "show all contacts: showall\n"
            "show user's phone: phone 'name'\n"
            "delete contact: delete 'name'\n")


@input_error
def add_user(name, phone) -> str:
    name_field = Name(name)
    if not name_field.is_valid_name():
        return 'Please enter the correct contact name'

    return USERS.add_record(name, phone)


@input_error
def change_phone(name, phone) -> str:
    if name not in USERS.data:
        return "There is no such contact!"

    new_phone = ''.join(filter(str.isdigit, phone))

    if not new_phone:
        return "Please enter a valid phone number."

    USERS.data[name].phones = {Phone(new_phone)}

    return f"Phone number for contact '{name}' has been changed to '{new_phone}'."


@input_error
def show_all():
    return USERS.show_all_records()


@input_error
def show_phone(name) -> str:
    for n, record in USERS.data.items():
        if n.lower() == name.lower():
            phones = ", ".join([phone.value for phone in record.phones])
            return f"Phone number for the contact '{name}': {phones}"
    return f'Contact for {name} not found'


@input_error
def del_contact(name) -> str:
    if name not in USERS.data:
        return "There is no such contact!"

    del USERS.data[name]
    return f"Contact '{name}' has been deleted from the address book."


def unknown_command(command):
    return f"Unknown command {command}\n{help_command()}"


def exit_message():
    return None


HANDLERS = {
    'hello': hello_message,
    'add': add_user,
    'change': change_phone,
    'showall': show_all,
    'delete': del_contact,
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
            handler = unknown_command
            args = command

        if not args:
            result = handler()
        else:
            result = handler(*args)

        if not result:
            break

        print(result)

    print('Good bye!')


if __name__ == '__main__':
    main()


