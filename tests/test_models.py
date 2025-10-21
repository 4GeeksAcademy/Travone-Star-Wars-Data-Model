from datetime import datetime
import models
import sys
sys.path.insert(0, 'src')


def test_import_models():
    # basic presence checks
    assert hasattr(models, 'User')
    assert hasattr(models, 'Planet')
    assert hasattr(models, 'Character')
    assert hasattr(models, 'Vehicle')
    assert hasattr(models, 'Favorite')
    assert hasattr(models, 'Comment')


def test_user_serialize():
    u = models.User(id=1, username='luke', email='luke@tatooine')
    s = u.serialize()
    assert s == {"id": 1, "username": "luke", "email": "luke@tatooine"}


def test_comment_serialize():
    dt = datetime(2020, 1, 2, 3, 4, 5)
    c = models.Comment(id=7, content='hello', created_at=dt,
                       user_id=1, character_id=None, planet_id=2)
    s = c.serialize()
    assert s['id'] == 7
    assert s['content'] == 'hello'
    assert s['created_at'] == dt.isoformat()
    assert s['user_id'] == 1
    assert s['planet_id'] == 2


def test_metadata_tables():
    names = set(models.db.metadata.tables.keys())
    expected = {'user', 'planet', 'character', 'vehicle',
                'favorite', 'vehicle_pilot', 'comment'}
    # metadata may include other tables depending on environment; ensure required ones exist
    assert expected.issubset(names)
