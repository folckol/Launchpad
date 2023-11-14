# import threading
# import time
# from tqdm import tqdm
#
# # функция для запуска прогресс бара
# def run_progress_bar(desc):
#
#     for ii in ['Sub Bar: 1','Sub Bar: 2','Sub Bar: 3','Sub Bar: 4']:
#
#         for i in tqdm(range(50), desc=desc+f' {ii}', position=descriptions.index(desc)):
#             time.sleep(0.1)
#
# # создаем список с описанием каждого прогресс бара
# descriptions = ['Progress bar 1', 'Progress bar 2', 'Progress bar 3']
#
# # запускаем каждый прогресс бар в отдельном потоке
# for desc in descriptions:
#     t = threading.Thread(target=run_progress_bar, args=(desc,))
#     t.start()
#     time.sleep(1)
#
# input()


# from tqdm import tqdm
# import time
#
# with tqdm(total=100, desc="ProgressProgressProgressProgressProgress", bar_format="{l_bar}{bar}| {postfix}") as pbar:
#     for i in range(100):
#         # какая-то работа
#         time.sleep(0.1)
#         pbar.update(1)  # обновление прогресс бара на каждой итерации
#         pbar.set_postfix({'Этап': 'Решение Капчи'})

Privates = []
Addresses = []
TW_data = []
Proxys = []
cap_key = ''
with open('Files/Addresses.txt', 'r') as file:
    for i in file:
        data = i.strip('\n')
        Addresses.append(data)
with open('Files/CapKey.txt', 'r') as file:
    for i in file:
        cap_key = i.strip('\n')
        break
with open('Files/Twitter_Cookies.txt', 'r') as file:
    for i in file:
        data = i.strip('\n')
        ready = f"auth_token={data.split('auth_token=')[1].split(';')[0]}; ct0={data.split('ct0=')[1].split(';')[0]}"
        TW_data.append(ready)
with open('Files/Proxys.txt', 'r') as file:
    for i in file:
        data = i.strip('\n')
        Proxys.append(data)
with open('Files/Privates.txt', 'r') as file:
    for i in file:
        data = i.strip('\n')
        Privates.append(data)


wallets = []
with open('s', 'r') as file:
    for i in file:
        wallets.append(i.strip('\n'))

# print(wallets)
# input()


newPrivates = []
newProxys = []
newTW_data = []
newAddresses = []
for i in range(len(Addresses)):
    if Addresses[i] not in wallets:
        pass
    else:
        newAddresses.append(Addresses[i]+'\n')
        newPrivates.append(Privates[i]+'\n')
        newProxys.append(Proxys[i]+'\n')
        newTW_data.append(TW_data[i]+'\n')

with open('Files/Addresses.txt', 'w') as file:
    file.writelines(newAddresses)
with open('Files/Proxys.txt', 'w') as file:
    file.writelines(newProxys)
with open('Files/Privates.txt', 'w') as file:
    file.writelines(newPrivates)
with open('Files/Twitter_Cookies.txt', 'w') as file:
    file.writelines(newTW_data)


