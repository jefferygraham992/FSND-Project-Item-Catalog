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
User1 = User(username="Jeffery Graham", email="jefferygraham992@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Steam Engines
type1 = CharacterType(user_id=1, type_name="Steam Engines")
session.add(type1)
session.commit()

thomas = Character(user_id=1, character_name="Thomas the Tank Engine", description="Thomas the Tank Engine is the most famous engine who is painted blue with red lining. He is a cheeky little engine and tries very hard to be a very useful. Thomas is easily identified by his No. 1 and bright blue color.", character_picture="http://www.topslotsntrains.com/uploaded_photos/Wooden-Railway-Thomas-the-Tank-Engine_0.jpg", character_kind=type1.type_name)
session.add(thomas)
session.commit()

edward = Character(user_id=1, character_name="Edward the Blue Engine", description="Edward the Blue Engine is one of the older and wiser engines on Sir Topham Hatt's railway. He is a blue 4-4-0 tender engine with red stripes and he is No. 2. Edward is a very kind engine and when other engines misbehave Sir Topham Hatt requests Edward to restore order on the railway.", character_picture="https://images-na.ssl-images-amazon.com/images/I/61Q5H-qysiL._SL1300_.jpg", character_kind=type1.type_name)
session.add(edward)
session.commit()

gordon = Character(user_id=1, character_name="Gordon the Big Express Engine", description="Gordon the Big Express Engine is blue and pulls the Express. He is goodhearted and is the fastest and strongest of all the engines on the Island of Sodor. Gordon wears the No. 4 and has a good-natured rivalry with fellow main line engines Henry the Green Engine and James the Red Engine.", character_picture="https://images-na.ssl-images-amazon.com/images/I/41OFogTH6VL._SY355_.jpg", character_kind=type1.type_name)
session.add(gordon)
session.commit()

james = Character(user_id=1, character_name="James the Red Engine", description="James the Red Engine is very proud of his shining brass dome and scarlet coat. He is a medium sized engine and he is the No. 5 red engine and likes to stay clean. James is a very useful engine who doesn't like to pull trucks, he prefers to pull coaches. He is a powerful engine and is allowed to pull the Express when Gordon is not around.", character_picture="https://images-na.ssl-images-amazon.com/images/I/81wmPXSCWOL._SX355_.jpg", character_kind=type1.type_name)
session.add(james)
session.commit()

toby = Character(user_id=1, character_name="Toby the Tram Engine", description="Toby the Tram Engine is an old fashioned looking engine who is square. He is a happy all the time and can be found working on the Quarry line with Henrietta, his faithful coach. Toby is No. 7 and has cowcatchers and sideplates. He usually works on the Ffarquhar branch line with Thomas the Tank Engine.", character_picture="https://images-na.ssl-images-amazon.com/images/I/41FXheT5BhL._SX300_.jpg", character_kind=type1.type_name)
session.add(toby)
session.commit()

# Diesel Engines
type2 = CharacterType(user_id=1, type_name="Diesel Engines")
session.add(type2)
session.commit()

diesel10 = Character(user_id=1, character_name="Diesel 10", description="Diesel 10 is a villainous diesel engine with a roof top hydraulic grabber or claw which is nicknamed Pinchy. He is ochre colored with white hazard stripes and is known to be mean, devious and is despised by the steam engines. Thomas gives him a 10 out of 10, for devious deeds and brutal strength!", character_picture="https://images-na.ssl-images-amazon.com/images/I/61mKx4R2nzL._SX355_.jpg", character_kind=type2.type_name)
session.add(diesel10)
session.commit()

# Narrow Gauge Engines
type3 = CharacterType(user_id=1, type_name="Narrow Gauge Engines")
session.add(type3)
session.commit()

luke = Character(user_id=1, character_name="Luke", description="Luke is a small engine, even for the Narrow Gauge Railway. When Luke arrived on Sodor, he hid out of shame believing that he caused an engine to fall into the sea. With Thomas' help, Luke learned the truth and was able to stop hiding.", character_picture="http://www.toysrus.com/graphics/product_images/pTRU1-15128898enh-z6.jpg", character_kind=type3.type_name)
session.add(luke)
session.commit()

# Electric Engines
type4 = CharacterType(user_id=1, type_name="Electric Engines")
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
