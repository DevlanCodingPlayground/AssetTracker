#
#   Crafted On Wed Jan 25 2023
#
# 
#   www.devlan.co.ke
#   hello@devlan.co.ke
#
#
#   The Devlan Solutions LTD End User License Agreement
#   Copyright (c) 2022 Devlan Solutions LTD
#
#
#   1. GRANT OF LICENSE 
#   Devlan Solutions LTD hereby grants to you (an individual) the revocable, personal, non-exclusive, and nontransferable right to
#   install and activate this system on two separated computers solely for your personal and non-commercial use,
#   unless you have purchased a commercial license from Devlan Solutions LTD. Sharing this Software with other individuals, 
#   or allowing other individuals to view the contents of this Software, is in violation of this license.
#   You may not make the Software available on a network, or in any way provide the Software to multiple users
#   unless you have first purchased at least a multi-user license from Devlan Solutions LTD.
#
#   2. COPYRIGHT 
#   The Software is owned by Devlan Solutions LTD and protected by copyright law and international copyright treaties. 
#   You may not remove or conceal any proprietary notices, labels or marks from the Software.
#
#
#   3. RESTRICTIONS ON USE
#   You may not, and you may not permit others to
#   (a) reverse engineer, decompile, decode, decrypt, disassemble, or in any way derive source code from, the Software;
#   (b) modify, distribute, or create derivative works of the Software;
#   (c) copy (other than one back-up copy), distribute, publicly display, transmit, sell, rent, lease or 
#   otherwise exploit the Software. 
#
#
#   4. TERM
#   This License is effective until terminated. 
#   You may terminate it at any time by destroying the Software, together with all copies thereof.
#   This License will also terminate if you fail to comply with any term or condition of this Agreement.
#   Upon such termination, you agree to destroy the Software, together with all copies thereof.
#
#
#   5. NO OTHER WARRANTIES. 
#   DEVLAN SOLUTIONS LTD  DOES NOT WARRANT THAT THE SOFTWARE IS ERROR FREE. 
#   DEVLAN SOLUTIONS LTD SOFTWARE DISCLAIMS ALL OTHER WARRANTIES WITH RESPECT TO THE SOFTWARE, 
#   EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY, 
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. 
#   SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF IMPLIED WARRANTIES OR LIMITATIONS
#   ON HOW LONG AN IMPLIED WARRANTY MAY LAST, OR THE EXCLUSION OR LIMITATION OF 
#   INCIDENTAL OR CONSEQUENTIAL DAMAGES,
#   SO THE ABOVE LIMITATIONS OR EXCLUSIONS MAY NOT APPLY TO YOU. 
#   THIS WARRANTY GIVES YOU SPECIFIC LEGAL RIGHTS AND YOU MAY ALSO 
#   HAVE OTHER RIGHTS WHICH VARY FROM JURISDICTION TO JURISDICTION.
#
#
#   6. SEVERABILITY
#   In the event of invalidity of any provision of this license, the parties agree that such invalidity shall not
#   affect the validity of the remaining portions of this license.
#
#
#   7. NO LIABILITY FOR CONSEQUENTIAL DAMAGES IN NO EVENT SHALL DEVLAN SOLUTIONS LTD OR ITS SUPPLIERS BE LIABLE TO YOU FOR ANY
#   CONSEQUENTIAL, SPECIAL, INCIDENTAL OR INDIRECT DAMAGES OF ANY KIND ARISING OUT OF THE DELIVERY, PERFORMANCE OR 
#   USE OF THE SOFTWARE, EVEN IF DEVLAN SOLUTIONS LTD HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES
#   IN NO EVENT WILL DEVLAN SOLUTIONS LTD  LIABILITY FOR ANY CLAIM, WHETHER IN CONTRACT 
#   TORT OR ANY OTHER THEORY OF LIABILITY, EXCEED THE LICENSE FEE PAID BY YOU, IF ANY.
#
#

from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'user'

    user_id            = db.Column(db.Integer, primary_key=True)
    user_fullname = db.Column(db.String(200), unique=False)
    user_phone_number = db.Column(db.String(200), unique=True)
    user_email         = db.Column(db.String(200), unique=True)
    user_password      = db.Column(db.LargeBinary)

    oauth_github  = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    @classmethod
    def find_by_email(cls, user_email: str) -> "Users":
        return cls.query.filter_by(user_email=user_email).first()

    @classmethod
    def find_by_username(cls, user_phone_number: str) -> "Users":
        return cls.query.filter_by(user_phone_number=user_phone_number).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "Users":
        return cls.query.filter_by(id=_id).first()
   
    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
          
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
    
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.filter_by(user_id=user_id).first()

@login_manager.request_loader
def request_loader(request):
    user_email = request.form.get('user_email')
    user = Users.query.filter_by(user_email=user_email).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
