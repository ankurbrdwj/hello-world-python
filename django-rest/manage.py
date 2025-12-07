#!/usr/bin/env python3
"""
Django management script
Similar to the main() method in Spring Boot

In Spring Boot:
@SpringBootApplication
public class MealApplication {
    public static void main(String[] args) {
        SpringApplication.run(MealApplication.class, args);
    }
}

In Django, this script is used to run the server and manage the application
"""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
