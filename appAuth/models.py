from django.db import models


# Create your models here.
#
# class UserTypes(models.Model):
#     title = models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2)
#
#     def __str__(self):
#         return self.title

class UserInfo(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64, default="")
    gender = models.SmallIntegerField(choices=((1, "Male"), (2, "Female")), verbose_name="Gender", default=None)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    user_type = models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2)
    company = models.ForeignKey(to="Company", to_field="id", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# We assume each person has only one credit card from each company
class Credit_card(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    credit_card_num = models.CharField(max_length=16, primary_key=True)
    host = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    expire_date = models.DateField()
    masked_num = models.CharField(max_length=3)
    limit = models.IntegerField()
    curr_balance = models.DecimalField(max_digits=7, decimal_places=2, default=50000)

    def __str__(self):
        return self.credit_card_num
