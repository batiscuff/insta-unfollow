from InstagramAPI import InstagramAPI


class InstagramUnfollowers:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.api = InstagramAPI(username, password)
        self.api.login()
        self.user_id = self.api.username_id  # свой user_id

        self.followers = self.get_total_followers(self.api, self.user_id)
        self.followings = self.get_total_followings(self.api, self.user_id)
        non_follow = self.non_followers(self.followers, self.followings)
        # число не подписаных взаимно
        self.total_non_followed = len(non_follow)

        print(self.results())

        if self.total_non_followed == 0:
            print("Вы отписались от всех")
            exit()
        else:
            for i in range(self.total_non_followed):
                if i >= self.total_non_followed:
                    break
                # Удаляет последнего юзера по никнейму
                user = list(self.non_follow.keys())[len(self.non_follow) - 1]
                # Отписывается и удаляет юзера pop() методом
                self.api.unfollow(non_follow[user])
                non_follow.pop(user)

    def results(self):
        results = [
                f"Колличество подписчиков: {len(self.followers)}",
                f"Колличество подписок: {len(self.followings)}",
                f"Колличество неподписаных: {self.total_non_followed}"
        ]
        return "\n".join(results)

    def get_total_followers(self, api, user_id) -> list:
        # Список кто подписан
        followers = list()
        next_max_id = True

        while next_max_id:
            if next_max_id is True:
                next_max_id = ""
            # Получаем список подписчиков. Сохраняется в новом запросе
            _ = self.api.getUserFollowers(self.user_id, maxid=next_max_id)
            """
        1) followers.extend() - Разширяет список добавляя в конец все елементы
        2) LastJson - загружает текст полученой страницы в питоновский словарь
        3) Метод get() возвращает значение по указанному ключу
        Если его нет, вернется пустой список
            *функция loads() - превращает данные JSON в объекты Python
            """
            followers.extend(self.api.LastJson.get("users", []))
            next_max_id = self.api.LastJson.get("next_max_id", "")
        # Возвращает список подписчиков
        return followers

    def get_total_followings(self, api, user_id) -> list:
        # Список на кого подписан(а)
        # Те самые операции что и с подписчиками
        followings = list()
        next_max_id = True

        while next_max_id:
            if next_max_id is True:
                next_max_id = ""

            _ = self.api.getUserFollowings(self.user_id, maxid=next_max_id)
            followings.extend(self.api.LastJson.get("users", []))
            next_max_id = self.api.LastJson.get("next_max_id", "")

        return followings

    def non_followers(self, followers: list, followings: list) -> dict:
        non_followers = dict()
        dict_followers = dict()

        for follower in followers:
            # username: pk (user id в базе данных инстаграмма)
            # 'glebglebovskii': 8118073631
            dict_followers[follower["username"]] = follower["pk"]

        for followed_user in followings:
            # Если юзер(из тех на кого подписан) не подписан на тебя
            # Добавляется в словарь non_followers
            if followed_user["username"] not in dict_followers:
                non_followers[followed_user["username"]] = followed_user["pk"]

        return non_followers


if __name__ == "__main__":
    print("------- Введите ваши данные --------")
    USERNAME = input("Введите ваш логин: ")
    PASSWORD = input("Введите ваш пароль: ")
    print(InstagramUnfollowers(USERNAME, PASSWORD))
