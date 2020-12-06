from termcolor import colored
import time

def credits():
    """Print Creditials"""
    print("""
Twitter : @palenath
Github : https://github.com/megadose/holehe
For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ\n""")


def show_mail(email):
    """ Printing email in function of the length of the email and legend"""

    stars = max(25, len(email))
    spaces = (((25 - len(email))//2) if (stars == 25) else 0)
    print(f"\033[H\033[J\n{'*'*stars}\n{' '*spaces}{email}\n"
            f"{'*'*stars}\n")


def show_out(out):
    for results in out:
        if results["rateLimit"]:
            print(colored(f"[x] {results['name']}", "red"))
        elif results["exists"] == False:
            print(colored(f"[-] {results['name']}", "magenta"))
        else:
            toprint = ""
            if results["emailrecovery"] is not None:
                toprint += " " + results["emailrecovery"]
            if results["phoneNumber"] is not None:
                toprint += " / " + results["phoneNumber"]
            if results["others"] is not None:
                toprint += " / FullName " + results["others"]["FullName"]
            print(colored(f"[+] {results['name']}{toprint}", "green"))


def shows(email, out, time, len_web, start_time):
    description = (f"{colored('[+] Email used','green')},"
                    f" {colored('[-] Email not used','magenta')},"
                    f" {colored(' [x] Rate limit','red')}")

    show_mail(email)
    show_out(out)
    print(f"\n{description}\n{str(len_web)} websites checked in "
            f"{round(time.time()-start_time, 2)} seconds")
    credits()
