import time
import math
import sys
import random
import os
from threading import Event

sys.setrecursionlimit(10000)

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_algorithm_description():
    """Виводить детальний опис алгоритму LCA"""
    print(f"{Colors.HEADER}{Colors.BOLD}=== АЛГОРИТМ LOWEST COMMON ANCESTOR (LCA) ==={Colors.ENDC}")
    print(f"{Colors.OKBLUE}📚 ОПИС АЛГОРИТМУ:{Colors.ENDC}")
    print("""
LCA (Lowest Common Ancestor) - найнижчий спільний предок двох вершин у дереві.

🔍 МЕТОД Binary Lifting:
1️⃣  Препроцесинг: створюємо таблицю предків для кожної вершини
2️⃣  Вирівнювання глибин: піднімаємо глибшу вершину до рівня меншої
3️⃣  Синхронний підйом: піднімаємо обидві вершини до спільного предка

⚡ Складність:
   • Препроцесинг: O(n log n)
   • Запит LCA: O(log n)
   • Пам'ять: O(n log n)

🎯 ЗАСТОСУВАННЯ: генеалогічні дерева, структури даних, алгоритми на графах
    """)
    input(f"{Colors.WARNING}Натисніть Enter для продовження...{Colors.ENDC}")

def print_interface_description():
    """Виводить опис інтерфейсу програми"""
    print(f"{Colors.HEADER}{Colors.BOLD}=== ОПИС ІНТЕРФЕЙСУ ==={Colors.ENDC}")
    print(f"{Colors.OKBLUE}🎮 КЕРУВАННЯ ПРОГРАМОЮ:{Colors.ENDC}")
    print("""
📋 ГОЛОВНЕ МЕНЮ:
   • Оберіть готовий приклад дерева
   • Створіть власне дерево
   • Переглядайте ASCII-візуалізацію

🔧 РЕЖИМИ ВИКОНАННЯ:
   1️⃣  Ручний режим - натискайте Enter для кожного кроку
   2️⃣  Автоматичний режим - встановіть швидкість виконання
   3️⃣  Змішаний режим - можливість паузи в автоматичному режимі

⌨️  КОМАНДИ ПІД ЧАС ВИКОНАННЯ:
   • Enter - наступний крок (ручний режим)
   • 'p' + Enter - пауза/продовження (авто режим)
   • 'q' + Enter - вихід з поточного запиту

🎨 ВІЗУАЛІЗАЦІЯ:
   • Зелений колір - поточні активні вершини
   • Жовтий колір - важлива інформація
   • Синій колір - структура дерева
    """)
    input(f"{Colors.WARNING}Натисніть Enter для продовження...{Colors.ENDC}")

# ---------------------- Демо приклади ----------------------

def get_demo_examples():
    random.seed(42)
    n = 127
    edges = []
    parents = [0]

    for i in range(1, n):
        parent = random.choice(parents[-20:])
        edges.append((parent, i))
        parents.append(i)

    return {
        "Мале дерево (6 вершин)": {
            "n": 6,
            "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)],
            "description": "Просте дерево для демонстрації базових принципів"
        },
        "Лінійне дерево (5 вершин)": {
            "n": 5,
            "edges": [(0, 1), (1, 2), (2, 3), (3, 4)],
            "description": "Найгірший випадок - дерево у вигляді ланцюга"
        },
        "Збалансоване дерево": {
            "n": 15,
            "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), 
                     (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12), 
                     (6, 13), (6, 14)],
            "description": "Повне бінарне дерево - оптимальний випадок"
        },
        "Випадкове розгалужене дерево (127 вершин)": {
            "n": n,
            "edges": edges,
            "description": "Велике дерево для тестування продуктивності"
        }
    }

# ---------------------- Головний алгоритм ----------------------

class LCAFinder:
    def __init__(self, n, edges):
        self.n = n
        self.edges = edges
        self.tree = [[] for _ in range(n)]
        self.LOG = math.ceil(math.log2(n)) + 1 if n > 1 else 1
        self.depth = [0] * n
        self.parent = [0] * n
        self.parents = [[0] * self.LOG for _ in range(n)]
        self.visited = [False] * n
        self.paused = False
        self.stop_execution = False
        
        print(f"{Colors.OKCYAN}🔧 Ініціалізація структур даних...{Colors.ENDC}")
        self.build_tree()
        self.dfs(0, 0)
        self.preprocess()
        print(f"{Colors.OKGREEN}✅ Препроцесинг завершено!{Colors.ENDC}")

    def build_tree(self):
        for u, v in self.edges:
            self.tree[u].append(v)
            self.tree[v].append(u)

    def dfs(self, v, p):
        self.parent[v] = p
        self.visited[v] = True
        for u in self.tree[v]:
            if not self.visited[u]:
                self.depth[u] = self.depth[v] + 1
                self.dfs(u, v)

    def preprocess(self):
        print(f"{Colors.OKCYAN}📊 Створення таблиці binary lifting...{Colors.ENDC}")
        for v in range(self.n):
            self.parents[v][0] = self.parent[v]
        for i in range(1, self.LOG):
            for v in range(self.n):
                self.parents[v][i] = self.parents[self.parents[v][i - 1]][i - 1]

    def wait_for_step(self, mode, delay):
        if self.stop_execution:
            return False
            
        if mode == "manual":
            response = input(f"{Colors.WARNING}Натисніть Enter для наступного кроку (або 'q' для виходу): {Colors.ENDC}")
            if response.strip().lower() == 'q':
                self.stop_execution = True
                return False
        elif mode == "auto":
            start_time = time.time()
            while time.time() - start_time < delay:
                if self.stop_execution:
                    return False
                time.sleep(0.1)
        return True

    def lca(self, v, u, mode="manual", delay=1.0):
        self.stop_execution = False
        original_v, original_u = v, u
        
        print(f"\n{Colors.BOLD}{Colors.HEADER}🔍 ПОЧАТОК ЗАПИТУ LCA({original_v}, {original_u}){Colors.ENDC}")
        print(f"{Colors.OKCYAN}Поточні вершини: v={v} (глибина {self.depth[v]}), u={u} (глибина {self.depth[u]}){Colors.ENDC}")
        
        if not self.wait_for_step(mode, delay):
            return None

        # Етап 1: Вирівнювання глибин
        if self.depth[v] > self.depth[u]:
            v, u = u, v
            print(f"{Colors.WARNING}🔄 Міняємо місцями: тепер v={v}, u={u}{Colors.ENDC}")
            if not self.wait_for_step(mode, delay):
                return None

        print(f"\n{Colors.BOLD}📏 ЕТАП 1: Вирівнювання глибин{Colors.ENDC}")
        print(f"Різниця глибин: {self.depth[u]} - {self.depth[v]} = {self.depth[u] - self.depth[v]}")
        
        diff = self.depth[u] - self.depth[v]
        step = 0
        for k in reversed(range(self.LOG)):
            if diff >= (1 << k):
                print(f"{Colors.OKGREEN}  Крок {step + 1}: Піднімаємо u з {u} на 2^{k} = {1 << k} кроків → {self.parents[u][k]}{Colors.ENDC}")
                u = self.parents[u][k]
                diff -= (1 << k)
                step += 1
                if not self.wait_for_step(mode, delay):
                    return None

        print(f"{Colors.OKBLUE}✅ Глибини вирівняні: v={v}, u={u} (обидва на глибині {self.depth[v]}){Colors.ENDC}")
        if not self.wait_for_step(mode, delay):
            return None

        if v == u:
            print(f"{Colors.OKGREEN}🎯 Вершини співпали! LCA({original_v}, {original_u}) = {v}{Colors.ENDC}")
            return v

        print(f"\n{Colors.BOLD}⬆️  ЕТАП 2: Синхронний підйом до LCA{Colors.ENDC}")
        step = 0
        for k in reversed(range(self.LOG)):
            if self.parents[v][k] != self.parents[u][k]:
                print(f"{Colors.OKGREEN}  Крок {step + 1}: Піднімаємо на 2^{k} = {1 << k} кроків{Colors.ENDC}")
                print(f"    v: {v} → {self.parents[v][k]}")
                print(f"    u: {u} → {self.parents[u][k]}")
                v = self.parents[v][k]
                u = self.parents[u][k]
                step += 1
                if not self.wait_for_step(mode, delay):
                    return None

        result = self.parent[v]
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}🎯 РЕЗУЛЬТАТ: LCA({original_v}, {original_u}) = {result}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Фінальні позиції: v={v}, u={u}, їх батько={result}{Colors.ENDC}")
        
        return result

