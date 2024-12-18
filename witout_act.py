import random

class Agent:
    def __init__(self, agent_id, resources):
        self.agent_id = agent_id
        self.resources = resources
        self.assigned_tasks = []

class TaskAssignment:
    def __init__(self, agents, algorithms):
        self.agents = sorted(agents, key=lambda agent: agent.resources)
        self.algorithms = dict(sorted(algorithms.items(), key=lambda item: item[1])) # Преобразуем в словарь для удобного доступа

    def assign_tasks(self):
        available_algorithms = list(self.algorithms.items()) #Создаем список кортежей (alg_id, cost)
        for agent in self.agents:
            for i, (alg_id, cost) in enumerate(available_algorithms[:]): # Используем срез, чтобы безопасно удалять элементы
                if agent.resources >= cost:
                    agent.assigned_tasks.append(alg_id)
                    agent.resources -= cost
                    del available_algorithms[i] # Удаляем элемент по индексу
                    break

        print("Распределение задач:")
        for agent in self.agents:
            print(f"Агент {agent.agent_id} (ресурсы: {agent.resources}): {agent.assigned_tasks}")

        total_resources_used = sum(self.algorithms[alg_id] for agent in self.agents for alg_id in agent.assigned_tasks)
        print(f"Всего использовано ресурсов: {total_resources_used}")


# Пример использования:
agents = [Agent(i, random.randint(1, 100)) for i in range(10)]
algorithms = {f"alg{i}": random.randint(50, 150) for i in range(5)}

task_assignment = TaskAssignment(agents, algorithms)
task_assignment.assign_tasks()