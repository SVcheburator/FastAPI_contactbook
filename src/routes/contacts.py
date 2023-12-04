from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts')


@router.get("/", response_model=List[ContactResponse], 
            description='No more than 15 requests per minute',
            )
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a list of contacts for a current user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: A list of contacts.
    :rtype: List[ContactResponse]
    """ 
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, 
            description='No more than 15 requests per minute',
            )
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a single contact with the specified ID for a current user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contact for.
    :type current_user: User
    :return: The contact with the specified ID.
    :rtype: ContactResponse
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search/{search_key}", response_model=List[ContactResponse])
async def search_contacts(search_key: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a list of contacts found for a current user by a key.

    :param search_key: A key to search contacts by.
    :type search_key: str
    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: A list of contacts.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.search_contacts(search_key, current_user, db)
    return contacts


@router.post("/", response_model=ContactResponse, 
            status_code=status.HTTP_201_CREATED, 
            description='No more than 10 requests per minute',
            )
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Creates a new contact for a current user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param db: The database session.
    :type db: Session
    :param current_user: The user to create the contact for.
    :type current_user: User
    :return: The newly created contact.
    :rtype: ContactResponse
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, 
            description='No more than 10 requests per minute',
            )
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Updates a single contact with the specified ID for a current user.

    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to update the contact for.
    :type current_user: User
    :return: The updated contact, or None if it does not exist.
    :rtype: ContactResponse
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Removes a single contact with the specified ID for a current user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The user to remove the contact for.
    :type current_user: User
    :return: The removed contact, or None if it does not exist.
    :rtype: ContactResponse
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/week_birthdays/", response_model=List[ContactResponse])
async def get_week_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Gets a list of contacts with birthdays within the next week.

    :param db: The database session.
    :type db: Session
    :param current_user: The user to retrieve contacts for.
    :type current_user: User
    :return: A list of contacts.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_week_birthdays(current_user, db)
    return contacts