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

from reportlab.pdfgen import canvas
from fpdf import FPDF


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


def createWeeklyReportPdf(data):
  """context = {
      'company': company,
      'client': client,
      'events': events,
      'employee': employee,
      'name': name,
      'payload': payload,
      'total_time': total_time,
      'week_dates': week_dates,
      'submission_deadline': submission_deadline,
    }
  """
  
  company = data["company"]
  client = data["client"]
  report_label = f"Weekly Time Sheet for {client.name}"
  headers = [
    'Attribute',
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Hours',
  ]
  bottom_headers = [
    '',
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    '',
  ]
  bottom_data = [
    '',
    '______________',
    '______________',
    '______________',
    '______________',
    '______________',
    '______________',
    '______________',
    '',
  ]
  employee = data["employee"]
  employee_name = f"{employee.user.last_name} {employee.user.first_name}".title()
  submitter = f"To be submitted by:  {employee_name} ".title()
  client_signature = f"Client Signature:  ________________"
  employee_signature = f"Employee Signature:  ________________"
  payload = data["payload"]
  # print("payload for pdf:",payload)
  body = []
  # for item in payload: print("Single Item", item)
  
  for index, items in enumerate(payload):
    # print("index, items: ", index, items)
    body.append([])
    body[index] = []
    attr = [f"Week {index + 1}", ""]
    body[index].append(attr)
    Sunday = items["events"]["sun"] or ["", ""]
    body[index].append(Sunday)
    Monday = items["events"]["mon"] or ["", ""]
    body[index].append(Monday)
    Tuesday = items["events"]["tue"] or ["", ""]
    body[index].append(Tuesday)
    Wednesday = items["events"]["wed"] or ["", ""]
    body[index].append(Wednesday)
    Thursday = items["events"]["thu"] or ["", ""]
    body[index].append(Thursday)
    Friday = items["events"]["fri"] or ["", ""]
    body[index].append(Friday)
    Saturday = items["events"]["sat"] or ["", ""]
    body[index].append(Saturday)
    # time = [str(items['time']), ""] or ["", ""]
    time = ["", ""] or ["", ""]  # Request from client
    body[index].append(time)
    
  # print(body)
  # body = payload["events"]
  
  
  total_time = data["total_time"]
  # total_hours = f"Total Hours:  {total_time}"
  total_hours = f"Total Hours: ___________________"  # Request from client
  week_dates = data["week_dates"]
  submission_deadline = data["submission_deadline"]
  submission_date = f"Submission Deadline:  {submission_deadline}"
  
  page_width = 297
  
  class WeeklyReport(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 18)
        # Calculate width of title and position
        w = self.get_string_width(company.name) + 6
        self.set_x((page_width - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        # # Thickness of frame (1 mm)
        # self.set_line_width(1)
        # Title
        self.cell(w, 9, company.name, 1, 1, 'C', 1)
        # Position Address
        w = self.get_string_width(company.name) + 6
        self.set_x((page_width - w) / 2)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        self.cell(w, 9, company.address, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def report_title(self, num, title):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((page_width - w) / 2)
        # Background color
        self.set_fill_color(255, 255, 255)
        # Title
        self.cell(w, 6, title, 0, 1, 'C', 1)
        # Line break
        self.ln(14)
        # Arial 9
        self.set_font('Arial', '', 9)
        # set starting position
        self.set_x(16)
        # Week Dates
        for index, week_date in enumerate(week_dates):
          date = f"Week {index + 1}:  {week_date}"
          self.cell(0, 6, date, 0, 1, 'L', 1)

    def report_body(self, headers, body):
        # Line break
        self.ln(10)
        # Arial 10
        self.set_font('Arial', '', 10)
        # Calculate the width for table and columns
        lens = [self.get_string_width(txt) + 16 for txt in headers]
        self.set_x((page_width - sum(lens)) / 2)
        # Table Headers
        for index, item in enumerate(headers):
          self.cell(w=lens[index], h=10, txt=item, border=1, ln=0, align='C', fill=0, link='')
        # Line break
        self.ln()
        # Calculate the width for table and columns
        self.set_x((page_width - sum(lens)) / 2)
        # Change font and font size
        self.set_font('Helvetica', '', 7)
        # Table Data Row 1
        for index, item in enumerate(body[0]):
          # print(item, index)
          self.cell(w=lens[index], h=10, txt=item[0], border=1, ln=0, align='C', fill=0, link='')
          # self.cell(w=lens[index], h=10, txt=item[0], border=1, ln=0, align='C', fill=0, link='')
        # Line break
        self.ln()
        try:
          # Calculate the width for table and columns
          self.set_x((page_width - sum(lens)) / 2)
          # Table Data Row 2
          for index, item in enumerate(body[1]):
            self.cell(w=lens[index], h=10, txt=item[1], border=1, ln=0, align='C', fill=0, link='')
          # Line break
          self.ln()
        except Exception as e:
          pass
        try:
          # Calculate the width for table and columns
          self.set_x((page_width - sum(lens)) / 2)
          # Table Data Row 3
          for index, item in enumerate(body):
            self.cell(w=lens[index], h=10, txt=item[2], border=1, ln=0, align='C', fill=0, link='')
          # Line break
          self.ln()
        except Exception as e:
          pass
        # Line break
        self.ln(20)
        try:
          # Calculate the width for table and columns
          self.set_x((page_width - sum(lens)) / 2)
          # Table bottom for custom time for employee
          for index, item in enumerate(bottom_data):
            self.cell(w=lens[index], h=10, txt=item, border=0, ln=0, align='C', fill=0, link='')
          # Line break
          self.ln()
        except Exception as e:
          pass
        try:
          # Calculate the width for table and columns
          self.set_x((page_width - sum(lens)) / 2)
          # Table bottom headers for custom time for employee
          for index, item in enumerate(bottom_headers):
            self.cell(w=lens[index], h=10, txt=item, border=0, ln=0, align='C', fill=0, link='')
          # Line break
          self.ln()
        except Exception as e:
          pass
         # Line break
        self.ln(20)
        # # Line break
        # self.ln()
        # # Line break
        # self.ln()
        # Change font and font size
        self.set_font('Arial', '', 9)
        # position submission date
        self.set_x(((page_width - sum(lens)) / 2) - 2)
        w = self.get_string_width(submission_date) + 6
        self.cell(w, 6, submission_date, 0, 0, 'C', 1)
        # postion total_hours
        w = self.get_string_width(total_hours) + 6
        self.set_x(page_width - (w + 12))
        self.cell(w, 6, total_hours, 0, 0, 'C', 1)
        # Line break
        self.ln(10)
        # position submission date
        self.set_x(((page_width - sum(lens)) / 2) - 2)
        w = self.get_string_width(submitter) + 6
        self.cell(w, 6, submitter, 0, 1, 'C', 1)
        # Line break
        self.ln(10)
        # position employee signature date
        self.set_x(((page_width - sum(lens)) / 2) - 2)
        w = self.get_string_width(employee_signature) + 6
        self.cell(w, 6, employee_signature, 0, 0, 'C', 1)
        # postion client_signature
        w = self.get_string_width(client_signature) + 6
        self.set_x(page_width - (w + 12))
        self.cell(w, 6, client_signature, 0, 0, 'C', 1)
        # Line break
        self.ln()
        # # Mention in italics
        # self.set_font('', 'I')
        # self.cell(0, 5, '(end of excerpt)')

    def print_report(self, num, title, headers, body):
        self.add_page(orientation="L")
        self.report_title(num, title)
        self.report_body(headers, body)
        
  pdf = WeeklyReport()
  pdf.set_title("Weekly Report")
  # pdf.set_author('Jules Verne')
  pdf.print_report(1, report_label, headers, body)
  # pdf.print_report(2, 'THE PROS AND CONS', '20k_c2.txt', context)
  file_name = f"weekly report for {employee_name} for {week_dates[0]}.pdf"
  pdf.output(f'./templates/pdf/{file_name}', 'F')
  # pdf.output(f'{file_name}', 'F')
  return file_name


def send_simple_email(request, template_path: str, reciepients: list, subject: str = "Email", context: dict = {}, attachment = None) -> bool:
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
    if attachment:
      msg.attach_file(attachment)
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
  # url = "http://www.hrtechleft.com/email/invite/:company"
  url = f"http://www.hrtechleft.com/email/invite/"
  url += f"?company={company.id}"
  
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

    
def employee_weekly_email_by_client(request, employee, client, company, name, email, week_list: list,):
      
  try:
    events = models.Event.objects.none()
    payload = []
    total_time = 0
    week_dates = []
    submission_deadline = datetime.now()
    
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
      if events:
        print("Events sorted by weekday;", events_by_weekday)
      
      hours_list = [utility.hourly_time_difference(utility.usable_time(event.start_time), utility.usable_time(event.end_time)) for event in events]
      week_time = sum(hours_list)
      # print("hours_list:", hours_list, "\n", "week_time:", week_time)
      
      total_time += week_time
      week_date = f"{week_start_date.date()} - {week_end_date.date()}"
      formatted_week_date = f"{week_start_date.strftime('%-d, %B %Y')} - {week_end_date.strftime('%-d, %B %Y')}"
      week_dates.append(formatted_week_date)
      
      deadline = week_end_date + timedelta(days=week.report_deadline)
      print("days, report_deadline:", week.report_deadline, deadline)
      submission_deadline = deadline.strftime('%-d, %B %Y')
      # print("week_time:", week_time, "total_time:", total_time, "week_date:", week_date, "submission_deadline:", submission_deadline)
      
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
        'week_date': formatted_week_date,
        'submission_deadline': submission_deadline,
        'events': events_by_weekday,
        'time': week_time
      }
      payload.append(data)
    # print(payload)
      
    if not events:
      raise Exception(f"There are no events for the client with id {client.id}")
    
    context = {
      'company': company,
      'client': client,
      'events': events,
      'employee': employee,
      'name': name,
      'payload': payload,
      'total_time': total_time,
      'week_dates': week_dates,
      'submission_deadline': submission_deadline,
    }
    
    attachment_path = None
    try:
      file_name = createWeeklyReportPdf(context)
      attachment_path = f"./templates/pdf/{file_name}"
    except Exception as e:
      print(f"exception creating pdf: {e}")
    
    try:
      email = send_simple_email(request, 'email/employee_weekly_report_email.html', [email], "Weekly Report", context, attachment_path)
      print(f'Employee weekly report nofitication mail for client {client} sent {email}\n')
    except Exception as e:
      print(f'An exception occurred while sending employee weekly report mail for client {client}: {e}')
      
  except Exception as e:
    if events:
      print(f"exception sending employee weekly report per client: {e}")


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
    
    # Remove duplicate clients
    clients = set(clients)
    
    print("Employee Clients:", clients)
    for client in clients:
      print(f"mail for employee with id: {employee.id}, for client with id: {client.id}")
      employee_weekly_email_by_client(request, employee, client, company, name, email, week_list)
    
    # return url
    
  except Exception as e:
    print(f'An exception occurred: {e}')
    

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
      if events:
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
    
    if not events:
      raise Exception(f"There are no events for the client with id {client.id}")
    
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
      print(f'Client weekly report notification email sent {email}\n')
      return True
    except Exception as e:
      print(f'An exception occurred while sending client weekly report mail: {e}')
      return False
        
  except Exception as e:
    if events:
      print(f'An exception occurred while getting client details: {e}\n')
