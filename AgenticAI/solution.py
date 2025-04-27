# solution.py

import os
import json
import re

from csi_agents.problem_statement import generate_problem_statements_from_agent, read_problem_from_file
from csi_agents.sponsors import find_sponsors_for_problem, find_sponsors_and_send_emails
from csi_agents.marketingagent import generate_marketing_content, parse_sections, save_sections, generate_poster_images, parse_participant_emails, send_emails_to_participants_from_list
from csi_agents.logistics_agent import run_logistics_flow
from csi_agents.postevent_agent import run_postevent_process
from csi_agents.support import ask_support_agent
from csi_agents.incident import mentor_drop_and_match
# from csi_agents.judge import deploy_judging_form_and_server, declare_winners

HACKATHON_FOLDER = "hackathons"

def save_hackathon(event_id, data):
    os.makedirs(HACKATHON_FOLDER, exist_ok=True)
    file_path = os.path.join(HACKATHON_FOLDER, f"{event_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"\n💾 Hackathon data saved to {file_path}")

def automate_hackathon_management():
    print("Choose an option:")
    print("1 - Complete Hackathon Setup (Problem → Sponsors → Marketing → Logistics)")
    print("2 - Post-event Management (Thank You Emails + Report)")
    print("3 - Support Chat (Ask any question)")
    print("4 - Incident Alerts Management (Send incident updates)")
    print("5 - Judging and Winner Declaration")

    option = input("Enter 1, 2, 3, 4, or 5: ").strip()

    from_email = "kindrasena8@gmail.com"
    from_password = "sdecbbhtntaqoysp"

    if option == "1":
        complete_hackathon_flow(from_email, from_password)

    elif option == "2":
        print("\nPost-Event Management")
        print("----------------------")

        photos_link = input("Enter link to event photos: ").strip()

        student_emails_input = input("Enter student emails (comma separated): ").strip()
        mentor_emails_input = input("Enter mentor emails (comma separated): ").strip()

        student_emails = [email.strip() for email in student_emails_input.split(",") if email.strip()]
        mentor_emails = [email.strip() for email in mentor_emails_input.split(",") if email.strip()]

        run_postevent_process(
            student_emails=student_emails,
            mentor_emails=mentor_emails,
            from_email=from_email,
            from_password=from_password,
            photos_link=photos_link
        )

    elif option == "3":
        print("\nSupport Chat Management")
        print("------------------------")
        ask_support_agent()

    elif option == "4":
        print("\nIncident Alerts Management")
        print("---------------------------")
        event_id = input("Enter Event ID (example: mental_health_april): ").strip()
        mentor_drop_and_match(event_id)

    elif option == "5":
        print("\nJudging and Winner Declaration")
        print("-------------------------------")
        print("1 - Deploy Judging Form")
        print("2 - Declare Winners")

        judge_choice = input("Enter 1 or 2: ").strip()

        if judge_choice == "1":
            deploy_judging_form_and_server()
        elif judge_choice == "2":
            declare_winners()
        else:
            print("❌ Invalid selection for judging management.")
    
    else:
        print("Invalid choice. Exiting.")

def complete_hackathon_flow(from_email, from_password):
    print("\n🚀 Complete Hackathon Setup Started\n")

    # STEP 1: Problem Statement
    print("\n📋 Step 1: Select or Generate Problem Statement\n")
    choice = input("1 - Read from file\n2 - Generate new problems\nChoose (1 or 2): ").strip()

    if choice == "1":
        file_path = input("Enter the file path to your problem statement: ").strip()
        problem_text = read_problem_from_file(file_path)
    elif choice == "2":
        domain = input("Enter a specific domain (optional, press Enter to skip): ").strip()
        problems_text = generate_problem_statements_from_agent(domain)
        problems = problems_text.split('---')
        problems = [p.strip() for p in problems if p.strip()]

        print("\nAvailable Problems:")
        for idx, prob in enumerate(problems):
            print(f"\nProblem {idx+1}:\n{prob}")

        selected = int(input("\nSelect a problem (1/2/3/4/5): ").strip())
        if selected < 1 or selected > len(problems):
            print("❌ Invalid selection. Exiting.")
            return

        problem_text = problems[selected - 1]
    else:
        print("❌ Invalid choice. Exiting.")
        return

    print("\n✅ Problem Statement Selected Successfully.\n")

    # STEP 2: Find Sponsors
    print("\n🏢 Step 2: Finding Potential Sponsors...\n")
    sponsor_emails_text = find_sponsors_for_problem(problem_text)
    sponsor_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", sponsor_emails_text)

    if sponsor_emails:
        print(f"✅ Found {len(sponsor_emails)} potential sponsors.")
        find_sponsors_and_send_emails(problem_text, from_email, from_password, event_date="TBD")
    else:
        print("⚠️ Warning: No sponsors found.")

    # STEP 3: Confirm Event Details
    print("\n🎯 Step 3: Confirm Event Details\n")
    event_name = input("Enter Event Name (e.g., Hack the Hackathon): ").strip()
    event_dates = input("Enter Event Dates (e.g., April 25–27, 2025): ").strip()
    event_location = input("Enter Event Location (e.g., CSI Building, UWM): ").strip()
    event_id = event_name.lower().replace(" ", "_") + "_" + event_dates.split()[0]

    # STEP 4: Marketing
    print("\n🎨 Step 4: Generate Marketing Content\n")
    audience = input("Enter Target Audience (e.g., Students, Faculty, Sponsors): ").strip()
    highlights = input("Enter Key Highlights (e.g., Prizes, Workshops, Networking): ").strip()
    tone_style = input("Enter Tone and Style (e.g., Energetic for Students, Professional for Sponsors): ").strip()

    full_marketing_content = generate_marketing_content(event_name, event_dates, event_location, audience, highlights, tone_style)
    sections = parse_sections(full_marketing_content)

    save_sections(sections)

    # Poster Generation
    poster_prompt = None
    for key in sections:
        if "poster description" in key.lower():
            poster_prompt = sections[key].strip()
            break

    if poster_prompt:
        generate_poster_images(poster_prompt)
    else:
        print("⚠️ No poster prompt found. Skipping poster generation.")

    # STEP 5: Logistics Management
    print("\n🚚 Step 5: Logistics Coordination\n")
    logistics_summary = run_logistics_flow(event_dates)

    # Final Save
    hackathon_data = {
        "event_id": event_id,
        "event_name": event_name,
        "event_dates": event_dates,
        "event_location": event_location,
        "problem_statement": problem_text,
        "sponsors": sponsor_emails,
        "marketing_materials": {
            "poster_description": sections.get("### Section 1: Event Poster Description", ""),
            "email_templates": sections.get("### Section 2: Email Templates", ""),
            "social_media_posts": sections.get("### Section 3: Social Media Posts", ""),
            "poster_slogans": sections.get("### Section 4: Poster Slogans", ""),
            "audience_segmentation": sections.get("### Section 5: Audience Segmentation", ""),
            "posting_calendar": sections.get("### Section 6: Posting Calendar", "")
        },
        "logistics_summary": logistics_summary,
        "catering_email_sent": False
    }

    save_hackathon(event_id, hackathon_data)

    print("\n✅ Hackathon Setup Successfully Completed!")

if __name__ == "__main__":
    automate_hackathon_management()