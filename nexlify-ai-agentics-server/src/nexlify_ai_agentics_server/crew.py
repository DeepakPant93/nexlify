from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from crewai.llm import LLM

MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL = os.getenv("MODEL")

@CrewBase
class NexlifyAiAgenticsServer():
	"""NexlifyAiAgenticsServer crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	llm = LLM(model=MODEL, api_key=MODEL_API_KEY, temperature=0.7)

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			llm=self.llm,
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			llm=self.llm,
			verbose=True
		)


	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			llm=self.llm,
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			llm=self.llm,
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
