from configparser import ConfigParser
from pyrogram import Client
import json

chats_data = {
    "Chats": []
}


def load_chats_data():
    try:
        with open('chats_data.json', 'r') as json_file:
            data = json.load(json_file)
            chats = data.get("Chats", [])
            if not chats:
                return None
            return data
    except FileNotFoundError:
        return None


config = ConfigParser()
config.read('config.ini')

api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')

app = Client('my_account', api_id=api_id, api_hash=api_hash)


app.start()


def add_users():
    print("Введите имена пользователей (без символа '@')\nВведите'/exit', чтобы закончить ")
    usernames = list(iter(lambda: input("Имя пользователя: "), '/exit'))

    return usernames


def check_users_id(usernames):
    users_id = []
    for user in usernames:
        try:
            users_id.append(app.get_users(user).id)
            
        except Exception as e:
            print(f"Ошибка при вводе имени: {str(e)}")

    return users_id


def create_chat():
    users_id = check_users_id(add_users())

    chat = app.create_group(
        title='Test group',
        users=users_id,
    )

    chat_id = chat.id

    chats_data["Chats"].append({
        "chat_id": chat_id,
        "users": users_id
    })

    print(f"Чат создан. ID чата: {chat_id}")

    with open('chats_data.json', 'w') as json_file:
        json.dump(chats_data, json_file, indent=4)


def add_to_chat(chat_id, chat_data):
    users_id = check_users_id(add_users())

    try:
        app.add_chat_members(chat_id, users_id)
        chat_data["user_ids"].extend(users_id)
    except Exception as e:
        print(f'При добавлении пользователя произошла ошибка{e}')


def is_chat_id_in_data(chat_id, data):
    if data:
        chat_ids = [chat.get("chat_id") for chat in data.get("Chats", [])]
        return chat_id in chat_ids
    return False


def main():
    while True:
        data = load_chats_data()
        choice = input('Нажмите 1 чтобы создать новый чат, '
                       '2 чтобы добавить пользователей в чат, '
                       'или 3 для завершения: ')

        if choice == '1':
            create_chat()
        elif choice == '2':
            if data:
                print("Существующие чаты:")
                for chat in data.get("Chats", []):
                    print(f"ID чата: {chat.get('chat_id')}")

                chat_id = input('\nВведите ID чата в который хотитте добавить пользователя:')

                if is_chat_id_in_data(int(chat_id), data):
                    add_to_chat(chat_id, data)
                else:
                    print("Данного ID нет в списке\n")
            else:
                print("Нет существующих чатов.")
        elif choice.lower() == '3':
            break


main()

app.stop()
