from django.core.management.base import BaseCommand
from user_registration.models import RegisteredEmail

class Command(BaseCommand):
    help = "Registers a list of emails into the RegisteredEmail model with names"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            required=True,
            help="Provide the emails in 'name:email' format, separated by commas. Example: user1:zongkenc3018@gmail.com,user2:example@gmail.com",
        )

    def handle(self, *args, **options):
        email_list = options["email"].split(",")
        
        for entry in email_list:
            cleaned_entry = entry.strip()
            if ":" in cleaned_entry:
                name, email = cleaned_entry.split(":", 1)  # Split into name and email
                name, email = name.strip(), email.strip()

                if email:
                    RegisteredEmail.objects.create(name=name, email_address=email)
                    self.stdout.write(self.style.SUCCESS(f"Registered: {name} - {email}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid entry: {entry}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipping malformed entry: {entry}"))

        self.stdout.write(self.style.SUCCESS("All valid emails registered successfully!"))
