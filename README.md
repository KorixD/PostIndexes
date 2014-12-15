Почтовые индексы

Общие сведения: 
Почтовому индексу сопоставляется адрес до улицы. Для получения дерева адресов и индексов осуществляется запрос к ФИАС(http://wiki.gis-lab.info/w/ФИАС#ADDROBJ).

* Сырые данные в формате .csv (поля - postindex, region, city, street)
* Запрос на http://geocode-maps.yandex.ru/1.x/?geocode=Россия, получение из ответа широты и долготы улицы
* Экспорт данных в формат turtle

Сырые данные из http://fias.nalog.ru/Public/DownloadPage.aspx

Онтология: 
http://schema.org/Place(geoCoordinates & postalAddress)