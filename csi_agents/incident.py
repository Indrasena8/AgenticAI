import json
import os
import re
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Paths
MENTORS_FILE = "/Users/indrasena/Indrasena/Studies/CS/Semester4/Agentic AI/AgenticAI/Mentors_data.json"
INCIDENT_FOLDER = "/Users/indrasena/Indrasena/Studies/CS/Semester4/Agentic AI/hackathons/incidents"

# Connect to Azure AI Project
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="westus3.api.azureml.ms;c5d47662-af4d-400e-ace6-ff70828d7d98;az-csi-grp1;agents"
)

# Your Incident Agent ID
incident_agent_id = "asst_64VB33nDaUxHPTA5yLRWSRjg"

# ===========================
# Load Mentors
# ===========================
def load_mentors():
    if not os.path.exists(MENTORS_FILE):
        print("❌ Mentors file not found.")
        return []
    with open(MENTORS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ===========================
# Log Incident to File
# ===========================
def log_incident(event_id, incident_type, message):
    os.makedirs(INCIDENT_FOLDER, exist_ok=True)
    incident_file = os.path.join(INCIDENT_FOLDER, f"{event_id}_incidents.json")
    
    incident_entry = {
        "Time": "TBD",  # Optional: later we can add real timestamps
        "Type": incident_type,
        "Message": message
    }
    
    incidents = []
    if os.path.exists(incident_file):
        with open(incident_file, "r", encoding="utf-8") as f:
            incidents = json.load(f)

    incidents.append(incident_entry)

    with open(incident_file, "w", encoding="utf-8") as f:
        json.dump(incidents, f, indent=4)
    print(f"📝 Incident logged for event '{event_id}'.")

# ===========================
# Ask Azure AI Agent for Mentor Suggestions
# ===========================
def ask_agent_for_mentor_recommendation(theme_text, mentors):
    # Format mentors neatly
    mentor_list_text = "\n".join([
        f"- {mentor['Name']}: Skills({', '.join(mentor['Skills'])}), Trust({mentor['Confidence']}%), Available({mentor['Available']})"
        for mentor in mentors
    ])

    input_prompt = f"""
Hackathon Problem Theme:

{theme_text}

List of Available Mentors:

{mentor_list_text}

Task:
Recommend the best mentor replacements based on skills matching the theme and highest trust/confidence.
Only return structured recommendations (Name, Skills, Confidence, Match %).

DO NOT write full emails or essays.
    """

    # Create new conversation thread
    thread = project_client.agents.create_thread()

    # Send user message
    project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=input_prompt
    )

    # Run agent
    run = project_client.agents.create_and_process_run(
        thread_id=thread.id,
        agent_id=incident_agent_id
    )

    # Get response
    messages = project_client.agents.list_messages(thread_id=thread.id)
    return messages.text_messages[0].text["value"]

# ===========================
# Mentor Drop and Match Main Flow
# ===========================
def mentor_drop_and_match(event_id):
    # Load event info
    event_file = os.path.join("hackathons", f"{event_id}.json")
    if not os.path.exists(event_file):
        print("❌ Event file not found.")
        return

    with open(event_file, "r", encoding="utf-8") as f:
        event_data = json.load(f)

    theme_text = event_data.get("problem_statement", "")

    # Load mentors
    mentors = load_mentors()
    if not mentors:
        return

    # Ask Azure Agent
    print("\n📡 Asking AI Incident Agent for Mentor Recommendations...\n")
    suggestions = ask_agent_for_mentor_recommendation(theme_text, mentors)

    print("\n✅ Mentor Suggestions Received:\n")
    print(suggestions)

    # Log the incident
    message = f"Mentor dropped. Recommendations provided:\n{suggestions}"
    log_incident(event_id, "Mentor Drop + Suggestions", message)

# ===========================
# Optional: For quick testing
# ===========================
if __name__ == "__main__":
    event_id = input("Enter Event ID (example: mental_health_april): ").strip()
    mentor_drop_and_match(event_id)
