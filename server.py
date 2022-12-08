import socket
from selenium import webdriver
from selenium.webdriver import Keys
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.0.100', 9515)) # Привязываем серверный сокет к ip устройства, на котором сервер, и 3030 порту.
s.listen(10) # Начинаем прослушивать входящие соединения.
website="http://192.168.0.215/" #http://redmine.testbase.ru/login" ip-camera
driver = webdriver.Chrome(executable_path="chromedriver.exe")
#объявления браузера и дравера для него(драйвер должен быть той же версии, что и браузер), в кавычках прописываетя относительный путь 
try:
    driver.get(url=website)
    time.sleep(2)
    driver.find_element_by_id("username").send_keys("spectator")
    time.sleep(0.5)
    driver.find_element_by_id("password").send_keys("0")
    time.sleep(0.5)
    driver.find_element_by_id("b_login").click()
    time.sleep(3)
    number=0 #номер пресета камеры
    adata=0 #пока 0 - меняем пресеты, пока 1 - ждём 
    while True:
        conn, addr = s.accept() # Метод который принимает входящее соединение.
        if "192.168.0.42" in addr: 
            print('Connected by', addr)      
            data = conn.recv(1024) # Получаем данные из сокета.
            adata=int(data.decode('utf-8'))
            print(data.decode('utf-8'), adata)
            print("data recFin")
            #if not data:
                #break
            conn.sendall(data) # Отправляем данные в сокет.
            conn.close()
        if adata==0:
            driver.find_element_by_id("i_xhz").clear()
            time.sleep(0.5)
            driver.find_element_by_id("i_xhz").send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            if number<18:
                number+=1
            else:
                number=1
            driver.find_element_by_id("i_xhz").send_keys(number)
            #driver.find_element_by_name("i_xhz").send_keys(data.decode('utf-8'))
            time.sleep(0.5)
            driver.find_element_by_id("b_xhz1").click()
            time.sleep(5)
except Exception as ex:
    print(ex)

# https://chromedriver.chromium.org/downloads  тут скачать драйвер
