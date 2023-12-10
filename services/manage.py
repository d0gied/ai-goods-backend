import argparse
import os

from colorama import Fore, Style

parser = argparse.ArgumentParser(description="Manage services")
parser.add_argument("--services", help="list services", action="store_true")
parser.add_argument("--tasks", help="list tasks", action="store_true")


def list_services():
    directories = [
        d for d in os.listdir(".") if os.path.isdir(d) and not d.startswith(".")
    ]
    return directories


def print_services():
    services = list_services()
    print(f"{Fore.BLUE}Services:{Style.RESET_ALL}")
    for service in services:
        print(f"- {Fore.GREEN}{service}{Style.RESET_ALL}")


def print_tasks():
    services = list_services()
    for service in services:
        if service in ("global_modules", "api", "data"):
            continue
        print(f"{Fore.GREEN}Service: {service}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}")
        os.system(f"cd {service} && poetry run python run.py --tasks && cd ..")
        print(f"{Style.RESET_ALL}")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.services:
        print_services()
    elif args.tasks:
        print_tasks()
    else:
        parser.print_help()
