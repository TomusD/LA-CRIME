from datetime import datetime
from django.db import connection
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from crime_app_api.serializers import ( 
    CrimeReportSerializer ,Query1Serializer, Query2Serializer, Query3Serializer, Query4Serializer, Query5Serializer,
    Query6AreaSerializer, Query6ReportDistrictSerializer, Query7Serializer, Query8Serializer,
    Query9Serializer, Query10AreaSerializer, Query10ReportDistrictSerializer, Query11Serializer,
    Query12Serializer, Query13Serializer, Query14Serializer, Query15Serializer, RegistrationSerializer
)

# Different API views for different queries

class query1(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Validate parameters
        if not start_time or not end_time:
            return Response(
                {'error': 'Please provide both starting time and ending time.'},
                status=400
            )

        # Validate time format
        try:
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            return Response(
                {'error': 'Time format must be HH:MM.'},
                status=400
            )

        # Query 1
        sql_query = '''
                SELECT 
                    cc.crm_cd AS crime_code, 
                    cc.crm_cd_desc AS crime_description,
                    COUNT(cr.dr_no_id) AS total_reports
                FROM crime_app_api_crimereport cr
                JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                JOIN crime_app_api_crimecode cc ON cc.crm_cd = crc.crm_cd_1_id
                WHERE cd.time_occ BETWEEN %s AND %s
                GROUP BY cc.crm_cd, cc.crm_cd_desc
                ORDER BY total_reports DESC;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [start_time_obj, end_time_obj])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        

        serializer = Query1Serializer(data, many=True)
        return Response(serializer.data)
    
class query2(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        date_rptd = request.query_params.get('date_rptd')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        crm_cd_1 = request.query_params.get('crm_cd_1')

        # Validate parameters
        if not all([date_rptd, start_time, end_time, crm_cd_1]):
            return Response(
                {'error': 'Please provide date reported, starting time, ending time and crm cd.'},
                status=400
            )

        # Validate date format
        try:
            date_rptd_obj = datetime.strptime(date_rptd, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Date reported format must be YYYY-MM-DD.'},
                status=400
            )

        # Validate time format
        try:
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            return Response(
                {'error': 'Time format must be HH:MM.'},
                status=400
            )
        
        # Query 2
        sql_query = '''
                SELECT cd.date_rptd AS date_reported,
                COUNT(cr.dr_no_id) AS total_reports
                FROM crime_app_api_crimereport cr
                JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                WHERE cd.date_rptd = %s
                AND cd.time_occ BETWEEN %s AND %s
                AND crc.crm_cd_1_id = %s
                GROUP BY cd.date_rptd
                ORDER BY date_reported;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [date_rptd_obj, start_time_obj, end_time_obj, crm_cd_1])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()


        data = [dict(zip(columns, row)) for row in rows]

        serializer = Query2Serializer(data, many=True)
        return Response(serializer.data)
    
class query3(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        date_occ = request.query_params.get('date_occ')

        # Validate parameters
        if not date_occ:
            return Response(
                {'error': 'Please provide date occured.'},
                status=400
            )

        # Validate date format
        try:
            date_occ_obj = datetime.strptime(date_occ, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Date occured format must be YYYY-MM-DD.'},
                status=400
            )
        
        # Query 3
        sql_query = '''
                SELECT 
                    a.area_name,
                    cc.crm_cd AS crime_code,
                    cc.crm_cd_desc AS crime_description,
                    COUNT(*) AS crime_count
                FROM crime_app_api_crimereport cr
                JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                JOIN crime_app_api_area a ON cr.area_id = a.area_id
                JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                JOIN crime_app_api_crimecode cc ON 
                    cc.crm_cd = crc.crm_cd_1_id OR 
                    cc.crm_cd = crc.crm_cd_2_id OR 
                    cc.crm_cd = crc.crm_cd_3_id OR 
                    cc.crm_cd = crc.crm_cd_4_id
                WHERE cd.date_occ = %s
                GROUP BY a.area_name, cc.crm_cd, cc.crm_cd_desc
                ORDER BY a.area_name, crime_count DESC;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [date_occ_obj])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        serializer = Query3Serializer(data, many=True)
        return Response(serializer.data)

class query4(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        date_occ_start = request.query_params.get('date_occ_start')
        date_occ_end = request.query_params.get('date_occ_end')

        # Validate parameters
        if not date_occ_start or not date_occ_end:
            return Response(
                {'error': 'Please provide starting date occured and ending date occured.'},
                status=400
            )

        # Validate date format
        try:
            date_occ_start_obj = datetime.strptime(date_occ_start, '%Y-%m-%d').date()
            date_occ_end_obj = datetime.strptime(date_occ_end, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Date occured format must be YYYY-MM-DD.'},
                status=400
            )
        
        # Query 4
        sql_query = '''
                SELECT 
                    EXTRACT(HOUR FROM cd.time_occ) AS hour,
                    COUNT(cd.dr_no_id) / COUNT(DISTINCT cd.date_occ)::float AS average_crimes_per_hour
                FROM crime_app_api_crimedate cd
                WHERE cd.date_occ BETWEEN %s AND %s
                GROUP BY hour
                ORDER BY hour;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [date_occ_start_obj, date_occ_end_obj])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        serializer = Query4Serializer(data, many=True)
        return Response(serializer.data)

