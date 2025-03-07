from fastapi import HTTPException

class RoomNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="会議室が見つかりません")

class DatabaseException(HTTPException):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"データベースエラー: {error}")

class ValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class RoomAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="この会議室名はすでに登録されています")
