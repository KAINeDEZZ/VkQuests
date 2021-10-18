from tortoise import fields, Model


class User(Model):
    stage = fields.IntField(default=0)
    stage_end: fields.ForeignKeyRelation['StageEnd']


class StageEnd(Model):
    stage = fields.IntField()
    time = fields.DatetimeField(auto_now_add=True)

    user = fields.ForeignKeyField('core.User')
