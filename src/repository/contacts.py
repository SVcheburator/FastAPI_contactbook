from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate

from datetime import datetime, timedelta


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def search_contacts(key , db: Session) -> List[Contact]:
    contacts = db.query(Contact).all()

    matching_contacts = []
    for contact in contacts:
        if contact.name == key or contact.surname == key or contact.email == key:
            matching_contacts.append(contact)
            
    return matching_contacts


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.favourite = body.favourite
        db.commit()
    return contact


async def get_week_birthdays(db: Session) -> List[Contact]:
    contacts = db.query(Contact).all()

    matching_contacts = []
    for contact in contacts:    
        bd = datetime(year=datetime.now().year, month=contact.birthday.month, day=contact.birthday.day)

        delta = bd - datetime.now()
        week_delta = timedelta(days=7)

        if timedelta(days=0) <= delta <= week_delta:
            matching_contacts.append(contact)

    return matching_contacts