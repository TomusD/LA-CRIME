from django.db import models
from django.contrib.auth.models import AbstractUser

class Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['area_name']),
        ]

    def __str__(self):
        return f"{self.area_id} - {self.area_name}"
    
class ReportDistrict(models.Model):
    report_dist_id = models.AutoField(primary_key=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    rpt_dist_no = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['rpt_dist_no']),
        ]
    
    def __str__(self):
        return f"{self.area} - {self.rpt_dist_no}"

class Weapon(models.Model):
    weapon_used_cd = models.IntegerField(primary_key=True, default=0)
    weapon_desc = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['weapon_desc']),
        ]

    def __str__(self):
        return self.weapon_desc or 'No Weapon'

class Status(models.Model):
    status_cd = models.CharField(max_length=2, primary_key=True)
    status_desc = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.status_cd} - {self.status_desc}"

class Premises(models.Model):
    premis_cd = models.IntegerField(primary_key=True)
    premis_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.premis_desc

class CrimeCode(models.Model):
    crm_cd = models.IntegerField(primary_key=True)
    crm_cd_desc = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['crm_cd_desc']),
        ]

    def __str__(self):
        return self.crm_cd_desc

class Victim(models.Model):
    victim_id = models.AutoField(primary_key=True)
    vict_age = models.IntegerField(null=True)
    vict_sex = models.CharField(max_length=5, null=True)
    vict_descent = models.CharField(max_length=5, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['vict_age']),
        ]

    def __str__(self):
        return f"{self.vict_age} - {self.vict_sex} - {self.vict_descent}"

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    cross_street = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    lon = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['lat', 'lon']),
        ]

    def __str__(self):
        return f"{self.street_address} - {self.cross_street} - {self.lat} - {self.lon}"

class ModusOperandi(models.Model):
    mo_code_id = models.AutoField(primary_key=True)
    mocodes = models.TextField()

    def __str__(self):
        return self.mocodes

class CrimeReport(models.Model):
    dr_no_id = models.IntegerField(primary_key=True)
    area = models.ForeignKey('Area', on_delete=models.CASCADE)
    victim = models.ForeignKey('Victim', on_delete=models.CASCADE)
    weapon = models.ForeignKey('Weapon', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    premise = models.ForeignKey('Premises', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    report_dist = models.ForeignKey('ReportDistrict', on_delete=models.CASCADE)
    mo_code = models.ForeignKey('ModusOperandi', on_delete=models.CASCADE)

    def __str__(self):
        return self.dr_no


class CrimeReportCode(models.Model):
    dr_no = models.OneToOneField(CrimeReport, on_delete=models.CASCADE, primary_key=True)
    crm_cd_1 = models.ForeignKey(
        CrimeCode, on_delete=models.CASCADE, related_name='primary_codes'
    )
    crm_cd_2 = models.ForeignKey(
        CrimeCode, on_delete=models.CASCADE, null=True, blank=True, related_name='secondary_codes'
    )
    crm_cd_3 = models.ForeignKey(
        CrimeCode, on_delete=models.CASCADE, null=True, blank=True, related_name='tertiary_codes'
    )
    crm_cd_4 = models.ForeignKey(
        CrimeCode, on_delete=models.CASCADE, null=True, blank=True, related_name='quaternary_codes'
    )

    def __str__(self):
        codes = [self.crm_cd_1.crm_cd]
        if self.crm_cd_2:
            codes.append(self.crm_cd_2.crm_cd)
        if self.crm_cd_3:
            codes.append(self.crm_cd_3.crm_cd)
        if self.crm_cd_4:
            codes.append(self.crm_cd_4.crm_cd)
        return f"{self.crime_report} - Codes: {', '.join(codes)}"

class CrimeDate(models.Model):
    dr_no = models.OneToOneField(CrimeReport, on_delete=models.CASCADE, primary_key=True)
    date_rptd = models.DateField()
    date_occ = models.DateField()
    time_occ = models.TimeField()

    def get_date_rptd_formatted(self):
        return self.date_rptd.strftime('%m/%d/%Y')

    def get_date_occ_formatted(self):
        return self.date_occ.strftime('%m/%d/%Y')

    class Meta:
        indexes = [
            models.Index(fields=['date_rptd']),
            models.Index(fields=['date_occ']),
            models.Index(fields=['time_occ']),
        ]

class AuthUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True) 
    
    def __str__(self):
        return self.username