from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request
from api.core.database import engine
from api.models import CustomerUser, RentalBusinessRegisterAccountInvite
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.responses import RedirectResponse
from api.services.auth_service import create_jwt_token, decrypt_jwt_token
from api.utils.enums import UserType


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == "admin" and password == "admin124":
            sqladmin_token = create_jwt_token(
                user_id=-1, user_type=UserType.SQLADMIN_USER
            )
            request.session.update({"admin_pannel_token": sqladmin_token})
            return True
        else:
            return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        sqladmin_token = request.session.get("admin_pannel_token")

        if (
            not sqladmin_token
            or datetime.now() > decrypt_jwt_token(sqladmin_token).expires_date
        ):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


def add_sql_admin_panel(app: FastAPI):
    authentication_backend = AdminAuth(secret_key="mysecretkey")
    admin = Admin(app, engine, authentication_backend=authentication_backend)

    class UserAdmin(ModelView, model=CustomerUser):
        column_list = [
            CustomerUser.private_id,
            CustomerUser.username,
            CustomerUser.password_encrypted,
        ]

    class AnotherView(ModelView, model=RentalBusinessRegisterAccountInvite):
        column_list = [
            RentalBusinessRegisterAccountInvite.private_id,
            RentalBusinessRegisterAccountInvite.token,
            RentalBusinessRegisterAccountInvite.email,
            RentalBusinessRegisterAccountInvite.used_by,
        ]

    admin.add_view(UserAdmin)
    admin.add_view(AnotherView)
