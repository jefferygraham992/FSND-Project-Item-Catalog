from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import CharacterType, Base, Character, User

engine = create_engine('sqlite:///thomascatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

session.query(User).delete()
session.commit()

session.query(CharacterType).delete()
session.commit()

session.query(Character).delete()
session.commit()

# Create dummy user
User1 = User(user_name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Steam Engines
type1 = CharacterType(user_id=1, type_name="Steam Engines")
session.add(type1)
session.commit()

character1 = Character(user_id=1, character_name="Thomas", description="Thomas's character changes from time to time, from cheeky to wise. He is portrayed as proud to run his own branch line and fond of the coaches, Annie and Clarabel. He has the number 1 painted on both his side tanks.", character_picture="https://upload.wikimedia.org/wikipedia/en/d/dc/Thomas_Tank_Engine_1.JPG", character_kind=type1.type_name)

session.add(character1)
session.commit()

# Diesel Engines
type2 = CharacterType(user_id=1, type_name="Diesel Engines")
session.add(type2)
session.commit()

# Narrow Gauge Engines
type3 = CharacterType(user_id=1, type_name="Narrow Gauge Engines")
session.add(type3)
session.commit()

# Miscellanous Vehicles
type4 = CharacterType(user_id=1, type_name="Miscellanous Vehicles")
session.add(type4)
session.commit()

types = session.query(CharacterType).all()
characters = session.query(Character).all()

for item in types:
    print(item.type_name)
    print("\n")

for character in characters:
    print(character.character_name)
    print(character.description)
    print(character.character_kind)
    print("\n")

