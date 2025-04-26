from agents.problem_statement import generate_problem_statements_from_agent, read_problem_from_file
from agents.sponsors import find_sponsors_and_send_emails

def automate_hackathon_management():
    print("Choose an option:")
    print("1 - I already have a problem statement (in a file)")
    print("2 - I need a new problem statement generated")
    print("3 - Company gave the problem statement (no sponsor reach out)")

    choice = input("Enter 1, 2, or 3: ").strip()

    problem_text = ""

    if choice == "1":
        file_path = input("Enter file path: ").strip()
        problem_text = read_problem_from_file(file_path)

    elif choice == "2":
        specific_domain = input("Enter domain (optional, press Enter to skip): ").strip()
        problems_text = generate_problem_statements_from_agent(specific_domain)

        # Split problems and let user choose
        problems = problems_text.split('---')
        problems = [p.strip() for p in problems if p.strip()]

        print("\nAvailable Problems:")
        for idx, prob in enumerate(problems):
            print(f"\nProblem {idx+1}:\n{prob}")

        selected = int(input("\nEnter the number of the problem you want to proceed with (1/2/3/4/5): ").strip())
        if selected < 1 or selected > len(problems):
            print("Invalid selection. Exiting.")
            return

        problem_text = problems[selected-1]

    elif choice == "3":
        print("Company provided the problem statement. No sponsor outreach needed.")
        return

    else:
        print("Invalid choice. Exiting.")
        return

    print("\nProblem Statement to Work On:\n", problem_text)

    # Ask for event date
    event_date = input("Enter the hackathon date (e.g., May 10–12, 2025): ").strip()

    # Now find sponsors and send emails
    from_email = input("\nEnter your email address (to send from): ").strip()
    from_password = input("Enter your email password or App Password: ").strip()

    find_sponsors_and_send_emails(problem_text, from_email, from_password, event_date)

if __name__ == "__main__":
    automate_hackathon_management()