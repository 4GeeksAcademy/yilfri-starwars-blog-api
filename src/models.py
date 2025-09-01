from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(
        String(24), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(48), nullable=False)
    lastname: Mapped[str] = mapped_column(String(48), nullable=False)

    favorite_planets: Mapped[List["Favorite_Planet"]
                             ] = relationship(back_populates="user")
    favorite_characters: Mapped[List["Favorite_Character"]] = relationship(
        back_populates="user")

    def __repr__(self):
        return f'[Usuario {self.id} - {self.username}]'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets],
            "favorite_characters": [character.serialize() for character in self.favorite_characters]
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(
        String(28), nullable=False)
    height: Mapped[float] = mapped_column(
        Float(), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)

    favorite_characters = relationship("Favorite_Character")

    def __repr__(self):
        return f'[Character {self.id} - {self.name}]'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(48), unique=True, nullable=False)
    rotation: Mapped[str] = mapped_column(
        String(48), nullable=False)
    gravity: Mapped[str] = mapped_column(
        String(48), nullable=False)
    diameter: Mapped[str] = mapped_column(
        String(48), nullable=False)
    terrain: Mapped[str] = mapped_column(
        String(48), nullable=False)

    favorite_planets = relationship("Favorite_Planet")

    def __repr__(self):
        return f'[Planet {self.id} - {self.name}]'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation": self.rotation,
            "gravity": self.gravity,
            "diameter": self.diameter,
            "terrain": self.terrain,
        }


class Favorite_Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id = mapped_column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="favorite_planets")

    planet_id = mapped_column(Integer, ForeignKey("planet.id"))
    planet = relationship("Planet", back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize(),
        }


class Favorite_Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id = mapped_column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="favorite_characters")

    character_id = mapped_column(Integer, ForeignKey("character.id"))
    character = relationship("Character", back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize()
        }
