
from app.public_toilets.models import PublicToilet
from app.users.models import User
from app.tests.helpers import override_get_db

test_user = User(email="test_email_public_toilet", password="test_password_public_toilet")
test_public_toilet = PublicToilet(name="test_name", description="test_description", lng=10, lat=10, rate=1, user=test_user)


def fill_db_with_necessary_dataa():
    db = override_get_db().__next__()
    # cleanup base before adding toilet
    db.query(PublicToilet).delete()
    db.add(test_public_toilet)
    db.commit()

fill_db_with_necessary_dataa()