class query5(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        date_occ = request.query_params.get('date_occ')
        lat_min = request.query_params.get('lat_min')
        lat_max = request.query_params.get('lat_max')
        lon_min = request.query_params.get('lon_min')
        lon_max = request.query_params.get('lon_max')

        # Validate parameters
        if not all([date_occ, lat_min, lat_max, lon_min, lon_max]):
            return Response(
                {'error': 'Please provide date occured, latitude and longitude.'},
                status=400
            )

        # Validate date format
        try:
            date_occ_obj = datetime.strptime(date_occ, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Date occured format must be YYYY-MM-DD.'},
                status=400
            )
        
        # Validate latitude and longitude
        try :
            lat_min = float(lat_min)
            lat_max = float(lat_max)
            lon_min = float(lon_min)
            lon_max = float(lon_max)
        except ValueError:
            return Response(
                {'error': 'Latitude and longitude must be float.'},
                status=400
            )
        
        # Query 5
        sql_query = '''
                SELECT 
                    cc.crm_cd AS crime_code,
                    cc.crm_cd_desc AS crime_description,
                    COUNT(*) AS crime_count
                FROM crime_app_api_crimereport cr
                JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                JOIN crime_app_api_crimecode cc ON 
                    cc.crm_cd = crc.crm_cd_1_id OR 
                    cc.crm_cd = crc.crm_cd_2_id OR 
                    cc.crm_cd = crc.crm_cd_3_id OR 
                    cc.crm_cd = crc.crm_cd_4_id
                JOIN crime_app_api_location loc ON cr.location_id = loc.location_id
                WHERE cd.date_occ = %s
                AND loc.lat >= %s AND loc.lat <= %s
                AND loc.lon >= %s AND loc.lon <= %s
                GROUP BY cc.crm_cd, cc.crm_cd_desc 
                ORDER BY crime_count DESC
                LIMIT 1;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [date_occ_obj, lat_min, lat_max, lon_min, lon_max])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        serializer = Query5Serializer(data, many=True)
        return Response(serializer.data)
    
class query6(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, flag):

        date_rptd_start = request.query_params.get('date_rptd_start')
        date_rptd_end = request.query_params.get('date_rptd_end')

        # Validate the flag
        if flag not in ['area', 'dist']:
            return Response(
                {'error': 'Invalid flag. Use "area" or "dist".'},
                status=400
            )

        # Validate parameters
        if not date_rptd_start or not date_rptd_end:
            return Response(
                {'error': 'Please provide starting date reported and ending date reported.'},
                status=400
            )
        
        # Validate date format
        try:
            date_rptd_start_obj = datetime.strptime(date_rptd_start, '%Y-%m-%d').date()
            date_rptd_end_obj = datetime.strptime(date_rptd_end, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Date reported format must be YYYY-MM-DD.'},
                status=400
            )
        
        
        # Query 6 for area
        sql_query_area = '''
                SELECT 
                    a.area_name,
                    COUNT(cr.dr_no_id) AS total_crimes
                FROM crime_app_api_crimereport cr
                JOIN crime_app_api_area a ON cr.area_id = a.area_id
                JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                WHERE cd.date_rptd BETWEEN %s AND %s
                GROUP BY a.area_name
                ORDER BY total_crimes DESC
                LIMIT 5;
        '''

        # Query 6 for report district
        sql_query_dist = '''
                SELECT 
                    r.rpt_dist_no AS reported_district_number,
                    COUNT(cr.dr_no_id) AS total_crimes
                FROM crime_app_api_crimereport cr
                JOIN crime_app_api_reportdistrict r ON cr.report_dist_id = r.report_dist_id
                JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                WHERE cd.date_rptd BETWEEN %s AND %s
                GROUP BY r.rpt_dist_no
                ORDER BY total_crimes DESC
                LIMIT 5;
        '''


        # Execute the query
        if flag == 'area':
            with connection.cursor() as cursor:
                cursor.execute(sql_query_area, [date_rptd_start_obj, date_rptd_end_obj])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            data = [dict(zip(columns, row)) for row in rows]
            serializer = Query6AreaSerializer(data, many=True)

        if flag == 'dist':
            with connection.cursor() as cursor:
                cursor.execute(sql_query_dist, [date_rptd_start_obj, date_rptd_end_obj])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            data = [dict(zip(columns, row)) for row in rows]
            serializer = Query6ReportDistrictSerializer(data, many=True)

        return Response(serializer.data)
    
class query7(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        date_rptd_start = request.query_params.get('date_rptd_start')
        date_rptd_end = request.query_params.get('date_rptd_end')
        date_occ_start = request.query_params.get('date_occ_start')
        date_occ_end = request.query_params.get('date_occ_end')

        # Validate parameters
        if not all([date_rptd_start, date_rptd_end, date_occ_start, date_occ_end]):
            return Response(
                {'error': 'Please provide starting date for report and occurrence and ending date for report and occurrence.'},
                status=400
            )
        
        # Validate date format
        try:
            date_rptd_start_obj = datetime.strptime(date_rptd_start, '%Y-%m-%d').date()
            date_rptd_end_obj = datetime.strptime(date_rptd_end, '%Y-%m-%d').date()
            date_occ_start_obj = datetime.strptime(date_occ_start, '%Y-%m-%d').date()
            date_occ_end_obj = datetime.strptime(date_occ_end, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Date reported format must be YYYY-MM-DD.'},
                status=400
            )
        
        
        # Query 7
        sql_query = '''
                WITH MostReportedArea AS (
                    SELECT 
                        cr.area_id AS area_id,
                        COUNT(*) AS total_reports
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    WHERE cd.date_rptd BETWEEN %s AND %s
                    GROUP BY cr.area_id
                    ORDER BY total_reports DESC
                    LIMIT 1
                ),
                CrimeCodes AS (
                    SELECT 
                        cr.dr_no_id,
                        crc.crm_cd_1_id AS crime_code
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    WHERE cr.area_id = (SELECT area_id FROM MostReportedArea)
                    AND cd.date_occ BETWEEN %s AND %s
                    UNION ALL
                    SELECT 
                        cr.dr_no_id,
                        crc.crm_cd_2_id AS crime_code
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    WHERE cr.area_id = (SELECT area_id FROM MostReportedArea)
                    AND cd.date_occ BETWEEN %s AND %s
                    AND crc.crm_cd_2_id IS NOT NULL
                    UNION ALL
                    SELECT 
                        cr.dr_no_id,
                        crc.crm_cd_3_id AS crime_code
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    WHERE cr.area_id = (SELECT area_id FROM MostReportedArea)
                    AND cd.date_occ BETWEEN %s AND %s
                    AND crc.crm_cd_3_id IS NOT NULL
                    UNION ALL
                    SELECT 
                        cr.dr_no_id,
                        crc.crm_cd_4_id AS crime_code
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    WHERE cr.area_id = (SELECT area_id FROM MostReportedArea)
                    AND cd.date_occ BETWEEN %s AND %s
                    AND crc.crm_cd_4_id IS NOT NULL
                ),
                CrimeCodePairs AS (
                    SELECT
                        c1.crime_code AS crime_code_1,
                        c2.crime_code AS crime_code_2
                    FROM CrimeCodes c1
                    JOIN CrimeCodes c2 ON c1.dr_no_id = c2.dr_no_id
                    WHERE c1.crime_code < c2.crime_code
                ),
                CrimeCodePairCounts AS (
                    SELECT 
                        LEAST(crime_code_1, crime_code_2) AS crime_code_1,
                        GREATEST(crime_code_1, crime_code_2) AS crime_code_2,
                        COUNT(*) AS occurrence_count
                    FROM CrimeCodePairs
                    GROUP BY LEAST(crime_code_1, crime_code_2), GREATEST(crime_code_1, crime_code_2)
                )
                SELECT 
                    cpc.crime_code_1,
                    cc1.crm_cd_desc AS crime_code_1_description,
                    cpc.crime_code_2,
                    cc2.crm_cd_desc AS crime_code_2_description,
                    cpc.occurrence_count
                FROM CrimeCodePairCounts cpc
                JOIN crime_app_api_crimecode cc1 ON cpc.crime_code_1 = cc1.crm_cd
                JOIN crime_app_api_crimecode cc2 ON cpc.crime_code_2 = cc2.crm_cd
                ORDER BY cpc.occurrence_count DESC
                LIMIT 1
        '''


        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [date_rptd_start_obj, date_rptd_end_obj, 
                                       date_occ_start_obj, date_occ_end_obj, date_occ_start_obj, date_occ_end_obj, 
                                       date_occ_start_obj, date_occ_end_obj, date_occ_start_obj, date_occ_end_obj])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query7Serializer(data, many=True)

        return Response(serializer.data)
    
class query8(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        crm_cd = request.query_params.get('crm_cd')
        date_occ_start = request.query_params.get('date_occ_start')
        date_occ_end = request.query_params.get('date_occ_end')

        # Validate parameters
        if not all([crm_cd, date_occ_start, date_occ_end]):
            return Response(
                {'error': 'Please provide starting date of occurrence, ending date of occurrence and the crime code.'},
                status=400
            )
        
        # Validate date format
        try:
            date_occ_start_obj = datetime.strptime(date_occ_start, '%Y-%m-%d').date()
            date_occ_end_obj = datetime.strptime(date_occ_end, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Date reported format must be YYYY-MM-DD.'},
                status=400
            )
        
        
        # Query 8
        sql_query = '''
                WITH GivenCrimeIncidents AS (
                    SELECT 
                        cr.dr_no_id
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    WHERE crc.crm_cd_1_id = %s
                    AND cd.date_occ BETWEEN %s AND %s
                ),
                CoOccurringCrimes AS (
                    SELECT 
                        crc.crm_cd_2_id AS crime_code
                    FROM crime_app_api_crimereportcode crc
                    WHERE crc.dr_no_id IN (SELECT dr_no_id FROM GivenCrimeIncidents)
                    AND crc.crm_cd_2_id IS NOT NULL
                    UNION ALL
                    SELECT 
                        crc.crm_cd_3_id AS crime_code
                    FROM crime_app_api_crimereportcode crc
                    WHERE crc.dr_no_id IN (SELECT dr_no_id FROM GivenCrimeIncidents)
                    AND crc.crm_cd_3_id IS NOT NULL
                    UNION ALL
                    SELECT 
                        crc.crm_cd_4_id AS crime_code
                    FROM crime_app_api_crimereportcode crc
                    WHERE crc.dr_no_id IN (SELECT dr_no_id FROM GivenCrimeIncidents)
                    AND crc.crm_cd_4_id IS NOT NULL
                ),
                CrimeCounts AS (
                    SELECT 
                        crime_code, 
                        COUNT(*) AS co_occurrence_count
                    FROM CoOccurringCrimes
                    GROUP BY crime_code
                )
                SELECT 
                    cc_counts.crime_code,
                    cc.crm_cd_desc AS crime_description
                FROM CrimeCounts cc_counts
                JOIN crime_app_api_crimecode cc ON cc_counts.crime_code = cc.crm_cd
                ORDER BY cc_counts.co_occurrence_count DESC
                LIMIT 1;           
        '''


        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [crm_cd, date_occ_start_obj, date_occ_end_obj])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query8Serializer(data, many=True)

        return Response(serializer.data)
    
class query9(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        # Query 9
        sql_query = '''
                WITH AgeGroups AS (
                    SELECT 
                        v.vict_age,
                        CASE
                            WHEN v.vict_age >= 0 THEN (v.vict_age / 5) * 5
                        END AS age_group_start,
                        CASE
                            WHEN v.vict_age >= 0 THEN ((v.vict_age / 5) * 5) + 4
                        END AS age_group_end,
                        cr.weapon_id AS weapon_id
                    FROM crime_app_api_victim v
                    JOIN crime_app_api_crimereport cr ON v.victim_id = cr.victim_id
                ),
                WeaponUsage AS (
                    SELECT 
                        age_group_start,
                        age_group_end,
                        w.weapon_desc AS weapon_description,
                        COUNT(*) AS weapon_count
                    FROM AgeGroups ag
                    JOIN crime_app_api_weapon w ON ag.weapon_id = w.weapon_used_cd
                    GROUP BY age_group_start, age_group_end, w.weapon_desc
                ),
                MostCommonWeapon AS (
                    SELECT 
                        age_group_start,
                        age_group_end,
                        weapon_description,
                        weapon_count,
                        RANK() OVER (PARTITION BY age_group_start, age_group_end ORDER BY weapon_count DESC) AS rank
                    FROM WeaponUsage
                )
                SELECT 
                    age_group_start,
                    age_group_end,
                    weapon_description,
                    weapon_count
                FROM MostCommonWeapon
                WHERE rank = 1
                ORDER BY age_group_start;          
        '''


        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query9Serializer(data, many=True)

        return Response(serializer.data)

class query10(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, flag):

        crm_cd = request.query_params.get('crm_cd')

        # Validate the flag
        if flag not in ['area', 'dist']:
            return Response(
                {'error': 'Invalid flag. Use "area" or "dist".'},
                status=400
            )

        # Validate parameters
        if not crm_cd:
            return Response(
                {'error': 'Please provide crime code.'},
                status=400
            )

        
        # Query 10 for area
        sql_query_area = '''
                WITH CrimeOccurrences AS (
                    SELECT
                        cr.area_id AS area_id,
                        a.area_name,
                        cd.date_occ AS crime_date
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN crime_app_api_area a ON cr.area_id = a.area_id
                    WHERE
                        crc.crm_cd_1_id = %s OR
                        crc.crm_cd_2_id = %s OR
                        crc.crm_cd_3_id = %s OR
                        crc.crm_cd_4_id = %s
                    ORDER BY cr.area_id, cd.date_occ
                ),
                TimeGaps AS (
                    SELECT
                        area_id,
                        area_name,
                        LAG(crime_date) OVER (PARTITION BY area_id ORDER BY crime_date) AS prev_crime_date,
                        crime_date AS current_crime_date
                    FROM CrimeOccurrences
                ),
                GapDurations AS (
                    SELECT
                        area_id,
                        area_name,
                        prev_crime_date,
                        current_crime_date,
                        current_crime_date - prev_crime_date AS gap_duration
                    FROM TimeGaps
                    WHERE prev_crime_date IS NOT NULL
                ),
                MaxGapPerArea AS (
                    SELECT
                        area_id,
                        area_name,
                        prev_crime_date AS gap_start,
                        current_crime_date AS gap_end,
                        gap_duration,
                        RANK() OVER (PARTITION BY area_id ORDER BY gap_duration DESC) AS area_rank
                    FROM GapDurations
                )
                SELECT
                    area_name,
                    gap_start,
                    gap_end,
                    gap_duration
                FROM MaxGapPerArea
                WHERE area_rank = 1
                ORDER BY gap_duration DESC
                LIMIT 1;
        '''
        # Query 10 for report district
        sql_query_dist = '''
                WITH CrimeOccurrences AS (
                    SELECT
                        cr.report_dist_id AS report_dist_id,
                        rd.rpt_dist_no,
                        a.area_name,
                        cd.date_occ AS crime_date
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    JOIN crime_app_api_reportdistrict rd ON cr.report_dist_id = rd.report_dist_id
                    JOIN crime_app_api_area a ON rd.area_id = a.area_id
                    WHERE
                        crc.crm_cd_1_id = %s OR
                        crc.crm_cd_2_id = %s OR
                        crc.crm_cd_3_id = %s OR
                        crc.crm_cd_4_id = %s
                    ORDER BY rd.rpt_dist_no, cd.date_occ
                ),
                TimeGaps AS (
                    SELECT
                        report_dist_id,
                        rpt_dist_no,
                        area_name,
                        LAG(crime_date) OVER (PARTITION BY report_dist_id ORDER BY crime_date) AS prev_crime_date,
                        crime_date AS current_crime_date
                    FROM CrimeOccurrences
                ),
                GapDurations AS (
                    SELECT
                        report_dist_id,
                        rpt_dist_no,
                        area_name,
                        prev_crime_date,
                        current_crime_date,
                        current_crime_date - prev_crime_date AS gap_duration
                    FROM TimeGaps
                    WHERE prev_crime_date IS NOT NULL
                ),
                MaxGapPerDistrict AS (
                    SELECT
                        report_dist_id,
                        rpt_dist_no,
                        area_name,
                        prev_crime_date AS gap_start,
                        current_crime_date AS gap_end,
                        gap_duration,
                        RANK() OVER (PARTITION BY report_dist_id ORDER BY gap_duration DESC) AS district_rank
                    FROM GapDurations
                )
                SELECT
                    rpt_dist_no AS reported_district_number,
                    area_name,
                    gap_start,
                    gap_end,
                    gap_duration
                FROM MaxGapPerDistrict
                WHERE district_rank = 1
                ORDER BY gap_duration DESC
                LIMIT 1;
        '''


        # Execute the query
        if flag == 'area':
            with connection.cursor() as cursor:
                cursor.execute(sql_query_area, [crm_cd, crm_cd, crm_cd, crm_cd])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            data = [dict(zip(columns, row)) for row in rows]
            serializer = Query10AreaSerializer(data, many=True)

        if flag == 'dist':
            with connection.cursor() as cursor:
                cursor.execute(sql_query_dist, [crm_cd, crm_cd, crm_cd, crm_cd])
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            data = [dict(zip(columns, row)) for row in rows]
            serializer = Query10ReportDistrictSerializer(data, many=True)

        return Response(serializer.data)

class query11(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        crm_cd1 = request.query_params.get('crm_cd1')
        crm_cd2 = request.query_params.get('crm_cd2')

        # Validate parameters
        if not crm_cd1 or not crm_cd2:
            return Response(
                {'error': 'Please provide crime codes.'},
                status=400
            )

        
        # Query 11
        sql_query = '''
            WITH CrimeOccurrences AS (
                SELECT 
                    a.area_name,
                    cd.date_rptd AS date_reported,
                    crc.crm_cd_1_id AS crime_code,
                    COUNT(cr.dr_no_id) AS report_count
                FROM crime_app_api_crimereport cr
                JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                JOIN crime_app_api_area a ON cr.area_id = a.area_id
                WHERE crc.crm_cd_1_id IN (%s, %s)
                GROUP BY a.area_name, cd.date_rptd, crc.crm_cd_1_id
            ),
            CrimePairOccurrences AS (
                SELECT
                    c1.area_name,
                    c1.date_reported,
                    c1.report_count AS crime_1_count,
                    c2.report_count AS crime_2_count
                FROM CrimeOccurrences c1
                JOIN CrimeOccurrences c2 
                    ON c1.area_name = c2.area_name
                    AND c1.date_reported = c2.date_reported
                    AND c1.crime_code = %s
                    AND c2.crime_code = %s
                WHERE c1.report_count > 1 AND c2.report_count > 1
            )
            SELECT 
                area_name,
                date_reported,
                crime_1_count,
                crime_2_count
            FROM CrimePairOccurrences
            ORDER BY area_name, date_reported;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [crm_cd1, crm_cd2, crm_cd1, crm_cd2])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query11Serializer(data, many=True)

        return Response(serializer.data)


