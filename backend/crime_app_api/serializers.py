from rest_framework import serializers
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from crime_app_api.models import (Area, ReportDistrict, CrimeReportCode, Weapon, Status, Premises, CrimeCode,
                                  Victim, Location, ModusOperandi, CrimeReport, CrimeDate)

# Serializers for the models

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['area_id', 'area_name']

class ReportDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDistrict
        fields = ['report_dist_id', 'area', 'rpt_dist_no']

class CrimeReportCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReportCode
        fields = ['crm_cd_1', 'crm_cd_2', 'crm_cd_3', 'crm_cd_4']

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['weapon_used_cd', 'weapon_desc']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['status_cd', 'status_desc']

class PremisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premises
        fields = ['premis_cd', 'premis_desc']

class CrimeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeCode
        fields = ['crm_cd', 'crm_cd_desc']

class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = ['victim_id', 'vict_age', 'vict_sex', 'vict_descent']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['street_address', 'cross_street', 'lat', 'lon']

class ModusOperandiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModusOperandi
        fields = ['mo_code_id', 'mocodes']

class CrimeDateSerializer(serializers.ModelSerializer):
    dr_no = serializers.PrimaryKeyRelatedField(read_only=True)
    date_rptd = serializers.DateField(read_only=True)

    class Meta:
        model = CrimeDate
        fields = ['dr_no', 'date_rptd','date_occ', 'time_occ']

