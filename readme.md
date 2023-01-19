
- Using Python/Django + mySqlite3 
- short demonstration video link: https://youtu.be/Icv1oRV-NJM
- Assupmtions: 
  1. Each user account has a unique name in one company
## Authorization Idea:
  User can login with username and password. Website can check if the user's username and password are correct. If the user's username and password are correct via comparing the data in the database, the user can access the website.
  Then Django will set cookie and session for the user. The cookie will be used to identify the user. The session will be used to store the user's information. The user can access the website with the cookie and session. So, we can know who are the current user, and what permission the user has.
  (Based on the entity's attribute - 'User-Type', we display different front-end pages for different users.)
    Reference the idea of Attribute-Based Access Control (ABAC) and Role-Based Access Control (RBAC)



## Database Design:
    class UserInfo(models.Model):
        name = models.CharField(max_length=64)
        address = models.CharField(max_length=64, default="")
        gender = models.SmallIntegerField(choices=((1, "Male"), (2, "Female")), verbose_name="Gender", default=None)
        email = models.CharField(max_length=64)
        password = models.CharField(max_length=64)
        user_type = models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2)
        company = models.ForeignKey(to="Company", to_field="id", on_delete=models.CASCADE, default=None)
        # union primary key for challenge2 (two companies now)
        class Meta:
            unique_together = [
                ("name", "company"),
            ]
    
    
        def __str__(self):
            return self.name

[//]: # ()

    class Company(models.Model):
        name = models.CharField(max_length=64)

        def __str__(self):
            return self.name

[//]: # (# We assume each person has only one credit card from each company)
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