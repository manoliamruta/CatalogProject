from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with
# the database and represents a "staging zone" for all the objects
# loaded into the database session object. Any change made
# against the objects in the session won't be persisted into
# the database until you call session.commit(). If you're not
# happy about the changes, you can revert all of them back to
# the last commit by calling session.rollback()
session = DBSession()

# Create a user
User1 = User(name="Amruta", email="manoliamruta@gmail.com")
session.add(User1)
session.commit()

# Items used in playing Soccer
category1 = Category(name="Soccer",
                     image="/static/soccer.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()

item1 = Item(name="Soccer Cleats",
             description=" Soccer cleats\
             , or what the English call boots, are like\
             baseball or softball cleats but the cleats \
             are short and made of rubber (metal cleats \
             are not allowed).",
             price="$2.99",
             user_id=User1.id,
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Shin Guards",
             description="Soccer is \
             definitely a contact sport. Shin guards help \
             reduce the chance of injury to the shin \
             (tibia). The shinguards should efficiently \
             protect the player's shins and fit securely \
             in their soccer socks.",
             price="$5.50",
             user_id=User1.id,
             category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Socks",
             description="Soccer socks are extremely \
             long. They cover shin-guards.",
             price="$3.99",
             user_id=User1.id,
             category=category1)

session.add(item3)
session.commit()

# Items used in playing Basketball
category1 = Category(name="Basketball",
                     image="/static/basketball.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()


item1 = Item(name="Basketball Sneakers",
             description="One needs \
             specialized shoes when playing basketball. \
             It should be able to give better support to \
             the ankle as compared to running shoes. The \
             basketball shoes should be high-tipped shoes \
             and provide extra comfort during a game. These \
             shoes are specially designed to maintain high \
             traction on the basketball court.",
             price="$7.99",
             user_id=User1.id,
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Athletic Socks",
             description=" Players should \
             wear two pairs of athletic socks. This will \
             help prevent their feet and toes from \
             blistering and will also provide additional \
             comfort for their feet.",
             price="$25",
             user_id=User1.id,
             category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Elbow Pads",
             description="There is a lot of \
             contact in basketball. Players should wear \
             elbow pads to prevent causing injuries to \
             others. Covering their elbows will reduce \
             the chance of another player being injured \
             if accidentally elbowed. ",
             price="15",
             user_id=User1.id,
             category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Knee Pads",
             description="Players should wear \
             knee pads to protect themselves during falls \
             or dives to the floor. ",
             price="12",
             user_id=User1.id,
             category=category1)

session.add(item4)
session.commit()

# Items used in playing Baseball
category1 = Category(name="Baseball",
                     image="/static/baseball.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()


item1 = Item(name="Baseball Glove",
             description="One of the \
             first things you'll need is a baseball glove. \
             A catcher uses a mitt, which is typically much \
             larger than a traditional baseball glove, and \
             designed to catch blazing fastballs from \
             pitchers.",
             price="$8.99",
             user_id=User1.id,
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Baseball Bat",
             description="There are many \
             different kinds of bats and, like gloves, \
             there are models for youth and adult. Youth \
             bats have smaller barrels and are a lot \
             lighter. Adult bats are heavier and have \
             bigger barrels. It's easier to hit the ball \
             more solidly with a bigger barrel, so my \
             advice is to get a bat that's as big as you can \
             handle. By handle I mean hold and swing \
             comfortably, and it doesn't feel like a log \
             in your hands. There are aluminum and other \
             types of metal bats and there are wood bats. \
             Most leagues lower than professional baseball \
             use metal bats.",
             price="$6.99",
             user_id=User1.id,
             category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Batting Helmet",
             description="If you're going \
             to be playing in a game, or stepping in to try \
             to hit live pitching, you'll need a helmet. \
             Helmets are made of strong plastic material \
             and have padding on the inside for safety \
             and comfort. ",
             price="$9.95",
             user_id=User1.id,
             category=category1)

session.add(item3)
session.commit()

# Items used in playing Frisbee
category1 = Category(name="Frisbee",
                     image="/static/frisbee.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()

# Items used in playing Snowboarding
category1 = Category(name="Snowboarding",
                     image="/static/snowboarding.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()

# Items used in playing Foosball
category1 = Category(name="Foosball",
                     image="/static/foosball.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()

# Items used in playing Skating
category1 = Category(name="Skating",
                     image="/static/skating.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()

# Items used in playing Hockey
category1 = Category(name="Hockey",
                     image="/static/hockey.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()

# Items used in playing Rock Climbing
category1 = Category(name="Rock Climbing",
                     image="/static/rockclimbing.jpeg",
                     user_id=User1.id)

session.add(category1)
session.commit()

# Items used in playing Rock Climbing
category1 = Category(name="Badminton",
                     image="/static/badminton.jpeg",
                     user_id=User1.id)

session.add(category1)
session.commit()

# Items used in playing Rock Climbing
category1 = Category(name="Cricket",
                     image="/static/cricket.jpg",
                     user_id=User1.id)

session.add(category1)
session.commit()


print "added categories and items!"
