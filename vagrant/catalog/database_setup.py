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


class CharacterType(Base):
    __tablename__ = 'character_type'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    type_name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'type_name': self.type_name
        }


class Character(Base):
    __tablename__ = 'character'

    character_name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    character_picture = Column(String(250))
    character_kind = Column(String(250), ForeignKey('character_type.type_name'))
    character_type = relationship(CharacterType)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'character_name': self.character_name,
            'description': self.description,
            'character_kind': self.character_kind,
            'character_picture': self.character_picture
        }


engine = create_engine('sqlite:///thomascatalog.db')


Base.metadata.create_all(engine)
