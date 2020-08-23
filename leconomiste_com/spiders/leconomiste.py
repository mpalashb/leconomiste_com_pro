# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class LeconomisteSpider(scrapy.Spider):
    name = 'leconomiste'
    allowed_domains = ['leconomiste.com']
    start_urls = ['https://www.leconomiste.com/archives/all']

    def parse(self, response):
        # links=response.css('span.field-content a::attr(href)').extract()
        links_ele=response.css('li.views-row')
        for link in links_ele:
            ab_link=link.css('span.field-content a::attr(href)').extract_first()
            ab_link=response.urljoin(ab_link)
            dates=link.css('span.date-display-single::text').extract_first()
            yield scrapy.Request(ab_link, meta={'dates':dates},callback=self.parse2)

        # next_page=response.xpath('//*[@title="Go to the next page"]//@href').extract_first()
        next_page=response.xpath('//*[@class="next"]//a//@href').extract_first()
        if next_page:
            ab_next_page=response.urljoin(next_page)
            yield scrapy.Request(ab_next_page)

    def parse2(self, response):
        href_link=response.url
        # dates=response.css('span.date-display-single::text').extract_first()
        dates=response.meta['dates']
        secelements=response.xpath('//*[@class="panel panel-default"]')
        for ele in secelements:
            lin=ele.xpath('.//h4//a//@href')
            if lin:
                lin=lin.extract()[-1]
            ab_lin=response.urljoin(lin)
            underlying_content=ele.xpath('.//*[@class="views-field views-field-nothing"]//p//text()').extract_first()
            yield scrapy.Request(ab_lin, meta={'href_link':href_link,'dates':dates,'underlying_content':underlying_content}, callback=self.parse_page)


            # lin=ele.xpath('.//*[@class="field-content"]//p//text()').extract()



    def parse_page(self, response):
        href_link=response.meta['href_link']
        link_con=response.url
        date=response.meta['dates']
        press_article_title=response.css('section.block h1::text').extract_first()
        if press_article_title:
            press_article_title=press_article_title.strip()
        underlying_content=response.meta['underlying_content']
        overview_content=response.xpath('//*[@property="content:encoded"]//text()').extract()

        yield{
                'href_link':href_link,
                'link_con':link_con,
                'date':date,
                'press_article_title':press_article_title,
                'underlying_content':underlying_content,
                'overview_content':overview_content


        }