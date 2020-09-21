# coding: utf-8

from sqlalchemy import desc, func, DateTime
from sqlalchemy.dialects.mysql import DOUBLE
from DB_Connection.db import sql_db
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.ext.hybrid import hybrid_property
from Utils.SqlEscape import *
import datetime

db = sql_db()


class UserDetails(db.Model):
    __tablename__ = 'user_details'

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(200), default="http://qldv.uet.vnu.edu.vn/upload/mindbook/default_avatar.jpg")
    latitude = db.Column(DOUBLE, nullable=True)
    longitude = db.Column(DOUBLE, nullable=True)
    sharing_details = db.relationship("SharingDetails", backref="sharing_details")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != 'password'}

    def update_position(self, latitude, longitude):
        setattr(self, "latitude", latitude)
        setattr(self, "longitude", longitude)
        db.session.commit()
        return True

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_user_name(cls, user_name):
        return cls.query.filter_by(user_name=user_name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()

    @classmethod
    def get_number_of_users(cls):
        return cls.query.count()

    @classmethod
    def return_all_pos(cls):
        def to_json(x):
            return {
                'id': x.user_id,
                'latitude' : x.latitude,
                'longitude' : x.longitude
            }

        return {'users': list(map(lambda x: to_json(x),  db.session.query(UserDetails.user_id, UserDetails.latitude, UserDetails.longitude).all()))}


    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.user_id,
                'user_name': x.user_name,
                'email': x.email,
                'password': x.password,
                'first_name': x.first_name,
                'last_name': x.last_name
            }

        return {'users': list(map(lambda x: to_json(x), UserDetails.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            print(num_rows_deleted)
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class BookDetails(db.Model):
    __tablename__ = 'book_details'

    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.Unicode(200, collation='utf8_bin'))
    book_description = db.Column(db.UnicodeText(collation='utf8_bin'))
    author_id = db.Column(db.Integer, db.ForeignKey("author_details.author_id"))
    book_cover = db.Column(db.Unicode(200, collation='utf8_bin'))
    book_epub = db.Column(db.Unicode(200, collation='utf8_bin'))
    cnt_5star = db.Column(db.Integer, default=0)
    cnt_4star = db.Column(db.Integer, default=0)
    cnt_3star = db.Column(db.Integer, default=0)
    cnt_2star = db.Column(db.Integer, default=0)
    cnt_1star = db.Column(db.Integer, default=0)
    book_audio = db.relationship("BookAudio", backref="book_audio")
    ratings_details = db.relationship("RatingDetails", backref="book_details")

    def save_to_db(self, force=False):
        if force or not self.find_by_id(id=self.book_id):
            db.session.add(self)
            db.session.commit()
            return True
        return False

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(book_title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(book_id=id).first()

    @classmethod
    def search_by_title(cls, title):
        return db.session.query(BookDetails.book_id).filter(BookDetails.book_title.ilike('%' + escape_sqlalchemy_like(title) + '%'))

    @classmethod
    def to_json(cls, x):
        return {
            'id': x.book_id,
            'book_title': x.book_title,
            'book_description': x.book_description,
            'book_cover': x.book_cover,
            'book_epub': x.book_epub,
            'rating': x.get_average_rating(),
        }

    @classmethod
    def return_all(cls, limit, page):
        return {'data': list(map(lambda x: cls.to_json(x),
                                 BookDetails.query.paginate(page=page, per_page=limit, error_out=False).items))}

    @classmethod
    def return_by_category(cls, category_id, limit, page):
        return BookDetails.query.join(BookCategories) \
            .join(AuthorDetails) \
            .filter(BookCategories.category_id == category_id) \
            .limit(limit).offset((page - 1) * limit)

    @classmethod
    def get_book_details(cls, book_id):
        book_details = BookDetails.query.filter_by(book_id=book_id).join(AuthorDetails)
        if not book_details:
            return False, 'Book does not exist'
        return True, book_details

    @classmethod
    def return_top_books(cls, limit, page):
        return BookDetails.query.order_by(BookDetails.get_average_rating_sql.desc()) \
            .paginate(page=page, per_page=limit, error_out=False).items

    def add_rating(self, rating_num):
        rating_num = int(rating_num)
        if not 1 <= rating_num <= 5:
            return False
        cnt_rating = 'cnt_{num}star'.format(num=rating_num)
        setattr(self, cnt_rating, getattr(self, cnt_rating) + 1)
        db.session.commit()
        return True

    def swap_rating(self, old_rating, new_rating):
        new_rating = int(new_rating)
        if not 1 <= new_rating <= 5:
            return False
        cnt_old = 'cnt_{num}star'.format(num=old_rating)
        cnt_new = 'cnt_{num}star'.format(num=new_rating)
        setattr(self, cnt_old, getattr(self, cnt_old) - 1)
        setattr(self, cnt_new, getattr(self, cnt_new) + 1)
        db.session.commit()
        return True

    def get_average_rating(self):
        total_sum, total_cnt = 0, 0
        for i in range(1, 6):
            cnt_rating = 'cnt_{num}star'.format(num=i)
            total_cnt += getattr(self, cnt_rating)
            total_sum += getattr(self, cnt_rating) * i
        if total_cnt:
            return round(total_sum / total_cnt, 2)
        else:
            return  0

    @hybrid_property
    def get_average_rating_sql(self):
        pass

    @get_average_rating_sql.expression
    def get_average_rating_sql(cls):
        return (cls.cnt_5star * 5 + cls.cnt_4star * 4 + cls.cnt_3star * 3 + cls.cnt_2star * 2 + cls.cnt_1star) / \
               (cls.cnt_5star + cls.cnt_4star + cls.cnt_3star + cls.cnt_2star + cls.cnt_1star)

class BookAudio(db.Model):
    __tablename__ = 'book_audio'

    audio_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book_details.book_id'))
    url = db.Column(db.Unicode(200, collation='utf8_bin'), default = "")
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class BookCategories(db.Model):
    __tablename__ = 'book_categories'

    book_id = db.Column(db.Integer, db.ForeignKey('book_details.book_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category_details.category_id'), primary_key=True)

    def save_to_db(self):
        if not self.check_dup(self.book_id, self.category_id):
            db.session.add(self)
            db.session.commit()
            return True
        return False

    @classmethod
    def find_by_book_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id).all()

    @classmethod
    def check_dup(cls, book_id, category_id):
        return cls.query.filter_by(book_id=book_id, category_id=category_id).first()


class AuthorDetails(db.Model):
    __tablename__ = 'author_details'

    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.Unicode(120, collation='utf8_bin'))
    book_details = db.relationship("BookDetails", backref="author_details")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, author_id):
        return cls.query.filter_by(author_id=author_id).first()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    @classmethod
    def search_by_name(cls, name):
        return db.session.query(BookDetails.book_id, AuthorDetails).join(BookDetails).filter(
            AuthorDetails.author_name.ilike('%' + escape_sqlalchemy_like(name) + '%'))


    @classmethod
    def to_json(cls, x):
        return {
            'author_id': x.author_id,
            'author_name': x.author_name,
        }

    @classmethod
    def return_all(cls, limit, page):
        return {'data': list(map(lambda x: cls.to_json(x),
                                 AuthorDetails.query.paginate(page=page, per_page=limit, error_out=False).items))}

    @classmethod
    def return_top(cls, limit, page):
        return cls.return_all(limit, page)


