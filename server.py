import socket
from selenium import webdriver
from selenium.webdriver import Keys
import time

addr_server = '192.168.0.44' #ip устройства, на котором сервер
port = 9515 #порт на устройстве (от 1024 до 49151)
website="http://192.168.0.215/" #адресс веб-интерфейса IP камеры
addr_reciever = "192.168.0.42" #ip адресс приёмника
driver = webdriver.Chrome(executable_path="chromedriver.exe")
#объявления браузера и дравера для него(драйвер должен быть той же версии, что и браузер), в кавычках прописываетя относительный путь
preset = 5 #количеств пресетов камеры
def log_web(): #авторизация в веб-интерфейсе камеры
    driver.find_element_by_id("username").send_keys("spectator")
    #by_id поиск по id элемента, send_keys вставляет текс в поле элемента (используется для textbox)
    #by_name()  поиск по имени элемента 
    #by_xpath("//*[contains(text(), Text)]") ищет элемент по тексту, например, <div .....>Text</div>
    time.sleep(0.5)
    driver.find_element_by_id("password").send_keys("0")
    time.sleep(0.5)
    driver.find_element_by_id("b_login").click()
    #click нажимает на найденный элемент
    pass
def control_cam(number): #переключение пресетов камеры в веб-интерфейсе
    driver.find_element_by_id("i_xhz").clear()
    #clear очищает текстовое поле
    time.sleep(0.5)
    driver.find_element_by_id("i_xhz").send_keys(Keys.BACKSPACE)
    time.sleep(0.5)            
    driver.find_element_by_id("i_xhz").send_keys(number)
    time.sleep(0.5)
    driver.find_element_by_id("b_xhz1").click()
    pass


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((addr_server , port)) # Привязываем серверный сокет к ip устройства, на котором сервер, и 9515 порту.
s.listen(10) # Начинаем прослушивать входящие соединения.
try:
    driver.get(url=website)
    time.sleep(2)
    log_web()
    time.sleep(3)
    number=0 #номер пресета камеры
    adata=0 #пока 0 - меняем пресеты, пока 1 - ждём 
    while True:
        conn, addr = s.accept() # Метод который принимает входящее соединение.
        if addr_reciever in addr: 
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
            if number<preset:
                number+=1
            else:
                number=1
            control_cam(number)
            time.sleep(5)
except Exception as ex:
    print(ex)

# https://chromedriver.chromium.org/downloads  тут скачать драйвер
