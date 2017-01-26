from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'picture': self.picture
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_name = Column(String(250), nullable=False)
    age_range = Column(String(15))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'category_name': self.category_name,
            'age_range': self.age_range
        }


class LegoSet(Base):
    __tablename__ = 'lego_set'

    set_name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    pieces = Column(Integer)
    set_id = Column(Integer)
    description = Column(String(250))
    categoryName = Column(String(250), ForeignKey('category.category_name'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'set_name': self.set_name,
            'pieces': self.pieces,
            'set_id': self.set_id,
            'description': self.description,
            'categoryName': self.categoryName
        }


engine = create_engine('sqlite:///itemcatalog.db')


Base.metadata.create_all(engine)
