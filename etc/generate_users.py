import random
import string

from addrbook.models import Teams
from administration.models import MMBPFUsers

wanna_users_cnt = 1500
generate_new_team = 0.3
team_names = [
    "Шмакодавы",
    "Кулебары",
    "Лешаимы",
    "Марсубаки",
    "Кватонабры",
    "Трыблеры",
    "Краблеры",
]
names = {
    1: {  # male
        "lnames": [
            "Куропаткин",
            "Хмырь",
            "Шниперсон",
            "Сакермахрепяков",
            "Трындотов",
            "Масабаков",
            "Курочкин",
            "Кривозадов",
            "Машковац",
            "Кац",
            "Шнакропос-Пердыщенский",
            "Сковорода",
        ],
        "fnames": [
            "Барбос",
            "Кот",
            "Арнольд",
            "Мышан",
            "Абдул",
            "Абдурахман",
            "Махмуд",
            "Шкипер",
            "Блямс",
            "Дрын",
            "Кощей",
            "Тышыпык",
            "Иван",
        ],
        "pnames": [
            "Иструпович",
            "Антилопович",
            "Козлятович",
            "Сахарович",
            "Израилевич",
            "Власипоиевич",
            "Ахмед-критопопович",
            "Шпакович",
            "Астрахопович",
            "Малятоватич",
            "Шриланкович",
            "Вашингтонович",
            "Амирханович",
        ],
    },
    2: {  # femail
        "lnames": [
            "Козлятова",
            "Сакермахрепякова",
            "Лыткарина",
            "Марябакова",
            "Алавердыева",
            "Имярекова",
            "Барбос-куропаткина",
            "Аннигиляторова",
            "Селёдкина",
            "Сковорода",
        ],
        "fnames": [
            "Машина",
            "Баранина",
            "Кошка",
            "Василиса",
            "Машка-облигация",
            "Ильбумбира",
            "Масяня",
            "Куляпа",
            "Малапуса",
            "Мурка",
            "Кулёма",
            "Клямка",
        ],
        "pnames": [
            "Кривозадовна",
            "Переславль-залесская",
            "Чертыховская",
            "Антрактовна",
            "Бруевична",
            "Ильинична",
            "Кузьминична",
            "Машинична",
            "Бруснична",
            "Куль-кирпична",
            "Бизнесововична",
            "Ашмантовна",
        ],
    },
}

tourist_club = [
    "Газмяс",
    "Безногие",
    "Безмячные",
    "Слепаки",
    "Одноногие",
    "Хоккеисты",
    "Сборная по шкурмаболу",
    "Спартак",
]


def get_rnd_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


team_obj = None
need_to_gen_team = True
for idx in range(0, wanna_users_cnt):
    if not need_to_gen_team and random.random() < generate_new_team:
        need_to_gen_team = True

    if need_to_gen_team:
        team_obj = Teams.objects.create(
            team_id=idx,
            name=f"{random.choice(team_names)}_{get_rnd_string(length=5)}",
        )
        need_to_gen_team = False

    gender = random.randrange(1, 3)
    MMBPFUsers.objects.create(
        username=get_rnd_string(length=15),
        first_name=random.choice(names[gender]["fnames"]),
        last_name=random.choice(names[gender]["lnames"]),
        patronymic=random.choice(names[gender]["pnames"]),
        gender=gender,
        tourist_club=random.choice(tourist_club),
        team=team_obj,
    )


print(f"Users in DB: {MMBPFUsers.objects.all().count()}")
