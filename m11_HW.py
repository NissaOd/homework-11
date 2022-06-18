from collections import UserDict
from datetime import datetime, date
from itertools import count


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'

    def __eq__(self, other) -> bool:
        return self.value == other.value



class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value:
            if value.isdigit():
                self.__value = value
            else:
                raise ValueError('Phone not corect')
            
            
            

class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value:
            try:
                datetime.strptime(value, '%d.%m.%Y')
            except ValueError as e:
                raise ValueError('not correct data formate') from e
                
    

class Record:
    def __init__(self, name: Name, phones = None, birthday: Birthday=None) -> None:
        if phones is None:
            phones = []
        self.name = name
        self.phone_list = phones
        self.birthday = birthday

    def __str__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phone_list])}'  \
        f' Birthday: {self.birthday}'

    def add_phone(self, phone: Phone) -> None:
        self.phone_list.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phone_list.remove(phone)

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        self.phone_list.remove(phone)
        self.phone_list.append(new_phone)
    
    def days_to_birthday(self):
        if not self.birthday:
            return 'unknow birthday'
        start = date.today()
        birthday_date = datetime.strptime(str(self.birthday),  '%d.%m.%Y')
        end = date(year=start.year, mounth=birthday_date.month, day=birthday_date.day)
        count_day=(end-start).days
        if count_day < 0:
            count_day +=365
        return count_day


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record


class PhoneUserAlreadyExists(Exception):
    """You cannot add an existing phone number to a user"""


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, contacts, *args):
        try:
            return self.func(contacts, *args)
        except IndexError:
            return 'Error! Give me name and phone please!'
        except KeyError:
            return 'Error! User not found!'
        except ValueError:
            return 'Error! Phone number is incorrect!'
        except PhoneUserAlreadyExists:
            return 'Error! You cannot add an existing phone number to a user'


def salute(*args):
    return 'Hello! How can I help you?'


@InputError
def add_contact(contacts, *args):
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in contacts:
        if phone in contacts[name.value].phone_list:
            raise PhoneUserAlreadyExists
        else:
            contacts[name.value].add_phone(phone)
            return f'Add phone {phone} to user {name}'
    else:
        if len(args) > 2:
            birthday = Birthday(args[2])
        else:
            birthday = Birthday(None)
        contacts[name.value] = Record(name, [phone], birthday)
        return f'Add user {name} with phone number {phone}'


@InputError
def change_contact(contacts, *args):
    name, old_phone, new_phone = args[0], args[1], args[2]
    verify_phone(Phone(new_phone))
    contacts[name].edit_phone(Phone(old_phone), Phone(new_phone))
    return f'Change to user {name} phone number from {old_phone} to {new_phone}'


@InputError
def show_phone(contacts, *args):
    name = args[0]
    phone = contacts[name]
    return f'{phone}'


@InputError
def del_phone(contacts, *args):
    name, phone = args[0], args[1]
    contacts[name].del_phone(Phone(phone))
    return f'Delete phone {phone} from user {name}'


def show_all(contacts, *args):
    result = 'List of all users:'
    for key in contacts:
        result += f'\n{contacts[key]}'
    return result

def birthday(contacts, *args):
    if args:
        name= args[0]
        return f'{contacts[name].birthday}'
    


def goodbye(*args):
    return 'Good bye!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def verify_phone(phone: Phone):
    new_phone = phone.value.removeprefix('+').replace('(', '').replace(')', '').replace('-', '')
    return str(int(new_phone))


def help_me(*args):
    return """Command format:
    help or ? - this help;
    hello - greeting;
    add name phone - add user to directory;
    change name old_phone new_phone - change the user's phone number;
    del name phone - delete the user's phone number;
    phone name - show the user's phone number;
    show all - show data of all users;
    good bye or close or exit or . - exit the program"""


COMMANDS = {salute: ['hello'], add_contact: ['add '], change_contact: ['change '], show_phone: ['phone '],
            help_me: ['?', 'help'], show_all: ['show all'], goodbye: ['good bye', 'close', 'exit', '.'],
            del_phone: ['del '], birthday: ['birthday']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                # print(key, args)
                return key, args
    else:
        return unknown_command, []


def main():
    contacts = AddressBook()
    while True:
        user_command = input('Enter command >>> ')
        command, data = command_parser(user_command)
        print(command(contacts, *data), '\n')
        if command is goodbye:
            break


if __name__ == '__main__':
    main()
