from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    
    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    climate: Mapped[str] = mapped_column(String(), nullable=True)
    terrain: Mapped[str] = mapped_column(String(), nullable=True)
    population: Mapped[str] = mapped_column(String(), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    gender: Mapped[str] = mapped_column(String(), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(), nullable=True)
    species: Mapped[str] = mapped_column(String(), nullable=True)
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    
    homeworld: Mapped["Planet"] = relationship("Planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "species": self.species,
            "homeworld_id": self.homeworld_id
        }

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    model: Mapped[str] = mapped_column(String(), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(), nullable=True)
    crew: Mapped[int] = mapped_column(Integer(), nullable=True)
    passengers: Mapped[int] = mapped_column(Integer(), nullable=True)
    vehicle_class: Mapped[str] = mapped_column(String(), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "crew": self.crew,
            "passengers": self.passengers,
            "vehicle_class": self.vehicle_class
        }

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="favorites")
    character: Mapped["Character"] = relationship("Character")
    planet: Mapped["Planet"] = relationship("Planet")
    vehicle: Mapped["Vehicle"] = relationship("Vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }

class VehiclePilot(db.Model):
    __tablename__ = 'vehicle_pilot'
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), primary_key=True)

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
