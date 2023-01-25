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


from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))




""" Login  """
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        user_id  = request.form['user_email'] # we can have here username OR email
        password = request.form['user_password']

        # Locate user
        user = Users.find_by_username(user_id)

        # if user not found
        if not user:

            user = Users.find_by_email(user_id)

            if not user:
                return render_template( 'accounts/login.html',
                                        msg='Unknown User or Email',
                                        form=login_form)

        # Check the password
        if verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))



""" Register """
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        user_phone_number = request.form['user_phone_number']
        user_email = request.form['user_email']

        # Check usename exists
        user = Users.query.filter_by(user_phone_number=user_phone_number).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Phone Number Already Registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(user_email=user_email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email Already Registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