class query12(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Validate parameters
        if not start_time or not end_time:
            return Response(
                {'error': 'Please provide starting and ending time.'},
                status=400
            )

        # Validate time format
        try:
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            return Response(
                {'error': 'Time format must be HH:MM.'},
                status=400
            )
        
        # Query 12
        sql_query = '''
                WITH CrimeOccurrences AS (
                    SELECT 
                        cr.dr_no_id,
                        cd.date_rptd AS report_date,
                        a.area_name,
                        w.weapon_desc
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    JOIN crime_app_api_area a ON cr.area_id = a.area_id
                    JOIN crime_app_api_weapon w ON cr.weapon_id = w.weapon_used_cd
                    WHERE cd.time_occ BETWEEN %s AND %s
                ),
                WeaponsUsedInMultipleAreas AS (
                    SELECT 
                        report_date,
                        weapon_desc
                    FROM CrimeOccurrences
                    GROUP BY report_date, weapon_desc
                    HAVING COUNT(DISTINCT area_name) > 1
                )
                SELECT 
                    cr.dr_no_id AS division_of_records_number
                FROM CrimeOccurrences cr
                JOIN WeaponsUsedInMultipleAreas wm ON 
                    cr.report_date = wm.report_date AND 
                    cr.weapon_desc = wm.weapon_desc;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [start_time_obj, end_time_obj])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query12Serializer(data, many=True)

        return Response(serializer.data)

class query13(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        num_occ = request.query_params.get('num_occ')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Validate parameters
        if not all([num_occ, start_time, end_time]):
            return Response(
                {'error': 'Please provide starting time, ending time and how many the times occured.'},
                status=400
            )

        # Validate time format
        try:
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            return Response(
                {'error': 'Time format must be HH:MM.'},
                status=400
            )
        
        # Query 13
        sql_query = '''
                -- Create a temporary tablespace to store the temporary tables
                SET temp_tablespaces = 'temp_tablespace';
                WITH OccurrenceGroups AS (
                    SELECT
                        cr.area_id AS area_id,
                        cd.date_occ,
                        cr.weapon_id AS weapon_id,
                        crc.crm_cd_1_id AS crm_cd,
                        COUNT(*) AS occurrence_count
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    WHERE cd.time_occ BETWEEN %s AND %s
                    GROUP BY cr.area_id, cd.date_occ, cr.weapon_id, crc.crm_cd_1_id
                    HAVING
                    COUNT(*) = %s
                ),
                FilteredReports AS (
                    SELECT
                        cr.dr_no_id,
                        cr.area_id AS area_id,
                        cd.date_occ,
                        cd.time_occ,
                        cr.weapon_id AS weapon_id,
                        crc.crm_cd_1_id AS crm_cd
                    FROM crime_app_api_crimereport cr
                    JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                    JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                    JOIN OccurrenceGroups og ON
                            cr.area_id = og.area_id AND
                            cd.date_occ = og.date_occ AND
                            cr.weapon_id = og.weapon_id AND
                            crc.crm_cd_1_id = og.crm_cd
                    WHERE cd.time_occ BETWEEN %s AND %s
                )
                    SELECT
                        a.area_name,
                        cd.date_occ AS date_occurred,
                        cc.crm_cd_desc AS crime_description,
                        w.weapon_desc AS weapon_description,
                        STRING_AGG(fr.dr_no_id::text, ', ') AS list_division_record_number
                    FROM FilteredReports fr
                    JOIN crime_app_api_area a ON fr.area_id = a.area_id
                    JOIN crime_app_api_crimedate cd ON fr.dr_no_id = cd.dr_no_id
                    JOIN crime_app_api_crimecode cc ON fr.crm_cd = cc.crm_cd
                    JOIN crime_app_api_weapon w ON fr.weapon_id = w.weapon_used_cd
                    GROUP BY a.area_name, cd.date_occ, cc.crm_cd_desc, w.weapon_desc
                    ORDER BY a.area_name, cd.date_occ, cc.crm_cd_desc, w.weapon_desc;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [start_time_obj, end_time_obj, num_occ, start_time_obj, end_time_obj])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query13Serializer(data, many=True)

        return Response(serializer.data)
    
