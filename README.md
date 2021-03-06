# Топология
![](/Nornir.png)

# Описание
В рассматриваемой топологии присутствует один L2 сегмент на основе коммутаторов SW1-SW4. Между коммутаторами настроены trunk интерфейсы. Маршрутизаторы R2-R3 выполняют роль рабочих станций, R1 - роль шлюза по умолчанию. Интерфейсы коммутаторов в сторону R1-R3 настроены в режиме access. Управление устройствами доступно через адреса из подсети 192.168.1.0/24.

# Задача
Найти заданный MAC адрес в данной топологии. Решение должно работать при изменении топологии и/или количества устройств в сети при сохранении ролей интерфейсов (trunk между коммутаторами, access для клиентских устройств).

# Входные данные
MAC адрес клиента (R2-R3), шлюза по умолчанию (R1) или SVI (SW1-SW4)

# Инструменты
Платформа Nornir

https://nornir.readthedocs.io/en/latest/

# Выходные данные
Имя коммутатора и исходящий интерфейс

# Окружение
* Ubuntu 18.04, GNS3 2.2.7
* Маршрутизаторы IOS 15.2(4)M11
* Коммутаторы IOSv 15.2

# Подготовка окружения
Объект Cloud позволяет предоставить эмулируемым устройствам доступ во внешнюю сеть, приближая тестовую среду к реальным условиям. Стоит отметить, что задачу допустимо решать, используя доступ к консоли устройств через Telnet. Такая модель отвечает использованию терминального сервера для доступа к устройствам. tap0 - виртуальный интерфейс в Linux, функционально аналогичный loopback в IOS.

## Создание tap0
``` shell
sudo apt-get install uml-utilities bridge-utils
sudo tunctl -t tap0
sudo ifconfig tap0 192.168.100.1/24 up
```

## Статический маршрут через tap0
``` shell
sudo ip route add 192.168.1.0/24 via 192.168.100.2
```

При необходимости использовать протоколы маршрутизации вместо статических маршрутов, можно использовать пакет Quagga.
