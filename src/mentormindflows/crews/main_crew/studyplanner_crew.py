from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class StudyPlannerCrew:
    """StudyPlanner Crew for generating personalized weekly Study plans for the student."""

    agents_config = "config/studyplanner_agents.yaml"
    tasks_config = "config/studyplanner_tasks.yaml"

    # Using LLaMA 3.2 3B model hosted on Ollama
    ollama_llm = LLM(
        model='ollama/llama3.2:3b',
        base_url='http://localhost:11434',
    )

    @agent
    def study_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["study_analyst_agent"],
            llm=self.ollama_llm,
            verbose=True, 
        )

    @agent
    def time_manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["time_manager_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )

    @agent
    def plan_formatter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["plan_formatter_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )

    @task
    def analyze_academics_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_academics_task"], 
        )

    @task
    def generate_schedule_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_schedule_task"],
        )
    
    @task
    def format_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config["format_plan_task"],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the StudyPlanner Crew with intelligent guidance agents."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
