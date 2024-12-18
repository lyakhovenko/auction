import random
from collections import defaultdict

class Agent:
    def __init__(self, agent_id, max_resources):
        self.agent_id = agent_id
        # Задаём случайное количество ресурсов для агента в интервале от 1 до max_resources
        self.resources = random.randint(1, max_resources)
        # Предложения для выполнения алгоритмов; ключи - названия алгоритмов, значения - стоимость
        self.offers = {}
        
    def create_offers(self, algorithms):
        # Генерируем случайное предложение стоимости для каждого алгоритма
        for algorithm in algorithms:
            # Стоимость выполнения - случайное число в зависимости от ресурсов агента
            self.offers[algorithm] = random.randint(1, self.resources//2)
    
    def get_best_offer(self):
        sorted_offers = sorted(self.offers.items(), key=lambda x: x[1])
        return sorted_offers[0] if sorted_offers else None

class Auction:
    def __init__(self, agents, algorithms):
        self.agents = agents
        self.algorithms = algorithms
        self.winners = {}
        
    def run_auction(self):
        # Шаг 5: Проверка предложений и исключение алгоритмов с единственным предложением
        #for algorithm in self.algorithms:
            #valid_offers = {agent.agent_id: agent.offers[algorithm] for agent in self.agents if algorithm in agent.offers}
                            # and len(agent.offers) > 1}
            #if len(valid_offers) > 0:
                #for _ in len(valid_offers):
                # Шаг 6: Выбор аукционера
                for agent in self.agents:
                    auctioneer = agent.agent_id
                    best_offer = self.agents[auctioneer].get_best_offer()
                    
                    # Определяем, кто ещё предложил лучший алгоритм
                    bidders = [agent.agent_id for agent in self.agents if best_offer[0] in agent.offers and agent.offers[best_offer[0]] == best_offer[1]]
                    
                    if len(bidders) > 0:
                        # Шаг 8: Формируем структуру данных с идентификаторами участников
                        self.winners[best_offer[0]] = bidders
                    else: self.winners[best_offer[0]] = self.agents[auctioneer]

                return self.winners

def main():
    # Шаг 1: Цель
    goal = "Распределение задач"
    
    # Шаг 2: Определяем набор алгоритмов
    algorithms = [f'alg{i+1}' for i in range(5)]  # Например, 5 алгоритмов
    
    # Создание 10 агентов с максимумом ресурсов 100
    agents = [Agent(agent_id=i, max_resources=100) for i in range(10)]
    
    # Генерация предложений для каждого агента
    for agent in agents:
        agent.create_offers(algorithms)
        print(agent.agent_id, agent.offers)
    
    # Шаг 3: Инициализация аукциона
    auction = Auction(agents, algorithms)
    
    # Запуск аукциона и получение победителей
    winners = auction.run_auction()
    
    # Печатаем результаты аукциона
    print(f"Результаты аукциона для цели: {goal}")
    #for agent in agents:
         #print(f"Агент {agent.agent_id} будет выполнять: {[f'Алгоритм {algorithms}' for winner in winners]}")
    for algorithm, bidders in winners.items():
        print(f"Алгоритм {algorithm} будет выполнять: {[f'Агент {bidder}' for bidder in bidders]}")

if __name__ == "__main__":
    main()