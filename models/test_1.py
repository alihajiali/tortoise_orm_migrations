from tortoise import fields
import tortoise.models
    
class Event1(tortoise.models.Model):
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        app = 'app_test_1'