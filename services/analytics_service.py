from database.models import Click

def save_click(session_local, short_code, ip, user_agent):
    db = session_local()
    try:
        click = Click(short_code = short_code, ip_address=ip, user_agent=user_agent)
        db.add(click)
        db.commit()
    finally:
        db.close()