from django_extensions.management import jobs
from user.signals import disable_trial_users


class Job(jobs.DailyJob):
    help = "Disable trial user's account 7 days after creation."

    def execute(self):
        disable_trial_users()