class RatingDetails(db.Model):
    __tablename__ = 'rating_details'

    user_id = db.Column(db.Integer, db.ForeignKey('user_details.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book_details.book_id'), primary_key=True)
    rating_num = db.Column(db.Integer)
    rating_comment = db.Column(db.UnicodeText(collation='utf8_bin'))
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    @classmethod
    def find_by_user(cls, user_id, limit, page):
        return {'data': list(map(lambda x: RatingDetails.as_dict(x),
                                 cls.query.filter_by(user_id=user_id)
                                 .limit(limit).offset((page - 1) * limit)))}

    @classmethod
    def get_new_rating(cls, limit, page):
        return db.session.query(UserDetails, RatingDetails, BookDetails, AuthorDetails.author_name).join(UserDetails)\
                .join(BookDetails).join(AuthorDetails)\
                .order_by(RatingDetails.created_date.desc()) \
                .paginate(page=page, per_page=limit, error_out=False).items

    @classmethod
    def find_by_user_and_rating_num(cls, user_id, rating_num):
        return cls.query.filter_by(user_id=user_id, rating_num=rating_num).count()

    @classmethod
    def find_by_book(cls, book_id, limit, page):
        return list(map(lambda x: RatingDetails.as_dict(x),
                        cls.query.filter_by(book_id=book_id)
                        .order_by(RatingDetails.created_date.desc())
                        .paginate(page=page, per_page=limit, error_out=False).items))

    @classmethod
    def find_existing(cls, user_id, book_id):
        return cls.query.filter_by(user_id=user_id, book_id=book_id).first()


