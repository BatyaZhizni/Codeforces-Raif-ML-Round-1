# основа моего решения это анализ личных встреч команд, с некоторым эвристиками

# загрузка необходимых библиотек
import pandas as pd
import numpy as np

# загрузка файла с тренировочными данными
train = pd.read_csv('train.csv')
# проставим импровизированную метку времени, чтобы можно было сортировать матчи после выборки
train["Time"] = np.arange(1, 39993)
# оставим только необходимые столбцы: время, номера команд и результаты матча
train = train[['Time', 'home_team', 'away_team', 'full_time_home_goals', 'full_time_away_goals']]

# получим на вход количество матчей
N = int(input())

# цикл обработки матчей
for _ in range(N):
    # запишем в переменную предматчевую статистику
    data_potok = input().split()

    # вытащим номера команд из предматчевой статистики
    home_team = float(data_potok[2])
    away_team = float(data_potok[3])

    # отберем личные встречи команд, и когда играли дома у одной и когда дома у другой
    tab1 = train[(train['home_team'] == home_team) & (train['away_team'] == away_team)][['Time', 'home_team', 'away_team', 'full_time_home_goals', 'full_time_away_goals']]
    tab2 = train[(train['home_team'] == away_team) & (train['away_team'] == home_team)][['Time', 'away_team', 'home_team', 'full_time_away_goals', 'full_time_home_goals']]
    # переименуем столбцы, чтобы конкатенация отработала правильно
    tab1.columns = ['Time', 'home_team', 'away_team', 'full_time_home_goals', 'full_time_away_goals']
    tab2.columns = ['Time', 'home_team', 'away_team', 'full_time_home_goals', 'full_time_away_goals']
    # соединим матчи из двух таблиц и отсортируем по времени
    total = pd.concat((tab1, tab2), axis=0)
    total = total.sort_values('Time').reset_index(drop=True)
    # вычислим результаты матчей
    results = (total['full_time_home_goals'] - total['full_time_away_goals']).values

    # для дальнейшего анализа оставляем только последние 10 личных встреч
    results = results[-10:]
    # считаем победы, поражения и ничьи для команды, которая принимает у себя матч в анализируемом матче
    wins = results[results > 0].shape[0]
    loses = results[results < 0].shape[0]
    draws = results[results == 0].shape[0]

    # здесь мы вытаскиваем значение дивизиона, в котором проходит матч
    # и не делаем ставку в нескольких из них, так как модель на них работала плохо
    if float(data_potok[0]) in [0, 6, 9, 15, 16]:
        print('SKIP', flush=True)
    else:
        # если между командами было меньше 3 личных встреч, мы не делаем ставку
        if (wins + loses + draws) > 3:
            # дальше мы сравниваем количество побед/поражений/ничейных матчей с общим количество и из этого делаем вывод ставить или нет
            # коэффициенты подбирались на валидации
            # для поражений отдельно сравниваем их количество с количеством побед и ничейных матчей

            # честно говоря, я так и не понял, где в ходе решения путал местами домашнюю и гостевую команду
            # по итогу вышло контринтуитивно, если побед больше я предсказываю поражение и наоборот
            # но изменяя AWAY на HOME, а HOME на AWAY, метрика менялась с 450 на -60, поэтому оставил как есть, допуская, что где-то недопонял условия
            if wins > (wins + loses + draws) * 0.37:
                print('AWAY', flush=True)
            elif loses > wins and loses > draws:
                print('HOME', flush=True)
            elif draws > (wins + loses + draws) * 0.37:
                print('DRAW', flush=True)
            else:
                print('SKIP', flush=True)
        else:
            print('SKIP', flush=True)

    # получаем на вход результаты матча, но в модели я их не использовал
    scores = input()
