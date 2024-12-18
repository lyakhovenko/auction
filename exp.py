import random
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, agent_id, resources):
        self.agent_id = agent_id
        self.resources = resources
        self.assigned_tasks = []
        self.bids = {}

    def generate_bid(self, algorithm_id, algorithm_cost):
        max_bid = int(algorithm_cost * 0.9)
        return random.randint(1, max(1, max_bid))


class TaskAssignment:
    def __init__(self, agents, algorithms):
        self.agents = sorted(agents, key=lambda agent: agent.resources)
        self.algorithms = dict(sorted(algorithms.items(), key=lambda item: item[1]))

    def assign_tasks(self):
        available_algorithms = list(self.algorithms.items())
        for agent in self.agents:
            for i, (alg_id, cost) in enumerate(available_algorithms[:]):
                if agent.resources >= cost:
                    agent.assigned_tasks.append(alg_id)
                    agent.resources -= cost
                    del available_algorithms[i]
                    break

        return sum(self.algorithms[alg_id] for agent in self.agents for alg_id in agent.assigned_tasks), len(sum((agent.assigned_tasks for agent in self.agents),[]))


class Auction:
    def __init__(self, agents, algorithms, resource_limit=1000):
        self.agents = agents
        self.algorithms = algorithms
        self.resource_limit = resource_limit
        self.available_algorithms = list(algorithms.items())
        self.total_resources_used = 0

    def run_auction(self):
        for alg_id, cost in self.available_algorithms:
            bids = {}
            for agent in self.agents:
                if agent.resources >= cost:
                    bid = agent.generate_bid(alg_id, cost)
                    bids[agent.agent_id] = bid
                    agent.bids[alg_id] = bid

            if bids:
                winning_agent_id = max(bids, key=bids.get)
                winning_agent = next((agent for agent in self.agents if agent.agent_id == winning_agent_id), None)

                if winning_agent:
                    winning_agent.assigned_tasks.append(alg_id)
                    winning_agent.resources -= cost
                    self.total_resources_used += cost

        return self.total_resources_used, len(sum((agent.assigned_tasks for agent in self.agents),[]))



def run_simulation(num_iterations, num_agents, num_algorithms):
    auction_results = []
    no_auction_results = []

    for _ in range(num_iterations):
        agents = [Agent(i, random.randint(1, 100)) for i in range(num_agents)]
        algorithms = {f"alg{i}": random.randint(50, 150) for i in range(num_algorithms)}

        #Auction simulation
        auction = Auction(agents.copy(), algorithms) #Создаем копии агентов для каждого запуска
        auction_resources_used, auction_tasks_completed = auction.run_auction()
        auction_results.append((auction_resources_used, auction_tasks_completed))


        #No auction simulation
        task_assignment = TaskAssignment(agents.copy(), algorithms)
        no_auction_resources_used, no_auction_tasks_completed = task_assignment.assign_tasks()
        no_auction_results.append((no_auction_resources_used, no_auction_tasks_completed))

    return auction_results, no_auction_results


num_iterations = 100
num_agents = 10
num_algorithms = 5

auction_results, no_auction_results = run_simulation(num_iterations, num_agents, num_algorithms)

# Подготовка данных для графиков
auction_resources = [result[0] for result in auction_results]
auction_tasks = [result[1] for result in auction_results]
no_auction_resources = [result[0] for result in no_auction_results]
no_auction_tasks = [result[1] for result in no_auction_results]


for i in auction_resources:
    if i == 0:
        auction_resources.remove(i)
print(auction_resources)


for i in no_auction_resources:
    if i == 0:
        no_auction_resources.remove(i)
# Построение графиков
plt.figure(figsize=(12, 6))  # Увеличиваем размер фигуры для лучшей читаемости

# График 1: Использование ресурсов
#plt.subplot(1, 2, 1)  # Создаем подграфик 1x2, выбираем первый
plt.plot(auction_resources, label="С аукционом", color='blue')
plt.plot(no_auction_resources, label="Без аукциона", color='red')
plt.xlabel("Итерация")
plt.ylabel("Использование ресурсов")
plt.title("Использование ресурсов")
plt.legend()

'''
# График 2: Количество выполненных задач
plt.subplot(1, 2, 2)  # Создаем подграфик 1x2, выбираем второй
plt.plot(auction_tasks, label="С аукционом", color='blue')
plt.plot(no_auction_tasks, label="Без аукциона", color='red')
plt.xlabel("Итерация")
plt.ylabel("Количество задач")
plt.title("Количество выполненных задач")
plt.legend()
'''
plt.tight_layout()  # Автоматически корректирует расположение подграфиков
plt.show()

avg_auction_resources = sum(result[0] for result in auction_results) / num_iterations
avg_auction_tasks = sum(result[1] for result in auction_results) / num_iterations
avg_no_auction_resources = sum(result[0] for result in no_auction_results) / num_iterations
avg_no_auction_tasks = sum(result[1] for result in no_auction_results) / num_iterations

print("Результаты симуляции:")
print(f"Среднее использование ресурсов (с аукционом): {avg_auction_resources:.2f}")
#print(f"Среднее количество выполненных задач (с аукционом): {avg_auction_tasks:.2f}")
print(f"Среднее использование ресурсов (без аукциона): {avg_no_auction_resources:.2f}")
#print(f"Среднее количество выполненных задач (без аукциона): {avg_no_auction_tasks:.2f}")