from core.database.models import User, Token, Post

from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar, Tuple, Dict

from utils.helper import ValidationException, generate_username
from core.schemas.model_schema import user_schema, users_schema, post_schema, posts_schema
from app.authentication import signJWT, decodeJWT
from core.database.connection import session

import passlib.hash as _hash

ID    = TypeVar("ID", "int", "str")

class UserToken:
    """
    user token.
    """

    def __init__(self, model: Type[List]):
        self.model = model

    def get(self, tbl: Session, email: str):
        """
        Get specific token using query.
        """
        query = tbl.query(self.model).filter(self.model.email == email).one_or_none()
        
        if query is None:
            return None

        return {'access_token': query.token}
    
    def create(self, token: str, id: str, email: str, tbl: Session):
        
        token_obj = self.model(email=email, 
                              user_id=id, 
                              token=token
                            )

        tbl.add(token_obj)
        tbl.commit()
        tbl.refresh(token_obj)
    
    def delete(self, token: str, tbl: Session) -> bool:
        """Delete a token."""
        token_query = tbl.query(self.model).filter(self.model.token == token)
        token_obj = token_query.one_or_none()
        
        if token_obj is None:
            return False
        
        token_query.delete(synchronize_session=False)
        tbl.commit()
        return True

class UserCRUD:
    """
    CRUD Operation for user.
    """

    def __init__(self, model):
        self.model = model
        
    def get_multiple(self, tbl: Session, limit:int = 100, offset: int = 0) -> List:
        """
        Get multiple users using a query limiting flag.
        """
        query = tbl.query(self.model).all()[offset:offset+limit]
        if not query:
            raise ValidationException([], 400, 'There are no users.')
        return users_schema.dump(query)

    def get(self, tbl: Session, id: ID) -> Optional[Dict]:
        """
        Get specific user using query.
        """
        query = tbl.query(self.model).filter(self.model.id == id).one_or_none()
        
        if query is None:
            raise ValidationException({}, 400, 'User Not Found!')
        
        return user_schema.dump(query)

    def create(self, tbl: Session, user: dict, ip_address: str, user_agent: str) -> Dict:
        """
        Create a user.
        """

        user_query = tbl.query(self.model).filter(self.model.email == user['email'])
        user_obj = user_query.first()

        if user_obj:
            raise ValidationException({}, 400, f'User already exists!')
        
        user_obj = self.model(email=user['email'], 
                              password=_hash.bcrypt.hash(user['password']), 
                              username=generate_username(user['name']), 
                              name=user['name'],
                              ip_address=ip_address,
                              user_agent=user_agent
                            )

        tbl.add(user_obj)
        tbl.commit()
        tbl.refresh(user_obj)
        return user_schema.dump(user_obj)
        
    def update(self, user: dict, id: ID, tbl: Session, media: any) -> Dict:
        """
        Update a user.
        """
        user_query = tbl.query(self.model).filter(self.model.id == id)
        user_obj = user_query.one_or_none()

        if user_obj is None:
            raise ValidationException({}, 400, f'No User with this id: {id} found')

        password = user['password']
        del user['password']
        
        user['password'] =  _hash.bcrypt.hash(password)
        
        user_query.filter(self.model.id == id).update(user,
                                                        synchronize_session=False)
        tbl.commit()
        tbl.refresh(user_obj)
        return user_schema.dump(user_obj)
    
    def delete(self, id: ID, tbl: Session) -> Dict:
        """Delete a user."""
        user_query = tbl.query(self.model).filter(self.model.id == id)
        user_obj = user_query.one_or_none()
        
        if user_obj is None:
            raise ValidationException({}, 400, f'No User with this id: {id} found')
        
        session.query(Token).filter_by(email=user_obj.email).delete()
        
        user_query.delete(synchronize_session=False)
        tbl.commit()
        return {}
    
    def change_password(self, user: dict, id: ID, tbl: Session) -> Dict:
        """
        Update a user password.
        """
        user_query = tbl.query(self.model).filter(self.model.id == id)
        user_obj = user_query.one_or_none()

        if user_obj is None:
            raise ValidationException({}, 400, f'No User with this id: {id} found')
        
        user_query.filter(self.model.id == id).update({"password": _hash.bcrypt.hash(user['password'])},
                                                        synchronize_session=False)
        tbl.commit()
        tbl.refresh(user_obj)
        return user_schema.dump(user_obj)
    
