from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Deal(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=50)
    fmv = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class DealProject(models.Model):
    deal = models.ForeignKey('Deal', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    tax_credit_transfer_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return f"{self.deal.name} - {self.project.name}"

    def calculate_tax_credit_transfer_amount(self):
        total_amount = 0
        for deal_project in self.dealproject_set.all():
            total_amount += deal_project.project.fmv * 0.3 * deal_project.tax_credit_transfer_rate
        return total_amount
