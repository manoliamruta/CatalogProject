import sys

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)  
    picture = Column(String(250))


class Category(Base):
	__tablename__ = "category"

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	image = Column(String(250))
	date = Column(DateTime, default=datetime.datetime.utcnow)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		#Returns object data in easily serializable form
		return {
			'name' :self.name,			
			'id' : self.id,			
			'image' : self.image,
			'date' : self.date,
		}
	

class Item(Base):
	__tablename__="item"

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(250))
	price = Column(String(8))	
	date = Column(DateTime, default=datetime.datetime.utcnow)
	category_id = Column(Integer, ForeignKey('category.id'))
	image = Column(String(250))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		#Returns object data in easily serializable form
		return {
			'name' :self.name,
			'description' : self.description,
			'id' : self.id,
			'price' : self.price,
			'date' : self.date,
		}
engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)

