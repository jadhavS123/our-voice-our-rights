from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import District, MGNREGAData
from .serializers import DistrictSerializer, MGNREGADataSerializer
import xml.etree.ElementTree as ET
import requests
import json
from typing import Optional
from datetime import datetime, timedelta
import pytz

def fetch_mgnrega_data_from_api(district_name=None):
    """
    Fetch MGNREGA data from the data.gov.in API
    """
    try:
        # API endpoint for MGNREGA data
        api_url = "https://api.data.gov.in/resource/ee03643a-ee4c-48c2-ac30-9f2ff26ab722"
        api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
        
        # Parameters for the API request
        params = {
            "api-key": api_key,
            "format": "xml",
            "limit": 1000  # Adjust as needed
        }
        
        # If a specific district is requested, add it to the filters
        if district_name:
            params["filters[district_name]"] = district_name
        
        # Make the API request
        response = requests.get(api_url, params=params, timeout=30)
        
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.content)
            records = root.find('records')
            
            if records is not None:
                for item in records.findall('item'):
                    # Extract district information
                    state_code_elem = item.find('state_code')
                    state_name_elem = item.find('state_name')
                    district_code_elem = item.find('district_code')
                    district_name_elem = item.find('district_name')
                    
                    state_code = get_text_from_element(state_code_elem)
                    state_name = get_text_from_element(state_name_elem)
                    district_code = get_text_from_element(district_code_elem)
                    district_name = get_text_from_element(district_name_elem)
                    
                    # Create or get district
                    district, created = District.objects.get_or_create(
                        district_code=district_code,
                        defaults={
                            'state_code': state_code,
                            'state_name': state_name,
                            'district_name': district_name
                        }
                    )
                    
                    # Extract MGNREGA data
                    fin_year_elem = item.find('fin_year')
                    month_elem = item.find('month')
                    
                    fin_year = get_text_from_element(fin_year_elem)
                    month = get_text_from_element(month_elem)
                    
                    # Check if we already have this data to avoid duplicates
                    existing_data = MGNREGAData.objects.filter(
                        district=district,
                        fin_year=fin_year,
                        month=month
                    ).first()
                    
                    if existing_data:
                        # Update existing record
                        mgnrega_data = existing_data
                    else:
                        # Create new record
                        mgnrega_data = MGNREGAData(district=district, fin_year=fin_year, month=month)
                    
                    # Extract all other data elements
                    approved_labour_budget_elem = item.find('Approved_Labour_Budget')
                    average_wage_rate_elem = item.find('Average_Wage_rate_per_day_per_person')
                    average_days_employment_elem = item.find('Average_days_of_employment_provided_per_Household')
                    differently_abled_persons_worked_elem = item.find('Differently_abled_persons_worked')
                    material_and_skilled_wages_elem = item.find('Material_and_skilled_Wages')
                    number_of_completed_works_elem = item.find('Number_of_Completed_Works')
                    number_of_gps_with_nil_exp_elem = item.find('Number_of_GPs_with_NIL_exp')
                    number_of_ongoing_works_elem = item.find('Number_of_Ongoing_Works')
                    persondays_central_liability_elem = item.find('Persondays_of_Central_Liability_so_far')
                    sc_persondays_elem = item.find('SC_persondays')
                    sc_workers_against_active_workers_elem = item.find('SC_workers_against_active_workers')
                    st_persondays_elem = item.find('ST_persondays')
                    st_workers_against_active_workers_elem = item.find('ST_workers_against_active_workers')
                    total_adm_expenditure_elem = item.find('Total_Adm_Expenditure')
                    total_exp_elem = item.find('Total_Exp')
                    wages_elem = item.find('Wages')
                    total_households_worked_elem = item.find('Total_Households_Worked')
                    total_individuals_worked_elem = item.find('Total_Individuals_Worked')
                    total_active_job_cards_elem = item.find('Total_No_of_Active_Job_Cards')
                    total_active_workers_elem = item.find('Total_No_of_Active_Workers')
                    total_hhs_completed_100_days_elem = item.find('Total_No_of_HHs_completed_100_Days_of_Wage_Employment')
                    total_jobcards_issued_elem = item.find('Total_No_of_JobCards_issued')
                    total_workers_elem = item.find('Total_No_of_Workers')
                    total_works_takenup_elem = item.find('Total_No_of_Works_Takenup')
                    women_persondays_elem = item.find('Women_Persondays')
                    percent_category_b_works_elem = item.find('percent_of_Category_B_Works')
                    percent_expenditure_agriculture_elem = item.find('percent_of_Expenditure_on_Agriculture_Allied_Works')
                    percent_nrm_expenditure_elem = item.find('percent_of_NRM_Expenditure')
                    percentage_payments_within_15_days_elem = item.find('percentage_payments_gererated_within_15_days')
                    remarks_elem = item.find('Remarks')
                    
                    # Update MGNREGA data record
                    mgnrega_data.approved_labour_budget = get_int_from_element(approved_labour_budget_elem)
                    mgnrega_data.average_wage_rate = get_float_from_element(average_wage_rate_elem)
                    mgnrega_data.average_days_employment = get_int_from_element(average_days_employment_elem)
                    mgnrega_data.differently_abled_persons_worked = get_int_from_element(differently_abled_persons_worked_elem)
                    mgnrega_data.material_and_skilled_wages = get_float_from_element(material_and_skilled_wages_elem)
                    mgnrega_data.number_of_completed_works = get_int_from_element(number_of_completed_works_elem)
                    mgnrega_data.number_of_gps_with_nil_exp = get_int_from_element(number_of_gps_with_nil_exp_elem)
                    mgnrega_data.number_of_ongoing_works = get_int_from_element(number_of_ongoing_works_elem)
                    mgnrega_data.persondays_central_liability = get_int_from_element(persondays_central_liability_elem)
                    mgnrega_data.sc_persondays = get_int_from_element(sc_persondays_elem)
                    mgnrega_data.sc_workers_against_active_workers = get_int_from_element(sc_workers_against_active_workers_elem)
                    mgnrega_data.st_persondays = get_int_from_element(st_persondays_elem)
                    mgnrega_data.st_workers_against_active_workers = get_int_from_element(st_workers_against_active_workers_elem)
                    mgnrega_data.total_adm_expenditure = get_float_from_element(total_adm_expenditure_elem)
                    mgnrega_data.total_exp = get_float_from_element(total_exp_elem)
                    mgnrega_data.wages = get_float_from_element(wages_elem)
                    mgnrega_data.total_households_worked = get_int_from_element(total_households_worked_elem)
                    mgnrega_data.total_individuals_worked = get_int_from_element(total_individuals_worked_elem)
                    mgnrega_data.total_active_job_cards = get_int_from_element(total_active_job_cards_elem)
                    mgnrega_data.total_active_workers = get_int_from_element(total_active_workers_elem)
                    mgnrega_data.total_hhs_completed_100_days = get_int_from_element(total_hhs_completed_100_days_elem)
                    mgnrega_data.total_jobcards_issued = get_int_from_element(total_jobcards_issued_elem)
                    mgnrega_data.total_workers = get_int_from_element(total_workers_elem)
                    mgnrega_data.total_works_takenup = get_int_from_element(total_works_takenup_elem)
                    mgnrega_data.women_persondays = get_int_from_element(women_persondays_elem)
                    mgnrega_data.percent_category_b_works = get_int_from_element(percent_category_b_works_elem)
                    mgnrega_data.percent_expenditure_agriculture = get_float_from_element(percent_expenditure_agriculture_elem)
                    mgnrega_data.percent_nrm_expenditure = get_float_from_element(percent_nrm_expenditure_elem)
                    mgnrega_data.percentage_payments_within_15_days = get_float_from_element(percentage_payments_within_15_days_elem)
                    mgnrega_data.remarks = get_text_from_element(remarks_elem)
                    
                    mgnrega_data.save()
                
                return True
        else:
            print(f"API request failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return False

@api_view(['GET'])
def district_list(request):
    """
    List all districts
    """
    districts = District.objects.all()
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def district_performance(request, district_name):
    """
    Retrieve performance data for a specific district
    """
    try:
        # Try to get the district
        district = District.objects.get(district_name__iexact=district_name)
        
        # Get the latest MGNREGA data for this district
        mgnrega_data = MGNREGAData.objects.filter(district=district).order_by('-last_updated')
        
        # If no data exists or data is older than 1 day, fetch fresh data from API
        should_fetch_fresh_data = False
        if not mgnrega_data.exists():
            should_fetch_fresh_data = True
        else:
            # Check if the latest data is older than 1 day
            latest_data = mgnrega_data.first()
            # Make sure we're comparing timezone-aware datetimes
            if latest_data.last_updated.tzinfo is None:
                # If the model's datetime is naive, make it timezone-aware
                latest_data_time = latest_data.last_updated.replace(tzinfo=pytz.UTC)
            else:
                latest_data_time = latest_data.last_updated
            
            # Get current time in UTC
            now = datetime.now(pytz.UTC)
            
            if latest_data_time < now - timedelta(days=1):
                should_fetch_fresh_data = True
        
        if should_fetch_fresh_data:
            # Try to fetch from API
            success = fetch_mgnrega_data_from_api(district_name)
            if success:
                mgnrega_data = MGNREGAData.objects.filter(district=district).order_by('-last_updated')
        
        if mgnrega_data.exists():
            serializer = MGNREGADataSerializer(mgnrega_data, many=True)
            return Response(serializer.data)
        else:
            # Return empty data if nothing found
            return Response([])
    except District.DoesNotExist:
        return Response({"error": "District not found"}, status=status.HTTP_404_NOT_FOUND)

def get_text_from_element(element: Optional[ET.Element]) -> str:
    """
    Safely extract text from an XML element
    """
    if element is not None:
        return element.text or ''
    return ''

def get_int_from_element(element: Optional[ET.Element]) -> Optional[int]:
    """
    Safely extract integer from an XML element
    """
    if element is not None and element.text:
        try:
            return int(element.text)
        except ValueError:
            return None
    return None

def get_float_from_element(element: Optional[ET.Element]) -> Optional[float]:
    """
    Safely extract float from an XML element
    """
    if element is not None and element.text:
        try:
            return float(element.text)
        except ValueError:
            return None
    return None

def parse_xml_data():
    """
    Parse the XML data from Server response.txt and populate our database
    """
    try:
        with open('Server response.txt', 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        root = ET.fromstring(xml_content)
        records = root.find('records')
        
        if records is not None:
            for item in records.findall('item'):
                # Extract district information
                state_code_elem = item.find('state_code')
                state_name_elem = item.find('state_name')
                district_code_elem = item.find('district_code')
                district_name_elem = item.find('district_name')
                
                state_code = get_text_from_element(state_code_elem)
                state_name = get_text_from_element(state_name_elem)
                district_code = get_text_from_element(district_code_elem)
                district_name = get_text_from_element(district_name_elem)
                
                # Create or get district
                district, created = District.objects.get_or_create(
                    district_code=district_code,
                    defaults={
                        'state_code': state_code,
                        'state_name': state_name,
                        'district_name': district_name
                    }
                )
                
                # Extract MGNREGA data
                fin_year_elem = item.find('fin_year')
                month_elem = item.find('month')
                
                fin_year = get_text_from_element(fin_year_elem)
                month = get_text_from_element(month_elem)
                
                # Extract all other data elements
                approved_labour_budget_elem = item.find('Approved_Labour_Budget')
                average_wage_rate_elem = item.find('Average_Wage_rate_per_day_per_person')
                average_days_employment_elem = item.find('Average_days_of_employment_provided_per_Household')
                differently_abled_persons_worked_elem = item.find('Differently_abled_persons_worked')
                material_and_skilled_wages_elem = item.find('Material_and_skilled_Wages')
                number_of_completed_works_elem = item.find('Number_of_Completed_Works')
                number_of_gps_with_nil_exp_elem = item.find('Number_of_GPs_with_NIL_exp')
                number_of_ongoing_works_elem = item.find('Number_of_Ongoing_Works')
                persondays_central_liability_elem = item.find('Persondays_of_Central_Liability_so_far')
                sc_persondays_elem = item.find('SC_persondays')
                sc_workers_against_active_workers_elem = item.find('SC_workers_against_active_workers')
                st_persondays_elem = item.find('ST_persondays')
                st_workers_against_active_workers_elem = item.find('ST_workers_against_active_workers')
                total_adm_expenditure_elem = item.find('Total_Adm_Expenditure')
                total_exp_elem = item.find('Total_Exp')
                wages_elem = item.find('Wages')
                total_households_worked_elem = item.find('Total_Households_Worked')
                total_individuals_worked_elem = item.find('Total_Individuals_Worked')
                total_active_job_cards_elem = item.find('Total_No_of_Active_Job_Cards')
                total_active_workers_elem = item.find('Total_No_of_Active_Workers')
                total_hhs_completed_100_days_elem = item.find('Total_No_of_HHs_completed_100_Days_of_Wage_Employment')
                total_jobcards_issued_elem = item.find('Total_No_of_JobCards_issued')
                total_workers_elem = item.find('Total_No_of_Workers')
                total_works_takenup_elem = item.find('Total_No_of_Works_Takenup')
                women_persondays_elem = item.find('Women_Persondays')
                percent_category_b_works_elem = item.find('percent_of_Category_B_Works')
                percent_expenditure_agriculture_elem = item.find('percent_of_Expenditure_on_Agriculture_Allied_Works')
                percent_nrm_expenditure_elem = item.find('percent_of_NRM_Expenditure')
                percentage_payments_within_15_days_elem = item.find('percentage_payments_gererated_within_15_days')
                remarks_elem = item.find('Remarks')
                
                # Create MGNREGA data record
                mgnrega_data = MGNREGAData(
                    district=district,
                    fin_year=fin_year,
                    month=month,
                    approved_labour_budget=get_int_from_element(approved_labour_budget_elem),
                    average_wage_rate=get_float_from_element(average_wage_rate_elem),
                    average_days_employment=get_int_from_element(average_days_employment_elem),
                    differently_abled_persons_worked=get_int_from_element(differently_abled_persons_worked_elem),
                    material_and_skilled_wages=get_float_from_element(material_and_skilled_wages_elem),
                    number_of_completed_works=get_int_from_element(number_of_completed_works_elem),
                    number_of_gps_with_nil_exp=get_int_from_element(number_of_gps_with_nil_exp_elem),
                    number_of_ongoing_works=get_int_from_element(number_of_ongoing_works_elem),
                    persondays_central_liability=get_int_from_element(persondays_central_liability_elem),
                    sc_persondays=get_int_from_element(sc_persondays_elem),
                    sc_workers_against_active_workers=get_int_from_element(sc_workers_against_active_workers_elem),
                    st_persondays=get_int_from_element(st_persondays_elem),
                    st_workers_against_active_workers=get_int_from_element(st_workers_against_active_workers_elem),
                    total_adm_expenditure=get_float_from_element(total_adm_expenditure_elem),
                    total_exp=get_float_from_element(total_exp_elem),
                    wages=get_float_from_element(wages_elem),
                    total_households_worked=get_int_from_element(total_households_worked_elem),
                    total_individuals_worked=get_int_from_element(total_individuals_worked_elem),
                    total_active_job_cards=get_int_from_element(total_active_job_cards_elem),
                    total_active_workers=get_int_from_element(total_active_workers_elem),
                    total_hhs_completed_100_days=get_int_from_element(total_hhs_completed_100_days_elem),
                    total_jobcards_issued=get_int_from_element(total_jobcards_issued_elem),
                    total_workers=get_int_from_element(total_workers_elem),
                    total_works_takenup=get_int_from_element(total_works_takenup_elem),
                    women_persondays=get_int_from_element(women_persondays_elem),
                    percent_category_b_works=get_int_from_element(percent_category_b_works_elem),
                    percent_expenditure_agriculture=get_float_from_element(percent_expenditure_agriculture_elem),
                    percent_nrm_expenditure=get_float_from_element(percent_nrm_expenditure_elem),
                    percentage_payments_within_15_days=get_float_from_element(percentage_payments_within_15_days_elem),
                    remarks=get_text_from_element(remarks_elem)
                )
                mgnrega_data.save()
                
        return True
    except Exception as e:
        print(f"Error parsing XML data: {e}")
        return False

@api_view(['GET'])
def initialize_data(request):
    """
    Initialize the database with data from the live API
    """
    success = fetch_mgnrega_data_from_api()
    if success:
        return Response({"status": "success", "message": "Data initialized successfully from live API"})
    else:
        # Fallback to local file if API fails
        success = parse_xml_data()
        if success:
            return Response({"status": "success", "message": "Data initialized from local file"})
        else:
            return Response({"status": "error", "message": "Failed to initialize data"}, status=500)

@api_view(['GET'])
def detect_district(request):
    """
    Detect district based on user's geolocation (placeholder implementation)
    In a real application, you would use a reverse geocoding service
    """
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if not lat or not lon:
        return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # In a real implementation, you would use a reverse geocoding service
    # to convert coordinates to district names
    # For now, we'll return a placeholder response
    return Response({
        "message": "Geolocation detected successfully",
        "latitude": lat,
        "longitude": lon,
        "district": None  # In a real app, this would be the detected district
    })