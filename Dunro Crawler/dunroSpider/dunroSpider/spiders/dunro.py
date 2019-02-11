# -*- coding: utf-8 -*-
import scrapy
import requests
import json

class DunroSpider(scrapy.Spider):
    name = 'dunro'
    allowed_domains = ['dunro.com']

    def start_requests(self):
        self.file = open('items.jl', 'w')
        basicIds = ['562c797b84002',
                    '590fa026c7e16',
                    '588d29838444f',
                    '5920c443053be',
                    '5587d8f957352',
                    '5419ab184a881',
                    '53f1993765f36',
                    '5664d35913e0f',
                    '593c72fb09516',
                    '58ad251089ab2',
                    '5753e78dc0108',
                    '5712191455e87',
                    '56cb117f01759',
                    '55e2a4582f8ec',
                    '563800dc32871',
                    '53f198c1800c7',
                    '560be471bb45c',
                    '560be02bc4c72',
                    '53f1990fe91f8',
                    '5651b7c4e5852',
                    '53f1990a394a5',
                    '53f19908b00af']
        urls = ['https://dunro.com/api/v1.3/business/show/' + uuid + '/extend' for uuid in basicIds]

        for url in urls:
            yield scrapy.Request(url=url)

    def makeUrl(self, uuid):
        return 'https://dunro.com/api/v1.3/business/show/' + uuid + '/extend'

    def parse(self, response):
        uuid = response.url.split("/")[-2]
        j = json.loads(response.text)['data']
        title, lat, lng = j['title'], j['lat'], j['lng']

        line = json.dumps({'title': title, 'uuid': uuid, 'lat': lat, 'lng': lng}) + ",\n"
        self.file.write(line)

        relateds = j['relatedBusinesses']
        for rel in relateds:
            uuid = rel['uuid']
            yield scrapy.Request(self.makeUrl(uuid))
