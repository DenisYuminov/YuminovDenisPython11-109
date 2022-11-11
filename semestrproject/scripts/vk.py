# import vk
# id_app = '51472648'
# login = '891287505501'
# password = 'Ds12ds15ds89'
# session = vk.AuthSession(id_app, login, password)
# vk_api = vk.API(session)
#
import vk_api


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main(login, password):
    """ Пример обработки двухфакторной аутентификации """


    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    response = vk.account.getProfileInfo(token="5c88205e5c88205e5c88205ec85f99495655c885c88205e3fe4c8d86c76d763956e9c17")

    return f'{response["first_name"]} {response["last_name"]}'

if __name__ == '__main__':
    print(main('+79128705501', 'DS12DS15DS89'))
