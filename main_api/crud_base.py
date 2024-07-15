import traceback
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_crudrouter.core.sqlalchemy import Session
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
# from sqlalchemy.orm import Session
from sqlmodel import select

from main_api.db.db import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_several(self, db: Session, ids: list[int]) -> List[ModelType]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

    def get_or_raise_404(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = self.get(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, commit=True) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        try:
            if commit:
                db.commit()
            else:
                db.flush()
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=repr(e))
        db.refresh(db_obj)
        return db_obj

    def get_or_create(
        self,
        db: Session,
        defaults: dict | None = None,
        commit: bool = True,
        **kwargs
    ) -> tuple[ModelType, bool]:
        db_obj = db.exec(select(self.model).filter_by(**kwargs)).one_or_none()
        if db_obj:
            return db_obj, False
        kwargs |= defaults or {}
        instance = self.model(**kwargs)
        db.add(instance)
        db_action = db.commit if commit else db.flush
        try:
            db_action()
            return instance, True
        except Exception as e:
            traceback.print_exception(e)
            db.rollback()
            instance = db.exec(select(self.model).filter_by(**kwargs)).one()
            return instance, False

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_or_update(
        self,
        db: Session,
        defaults: dict | None = None,
        commit: bool = True,
        **kwargs
    ) -> tuple[ModelType, bool]:
        created = True
        try:
            db_obj = db.exec(select(self.model).filter_by(**kwargs)).one_or_none()
        except MultipleResultsFound as exc:
            raise exc

        if db_obj:
            for key in defaults.keys():
                setattr(db_obj, key, defaults[key])
            created = False
        else:
            kwargs |= defaults or {}
            db_obj = self.model(**kwargs)
        db.add(db_obj)
        db_action = db.commit if commit else db.flush
        try:
            db_action()
            return db_obj, created
        except Exception as e:
            traceback.print_exception(e)
            db.rollback()
            instance = db.exec(select(self.model).filter_by(**kwargs)).one()
            return instance, False

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_or_404(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail='Not found')
        db.delete(obj)
        db.commit()
        return obj