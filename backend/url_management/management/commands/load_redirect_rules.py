import json
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from url_management.models import RedirectRule


class Command(BaseCommand):
    help = 'Loads redirect rules from a JSON fixture file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username who will own the redirect rules',
            required=True
        )
        parser.add_argument(
            '--file',
            type=str,
            help='Path to JSON file with redirect rules',
            default='url_management/tests/fixtures/redirect_rules.json'
        )

    def handle(self, *args, **options):
        try:
            # Get or create user
            user, created = User.objects.get_or_create(
                username=options['username'],
                defaults={'is_active': True}
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created new user: {options["username"]}')
                )

            # Load fixture file
            fixture_path = Path(options['file'])
            if not fixture_path.exists():
                raise CommandError(f'File not found: {options["file"]}')

            with open(fixture_path, 'r') as f:
                data = json.load(f)

            # Create redirect rules
            created_count = 0
            for rule_data in data['redirect_rules']:
                RedirectRule.objects.create(
                    owner=user,
                    redirect_url=rule_data['redirect_url'],
                    is_private=rule_data['is_private']
                )
                created_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {created_count} redirect rules'
                )
            )

        except Exception as e:
            raise CommandError(f'Error loading redirect rules: {str(e)}')