class CategoryDetails(db.Model):
    __tablename__ = 'category_details'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name_vi = db.Column(db.Unicode(120, collation='utf8_bin'))
    category_name_en = db.Column(db.Unicode(120, collation='utf8_bin'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(category_id=id).first()

    @classmethod
    def to_json(cls, x):
        return {
            'category_id': x.category_id,
            'category_name': x.category_name_vi
        }

    @classmethod
    def return_all(cls, limit, page):
        data = None
        if limit == -1:
            data = CategoryDetails.query.all()
        else:
            data = CategoryDetails.query.paginate(page=page, per_page=limit, error_out=False).items
        return {'data': list(map(lambda x: cls.to_json(x), data))}

    @classmethod
    def search_by_category_name(cls, name, lang):
        if lang == "vi":
            return db.session.query(BookCategories.book_id, CategoryDetails).join(BookCategories).filter(CategoryDetails.category_name_vi.ilike('%' + escape_sqlalchemy_like(name) + '%'))
        else:
            return db.session.query(BookCategories.book_id, CategoryDetails).join(BookCategories).filter(CategoryDetails.category_name_en.ilike('%' + escape_sqlalchemy_like(name) + '%'))

    @classmethod
    def popular_categories(cls, limit, page):
        return db.session.query(
            func.count(BookCategories.category_id).label('num_books'),
            CategoryDetails.category_id,
            CategoryDetails.category_name_vi
        ).join(CategoryDetails) \
            .group_by(BookCategories.category_id) \
            .order_by(desc('num_books')) \
            .paginate(page=page, per_page=limit, error_out=False).items



class BannerDetails(db.Model):
    __tablename__ = 'banner_details'

    banner_id = db.Column(db.Integer, primary_key=True)
    banner_image = db.Column(db.String(200))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def to_json(cls, x):
        return {
            'id': x.banner_id,
            'image': x.banner_image
        }

    @classmethod
    def return_all(cls, limit, page):
        data = None
        data = BannerDetails.query.paginate(page=page, per_page=limit, error_out=False).items
        return {'data': list(map(lambda x: cls.to_json(x), data))}

class Playlist(db.Model):
    __tablename__ = 'playlist'

    playlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.user_id'))
    name = db.Column(db.Unicode(200, collation='utf8_bin'))
    books_count = db.Column(db.Integer, default = 0)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_by_user(cls, user_id):
        return Playlist.query.filter(Playlist.user_id == user_id)

    @classmethod
    def return_by_playlist_id(cls, playlist_id):
        return Playlist.query.filter(Playlist.playlist_id == playlist_id).first()

    def add_book(self):
        setattr(self, 'books_count', getattr(self, 'books_count') + 1)
        db.session.commit()
        return True

    def remove_book(self):
        setattr(self, 'books_count', getattr(self, 'books_count') - 1)
        db.session.commit()
        return True

    @classmethod
    def find_existing(cls, user_id, name):
        return cls.query.filter_by(user_id=user_id, name=name).first()

class PlaylistDetails(db.Model):
    __tablename__ = 'playlist_details'

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book_details.book_id'), primary_key=True)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    @classmethod
    def find_by_playlist_id(cls, playlist_id):
        return cls.query.filter_by(playlist_id=playlist_id)

    @classmethod
    def find_existing(cls, playlist_id, book_id):
        return cls.query.filter_by(playlist_id=playlist_id, book_id=book_id).first()

    @classmethod
    def delete_record(cls, playlist_id, book_id):
        PlaylistDetails.query.filter(PlaylistDetails.playlist_id == playlist_id).filter(
            PlaylistDetails.book_id == book_id).delete()
        db.session.commit()

class SharingDetails(db.Model):
    __tablename__ = 'sharing_details'

    user_id = db.Column(db.Integer, db.ForeignKey('user_details.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book_details.book_id'), primary_key=True)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_book_id(self):
        return self.book_id


    @classmethod
    def find_existing(cls, user_id, book_id):
        return cls.query.filter_by(user_id=user_id, book_id=book_id).first()

    @classmethod
    def delete_record(cls, user_id, book_id):
        SharingDetails.query.filter(SharingDetails.user_id == user_id).filter(SharingDetails.book_id == book_id).delete()
        db.session.commit()