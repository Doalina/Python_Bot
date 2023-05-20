from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def is_valid_name(self):
        return True if self.value.isalpha() else False


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def is_valid_phone(self):
        is_valid = True if self.value.isnumeric() else False
        return is_valid


class Record:
    def __init__(self, name: Name, phone: Phone):
        self.name = name
        self.phones = set()
        self.birthday = None
        self.phones.add(phone)

    def add_phone(self, phone) -> str:
        message = "Phone was added."
        self.phones.add(phone)
        return message

    def change_phone(self, name, phone) -> str:
        if name not in self.data:
            return "There is no such contact!"
        else:
            record = self.data[name]
            record.phones = {Phone(phone)}
            return f'Phone number for {name} has been changed!'

    def delete_phone(self, phone: Phone) -> str:
        message = 'Phone was not removed because it was not found.'
        for i in self.phones:
            if i.value == phone.value:
                self.phones.remove(i)
                message = "Phone deleted."
                break
        return message


class AddressBook(UserDict):
    def add_record(self, name, phone) -> str:
        name_field = Name(name)
        phone_field = Phone(phone)
        if not name_field.is_valid_name() or not phone_field.is_valid_phone():
            return 'Please enter the correct number or contact name'

        for record in self.data.values():
            if name_field.value == record.name.value:
                return 'A contact with the same name already exists'
            if phone_field.value in [p.value for p in record.phones]:
                return 'A contact with the same phone number already exists'

        record = Record(name_field, phone_field)
        self.data[name_field.value] = record
        message = 'Record added to the address book!'
        return message

    def del_record(self, name) -> str:
        if name in self.data:
            self.data.pop(name)
            message = 'Record deleted from the address book.'
        else:
            message = 'Record not found in the address book.'
        return message

    def show_all_records(self) -> str:
        if not self.data:
            return 'There are no saved contacts yet'
        message = f'\nRecords in the address book:\n'
        for name, record in self.data.items():
            phones = ", ".join([phone.value for phone in record.phones])
            message += f'{name}: {phones}\n'
        return message