class UserAuthentication:
    """
    user authentication process.
    """

    def __init__(self, model):
        self.model = model

    def check_user(self, user: dict, tbl: Session) -> Tuple[bool, str]:
        user_obj = tbl.query(self.model).filter_by(email=user['email']).first()

        exists = user_obj is not None and user_obj.verify_password(user['password'])

        if exists:
            return (True, user_obj.id)
        return (False, None)
        
    def login(self, user: dict, tbl: Session):

        is_valid_user, id = self.check_user(user, tbl)

        if not is_valid_user:
            raise ValidationException({}, 400, "Wrong login details!")

        check_token = UserToken(Token).get(tbl, user['email'])

        # check if token is not expired and user is already has token or check token exists for new user
        if check_token is not None:

            # check if token is expired or not
            try:
                payload = decodeJWT(check_token['access_token'])
            except:
                payload = None

            # if token is expired then delete token object
            if payload is None:
                UserToken(Token).delete(check_token['access_token'], tbl)
            else:
                return check_token
        
        res = signJWT(str(id), user['email'])

        # create user token
        UserToken(Token).create(res['access_token'], id, user['email'], tbl)
        return res

    def logout(self, user_: str, tbl: Session) -> Optional[Dict]:
        token_obj = UserToken(Token).delete(user_.email, tbl)

        if token_obj:
            return {}
        else:
            raise ValidationException({}, 400, "Already Logout!")
        
class PostCRUD:
    """
    CRUD Operation for post.
    """

    def __init__(self, model):
        self.model = model

    def get_multiple(self, tbl: Session, limit:int = 100, offset: int = 0) -> List:
        """
        Get multiple posts using a query limiting flag.
        """
        query = tbl.query(self.model).all()[offset:offset+limit]
        if not query:
            raise ValidationException([], 400, 'There are no posts.')
        return posts_schema.dump(query)

    def get(self, tbl: Session, id: ID) -> Optional[Dict]:
        """
        Get specific post using query.
        """
        query = tbl.query(self.model).filter(self.model.id == id).one_or_none()
        
        if query is None:
            raise ValidationException({}, 400, 'Post Not Found!')
        
        return post_schema.dump(query)

    def create(self, tbl: Session, post: dict, user: str, ip_address: str, user_agent: str) -> Dict:
        """
        Create a post.
        """

        post_query = tbl.query(self.model).filter(self.model.post_name == post['post_name'])
        exists = post_query.one_or_none()

        if exists is not None:
            raise ValidationException({}, 400, f'Post with this name already exists!')
        
        post_obj = self.model(post_name=post['post_name'], 
                              post_text=post['post_text'], 
                              ip_address=ip_address, 
                              user_agent=user_agent, 
                              user_id=user
                              )

        tbl.add(post_obj)
        tbl.commit()
        tbl.refresh(post_obj)
        return post_schema.dump(post_obj)
    
    def update(self, post: dict, id: ID, tbl: Session, ip_address: str, user_agent: str, user: str) -> Post:
        """
        Update a post.
        """
        post_query = tbl.query(self.model).filter(self.model.id == id)
        post_obj = post_query.one_or_none()

        if post_obj is None:
            raise ValidationException({}, 400, f'No post with this id: {id} found')
        
        post['user_id'] = user
        post['ip_address'] = ip_address
        post['user_agent'] = user_agent
        
        post_query.filter(self.model.id == id).update(post,
                                                        synchronize_session=False)
        tbl.commit()
        tbl.refresh(post_obj)
        return post_schema.dump(post_obj)
        
    
user                = UserCRUD(User) 
authenticate        = UserAuthentication(User) 
post                = PostCRUD(Post) 