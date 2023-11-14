import random
import ssl
import time
from threading import Thread

import capmonster_python
import requests
import cloudscraper
from capmonster_python import RecaptchaV2Task, RecaptchaV3Task

from bs4 import BeautifulSoup
from eth_account.messages import encode_defunct
from tqdm import tqdm
from web3.auto import w3
import imaplib
import email
from email.header import decode_header
import re

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def ApproveMail(login, password):

    count = 0
    while count < 5:

        # Введите свои данные учетной записи
        email_user = login
        email_pass = password

        if '@rambler' in login or '@lenta' in login or '@autorambler' in login:
            # Подключение к серверу IMAP
            mail = imaplib.IMAP4_SSL("imap.rambler.ru")

        else:
            mail = imaplib.IMAP4_SSL("imap.mail.ru")

        mail.login(email_user, email_pass)

        # Выбор почтового ящика
        mail.select("inbox")

        # Поиск писем с определенной темой
        typ, msgnums = mail.search(None, 'SUBJECT "Please verify your email address"')
        msgnums = msgnums[0].split()

        # Обработка писем
        link = ''

        for num in msgnums:
            typ, data = mail.fetch(num, "(BODY[TEXT])")
            msg = email.message_from_bytes(data[0][1])
            text = msg.get_payload(decode=True).decode()

            # print(text.replace('=\r\n', '').split('<a href=3D"'))

            # Поиск ссылки в тексте письма
            link_pattern = r'https://launchpad.collectify.app/main/api/raffle/email\S*'
            match = re.search(link_pattern, text.replace('=\r\n', '').replace('"', ' '))

            if match:
                link = match.group()
                # print(f"Найдена ссылка: {link}")
            else:
                # print("Ссылка не найдена")
                count +=1
                time.sleep(2)

        # Завершение сессии и выход
        mail.close()
        mail.logout()

        return link

    return None


def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{2}_{3}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{1}.{2}) Gecko/20100101 Firefox/{1}.{2}',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(70, 108)
    firefox_version = random.randint(70, 108)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(1000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent

class Twitter:

    def __init__(self, auth_token, csrf, proxy):

        self.session = self._make_scraper()
        self.session.proxies = proxy
        self.session.user_agent = random_user_agent()

        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

        self.csrf = csrf
        self.auth_token = auth_token
        self.cookie = f'auth_token={self.auth_token}; ct0={self.csrf}'

        liketweet_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {authorization_token}',
            'x-csrf-token': self.csrf,
            'cookie': self.cookie
        }

        self.session.headers.update(liketweet_headers)

        # print('Аккаунт готов')


    # Основные функции твиттер аккаунта

    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )


    def Like(self, id):

        # print('asdsd')

        payload = {
            "variables": {
                "tweet_id": str(id)
            },
            "queryId": "lI07N6Otwv1PhnEgXILM7A"
        }

        with self.session.post("https://api.twitter.com/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet",  json=payload, timeout=5) as response:
            if response.ok:
                # print(response.text)
                pass

    def Retweet(self, id):
        payload = {
            "variables": {
                "tweet_id": str(id)
            },
            "queryId": "ojPdsZsimiJrUGLR1sjUtA"
        }

        with self.session.post("https://api.twitter.com/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet", json=payload, timeout=30) as response:
            if response.ok:
                # print(response.text)
                pass

    def Follow(self, user_id):
        # Не работает
        self.session.headers.update({'Content-Type': 'application/json'})

        with self.session.post(f"https://api.twitter.com/1.1/friendships/create.json?user_id={user_id}&follow=True", timeout=30) as response:
            # print(response.text)

            if 'suspended' in response.text:
                # print(f'Аккаунт {self.name} забанен')
                return 'ban'
            else:
                return 1


