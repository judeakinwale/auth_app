from company import models, utils
from util import utils as utility
from datetime import datetime
import calendar


def company_first_time_setup(request, company=None):
  if not company:
    company = utility.auth_user_company(request)
  
  # create active month
  utils.get_active_month(request, company)
  print("Active month updated or created")
  
  # create employee model for company admin
  payload = {
    "user": request.user,
    "company": company,
    "role": "Admin",
  }
  defaults = {"employee_id": generate_employee_id("EMP"),}
  employee, created = models.Employee.objects.get_or_create(**payload, defaults=defaults)
  print("Employee instance created for company admin" if created else "company admin updated")
  
  # create month instances for all months in the current year
  create_months_for_current_year(company)
  
  print("First Time Setup Completed")
  return True  
  
  
def generate_employee_id(prefix:str, length:int=5, seperator:str=" ") -> str:
  try:
    latest_employee = models.Employee.objects.all().sort("-created_at")[0]
    latest_employee_id = latest_employee.employee_id
    string_id = latest_employee_id.split(seperator)[1]
    id = int(string_id)
    id += 1
    str_id = str(id).zfill(length)
    new_id = f"{prefix}{seperator}{id}"
    exising_employee_with_new_id = models.Employee.objects.filter(employee_id=new_id)
    if not existing_employee_with_new_id:
      return new_id
  except Exception as e:
    print(f"Exception while generating employee id: {e}")
    generate_employee_id(prefix, length)
    
    
def create_months_for_current_year(company: models.Company) -> bool:
  try:
    year = datetime.now().year  # get current year
    months = list(calendar.month_name[1:])  # get all months in a year

    for month in months:
      models.Month.objects.get_or_create(company=company, month=month, year=year)
    print("All months for the current year for the company should now exist")
    return True
  except Exception as e:
    print(f"Exception while creating all months in a year for company with id: {company.id}: {e}")
    return False