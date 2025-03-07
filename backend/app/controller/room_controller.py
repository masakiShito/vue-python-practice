from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..service.room_service import get_rooms, create_room, update_room, delete_room
from ..schemas.room import RoomCreate, RoomUpdate, RoomResponse
from typing import List
from ..exceptions import RoomNotFoundException, DatabaseException, RoomAlreadyExistsException

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)

# DBセッションの依存関係を作成
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 会議室一覧を取得
@router.get("/", response_model=List[RoomResponse])
def read_rooms(db: Session = Depends(get_db)):
    try:
        return get_rooms(db)
    except RoomNotFoundException as e:
        raise e
    except DatabaseException as e:
        raise e
    except Exception as e:
        raise DatabaseException(str(e))

# 会議室を登録
@router.post("/", response_model=RoomResponse, status_code=201)
def create_new_room(room_data: RoomCreate, db: Session = Depends(get_db)):
    try:
        return create_room(db, room_data)
    except RoomAlreadyExistsException as e:
        raise e
    except DatabaseException as e:
        raise e
    except Exception as e:
        raise DatabaseException(str(e))

# 会議室を更新
@router.put("/{room_id}", response_model=RoomResponse)
def update_existing_room(room_id: int, room_data: RoomUpdate, db: Session = Depends(get_db)):
    try:
        return update_room(db, room_id, room_data)
    except RoomNotFoundException as e:
        raise e
    except RoomAlreadyExistsException as e:
        raise e
    except DatabaseException as e:
        raise e
    except Exception as e:
        raise DatabaseException(str(e))

# 会議室を削除（論理削除）
@router.delete("/{room_id}", status_code=204)
def delete_existing_room(room_id: int, db: Session = Depends(get_db)):
    try:
        delete_room(db, room_id)
    except RoomNotFoundException as e:
        raise e
    except DatabaseException as e:
        raise e
    except Exception as e:
        raise DatabaseException(str(e))
