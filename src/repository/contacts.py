from datetime import datetime
from typing import List
from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(name=body.name)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def query_search(query_field: str, query_value: str, db: Session):
    valid_fields = ['first_name', 'last_name', 'email']
    if query_field not in valid_fields:
        raise HTTPException(status_code=404, detail=f"Invalid query field. Valid fields: {valid_fields}")
    
    contacts = db.query(Contact).filter(getattr(Contact, query_field).ilike(f"%{query_value}%")).all()
    return {"contacts": contacts}


async def birthdays(db: Session) -> List[Contact]:
    contacts = db.query(Contact).all()
    result = []
    today = datetime.now()
      
    for contact in contacts:
        b_day = datetime(year=datetime.now().year, month=contact.birthday.month, day=contact.birthday.day)
        if b_day < today:
            b_day = b_day.replace(year=datetime.now().year+1)

        time_to_birthday = abs(b_day - today)

        if time_to_birthday.days < 8:
            result.append(contact)

    return result


