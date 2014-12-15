Почтовые индексы

Общие сведения: 
Почтовому индексу сопоставляется адрес до улицы. Для получения дерева адресов и индексов осуществляется запрос к ФИАС(http://wiki.gis-lab.info/w/ФИАС#ADDROBJ).

* Сырые данные в формате .csv (поля - postindex, region, city, street)
* Запрос на http://geocode-maps.yandex.ru/1.x/?geocode=Россия, получение из ответа широты и долготы улицы
* Экспорт данных в формат turtle

Сырые данные open-street.cv

Онтология: 
Schema, URI: http://schema.org/ (geoCoordinates & postalAddress)

Примеры SPARQL-запросов:
 - prefix schema: <http://schema.org/>
select ?x ?z ?a  where {?x a schema:Place. ?x schema:GeoCoordinates ?y. ?y schema:latitude ?z. ?y schema:longitude ?a.}

select ?y ?x where {?a a schema:PostalAddress. ?a schema:postalCode ?x. ?a schema:streetAddress ?y.}