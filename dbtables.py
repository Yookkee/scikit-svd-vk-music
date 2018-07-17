import peewee as pw

database = pw.SqliteDatabase('DATABASE')

class BaseModel(pw.Model):
    class Meta:
        database = database

class User(BaseModel):
    user_id = pw.IntegerField(primary_key=True)

class Music(BaseModel):
    post_id = pw.IntegerField(primary_key=True)
    owner_id = pw.IntegerField()
    artist = pw.CharField()
    title = pw.CharField()

class Like(BaseModel):
    user = pw.ForeignKeyField(User)
    music = pw.ForeignKeyField(Music)

def create_tables():
    with database:
        database.create_tables([User, Music, Like])

create_tables()