class query14(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        area_id = request.query_params.get('area_id')

        # Validate parameters
        if not area_id:
            return Response(
                {'error': 'Please provide Area ID.'},
                status=400
            )

        # Query 14
        sql_query = '''
                SELECT
                    cr.dr_no_id AS division_of_records_number
                FROM
                    crime_app_api_crimereport cr
                WHERE
                    cr.area_id = %s
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [area_id])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query14Serializer(data, many=True)

        return Response(serializer.data)
    
class query15(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        dr_no = request.query_params.get('dr_no')

        # Validate parameters
        if not dr_no:
            return Response(
                {'error': 'Please provide Division of Records Number.'},
                status=400
            )
        
        # Query 15
        sql_query = '''
                SELECT
                    cr.dr_no_id AS  division_of_records_number,
                    cd.date_rptd AS date_reported,
                    cd.date_occ AS date_occurred,
                    cd.time_occ AS time_occurred,
                    cr.area_id AS area_id,
                    a.area_name AS area_name,
                    rd.rpt_dist_no AS reported_district_number,
                    crc.crm_cd_1_id AS crime_code_1,
                    cc1.crm_cd_desc AS crime_code_description_1,
                    crc.crm_cd_2_id AS crime_code_2,
                    cc2.crm_cd_desc AS crime_code_description_2,
                    crc.crm_cd_3_id AS crime_code_3,
                    cc3.crm_cd_desc AS crime_code_description_3,
                    crc.crm_cd_4_id AS crime_code_4,
                    cc4.crm_cd_desc AS crime_code_description_4,
                    mo.mocodes AS mocodes,
                    v.vict_age AS victim_age,
                    v.vict_sex AS victim_sex,
                    v.vict_descent AS victim_descent,
                    p.premis_cd AS premis_code,
                    p.premis_desc AS premis_description,
                    w.weapon_used_cd AS weapon_used_code,
                    w.weapon_desc AS weapon_description,
                    s.status_cd AS status,
                    s.status_desc AS status_description,
                    l.street_address AS location,
                    l.cross_street AS cross_street,
                    l.lat AS latitude,
                    l.lon AS longitude
                FROM
                    crime_app_api_crimereport cr
                LEFT JOIN crime_app_api_crimedate cd ON cr.dr_no_id = cd.dr_no_id
                LEFT JOIN crime_app_api_area a ON cr.area_id = a.area_id
                LEFT JOIN crime_app_api_reportdistrict rd ON cr.report_dist_id = rd.report_dist_id
                LEFT JOIN crime_app_api_crimereportcode crc ON cr.dr_no_id = crc.dr_no_id
                LEFT JOIN crime_app_api_crimecode cc1 ON crc.crm_cd_1_id = cc1.crm_cd
                LEFT JOIN crime_app_api_crimecode cc2 ON crc.crm_cd_2_id = cc2.crm_cd
                LEFT JOIN crime_app_api_crimecode cc3 ON crc.crm_cd_3_id = cc3.crm_cd
                LEFT JOIN crime_app_api_crimecode cc4 ON crc.crm_cd_4_id = cc4.crm_cd
                LEFT JOIN crime_app_api_modusoperandi mo ON cr.mo_code_id = mo.mo_code_id
                LEFT JOIN crime_app_api_victim v ON cr.victim_id = v.victim_id
                LEFT JOIN crime_app_api_premises p ON cr.premise_id = p.premis_cd
                LEFT JOIN crime_app_api_weapon w ON cr.weapon_id = w.weapon_used_cd
                LEFT JOIN crime_app_api_status s ON cr.status_id = s.status_cd
                LEFT JOIN crime_app_api_location l ON cr.location_id = l.location_id
                WHERE
                    cr.dr_no_id = %s;
        '''

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [dr_no])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        serializer = Query15Serializer(data, many=True)

        return Response(serializer.data)
    
class addNewCrime(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CrimeReportSerializer(data=request.data)
        if serializer.is_valid():
            crime_report = serializer.save()
            return Response(
                {'message': 'Crime report added successfully.', 'dr_no': crime_report.dr_no_id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer