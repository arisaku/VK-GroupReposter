import vk_api
from termcolor import colored
import time

def is_valid_token(token):
    try:
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        user_info = vk.users.get()
        return bool(user_info)
    except vk_api.exceptions.ApiError:
        return False

def log_repost(result, token, repost_id, user_info):
    if result:
        success_status = "успешно"
        color = 'green'
    else:
        success_status = "неудачно"
        color = 'red'
    message = (
        f"Репост в сообщество {repost_id}\n"
        f"С аккаунта {user_info['first_name']} {user_info['last_name']} (id{user_info['id']})\n"
        f"Токен: {token}\n"
        f"Выполнен: {success_status}\n"
    )
    print(colored(message, color))

with open('token.txt', 'r') as file:
    tokens = file.read().splitlines()

with open('repost_ids.txt', 'r') as file:
    repostids = file.read().splitlines()

with open('ownergroup.txt', 'r') as file:
    ownergroup = file.read()

post_id_to_repost = input('Введите id поста: ')

for token in tokens:
    token = token.strip()
    if is_valid_token(token):
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        try:
            response = vk.wall.get(owner_id=ownergroup, count=1)
            user_info = vk.users.get()
            for repost_id in repostids:
                try:
                    reposted_post = vk.wall.repost(object=f'wall{ownergroup}_{post_id_to_repost}', group_id=repost_id)
                    log_repost(True, token, repost_id, user_info[0])
                except vk_api.exceptions.ApiError as e:
                    log_repost(False, token, repost_id, user_info[0])
                time.sleep(15)
        except vk_api.exceptions.ApiError as e:
            print(colored(f'Ошибка при получении последнего поста с использованием токена {token}: {e}', 'red'))
    else:
        print(colored(f'Токен недействителен и не будет использоваться: {token}', 'red'))
