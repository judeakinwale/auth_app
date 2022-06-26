from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.urls import reverse
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from company import models
from util import utils as utility

from datetime import datetime, timedelta
import calendar


def get_user_company(request):
  company = None
  if request.user.is_superuser:
    return company

  try:
    if request.user.is_staff:
        company=request.user.company    
    company=request.user.employee.company
  except Exception:
    company = None
  return company


def get_active_month(request, company=None):

  if not company:
    company = utility.auth_user_company(request)

  # get current month name and current year
  today = datetime.now().date()
  year = str(today.year)  # Returns year as a 4 digit integer
  # month = str(today.month)  # Returns the month as a number
  month = today.strftime("%B")  # Returns the month full name ie. March
  defaults = {
    "month":month,
    "year": year,
  }
  
  active_month = models.Month.objects.none()
  try:
    months = models.Month.objects.filter(company=company, is_active=True)
    active_month, created = models.Month.objects.get_or_create(company=company, is_active=True, defaults=defaults)
    return active_month
  except Exception as e:
    if months:
      active_month = models.Month.objects.none()
      raise Exception("There are more than one active months")
    raise Exception(e)
    
    # # get current month name and current year
    # today = datetime.now().date()
    # year = str(today.year)  # Returns year as a 4 digit integer
    # # month = str(today.month)  # Returns the month as a number
    # month = today.strftime("%B")  # Returns the month full name ie. March
    
    # # try:
    # #   active_month, created = models.Month.objects.get_or_create(month=month, year=year, company=company, is_active=True)
    # # except:
    # #   # active_month = models.Month.objects.none()
    # #   raise Exception(e)
    
  return active_month


def sort_events_by_weekday(events):
  result = {}
  # result["sun"] = ""
  # result["mon"] = ""
  # result["tue"] = ""
  # result["wed"] = ""
  # result["thu"] = ""
  # result["fri"] = ""
  # result["sat"] = ""
  result["sun"] = []
  result["mon"] = []
  result["tue"] = []
  result["wed"] = []
  result["thu"] = []
  result["fri"] = []
  result["sat"] = []
  for event in events:
    event_times = f"{event.start_time} - {event.end_time}"
    if event.date_weekday() == 6:
      # result["sun"] = f"{result['sun']}{event_times}\n"
      result["sun"].append(event_times)
    if event.date_weekday() == 0:
      # result["mon"] = f"{result['mon']}{event_times}\n"
      result["mon"].append(event_times)
    if event.date_weekday() == 1:
      # result["tue"] = f"{result['tue']}{event_times}\n"
      result["tue"].append(event_times)
    if event.date_weekday() == 2:
      # result["wed"] = f"{result['wed']}{event_times}\n"
      result["wed"].append(event_times)
    if event.date_weekday() == 3:
      # result["thu"] = f"{result['thu']}{event_times}\n"
      result["thu"].append(event_times)
    if event.date_weekday() == 4:
      # result["fri"] = f"{result['fri']}{event_times}\n"
      result["fri"].append(event_times)
    if event.date_weekday() == 5:
      # result["sat"] = f"{result['sat']}{event_times}\n"
      result["sat"].append(event_times)
      
  return result


