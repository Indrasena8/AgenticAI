# logistics_agent.py

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import smtplib
from email.mime.text import MIMEText

# Connect to Azure AI Project
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="westus3.api.azureml.ms;c5d47662-af4d-400e-ace6-ff70828d7d98;az-csi-grp1;agents"
)

logistics_agent_id = "asst_7q2GEyVdK37emTrPu8skkbkM"

def get_catering_summary(event_date, event_time, event_location):
    thread = project_client.agents.create_thread()

    catering_prompt = f"""
We are preparing catering for the upcoming hackathon.

Event Date: {event_date}
Event Time: {event_time}
Event Location: {event_location}

Please summarize the catering needs according to your guidelines.
"""

    project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=catering_prompt
    )

    run = project_client.agents.create_and_process_run(
        thread_id=thread.id,
        agent_id=logistics_agent_id
    )

    messages = project_client.agents.list_messages(thread_id=thread.id)

    catering_summary = messages.text_messages[0].text["value"]

    return catering_summary

def send_catering_email(summary_text, catering_team_email, from_email, from_password):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = "Hackathon Catering Requirements"

    body = f"""
Dear Catering Team,

Here are the summarized catering requirements for our upcoming hackathon:

{summary_text}

Please let us know if you need any further information.

Thank you,
Hackathon Logistics Team
""".strip()

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = catering_team_email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, catering_team_email, msg.as_string())
    server.quit()

    print(f"✅ Catering email sent successfully to {catering_team_email}")

def run_logistics_flow(event_date):
    print("\n🚚 Logistics: Preparing catering requirements...\n")

    event_time = input("Enter Event Time (e.g., 12 PM to 5 PM): ").strip()
    event_location = input("Enter Event Location (e.g., CSI Building, UWM): ").strip()

    summary = get_catering_summary(event_date, event_time, event_location)

    print("\n📝 Catering Summary:\n")
    print(summary)

    choice = input("\nDo you want to send this summary to the catering team? (yes/no): ").strip().lower()

    if choice == "yes":
        catering_team_email = "indrasenakalyanam@gmail.com"  # You can replace this later
        from_email = "kindrasena8@gmail.com"
        from_password = "sdecbbhtntaqoysp"

        send_catering_email(summary, catering_team_email, from_email, from_password)
    else:
        print("\n🚫 Skipped sending email.")