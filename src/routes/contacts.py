from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/tags', tags=["tags"])

# Отримати список всіх контактів
@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_tags(skip, limit, db)
    return contacts


# Отримати один контакт за ідентифікатором
@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The contact is not found")
    return contact


# Створити новий контакт
@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


# Оновити існуючий контакт
@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The contact is not found")
    return contact


# Видалити контакт
@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The contact is not found")
    return contact


# Пошук за іменем, прізвищем чи адресою електронної пошти
@router.get("/{query_field}/{query_value}", response_model=List[ContactResponse])
async def query_search(query_field: str = '', query_value: str = '', db: Session = Depends(get_db)):
    contacts = await repository_contacts.querys_contacts(query_field, query_value, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts are not found")
    return contacts


# Отримати список контактів з днями народження на найближчі 7 днів
@router.get("/birthdays/", response_model=List[ContactResponse])
async def birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.birthdays(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts are not found")
    return contacts