class Account:

    def __init__(self, proxy, address, private, auth_token, csrf, pbar):

        proxy = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"

        self.cap_key = cap_key
        self.address = address.lower()
        self.private_key = private
        self.tw_auth_token = auth_token
        self.tw_csrf = csrf
        self.proxy = {'http': proxy, 'https': proxy}
        self.pbar = pbar


    def execute_task(self):

        self.ref = 'SW35MC9LQX'

        # try:
        self.session = self._make_scraper()
        self.session.proxies = self.proxy
        self.session.user_agent = random_user_agent()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.pbar.set_postfix({'Этап': 'Подключение кошелька'})
        self.token = self.Connect()
        if self.token == 'Неправильные данные от кошелька':
            return self.token

        self.pbar.set_postfix({'Этап': 'Подключение Твиттера'})
        try:
            # print(self.proxy)
            self.Twitter()
        except Exception as e:
            return 'Error'



        time.sleep(random.randint(10, 150) / 100)
        self.pbar.set_postfix({'Этап': 'Выполнение активностей'})
        status = self.Twitter_actions()
        if status != None:
            return status

        self.pbar.set_postfix({'Этап': 'Подключение почты'})
        with self.session.get('https://launchpad.collectify.app/main/api/raffle/emailBindByThird?channel=twitter_email', timeout=10) as response:

            if response.json()['success'] == True:
                self.pbar.update(1)
                pass
            else:

                mail_data = ''
                with open('Files/Mails.txt', 'r') as file:
                    lines = file.readlines()
                mail_data = lines[0].strip('\n')
                with open('Files/Mails.txt', 'w') as file:
                    file.writelines(lines[1:])

                payload = {"email":mail_data.split(':')[0]}
                with self.session.post('https://launchpad.collectify.app/main/api/raffle/emailBind', timeout=10) as response:
                    time.sleep(3)
                    self.pbar.update(1)
                    if response.json()['success'] != True:
                        link = ApproveMail(mail_data.split(':')[0], mail_data.split(':')[1])

                        if link == None:
                            return 'Ошибка с почтой'
                    else:
                        pass

        self.pbar.set_postfix({'Этап': 'Решение капчи'})
        capmonster = RecaptchaV2Task(self.cap_key)

        capmonster.set_proxy('http',f"{self.proxy['http'].split('/')[-1].split('@')[-1].split(':')[0]}",f"{self.proxy['http'].split('/')[-1].split('@')[-1].split(':')[1]}",f"{self.proxy['http'].split('/')[-1].split('@')[0].split(':')[0]}",f"{self.proxy['http'].split('/')[-1].split('@')[0].split(':')[1]}")
        capmonster.set_user_agent(self.session.user_agent)

        task_id = capmonster.create_task("https://launchpad.collectify.app/", "6LcQ9XAgAAAAABgn_cylXvCB6rYbfmR3w9gWaRm2")
        result = capmonster.join_task_result(task_id)
        resp = result.get("gRecaptchaResponse")
        self.pbar.update(1)
        # print(resp)

        self.pbar.set_postfix({'Этап': 'Регистрация на раффл'})
        self.session.headers.update({'authorization': f'Bearer {self.token}'})
        with self.session.get(f'https://launchpad.collectify.app/main/api/raffle/8XJ96UH56/join?invite_code={self.ref}&recaptcha_code={resp}', timeout=10) as response:
            # print(response.text)
            self.pbar.update(1)

        self.pbar.update(1)

        return 'Готово'



    def Twitter(self):

        self.session.headers.clear()

        self.session.headers.update({'authorization': f'Bearer {self.token}'})

        with self.session.get(f'https://launchpad.collectify.app/main/api/twitter/login?return_url=https%3A%2F%2Flaunchpad.collectify.app%2F%23%2Fparticipate%3Fid%3D8XJ96UH56%26inviteCode%3D{self.ref}', timeout=3, allow_redirects=False) as response:
            self.pbar.update(1)
            # print(response.text)
            link = response.json()['data']['auth_url']
            oauth_token = link.split('=')[-1]

            self.session.cookies.update({'auth_token': self.tw_auth_token, 'ct0': self.tw_csrf})

            with self.session.get(link, timeout=10) as response:
                self.pbar.update(1)
                soup = BeautifulSoup(response.text, 'html.parser')
                authenticity_token = soup.find('input', attrs={'name': 'authenticity_token'}).get('value')

                self.session.headers.update({'content-type': 'application/x-www-form-urlencoded'})

                payload = {'authenticity_token': authenticity_token,
                           'redirect_after_login': link,
                           'oauth_token': oauth_token}

                with self.session.post('https://api.twitter.com/oauth/authorize', data=payload, timeout=10, allow_redirects=False) as response:
                    self.pbar.update(1)

                    soup = BeautifulSoup(response.text, 'html.parser')
                    link = soup.find('a', class_='maintain-context').get('href')

                    # print(link)

                    with self.session.get(link, timeout=10) as response:
                        pass


    def Twitter_actions(self):

        status = Twitter(self.tw_auth_token, self.tw_csrf, self.proxy).Follow(1069827177527431168)
        self.pbar.update(1)

        if status == 'ban':
            return 'Твиттер забанен'

        time.sleep(random.randint(10,150)/100)
        Twitter(self.tw_auth_token, self.tw_csrf, self.proxy).Follow(1232603898268925954)
        self.pbar.update(1)
        time.sleep(random.randint(10, 150) / 100)
        Twitter(self.tw_auth_token, self.tw_csrf, self.proxy).Follow(1587705927859589121)
        self.pbar.update(1)
        time.sleep(random.randint(10, 150) / 100)
        Twitter(self.tw_auth_token, self.tw_csrf, self.proxy).Like(1640987157786669057)
        self.pbar.update(1)
        time.sleep(random.randint(10, 150) / 100)
        Twitter(self.tw_auth_token, self.tw_csrf, self.proxy).Retweet(1640987157786669057)
        self.pbar.update(1)
        time.sleep(random.randint(150, 250) / 100)

        return None


    def Connect(self):

        with self.session.get('https://launchpad.collectify.app/#/participate?id=8XJ96UH56', timeout=10) as resp:
            pass

        self.session.headers.update({'authority': 'launchpad.collectify.app',
                                     'origin': 'https://launchpad.collectify.app',
                                     'referer': 'https://launchpad.collectify.app/',
                                     'accept': 'application/json, text/plain, */*',
                                     'chainid': '52',
                                     'content-type': 'application/json',
                                     'sec-fetch-dest': 'empty',
                                     'user-agent': self.session.user_agent})

        with self.session.get(f'https://launchpad.collectify.app/main/api/sessions/randomStr/{self.address}', timeout=15) as response:
            # print(response.text)
            data = response.json()['data']

            nonce = self.nonce(data)
            # print(nonce)
            message = encode_defunct(text=nonce)
            signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
            signature = signed_message["signature"].hex()
            # print(signature)

            payload = {"address": self.address,
                       "message": nonce,
                       "signature": signature}

            self.session.headers.update({'content-length': '261'})

            # print(payload)
            self.pbar.update(1)
            with self.session.post('https://launchpad.collectify.app/main/api/market_user/login', json=payload, timeout=10, allow_redirects=True) as response:
                # print(response.text)
                # print(self.address, self.private_key)
                # print(response.headers)
                try:
                    token = response.json()['data']['access_token']
                    self.pbar.update(1)
                    return token
                except:
                    return 'Неправильные данные от кошелька'



    def nonce(self, code) -> str:
        return f'Verify account ownership, nonce: {code}'

    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )




