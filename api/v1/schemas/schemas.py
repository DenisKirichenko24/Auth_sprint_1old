from flasgger import Schema, SwaggerView, fields


class SignUp(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()


class Login(Schema):
    email = fields.Str()
    password = fields.Str()


class RefreshToken(Schema):
    refresh_token = fields.Str()


class ChangePassword(Schema):
    old_password = fields.Str()
    new_password = fields.Str()
    email = fields.Str()
    access_token = fields.Str()


class ChangeData(Schema):
    new_username = fields.Str()
    new_email = fields.Str()
    access_token = fields.Str()


class SignUpView(SwaggerView):
    tags = ['SignUp']
    parameters = [
        {
            'name': 'username',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'email',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'password',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'User sign up',
            'schema': SignUp
        }
    }


class LoginView(SwaggerView):
    tags = ['Login']
    parameters = [
        {
            'name': 'email',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'password',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'User login',
            'schema': Login
        }
    }


class RefreshView(SwaggerView):
    tags = ['Refresh token']
    parameters = [
        {
            'name': 'refresh_token',
            'in': 'headers',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Refresh tokens',
            'schema': RefreshToken
        }
    }


class ChangePasswordView(SwaggerView):
    tags = ['Password change']
    parameters = [
        {
            'name': 'old_password',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'new_password',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'email',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'access_token',
            'in': 'headers',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Password change',
            'schema': ChangePassword
        }
    }


class ChangeDataView(SwaggerView):
    tags = ['Personal data change']
    parameters = [
        {
            'name': 'new_username',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'new_email',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'access_token',
            'in': 'headers',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Personal data change',
            'schema': ChangeData
        }
    }