def send_simple_email(request, template_path: str, reciepients: list, subject: str = "Email", context: dict = {}) -> bool:
  try:
    sender_email = f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>"
    message = get_template(template_path).render(context) # path to the email template - 'email/results.html'

    msg = EmailMessage(
      subject,
      message,
      sender_email,
      reciepients,
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

    print(f"\nMail successfully sent: {msg}")
    return True
  except Exception as e:
    raise Exception(f"{e}")
    return False


def send_company_link(request, email: str) -> str:
  user = request.user
  try:
    company = user.employee.company
  except:
    company = user.company
  # url = request.get_absolute_url()
  # url = request.build_absolute_uri(reverse(f'company:employee-list')) 
  url = "http://www.hrtechleft.com/"
  url += f"create?company={company.id}"
  
  context = {
    'company': company,
    'user': user,
    'url': url,
  }
  try:
    email = send_simple_email(request, 'email/company_link.html', [email], "Company Link", context)
    print(f'Company link sent {email}')
    return url
  except Exception as e:
    raise Exception(f'An exception occurred while sending the company link: {e}')
    


def send_employee_event_email(request, employee, event_ids: list) -> str:
  try:
    company = employee.company
    name = f"{employee.user.first_name}"
    email = employee.user.email
    events = models.Event.objects.filter(
      Q(id__in=event_ids) 
      # & Q(company=company) 
      & Q(employee=employee) 
      # & ~Q(status="Completed") | ~Q(status="Dropped")
    )

    context = {
      'company': company,
      'events': events,
      'employee': employee,
      'name': name,
      # 'url': url,
    }
    try:
      email = send_simple_email(request, 'email/employee_event_email.html', [email], "Shift Details", context)
      print(f'Employee event nofitication mail sent {email}')
    except Exception as e:
      print(f'An exception occurred while sending employee event mail: {e}')
      
    # return url
    
  except Exception as e:
    print(f'An exception occurred while getting employee details: {e}')


def send_client_event_email(request, client, event_ids: list) -> str:
  try:
    user = client.name
    email = client.email
    company = client.company
    url = "https:// " # link to frontend schedule page for client
    events = models.Event.objects.filter(
      Q(id__in=event_ids) 
      # & Q(company=company) 
      & Q(client=client) 
      # & ~Q(status="Completed") | ~Q(status="Dropped")
    )
    if not client.email:
      print("no client email")
      return False

    if len(events) < 1:
      return False
    
    context = {
      'company': company,
      'events': events,
      'client': client,
      'name': user,
      'url': url,
    }
    try:
      email = send_simple_email(request, 'email/client_event_email.html', [email], "Company Link", context)
      print(f'Client event notification email sent {email}')
      return True
    except Exception as e:
      print(f'An exception occurred while sending client event mail: {e}')
      return False
      
    # return url
        
  except Exception as e:
    print(f'An exception occurred while getting client details: {e}')


# def send_employee_event_email(request, employee, events) -> str:
def send_employee_schedule_publish_email(request, employee, month=None) -> str:
  try:
    company = employee.company
    name = f"{employee.user.first_name}"
    email = employee.user.email
    month = get_month_dates(request, month=month)
    month_start_date = month["start_timestamp"]
    month_end_date = month["end_timestamp"]
    events = models.Event.objects.filter(
      Q(company=company) & Q(employee=employee) 
      & Q(date__gte=month_start_date) & Q(date__lte=month_end_date) 
      # & ~Q(status="Completed") | ~Q(status="Dropped")
    )
    
    context = {
      'company': company,
      'events': events,
      'employee': employee,
      'name': name,
      # 'url': url,
    }
    try:
      email = send_simple_email(request, 'email/employee_schedule_publish_email.html', [email], "Monthly Schedule", context)
      print(f'Employee schedule publish mail sent {email}')
    except Exception as e:
      print(f'An exception occurred while sending the published schedule email: {e}')
      
    # return url
        
  except Exception as e:
    print(f'An exception occurred while getting employee details: {e}')


def get_month_dates(request, month = None):
  if month is None:
    month = get_active_month(request)

  try:
    if month is None:
      raise Exception(f"Cannot Get Active Month")
      return None
    
    day = 1
    year = int(month.year)
    
    month_repr = f"{day} {month.month}, {month.year}"
    month_start = datetime.strptime(month_repr, '%d %B, %Y')
    
    month_int = str(datetime.strptime(month.month, '%B'))
    
    month_range = calendar.monthrange(year, month_start.month)
    
    last_day = month_range[1]
    month_end_repr = f"{last_day} {month.month}, {month.year}"
    month_end = datetime.strptime(month_end_repr, '%d %B, %Y')
    
    month_start_date = month_start.strftime('%Y-%m-%d')
    month_start_date_timestamp = str(int(round(datetime.timestamp(month_start))) * 1000)
    month_end_date = month_end.strftime('%Y-%m-%d')
    month_end_date_timestamp = str(int(round(datetime.timestamp(month_end))) * 1000)
    
    responses = {
      "start_timestamp": month_start_date_timestamp,
      "end_timestamp": month_end_date_timestamp,
      "start": month_start_date,
      "end": month_end_date,
    }
    return responses
  except Exception as e:
    raise Exception(e)
    return None
  

def send_employee_weekly_report_email(request, employee, week_list: list, event_ids: list) -> str:
  try:
    company = employee.company
    name = f"{employee.user.first_name}"
    email = employee.user.email
    # events = models.Event.objects.filter(
    #   Q(id__in=event_ids) 
    #   # & Q(company=company) 
    #   & Q(employee=employee) 
    #   # & ~Q(status="Completed") | ~Q(status="Dropped")
    # )

    clients = []
    events = models.Event.objects.none()
    
    for count, week_id in enumerate(week_list):
      week = models.Week.objects.get(id=week_id)
      week_start_date = datetime.strptime(week.start_date, "%Y-%m-%d")
      week_start_timestamp = int(round(week_start_date.timestamp()))
      # print("week_start_date:", week_start_date, "\n", "week_start_timestamp:", week_start_timestamp)
      
      week_end_date = datetime.strptime(week.end_date, "%Y-%m-%d")
      week_end_timestamp = int(round(week_end_date.timestamp()))
      # print("week_end_date:", week_end_date, "\n", "week_end_timestamp:", week_end_timestamp)
      
      events = models.Event.objects.filter(employee=employee, date__gte=week_start_timestamp, date__lte=week_end_timestamp)
      clients = [event.client for event in events]
      
    for client in clients:
      employee_weekly_email_by_client(request, employee, client, company, name, email, week_list)
    
    # return url
    
  except Exception as e:
    print(f'An exception occurred: {e}')
    
    
def employee_weekly_email_by_client(request, employee, client, company, name, email, week_list: list,):
      
    events = models.Event.objects.none()
    payload = []
    total_time = 0
    week_dates = []
    
    for count, week_id in enumerate(week_list):
      week = models.Week.objects.get(id=week_id)
      week_start_date = datetime.strptime(week.start_date, "%Y-%m-%d")
      week_start_timestamp = int(round(week_start_date.timestamp()))
      # print("week_start_date:", week_start_date, "\n", "week_start_timestamp:", week_start_timestamp)
      
      week_end_date = datetime.strptime(week.end_date, "%Y-%m-%d")
      week_end_timestamp = int(round(week_end_date.timestamp()))
      # print("week_end_date:", week_end_date, "\n", "week_end_timestamp:", week_end_timestamp)
      
      events = models.Event.objects.filter(employee=employee, client=client, date__gte=week_start_timestamp, date__lte=week_end_timestamp)
      events_by_weekday = sort_events_by_weekday(events)
      print("Events sorted by weekday;", events_by_weekday)
      
      hours_list = [utility.hourly_time_difference(utility.usable_time(event.start_time), utility.usable_time(event.end_time)) for event in events]
      week_time = sum(hours_list)
      # print("hours_list:", hours_list, "\n", "week_time:", week_time)
      
      total_time += week_time
      week_date = f"{week_start_date.date()} - {week_end_date.date()}"
      week_dates.append(week_date)
      
      submission_deadline = week_start_date + timedelta(days=week.report_deadline)
      
      # data = {}
      # # data[f'{count}'] = {
      # #   'week': week,
      # #   'events': events,
      # #   'time': week_time
      # # }
      # data['week'] = week
      # data['events'] = events
      # data['time'] = week_time
      
      data = {
        'week': week,
        'week_date': f"{week_start_date.date()} - {week_end_date.date()}",
        'submission_deadline': submission_deadline.date(),
        'events': events_by_weekday,
        'time': week_time
      }
      payload.append(data)
    # print(payload)
      
    context = {
      'company': company,
      'client': client,
      'events': events,
      'employee': employee,
      'name': name,
      'payload': payload,
      'total_time': total_time,
      'week_dates': week_dates
    }
    
    try:
      email = send_simple_email(request, 'email/employee_weekly_report_email.html', [email], "Weekly Report", context)
      print(f'Employee weekly report nofitication mail for client {client} sent {email}')
    except Exception as e:
      print(f'An exception occurred while sending employee weekly report mail for client {client}: {e}')


def send_client_weekly_report_email(request, client, week_list: list, event_ids: list) -> str:
  try:
    name = client.name
    email = client.email
    company = client.company
    url = "http://www.hrtechleft.com/app/schedule" # link to frontend schedule page for client
    
    # events = models.Event.objects.filter(
    #   Q(id__in=event_ids) 
    #   # & Q(company=company) 
    #   & Q(client=client) 
    #   # & ~Q(status="Completed") | ~Q(status="Dropped")
    # )

    if not client.email:
      # print("no client email")
      raise Exception("Client Has no Email")
      return False
    
    events = models.Event.objects.none()
    payload = []
    total_time = 0
    
    for count, week_id in enumerate(week_list):
      week = models.Week.objects.get(id=week_id)
      week_start_date = datetime.strptime(week.start_date, "%Y-%m-%d")
      week_start_timestamp = int(round(week_start_date.timestamp()))
      # print("week_start_date:", week_start_date, "\n", "week_start_timestamp:", week_start_timestamp)
      
      week_end_date = datetime.strptime(week.end_date, "%Y-%m-%d")
      week_end_timestamp = int(round(week_end_date.timestamp()))
      # print("week_end_date:", week_end_date, "\n", "week_end_timestamp:", week_end_timestamp)
      
      events = models.Event.objects.filter(client=client, date__gte=week_start_timestamp, date__lte=week_end_timestamp)
      events_by_weekday = sort_events_by_weekday(events)
      print("Events sorted by weekday;", events_by_weekday)
      
      hours_list = [utility.hourly_time_difference(utility.usable_time(event.start_time), utility.usable_time(event.end_time)) for event in events]
      week_time = sum(hours_list)
      # print("hours_list:", hours_list, "\n", "week_time:", week_time)
      
      total_time += week_time
      
      # data = {}
      # # data[f'{count}'] = {
      # #   'week': week,
      # #   'events': events,
      # #   'time': week_time
      # # }
      # data['week'] = week
      # data['events'] = events
      # data['time'] = week_time
      
      data = {
        'week': week,
        'events': events_by_weekday,
        'time': week_time
      }
      payload.append(data)
    # print(payload)
      
    context = {
      'company': company,
      'events': events,
      'client': client,
      'name': name,
      'payload': payload,
      'total_time': total_time,
      'url': url,
    }

    try:
      email = send_simple_email(request, 'email/client_weekly_report_email.html', [email], "Weekly Report", context)
      print(f'Client weekly report notification email sent {email}')
      return True
    except Exception as e:
      print(f'An exception occurred while sending client weekly report mail: {e}')
      return False
        
  except Exception as e:
    print(f'An exception occurred while getting client details: {e}')