class CrimeReportSerializer(serializers.ModelSerializer):
    dr_no = serializers.CharField()
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    victim = VictimSerializer()
    weapon = serializers.PrimaryKeyRelatedField(queryset=Weapon.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    premise = serializers.PrimaryKeyRelatedField(queryset=Premises.objects.all())
    location = LocationSerializer()
    rpt_dist_no = serializers.CharField()
    mocodes = serializers.CharField()
    crimereportcode = CrimeReportCodeSerializer()
    crimedate = CrimeDateSerializer()

    class Meta:
        model = CrimeReport
        fields = [
            'dr_no', 'area', 'victim', 'weapon', 'status',
            'premise', 'location', 'rpt_dist_no', 'mocodes', 'crimereportcode', 'crimedate'
        ]

    def create(self, validated_data):

        # Extract 'rpt_dist_no', 'area' and 'mocodes'
        rpt_dist_no = validated_data.pop('rpt_dist_no')
        area = validated_data['area']
        mocodes = validated_data.pop('mocodes')

        # Extract nested data and 'dr_no' 
        dr_no = validated_data.pop('dr_no')
        victim_data = validated_data.pop('victim')
        location_data = validated_data.pop('location')
        crimereportcode_data = validated_data.pop('crimereportcode')
        crimedate_data = validated_data.pop('crimedate')

        # Get or create ReportDistrict
        report_dist, created = ReportDistrict.objects.get_or_create(
            rpt_dist_no=rpt_dist_no,
            area=area
        )


        # Get or create ModusOperandi
        mo_code, created = ModusOperandi.objects.get_or_create(mocodes=mocodes)

        # Get or Create Victim
        victim, created = Victim.objects.get_or_create(**victim_data)

        # Get or Create Location
        location, created = Location.objects.get_or_create(area=area, **location_data)

        # Set date_rptd to current date
        date_rptd=datetime.now().date()

        # Create DR_NO
        dr_no = str(dr_no)
        no_area = str(area).split(" - ")[0]
        years = str(date_rptd)[:4][-2:]
        if len(no_area) == 1:
            dr_no = years + '0' + no_area + dr_no
        if len(no_area) == 2:
            dr_no = years + no_area + dr_no

        # Create CrimeReport
        crime_report = CrimeReport.objects.create(
            dr_no_id=dr_no,
            area=area,
            victim=victim,
            weapon=validated_data['weapon'],
            status=validated_data['status'],
            premise=validated_data['premise'],
            location=location,
            report_dist=report_dist,
            mo_code=mo_code
        )

        # Create CrimeDate
        CrimeDate.objects.create(
            dr_no=crime_report,
            date_rptd=date_rptd,
            date_occ=crimedate_data.get('date_occ'),
            time_occ=crimedate_data.get('time_occ')
        )

        # Create CrimeReportCode
        CrimeReportCode.objects.create(
            dr_no=crime_report,
            **crimereportcode_data
        )

        return crime_report
        
    

class Query1Serializer(serializers.Serializer):
    crime_code = serializers.IntegerField()
    crime_description = serializers.CharField()
    total_reports = serializers.IntegerField()
    
class Query2Serializer(serializers.Serializer):
    date_reported = serializers.DateField()
    total_reports = serializers.IntegerField()

class Query3Serializer(serializers.Serializer):
    area_name = serializers.CharField()
    crime_code = serializers.IntegerField()
    crime_description = serializers.CharField()
    crime_count = serializers.IntegerField()

class Query4Serializer(serializers.Serializer):
    hour = serializers.IntegerField()
    average_crimes_per_hour = serializers.FloatField()

class Query5Serializer(serializers.Serializer):
    crime_code = serializers.IntegerField()
    crime_description = serializers.CharField()
    crime_count = serializers.IntegerField()

class Query6AreaSerializer(serializers.Serializer):
    area_name = serializers.CharField()
    total_crimes = serializers.IntegerField()

class Query6ReportDistrictSerializer(serializers.Serializer):
    reported_district_number = serializers.IntegerField()
    total_crimes = serializers.IntegerField()

class Query7Serializer(serializers.Serializer):
    crime_code_1 = serializers.IntegerField()
    crime_code_1_description = serializers.CharField()
    crime_code_2 = serializers.IntegerField()
    crime_code_2_description = serializers.CharField()
    occurrence_count = serializers.IntegerField()

class Query8Serializer(serializers.Serializer):
    crime_code = serializers.IntegerField()
    crime_description = serializers.CharField()

class Query9Serializer(serializers.Serializer):
    age_group_start = serializers.IntegerField()
    age_group_end = serializers.IntegerField()
    weapon_description = serializers.CharField()
    weapon_count = serializers.IntegerField()

class Query10AreaSerializer(serializers.Serializer):
    area_name = serializers.CharField()
    gap_start = serializers.DateField()
    gap_end = serializers.DateField()
    gap_duration = serializers.IntegerField()

class Query10ReportDistrictSerializer(serializers.Serializer):
    reported_district_number = serializers.IntegerField()
    area_name = serializers.CharField()
    gap_start = serializers.DateField()
    gap_end = serializers.DateField()
    gap_duration = serializers.IntegerField()

class Query11Serializer(serializers.Serializer):
    area_name = serializers.CharField()
    date_reported = serializers.DateField()
    crime_1_count = serializers.IntegerField()
    crime_2_count = serializers.IntegerField()

class Query12Serializer(serializers.Serializer):
    division_of_records_number = serializers.IntegerField()

class Query13Serializer(serializers.Serializer):
    area_name = serializers.CharField()
    date_occurred = serializers.DateField()
    crime_description = serializers.CharField()
    weapon_description = serializers.CharField()
    list_division_record_number = serializers.CharField()

class Query14Serializer(serializers.Serializer):
    division_of_records_number = serializers.IntegerField()

class Query15Serializer(serializers.Serializer):
    division_of_records_number = serializers.IntegerField()
    date_reported = serializers.DateField()
    date_occurred = serializers.DateField()
    time_occurred = serializers.TimeField()
    area_id = serializers.IntegerField()
    area_name = serializers.CharField()
    reported_district_number = serializers.IntegerField()
    crime_code_1 = serializers.IntegerField()
    crime_code_description_1 = serializers.CharField()
    crime_code_2 = serializers.IntegerField()
    crime_code_description_2 = serializers.CharField()
    crime_code_3 = serializers.IntegerField()
    crime_code_description_3 = serializers.CharField()
    crime_code_4 = serializers.IntegerField()
    crime_code_description_4 = serializers.CharField()
    mocodes = serializers.CharField()
    victim_age = serializers.IntegerField()
    victim_sex = serializers.CharField()
    victim_descent = serializers.CharField()
    premis_code = serializers.IntegerField()
    premis_description = serializers.CharField()
    weapon_used_code = serializers.IntegerField()
    weapon_description = serializers.CharField()
    status = serializers.CharField()
    status_description = serializers.CharField()
    location = serializers.CharField()
    cross_street = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class RegistrationSerializer(serializers.ModelSerializer):
    User = get_user_model()
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password'
    )

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = self.User.objects.create_user(**validated_data)
        return user