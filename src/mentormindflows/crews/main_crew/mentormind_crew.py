# from crewai import LLM, Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# # from crewai_tools import FileWriterTool, FileReadTool
# from mentormindflows.tools.writeFile_tool import WriteFileTool

# # file_writer_studyplan = FileWriterTool(file_name="study_plan.md",directory="outputs",overwrite="True")
# # file_writer_career = FileWriterTool(file_name="career_guide.md",directory="outputs",overwrite="True")
# # file_writer_peer_comparison = FileWriterTool(file_name="peer_comparison.md",directory="outputs",overwrite="True")

# @CrewBase
# class MentorMindCrew:
#     """MentorMind Crew for generating personalized student recommendations and guidance."""

#     agents_config = "config/agents.yaml"
#     tasks_config = "config/tasks.yaml"

#     # Using LLaMA 3.2 3B model hosted on Ollama
#     ollama_llm = LLM(
#         model='ollama/llama3.2:3b',
#         base_url='http://localhost:11434',
#     )

#     @agent
#     def study_planner_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["study_planner_agent"],
#             llm=self.ollama_llm,
#             verbose=True,
#             tools=[WriteFileTool()],            
#         )

#     @agent
#     def career_guide_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["career_guide_agent"],
#             llm=self.ollama_llm,
#             verbose=True,
#             tools=[WriteFileTool()],
#         )

#     @agent
#     def peer_comparison_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["peer_comparison_agent"],
#             llm=self.ollama_llm,
#             verbose=True,
#             tools=[WriteFileTool()],
#         )
    
#     @agent
#     def report_generator_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["report_generator_agent"],
#             llm=self.ollama_llm,
#             verbose=True,
#         )

#     @task
#     def study_planner_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["study_planner_task"], 
#         )

#     @task
#     def career_guide_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["career_guide_task"],
#         )

#     @task
#     def peer_comparison_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["peer_comparison_task"],
#         )
    
#     @task
#     def report_generator_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["report_generator_task"],
#         )


#     @crew
#     def crew(self) -> Crew:
#         """Creates the MentorMind Crew with intelligent guidance agents."""
#         return Crew(
#             agents=self.agents,
#             tasks=self.tasks,
#             process=Process.sequential,
#             verbose=True,
#         )
