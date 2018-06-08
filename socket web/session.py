session = {}


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, None)
    # username = request.cookies.get('user', '【游客】')
    return username