# ---------------------- Візуалізація дерева ----------------------

def print_tree_ascii(tree, root=0, highlight_nodes=None):
    if highlight_nodes is None:
        highlight_nodes = set()
    
    def dfs(v, prefix, is_last, parent_v):
        node_str = str(v)
        if v in highlight_nodes:
            node_str = f"{Colors.OKGREEN}{Colors.BOLD}{node_str}{Colors.ENDC}"
        
        print(prefix + ("└── " if is_last else "├── ") + node_str)
        children = [u for u in tree[v] if u != parent_v]
        children.sort() 
        for i, u in enumerate(children):
            dfs(u, prefix + ("    " if is_last else "│   "), i == len(children) - 1, v)

    n = len(tree)
    parent = [-1] * n

    def build_parents(v, p):
        parent[v] = p
        for u in tree[v]:
            if u != p:
                build_parents(u, v)

    build_parents(root, -1)
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}🌳 СТРУКТУРА ДЕРЕВА:{Colors.ENDC}")
    dfs(root, "", True, -1)

def show_tree_info(finder):
    print(f"\n{Colors.OKCYAN}📊 ІНФОРМАЦІЯ ПРО ДЕРЕВО:{Colors.ENDC}")
    print(f"  • Кількість вершин: {finder.n}")
    print(f"  • Максимальна глибина: {max(finder.depth)}")
    print(f"  • Розмір таблиці binary lifting: {finder.LOG}")
    print(f"  • Корінь дерева: 0")

# ---------------------- Меню ----------------------

def choose_execution_mode():
    print(f"\n{Colors.HEADER}🎮 ОБЕРІТЬ РЕЖИМ ВИКОНАННЯ:{Colors.ENDC}")
    print(f"  1. {Colors.OKGREEN}Ручний режим{Colors.ENDC} - покроково з натисканням Enter")
    print(f"  2. {Colors.OKBLUE}Автоматичний режим{Colors.ENDC} - з заданою швидкістю")
    
    while True:
        try:
            choice = int(input("Ваш вибір (1-2): "))
            if choice == 1:
                return "manual", 0
            elif choice == 2:
                while True:
                    try:
                        delay = float(input("Введіть затримку між кроками (секунди, наприклад 1.5): "))
                        if delay >= 0:
                            return "auto", delay
                        else:
                            print("Затримка повинна бути не менше 0")
                    except ValueError:
                        print("Введіть коректне число")
            else:
                print("Оберіть 1 або 2")
        except ValueError:
            print("Введіть коректне число")

