from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from mentormindflows.tools.writeFile_tool import WriteFileTool

@CrewBase
class PeerComparisonCrew:
    agents_config = "config/peercomparison_agents.yaml"
    tasks_config = "config/peercomparison_tasks.yaml"

    ollama_llm = LLM(
        model='ollama/llama3.2:3b',
        base_url='http://localhost:11434',
    )

    @agent
    def data_comparing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_comparing_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )
    
    @agent
    def insight_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["insight_generator_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )
    
    @agent
    def mindmap_visualizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["mindmap_visualizer_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )

    @task
    def compare_with_peers_task(self) -> Task:
        return Task(
            config=self.tasks_config["compare_with_peers_task"],
        )
    
    @task
    def generate_peer_insights_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_peer_insights_task"],
        )


    @task
    def visualize_peer_mindmap_task(self) -> Task:
        return Task(
            config=self.tasks_config["visualize_peer_mindmap_task"],
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )