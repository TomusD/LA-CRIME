import pandas as pd
from django.core.management.base import BaseCommand
from crime_app_api.models import (
    Area, ReportDistrict, CrimeReportCode, Weapon, Status, Premises,
    CrimeCode, Victim, Location, ModusOperandi, CrimeReport, CrimeDate
)
from datetime import datetime

filepath = 'F://github/Triantafulloy-Thanasis-Project01-AM7115132300010/Crime_Data_from_2020_to_Present_20241025_clean.csv'

# Read the CSV file
df = pd.read_csv(filepath)

# Convert the 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4' columns to Integers
crime_code_columns = ['Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4']
for column in crime_code_columns:
    if column in df.columns:
        df[column] = df[column].astype('Int64')

class Command(BaseCommand):
    help = 'Import data from CSV file to the database'

    def handle(self, *args, **options):
        self.import_data(filepath)

    # Import data from CSV file to the database
    def import_data(self, filepath):
        df = pd.read_csv(filepath)
        batch_size = 100000
        num_rows = len(df)
        for i in range(0, num_rows, batch_size):
            batch_df = df.iloc[i:i+batch_size]
            self.import_batch(batch_df)

    # Bulk create CrimeReportCode and CrimeDate
    def import_batch(self, batch_df):
        crime_report_codes = []
        crime_dates = []
        for _, row in batch_df.iterrows():
            crime_report_code, crime_date = self.import_row(row.to_dict())
            crime_report_codes.append(crime_report_code)
            crime_dates.append(crime_date)
        CrimeReportCode.objects.bulk_create(crime_report_codes)
        CrimeDate.objects.bulk_create(crime_dates)

    def import_row(self, row):
        # Area
        area, _ = Area.objects.get_or_create(
            area_id=row['AREA'],
            defaults={
                'area_name': row['AREA NAME']
            }
        )

        # ReportDistrict
        report_district, _ = ReportDistrict.objects.get_or_create(
            area=area,
            rpt_dist_no=row['Rpt Dist No']
        )

        # Weapon
        weapon, _ = Weapon.objects.get_or_create(
            weapon_used_cd=row['Weapon Used Cd'],
            weapon_desc=row['Weapon Desc']
        )

        # Status
        status, _ = Status.objects.get_or_create(
            status_cd=row['Status'],
            status_desc=row['Status Desc']
        )

        # Premises
        premises, _ = Premises.objects.get_or_create(
            premis_cd=row['Premis Cd'],
            premis_desc=row['Premis Desc']
        )

        # Victim
        victim, _ = Victim.objects.get_or_create(
            vict_age=row['Vict Age'],
            vict_sex=row['Vict Sex'],
            vict_descent=row['Vict Descent']
        )

        # Location
        location, _ = Location.objects.get_or_create(
            area=area,
            street_address=row['LOCATION'],
            cross_street=row['Cross Street'],
            lat=row['LAT'],
            lon=row['LON']
        )

        # ModusOperandi
        mo, _ = ModusOperandi.objects.get_or_create(
            mocodes=row['Mocodes']
        )

        # CrimeReport
        crime_report, _ = CrimeReport.objects.get_or_create(
            dr_no_id=row['DR_NO'],
            area=area,
            victim=victim,
            weapon=weapon,
            status=status,
            premise=premises,
            location=location,
            report_dist=report_district,
            mo_code=mo
        )

        # CrimeCode
        primary_crime_code = None
        if pd.notna(row['Crm Cd']):
            primary_crime_code, _ = CrimeCode.objects.get_or_create(
                crm_cd=int(row['Crm Cd']),
                defaults={'crm_cd_desc': row['Crm Cd Desc']}
            )

        # Secondary crime code
        secondary_crime_code = None
        if pd.notna(row.get('Crm Cd 2')):
            secondary_crime_code, _ = CrimeCode.objects.get_or_create(
                crm_cd=int(row['Crm Cd 2'])
            )

        # Tertiary crime code
        tertiary_crime_code = None
        if pd.notna(row.get('Crm Cd 3')):
            tertiary_crime_code, _ = CrimeCode.objects.get_or_create(
                crm_cd=int(row['Crm Cd 3'])
            )

        # Quaternary crime code
        quaternary_crime_code = None
        if pd.notna(row.get('Crm Cd 4')):
            quaternary_crime_code, _ = CrimeCode.objects.get_or_create(
                crm_cd=int(row['Crm Cd 4'])
            )

        # CrimeReportCode entry
        crime_report_code = CrimeReportCode(
            dr_no=crime_report,
            crm_cd_1=primary_crime_code,
            crm_cd_2=secondary_crime_code,
            crm_cd_3=tertiary_crime_code,
            crm_cd_4=quaternary_crime_code
        )

        # Parse dates and times
        date_rptd = None
        if row['Date Rptd']:
            date_rptd = datetime.strptime(row['Date Rptd'], "%m/%d/%Y %I:%M:%S %p").date()

        date_occ = None
        if row['DATE OCC']:
            date_occ = datetime.strptime(row['DATE OCC'], "%m/%d/%Y %I:%M:%S %p").date()

        time_occ = None
        time_occ_value = row['TIME OCC']
        if time_occ_value:
            time_occ_str = str(time_occ_value).zfill(4)
            time_occ = datetime.strptime(time_occ_str, "%H%M").time()

        # CrimeDate entry
        crime_date = CrimeDate(
            dr_no=crime_report,
            date_rptd=date_rptd,
            date_occ=date_occ,
            time_occ=time_occ
        )

        return crime_report_code, crime_date