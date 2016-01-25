# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class ValpakPipeline(object):
    def process_item(self, item, spider):
        return item


class ValpakImagePipeline(ImagesPipeline):


    def file_path(self, request, response=None, info=None):
        image_guid = request.meta['sku']
        # check if image already exists and add some random char to the file name
        path_format = 'full/{}.jpg'
        working_dir = os.getcwd() + '/imagesdot/valpak/'
        file_name = image_guid + ".0"
        path = path_format.format(file_name)
        full_path = working_dir + path
        if os.path.exists(full_path):
            file_name = image_guid + ".1"
            path = path_format.format(file_name)
            full_path = working_dir + path
            if os.path.exists(full_path):
                file_name = image_guid + ".2"
                path = path_format.format(file_name)
                full_path = working_dir + path
                if os.path.exists(full_path):
                    file_name = image_guid + ".3"
                    path = path_format.format(file_name)
        request.meta['file_name'] = file_name
        return path


    def thumb_path(self, request, thumb_id, response=None, info=None):
        print(request.meta['file_name'])
        image_guid = request.meta['file_name']
        # check if image already exists and add some random char to the file name
        path_format = 'thumb/{0}/{1}_{0}.jpg'
        return 'thumbs/{0}/{1}_{0}.jpg'.format(thumb_id, image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta=item)

