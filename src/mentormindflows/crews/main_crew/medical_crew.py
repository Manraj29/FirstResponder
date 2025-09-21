from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from mentormindflows.tools.csv_logger_tool import CSVLoggerTool
from mentormindflows.crews.gmailcrew.tools.gmail_tool import GmailTool

# Ensure Gemini API key is available for litellm
_api_key = os.getenv("GEMINI_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if _api_key:
    os.environ.setdefault("GOOGLE_API_KEY", _api_key)
    os.environ.setdefault("GEMINI_API_KEY", _api_key)

# Toolsn=
csv_logger_tool = CSVLoggerTool()
gmail_tool = GmailTool()

@CrewBase
class MedicalCrew:
    agents_config = "config/medical_agents.yaml"
    tasks_config = "config/medical_tasks.yaml"

    gemini_llm = LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.7
    )

    @agent
    def notify_authority_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["notify_authority_agent"],
            llm=self.gemini_llm,
            verbose=True,
            tools=[gmail_tool],
        )

    @agent
    def guidance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["guidance_agent"],
            llm=self.gemini_llm,
            verbose=True,
        )

    @agent
    def data_logger_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_logger_agent"],
            llm=self.gemini_llm,
            verbose=True,
            tools=[csv_logger_tool],
        )

    @task
    def provide_guidance_task(self) -> Task:
        return Task(
            config=self.tasks_config["guidance_collect_info"],
        )

    @task
    def log_incident_task(self) -> Task:
        return Task(
            config=self.tasks_config["log_incident"],
        )

    @task
    def notify_authorities_task(self) -> Task:
        return Task(
            config=self.tasks_config["notify_authority"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
