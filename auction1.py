import random

class Agent:
    def __init__(self, agent_id, resources):
        self.agent_id = agent_id
        self.resources = resources
        self.assigned_tasks = []

    def generate_offer(self, algorithms):
        offer = {}
        for alg_id, alg_cost in algorithms.items():
            # Простая стратегия ценообразования: случайная стоимость в пределах доступных ресурсов
            offer[alg_id] = random.randint(1, min(alg_cost, self.resources))  
        return offer

    def sort_offer(self, offer):
        return dict(sorted(offer.items(), key=lambda item: item[1]))

    def is_best_algorithm(self, algorithm_id, sorted_offer):
      return list(sorted_offer.keys())[0] == algorithm_id


class Auction:
    def __init__(self, agents, algorithms, goal):
        self.agents = agents
        self.algorithms = algorithms
        self.goal = goal
        self.total_resources_limit = 1000
        self.available_algorithms = algorithms.copy()

    def run_auction(self):
        # Шаг 3: Каждый агент формирует ценовой массив
        offers = {agent.agent_id: agent.generate_offer(self.available_algorithms) for agent in self.agents}
        #print('offers: ', offers)

        # Шаг 4: Каждый агент сортирует предложения
        sorted_offers = {agent_id: agents[agent_id].sort_offer(offer) for agent_id, offer in offers.items()}
        #print('sorted_offers: ', sorted_offers)


        # Шаг 5: Удаление алгоритмов с одним предложением
        algorithms_to_remove = set()
        for agent_id, offer in sorted_offers.items():
            for alg_id, cost in offer.items():
              if list(offers.values()).count(alg_id) == 1:
                algorithms_to_remove.add(alg_id)
                self.agents[agent_id].assigned_tasks.append(alg_id)


        self.available_algorithms = {k: v for k, v in self.available_algorithms.items() if k not in algorithms_to_remove}
        #print(self.available_algorithms)

        # Шаг 6-8 (улучшенная, но все еще упрощенная версия):
        available_agents = [agent for agent in self.agents if not agent.assigned_tasks]
        available_algorithms = list(self.available_algorithms.keys())
        random.shuffle(available_algorithms) #случайный порядок для более равномерного распределения


        for alg_id in available_algorithms:
            best_agent = None
            min_cost = float('inf')
            for agent in available_agents:
                if alg_id in sorted_offers[agent.agent_id]:
                  cost = sorted_offers[agent.agent_id][alg_id]
                  if cost < min_cost:
                      min_cost = cost
                      best_agent = agent

            if best_agent:
              best_agent.assigned_tasks.append(alg_id)
              available_agents.remove(best_agent)


        print("Распределение задач:")
        for agent in self.agents:
            print(f"Агент {agent.agent_id}: {agent.assigned_tasks}")
        total_resources_used = sum(self.algorithms[alg_id] for agent in self.agents for alg_id in agent.assigned_tasks)
        print(f"Всего использовано ресурсов: {total_resources_used}")

#Пример использования:

agents = [Agent(i, random.randint(1, 100)) for i in range(10)]
algorithms = {f"alg{i}": random.randint(50, 150) for i in range(5)} # Пример 5 алгоритмов
goal = "Общая цель"

auction = Auction(agents, algorithms, goal)
auction.run_auction()