# coding=UTF-8

from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, Namespace, XSD
from scrapy import Spider, Item, Field, log, signals
import urllib
from xml.etree import ElementTree as ET

# http://basicdata.ru/download/fias/

# copy(select distinct street.postalcode as postalcode,
# 	region.shortname r_shortname, region.formalname as region,
# 	subregion.shortname as sr_subregion, subregion.formalname as subregion,
# 	city.shortname as c_subregion, city.formalname as city,
# 	street.shortname as str_shortname, street.formalname as street
#
# 	from d_fias_addrobj as region
# 	join d_fias_addrobj as subregion on (region.aoguid = subregion.parentguid)
# 	join d_fias_addrobj as city on (subregion.aoguid = city.parentguid)
# 	join d_fias_addrobj as street on (city.aoguid = street.parentguid)
# 	where region.aolevel = 1 and street.aolevel = 7) to '/tmp/data.csv' with csv;

class Street(Item):
  postindex = Field()
  region = Field()
  city = Field()
  street = Field()

class StreetRepo(object):
  def __init__(self):
    self.namespace = Namespace('http://schema.org/')
    self.base = 'http://ifmo.com/address/'
    self.count = 0
    self.repo = Graph(store='default')
    self.repo.bind('schema', self.namespace)

  def process_street(self, item):
    self.count += 1
    resource = URIRef(self.base + str(self.count))
    geo = URIRef(self.base + str(self.count) + '/geo')
    address = URIRef(self.base + str(self.count) + '/address')

    self.repo.add((resource, RDF.type, self.namespace.Place))
    self.repo.add((resource, self.namespace.GeoCoordinates, geo))
    self.repo.add((resource, self.namespace.PostalAddress, address))

    self.repo.add((geo, RDF.type, self.namespace.GeoCoordinates))
    self.repo.add((address, RDF.type, self.namespace.PostalAddress))

    self.repo.add((address, self.namespace.postalCode, Literal(item['postindex'], lang='en')))
    self.repo.add((address, self.namespace.addressRegion, Literal(item['region'], lang='ru')))
    self.repo.add((address, self.namespace.addressLocality, Literal(item['city'], lang='ru')))
    self.repo.add((address, self.namespace.streetAddress, Literal(item['street'], lang='ru')))

    request = "http://geocode-maps.yandex.ru/1.x/?geocode=Россия, " + item['region'] + " " + item['city'] + " " + item['street']
    geo_root = ET.parse(urllib.urlopen(request)).getroot()
    pos = geo_root.findall('.//{http://www.opengis.net/gml}pos')
    if(len(pos) > 0):
      coords = pos[0].text.split(" ")
      lat = coords[1]
      lon = coords[0]
      self.repo.add((geo, self.namespace.latitude, Literal(lat, lang='en')))
      self.repo.add((geo, self.namespace.longitude, Literal(lon, lang='en')))
    print self.count


  def close(self):
    f = open('open-street.ttl','w')
    self.repo.serialize(f, format='turtle')
    self.repo.close()

def main():
  repo = StreetRepo()
  data = open("open-street.csv","r")
  result = []

  count = 0
  for line in data:
    fields = line.split(",")
    street = Street()
    street['postindex'] = fields[0]
    street['region'] = (fields[1] + " " + fields[2] + " " + fields[3] + " " + fields[4]).strip()
    street['city'] = (fields[5] + " " + fields[6]).strip()
    street['street'] = (fields[7] + " " + fields[8]).strip()
    repo.process_street(street)
    count = count + 1
    if (count == 100):
        break
  repo.close()
  data.close()

if __name__ == "__main__":
  main()