def thread(array, o):

    for i in array:
        pbar = tqdm(total=14, desc=i['address'], bar_format="{l_bar}{bar}| {postfix}")
        try:
            status=Account(proxy=i['proxy'],
                    address=i['address'],
                    private=i['private'],
                    auth_token=i['auth_token'],
                    csrf=i['csrf'],
                    pbar=pbar).execute_task()
            pbar.set_postfix({'Этап': status})
        except Exception as e:
            # print(e)

            pbar.set_postfix({'Этап': 'Ошибка'})
            # print('')

def split_list(lst, n):
    avg = len(lst) / float(n)
    result = []
    last = 0.0

    while last < len(lst):
        result.append(lst[int(last):int(last + avg)])
        last += avg

    return result

if __name__ == '__main__':

    Privates = []
    Addresses = []
    TW_data = []
    Proxys = []
    cap_key = ''
    with open('Files/CapKey.txt', 'r') as file:
        for i in file:
            cap_key = i.strip('\n')
            break
    with open('Files/Twitter_Cookies.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            ready = f"auth_token={data.split('auth_token=')[1].split(';')[0]}; ct0={data.split('ct0=')[1].split(';')[0]}"
            TW_data.append(ready)
    with open('Files/Addresses.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Addresses.append(data)
    with open('Files/Proxys.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Proxys.append(data)
    with open('Files/Privates.txt', 'r') as file:
        for i in file:
            data = i.strip('\n')
            Privates.append(data)

    if len(Addresses) != len(Proxys) != len(TW_data) != len(Privates):
        print('Количество ресурсов в текстовиках разнятся, сделайте так, чтобы ресурсов было одинаковое кол-во')
        input()
        exit(1)
    if len(cap_key) < 5:
        print('Вы не указали ключ от Capmonster')
        input()
        exit(1)

    while True:
        try:
            threads_number = int(input('Укажите количество потоков: '))
            if threads_number < 1:
                print('Укажите значение целым числом больше 0\n')
                continue
            break
        except:
            print('Укажите значение целым числом больше 0\n')

    FullArray = []
    for i in range(len(Addresses)):
        FullArray.append({'proxy': Proxys[i],
                          'address': Addresses[i],
                          'private': Privates[i],
                          'auth_token': TW_data[i].split('auth_token=')[1].split(';')[0],
                          'csrf': TW_data[i].split('ct0=')[1].split(';')[0]})

    SplitedArray = split_list(FullArray, threads_number)

    print('Абуз начался\n')

    threads = []
    for i in range(threads_number):
        thread_ = Thread(target=thread, args=(SplitedArray[i], 1))
        thread_.start()
        threads.append(thread_)

    for i in threads:
        i.join()

    print('Абуз окончен                                                                                                                                ')
    input()


