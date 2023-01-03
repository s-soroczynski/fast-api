
from app.users import models
from app.tests.helpers import override_get_db, test_user


def fill_db_with_necessary_data():
    db = override_get_db().__next__()
    # cleanup base before adding user
    db.query(models.User).delete()
    db.add(test_user)
    db.commit()

fill_db_with_necessary_data()