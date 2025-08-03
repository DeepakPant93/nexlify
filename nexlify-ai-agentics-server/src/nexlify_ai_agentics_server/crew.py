from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from crewai.llm import LLM
from nexlify_ai_agentics_server.tools.nexlify_search_tool import NexlifySearchTool
from crewai_tools import SerperDevTool

MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL = os.getenv("MODEL")
# Set the Google API key for SerperDevTool
os.environ["GOOGLE_API_KEY"] = os.getenv("MODEL_API_KEY")

@CrewBase
class NexlifyAiAgenticsServer():
	"""NexlifyAiAgenticsServer crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	llm = LLM(model=MODEL, api_key=MODEL_API_KEY, temperature=0.7)

	# Initialize the tools
	web_search_tool = SerperDevTool(
    country="in",  # Set to 'in' for India
    locale="en",  # Set locale to English
    n_results=3,  # You can adjust the number of results as needed
	)
	nexlify_search_tool = NexlifySearchTool()




	@agent
	def vector_db_searcher(self) -> Agent:
		return Agent(
			config=self.agents_config['vector_db_searcher'],
			llm=self.llm,
			verbose=True
		)

	@agent
	def internet_searcher(self) -> Agent:
		return Agent(
			config=self.agents_config['internet_searcher'],
			llm=self.llm,
			verbose=True
		)

	@agent
	def result_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['result_analyzer'],
			llm=self.llm,
			verbose=True
		)

	@task
	def vector_db_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['vector_db_search_task'],
			llm=self.llm,
			tools=[self.nexlify_search_tool],
		)

	@task
	def internet_search_task(self) -> Task:
		return Task(
			config=self.tasks_config['internet_search_task'],
			llm=self.llm,
			tools=[self.web_search_tool],
		)

	@task
	def result_analyzer_task(self) -> Task:
		return Task(
			config=self.tasks_config['result_analyzer_task'],
			llm=self.llm,
			context=[
				self.vector_db_search_task(),
				self.internet_search_task(),
			]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the NexlifyAiAgenticsServer crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			name='NexlifyAiAgenticsServer',
		)
