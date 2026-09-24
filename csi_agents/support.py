from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="westus3.api.azureml.ms;c5d47662-af4d-400e-ace6-ff70828d7d98;az-csi-grp1;agents"
)

support_agent_id = "asst_DXN2Ab6mMzLhLe7tOCszwhEG"

def ask_support_agent():
    print("\n🤖 Starting Support Chat! Type '2' anytime to return to main menu.")

    while True:
        print("\nOptions:")
        print("1 - Ask a new support question")
        print("2 - Exit support chat")

        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice == "1":
            user_question = input("\nType your support question: ").strip()

            if not user_question:
                print("❗ Empty question. Please type something.")
                continue

            thread = project_client.agents.create_thread()

            project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=user_question
            )

            run = project_client.agents.create_and_process_run(
                thread_id=thread.id,
                agent_id=support_agent_id
            )

            messages = project_client.agents.list_messages(thread_id=thread.id)

            print("\n🧠 Support Agent's Reply:")
            print(messages.text_messages[0].text["value"])

        elif choice == "2":
            print("\n👋 Exiting support chat...")
            break

        else:
            print("\n❌ Invalid choice. Please enter 1 or 2.")