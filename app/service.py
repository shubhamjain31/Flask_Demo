from core.database.models import User

from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar, Tuple

ID    = TypeVar("ID", "int", "str")

class UserCRUD:
    """
    CRUD Operation for user.
    """

    def __init__(self, model):
        self.model = model
        
    def get_multiple(self, db: Session, limit:int = 100, offset: int = 0) -> List[User]:
        """
        Get multiple users using a query limiting flag.
        """
        query = db.query(self.model).all()[offset:offset+limit]
        # if not query:
        #     raise ValidationException([], status.HTTP_400_BAD_REQUEST, 'There are no users.')
        # return parse_obj_as(List[User], query)
        return list(query)

    def get(self, db: Session, id: ID) -> Optional[User]:
        """
        Get specific user using query.
        """
        query = db.query(self.model).filter(self.model.id == id).one_or_none()
        
        # if query is None:
        #     raise ValidationException({}, status.HTTP_404_NOT_FOUND, 'User Not Found!')
        
        return query

    # def create(self, user: UserCreate, db: Session) -> User:
    #     """
    #     Create a user.
    #     """

    #     user_query = db.query(self.model).filter(self.model.email == user['email'])
    #     user_obj = user_query.first()

    #     if user_obj:
    #         raise ValidationException({}, status.HTTP_404_NOT_FOUND, f'User already exists!')
        
    #     user_obj = self.model(email=user['email'], 
    #                           password=_hash.bcrypt.hash(user['password']), 
    #                           username=generate_username(user['name']), 
    #                           name=user['name'],
    #                           ip_address=user['ip_address'],
    #                           user_agent=user['user_agent']
    #                         )

    #     db.add(user_obj)
    #     db.commit()
    #     db.refresh(user_obj)
    #     return user_obj
        
    # def update(self, user: UserUpdate, id: ID, db: Session) -> User:
    #     """
    #     Update a user.
    #     """
    #     user_query = db.query(self.model).filter(self.model.id == id)
    #     user_obj = user_query.one_or_none()

    #     if user_obj is None:
    #         raise ValidationException({}, status.HTTP_404_NOT_FOUND, f'No User with this id: {id} found')
        
    #     update_data = user.dict(exclude_unset=True)

    #     password = update_data['password']
    #     del update_data['password']
        
    #     update_data['password'] =  _hash.bcrypt.hash(password)
        
    #     user_query.filter(self.model.id == id).update(update_data,
    #                                                     synchronize_session=False)
    #     db.commit()
    #     db.refresh(user_obj)
    #     return user_obj
    
    # def delete(self, id: ID, db: Session) -> User:
    #     """Delete a user."""
    #     user_query = db.query(self.model).filter(self.model.id == id)
    #     user_obj = user_query.one_or_none()
        
    #     if user_obj is None:
    #         raise ValidationException({}, status.HTTP_404_NOT_FOUND, f'No User with this id: {id} found')
        
    #     user_query.delete(synchronize_session=False)
    #     db.commit()
    #     return {}
    
user                = UserCRUD(User) 