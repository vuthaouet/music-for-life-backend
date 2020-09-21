import sys
sys.path.insert(0, './')

from Model.models import *
import json
from urllib.parse import urlparse
import os
from Utils.reader_helper import load_json
import csv
class ImportData:

    def __init__(self, datapath):
        self.books = load_json(datapath + "/books.txt")['Sheet1']
        self.datapath = datapath
        self.base_url = "http://qldv.uet.vnu.edu.vn/upload/mindbook/"
        self.category_dict = self.load_category_dict(self.books)
        self.author_dict = self.load_author_dict(self.books)

    def load_category_dict(self, books):
        categories = set()
        for book in books:
            book_categories = [x.strip(' ') for x in book["Thể loại"].split(",")];
            categories.update(book_categories)
        print(categories)
        d = {x: index+1 for index, x in enumerate(categories)}
        return d

    def load_author_dict(self, books):
        authors = set()
        for book in books:
            book_author = book["Tác giả"].strip(" ");
            authors.add(book_author);
        d = {x: index+1 for index, x in enumerate(authors)}
        print(d)
        return d

    def import_authors(self):
        for item in self.author_dict.keys():
            author = AuthorDetails(author_name=item)
            author.save_to_db()

    def import_categories(self):
        for item in self.category_dict.keys():
            category = CategoryDetails(category_name_vi=item)
            category.save_to_db()

    def import_books(self):
        for item in self.books:
            print(self.base_url + "epub/" + item["STT"] + "/" + os.listdir(self.datapath + "/epub/" + item["STT"])[0])
            book = BookDetails(book_title=item["Tên sách"], book_description=item["Giới thiệu"],
                               author_id= self.author_dict[item["Tác giả"].strip(" ")],
                               book_cover= self.base_url + "images/" + item["STT"] + "/" + os.listdir(self.datapath + "/images/" + item["STT"])[0],
                               book_epub = self.base_url + "epub/" + item["STT"] + "/" + os.listdir(self.datapath + "/epub/" + item["STT"])[0])
            book.save_to_db(force=True)

    def import_audio(self):
        for item in self.books:
            list_path = os.listdir(self.datapath + "/audio/" + item["STT"])
            for path in list_path:
                print(int(item["STT"]))
                print(self.base_url + "audio/" + item["STT"] + "/" +path)
                audio = BookAudio(book_id=int(item["STT"]), url=self.base_url + "audio/" + item["STT"] + "/" +path)
                audio.save_to_db()


    def import_book_categories(self):
        for index, item in enumerate(self.books):
            book_categories = [x.strip(' ') for x in item["Thể loại"].split(",")];
            for tmp in book_categories:
                book_categories = BookCategories(book_id=index+1, category_id=self.category_dict[tmp])
                book_categories.save_to_db()


def refactor_file(root):
    for path, subdirs, files in os.walk(root):
        for name in files:
            d_path = os.path.join(path, name)
            os.rename(d_path, d_path.replace("-", "").replace(" ", "_"))
            # if "Mobile\images" in d_path:
            #     if ".epub" in d_path:
            #         os.remove(d_path)
            #     if ".mp3" in d_path:
            #         os.remove(d_path)
            # if "Mobile\\audio" in d_path:
            #     if ".jpg" in d_path:
            #         os.remove(d_path)
            #     if ".epub" in d_path:
            #         os.remove(d_path)
            # if "Mobile\epub" in d_path:
            #     if ".jpg" in d_path:
            #         os.remove(d_path)
            #     if ".mp3" in d_path:
            #         os.remove(d_path)
            # if ".txt" in d_path:
            #     os.remove(d_path)

# refactor_file("E://Ky_II_2019_2020/PTUDDD/Mobile")
