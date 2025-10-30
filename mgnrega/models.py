from django.db import models

class District(models.Model):
    state_code = models.CharField(max_length=10)
    state_name = models.CharField(max_length=100)
    district_code = models.CharField(max_length=10)
    district_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.district_name}, {self.state_name}"

class MGNREGAData(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    fin_year = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    
    # Employment data
    approved_labour_budget = models.BigIntegerField(null=True, blank=True)
    average_wage_rate = models.FloatField(null=True, blank=True)
    average_days_employment = models.IntegerField(null=True, blank=True)
    differently_abled_persons_worked = models.IntegerField(null=True, blank=True)
    material_and_skilled_wages = models.FloatField(null=True, blank=True)
    number_of_completed_works = models.IntegerField(null=True, blank=True)
    number_of_gps_with_nil_exp = models.IntegerField(null=True, blank=True)
    number_of_ongoing_works = models.IntegerField(null=True, blank=True)
    persondays_central_liability = models.BigIntegerField(null=True, blank=True)
    
    # Social category data
    sc_persondays = models.BigIntegerField(null=True, blank=True)
    sc_workers_against_active_workers = models.IntegerField(null=True, blank=True)
    st_persondays = models.BigIntegerField(null=True, blank=True)
    st_workers_against_active_workers = models.IntegerField(null=True, blank=True)
    
    # Expenditure data
    total_adm_expenditure = models.FloatField(null=True, blank=True)
    total_exp = models.FloatField(null=True, blank=True)
    wages = models.FloatField(null=True, blank=True)
    
    # Household and worker data
    total_households_worked = models.IntegerField(null=True, blank=True)
    total_individuals_worked = models.IntegerField(null=True, blank=True)
    total_active_job_cards = models.IntegerField(null=True, blank=True)
    total_active_workers = models.IntegerField(null=True, blank=True)
    total_hhs_completed_100_days = models.IntegerField(null=True, blank=True)
    total_jobcards_issued = models.IntegerField(null=True, blank=True)
    total_workers = models.IntegerField(null=True, blank=True)
    total_works_takenup = models.IntegerField(null=True, blank=True)
    
    # Women data
    women_persondays = models.BigIntegerField(null=True, blank=True)
    
    # Percentage data
    percent_category_b_works = models.IntegerField(null=True, blank=True)
    percent_expenditure_agriculture = models.FloatField(null=True, blank=True)
    percent_nrm_expenditure = models.FloatField(null=True, blank=True)
    percentage_payments_within_15_days = models.FloatField(null=True, blank=True)
    
    # Remarks
    remarks = models.TextField(blank=True)
    
    # Timestamp for when data was fetched
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"MGNREGA Data for {self.month} {self.fin_year}"