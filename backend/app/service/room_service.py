from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.room import Room
from ..schemas.room import RoomCreate, RoomUpdate, RoomResponse
from typing import List
from ..exceptions import RoomNotFoundException, DatabaseException, RoomAlreadyExistsException


def get_rooms(db: Session) -> List[RoomResponse]:
    try:
        rooms = db.query(Room).filter(Room.is_deleted == False).all()  # ← 論理削除された会議室を除外
        if not rooms:
            raise RoomNotFoundException()
        return rooms
    except Exception as e:
        raise DatabaseException(str(e))


def create_room(db: Session, room_data: RoomCreate) -> RoomResponse:
    try:
        new_room = Room(name=room_data.name, capacity=room_data.capacity)
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        return new_room
    except IntegrityError:
        db.rollback()
        raise RoomAlreadyExistsException()
    except Exception as e:
        db.rollback()
        raise DatabaseException(str(e))


def update_room(db: Session, room_id: int, room_data: RoomUpdate) -> RoomResponse:
    try:
        room = db.query(Room).filter(Room.id == room_id, Room.is_deleted == False).first()
        if not room:
            raise RoomNotFoundException()

        if room_data.name is not None:
            room.name = room_data.name
        if room_data.capacity is not None:
            room.capacity = room_data.capacity

        db.commit()
        db.refresh(room)
        return room
    except IntegrityError:
        db.rollback()
        raise RoomAlreadyExistsException()
    except Exception as e:
        db.rollback()
        raise DatabaseException(str(e))


def delete_room(db: Session, room_id: int) -> None:
    try:
        room = db.query(Room).filter(Room.id == room_id, Room.is_deleted == False).first()
        if not room:
            raise RoomNotFoundException()

        room.is_deleted = True  # ← 論理削除
        db.commit()
    except Exception as e:
        db.rollback()
        raise DatabaseException(str(e))
