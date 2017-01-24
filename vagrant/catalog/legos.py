from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, LegoSet, User

engine = create_engine('sqlite:///catalogitems.db')
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

session.query(Category).delete()
session.commit()

session.query(LegoSet).delete()
session.commit()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Lego Minecraft category
category1 = Category(user_id=1, name="LEGO Minecraft", age_range="Ages 8+")
session.add(category1)
session.commit()

legoSet1 = LegoSet(user_id=1, name="The Village", picture="#", lot_id=21128, pieces=1600, description="Join forces with Alex at the busy Minecraft village, including a variety of biomes plus a watchtower, library, blacksmith, butcher and marketplace. Enjoy hands-on Minecraft adventures featuring your favorite characters and objects with this LEGO Minecraft set-designed for young fans of the highly successful sandbox video game", category=category1)

session.add(legoSet1)
session.commit()

# Lego Creator Expert category
category2 = Category(user_id=1, name="LEGO Creator Expert", age_range="Ages 14+")
session.add(category2)
session.commit()

# Lego Ghostusters category
category3 = Category(user_id=1, name="LEGO Ghostbusters", age_range="Ages 8+")
session.add(category3)
session.commit()

# Lego Technic category
category4 = Category(user_id=1, name="LEGO Technic", age_range="Ages 11+")
session.add(category4)
session.commit()

# Lego Star Wars category
category5 = Category(user_id=1, name="LEGO Star Wars", age_range="Ages 7+")
session.add(category5)
session.commit()

# Lego Super Heroes category
category6 = Category(user_id=1, name="LEGO Super Heroes", age_range="Ages 6+")
session.add(category6)
session.commit()

# Lego Ninjago category
category7 = Category(user_id=1, name="LEGO Ninjago", age_range="Ages 6+")
session.add(category7)
session.commit()

# Lego City category
category8 = Category(user_id=1, name="LEGO City", age_range="Ages 6+")
session.add(category8)
session.commit()

categories = session.query(Category).all()
lego_sets = session.query(LegoSet).all()

for category in categories:
    print(category.name)
    print("\n")

for lego_set in lego_sets:
    print(lego_set.name)
    print("\n")
