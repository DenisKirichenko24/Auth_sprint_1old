class LoginData:
    data = {'login': 'test', 'password': 'test'}


user = LoginData()


def test_login(make_post_request):
    response = make_post_request('/login', params=user.data, headers={'content-type': 'application/json'})
    print(response)