def main():
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║     ВІЗУАЛІЗАТОР АЛГОРИТМУ LCA (Binary Lifting)          ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    examples = get_demo_examples()

    while True:
        print(f"\n{Colors.HEADER}{Colors.BOLD}📋 ГОЛОВНЕ МЕНЮ:{Colors.ENDC}")
        print(f"  1. {Colors.OKCYAN}Опис алгоритму{Colors.ENDC}")
        print(f"  2. {Colors.OKCYAN}Опис інтерфейсу{Colors.ENDC}")
        
        for i, name in enumerate(examples):
            print(f"  {i + 3}. {Colors.OKGREEN}{name}{Colors.ENDC}")
        
        print(f"  {len(examples) + 3}. {Colors.WARNING}Створити власне дерево{Colors.ENDC}")
        print(f"  0. {Colors.FAIL}Вийти{Colors.ENDC}")

        try:
            choice = int(input(f"\n{Colors.BOLD}Ваш вибір: {Colors.ENDC}"))
        except ValueError:
            print(f"{Colors.FAIL}Введіть коректне число!{Colors.ENDC}")
            continue

        if choice == 0:
            print(f"{Colors.OKCYAN}До побачення! 👋{Colors.ENDC}")
            break
        elif choice == 1:
            clear_screen()
            print_algorithm_description()
            clear_screen()
            continue
        elif choice == 2:
            clear_screen()
            print_interface_description()
            clear_screen()
            continue
        elif 3 <= choice <= len(examples) + 2:
            name = list(examples)[choice - 3]
            data = examples[name]
            print(f"\n{Colors.OKBLUE}📝 Опис: {data['description']}{Colors.ENDC}")
        elif choice == len(examples) + 3:
            try:
                n = int(input("Кількість вершин: "))
                if n <= 0:
                    print(f"{Colors.FAIL}Кількість вершин повинна бути більше 0{Colors.ENDC}")
                    continue
                    
                m = n - 1
                edges = []
                print(f"Введіть {m} ребер у форматі 'u v' (вершини від 0 до {n-1}):")
                
                for i in range(m):
                    while True:
                        try:
                            u, v = map(int, input(f"Ребро {i+1}: ").split())
                            if 0 <= u < n and 0 <= v < n:
                                edges.append((u, v))
                                break
                            else:
                                print(f"Вершини повинні бути від 0 до {n-1}")
                        except ValueError:
                            print("Введіть два числа через пробіл")
                
                data = {"n": n, "edges": edges, "description": "Користувацьке дерево"}
            except ValueError:
                print(f"{Colors.FAIL}Введіть коректне число!{Colors.ENDC}")
                continue
        else:
            print(f"{Colors.FAIL}Неправильний вибір!{Colors.ENDC}")
            continue

        try:
            finder = LCAFinder(data["n"], data["edges"])
            print_tree_ascii(finder.tree, root=0)
            show_tree_info(finder)

            while True:
                print(f"\n{Colors.HEADER}🔍 ЗАПИТИ LCA:{Colors.ENDC}")
                query = input("Введіть дві вершини для LCA (наприклад: 3 5) або 'back' для повернення: ").strip()
                
                if query.lower() == 'back':
                    break
                    
                try:
                    v, u = map(int, query.split())
                    if not (0 <= v < data["n"]) or not (0 <= u < data["n"]):
                        print(f"{Colors.FAIL}Допустимі індекси вершин: від 0 до {data['n'] - 1}{Colors.ENDC}")
                        continue
                except ValueError:
                    print(f"{Colors.FAIL}Невірний формат. Приклад: 3 4{Colors.ENDC}")
                    continue

                mode, delay = choose_execution_mode()
                
                print(f"\n{Colors.OKCYAN}Режим: {'Ручний' if mode == 'manual' else f'Автоматичний ({delay}s)'}{Colors.ENDC}")
                if mode == "auto":
                    print(f"{Colors.WARNING}Підказка: введіть 'p' щоб призупинити виконання{Colors.ENDC}")
                
                result = finder.lca(v, u, mode, delay)
                if result is not None:
                    input(f"\n{Colors.OKGREEN}Натисніть Enter для продовження...{Colors.ENDC}")

        except Exception as e:
            print(f"{Colors.FAIL}Помилка: {e}{Colors.ENDC}")
            print(f"{Colors.WARNING}Перевірте правильність введених даних{Colors.ENDC}")


if __name__ == '__main__':
    main()
