import heapq #utilizada para realizar una cola de prioridad para ek algoritmo de dijstra
from collections import defaultdict #Proporciona un diccionario con valores por defecto.
import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Función para cargar destinos y vuelos desde un archivo
def load_data(filename):
    destinations = {}
    flights = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        mode = None
        for line in lines:
            line = line.strip()
            if line == "# Destinos":
                mode = "destinos"
                continue
            elif line == "# Vuelos":
                mode = "vuelos"
                continue

            if mode == "destinos" and line:
                code, name, visa_required = line.split(',')
                destinations[code] = {"name": name, "visa_required": visa_required == "Yes"}
            elif mode == "vuelos" and line:
                src, dst, cost = line.split(',')
                flights.append((src, dst, float(cost)))
                flights.append((dst, src, float(cost)))  # Asumimos vuelos bidireccionales
    return destinations, flights

# Función para construir el grafo de vuelos
def build_graph(flights):
    graph = defaultdict(list)
    for src, dst, cost in flights:
        graph[src].append((dst, cost))
    return graph

# Función para encontrar la ruta más barata usando Dijkstra
def find_cheapest_route(graph, destinations, start, end, has_visa):
    heap = [(0, start, [])]
    visited = set()

    while heap:
        cost, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        
        if node == end:
            return cost, path
        
        for neighbor, price in graph[node]:
            if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
                heapq.heappush(heap, (cost + price, neighbor, path))
    
    return float("inf"), []


# Función para encontrar la ruta con menos escalas usando Dijkstra
def find_shortest_route(graph, destinations, start, end, has_visa):
    heap = [(0, start, [])]  # (number of stops, current node, path)
    visited = set()

    while heap:
        stops, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        
        if node == end:
            total_cost = sum(graph[path[i]][j][1] for i in range(len(path)-1) for j in range(len(graph[path[i]])) if graph[path[i]][j][0] == path[i+1])
            return stops, path, total_cost
        
        for neighbor, _ in graph[node]:
            if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
                heapq.heappush(heap, (stops + 1, neighbor, path))
    
    return float("inf"), [], 0

# Función para mostrar el menú
def show_menu(root, destinations, flights, graph):
    root.title("Metro Travel")
    root.geometry("400x300")

    tk.Label(root, text="Bienvenido a Metro Travel", font=("Arial", 16)).pack(pady=10)

    def print_destinations():
        dest_window = tk.Toplevel(root)
        dest_window.title("Destinos Cargados")
        dest_window.geometry("400x300")

        text = tk.Text(dest_window, wrap=tk.WORD)
        text.pack(expand=True, fill=tk.BOTH)

        dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
        text.insert(tk.END, dest_str)
        text.config(state=tk.DISABLED)  # Desactivar la edición del widget de texto

    def print_flights():
        flights_window = tk.Toplevel(root)
        flights_window.title("Vuelos Cargados")
        flights_window.geometry("400x300")

        text = tk.Text(flights_window, wrap=tk.WORD)
        text.pack(expand=True, fill=tk.BOTH)

        flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
        text.insert(tk.END, flights_str)
        text.config(state=tk.DISABLED) 

    # def draw_graph(canvas, graph, destinations, path=[], route_info=""):
    #     canvas.delete("all")
    #     nodes = list(destinations.keys())
    #     pos = {}
    #     # Aumentar el tamaño del área de dibujo para mejorar la visibilidad
    #     width, height = 800, 600
    #     canvas.config(width=width, height=height)
    #     for node in nodes:
    #         pos[node] = (random.randint(50, width - 50), random.randint(50, height - 50))
        
    #     for node, neighbors in graph.items():
    #         x1, y1 = pos[node]
    #         canvas.create_oval(x1-10, y1-10, x1+10, y1+10, fill="skyblue")
    #         canvas.create_text(x1, y1, text=node, fill="black")
    #         for neighbor, cost in neighbors:
    #             x2, y2 = pos[neighbor]
    #             if (node in path and neighbor in path and 
    #                 abs(path.index(node) - path.index(neighbor)) == 1):
    #                 canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
    #             else:
    #                 canvas.create_line(x1, y1, x2, y2, fill="gray")
    #             mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    #             canvas.create_text(mid_x, mid_y, text=f"${cost:.2f}", fill="red")
        
    #     if route_info:
    #         canvas.create_text(width / 2, height - 20, text=route_info, fill="blue", font=("Arial", 10, "bold"))



    def draw_graph(canvas, graph, destinations, path=[], route_info=""):
        canvas.delete("all")
        nodes = list(destinations.keys())
        pos = {}
        # Aumentar el tamaño del área de dibujo para mejorar la visibilidad
        width, height = 800, 600
        canvas.config(width=width, height=height)
        for node in nodes:
            pos[node] = (random.randint(50, width - 50), random.randint(50, height - 50))
        
        for node, neighbors in graph.items():
            x1, y1 = pos[node]
            # Ajustar el radio del círculo para que el texto quede dentro
            radius = 20
            canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius, fill="pink")
            canvas.create_text(x1, y1, text=node, fill="black", font=("Arial", 10, "bold"))
            for neighbor, cost in neighbors:
                x2, y2 = pos[neighbor]
                if (node in path and neighbor in path and 
                    abs(path.index(node) - path.index(neighbor)) == 1):
                    canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
                else:
                    canvas.create_line(x1, y1, x2, y2, fill="gray")
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                canvas.create_text(mid_x, mid_y, text=f"${cost:.2f}", fill="red")

        if route_info:
            canvas.create_text(width / 2, height - 20, text=route_info, fill="blue", font=("Arial", 15, "bold"))

   

    def print_graph_gui(path=[], route_info=""):
        if not path:  # Si no hay ruta válida, muestra un mensaje en lugar del grafo
            messagebox.showinfo("Información", route_info)
            return
        
        graph_window = tk.Toplevel()
        graph_window.title("Grafo de vuelos")
        graph_window.geometry("800x600")

        # Crear un frame para contener el lienzo y la barra de desplazamiento
        frame = tk.Frame(graph_window)
        frame.pack(fill=tk.BOTH, expand=tk.YES)

        canvas = tk.Canvas(frame, width=800, height=600, bg="white")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        # Crear una barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar la barra de desplazamiento para que se mueva con el lienzo
        canvas.configure(yscrollcommand=scrollbar.set)

        draw_graph(canvas, graph, destinations, path, route_info)

        # Ajustar el tamaño del lienzo al contenido
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        graph_window.mainloop()
    
    def print_graph_gui_vuelos(path=[], route_info=""):
        graph_window = tk.Toplevel(root)
        graph_window.title("Grafo de vuelos")
        graph_window.geometry("800x600")  # Ajustar el tamaño de la ventana para que coincida con el tamaño del lienzo

        canvas = tk.Canvas(graph_window, width=800, height=600, bg="white")
        canvas.pack()

        draw_graph(canvas, graph, destinations, path, route_info)




    def search_route():
        start = None
        end = None
        
        while start not in destinations:
            start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
            if start not in destinations:
                messagebox.showerror("Error", "Código de aeropuerto de origen no válido. Vuelve a ingresar un código existente.")
        
        while end not in destinations:
            end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
            if end not in destinations:
                messagebox.showerror("Error", "Código de aeropuerto de destino no válido. Vuelve a ingresar un código existente.")
        
        while True:
            visa_input = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower()
            if visa_input == "si":
                has_visa = True
                break
            elif visa_input == "no":
                has_visa = False
                break
            else:
                messagebox.showerror("Error", "Por favor, ingresa 'si' o 'no'.")

        route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

        if route_type == "costo":
            cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
            if cost == float("inf"):
                route_info = "No hay ruta disponible que cumpla con los requisitos."
            else:
                route_info = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
            print_graph_gui(cheapest_path, route_info)
           
        elif route_type == "escalas":
            stops, shortest_path, total_cost = find_shortest_route(graph, destinations, start, end, has_visa)
            if stops == float("inf"):
                route_info = "No hay ruta disponible que cumpla con los requisitos."
            else:
                route_info = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}\nCosto total: ${total_cost:.2f}"
            print_graph_gui(shortest_path, route_info)
            
        else:
            messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

    tk.Button(root, text="Imprimir destinos cargados", width=30, command=print_destinations).pack(pady=10)
    tk.Button(root, text="Imprimir vuelos cargados", width=30, command=print_flights).pack(pady=10)
    tk.Button(root, text="Imprimir grafo de vuelos", width=30, command=lambda: print_graph_gui_vuelos()).pack(pady=10)
    tk.Button(root, text="Buscar ruta", width=30, command=search_route).pack(pady=10)
    tk.Button(root, text="Salir", width=30, command=root.destroy).pack(pady=10)

# Función principal
def main():
    # Cargar destinos y vuelos desde el archivo
    destinations, flights = load_data('flights.txt')
    graph = build_graph(flights)

    root = tk.Tk()

    show_menu(root, destinations, flights, graph)

    root.mainloop()

if __name__ == "__main__":
    main()





# import heapq
# from collections import defaultdict
# import tkinter as tk
# from tkinter import simpledialog, messagebox
# import random

# # Función para cargar destinos y vuelos desde un archivo
# def load_data(filename):
#     destinations = {}
#     flights = []
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#         mode = None
#         for line in lines:
#             line = line.strip()
#             if line == "# Destinos":
#                 mode = "destinos"
#                 continue
#             elif line == "# Vuelos":
#                 mode = "vuelos"
#                 continue

#             if mode == "destinos" and line:
#                 code, name, visa_required = line.split(',')
#                 destinations[code] = {"name": name, "visa_required": visa_required == "Yes"}
#             elif mode == "vuelos" and line:
#                 src, dst, cost = line.split(',')
#                 flights.append((src, dst, float(cost)))
#                 flights.append((dst, src, float(cost)))  # Asumimos vuelos bidireccionales
#     return destinations, flights

# # Función para construir el grafo de vuelos
# def build_graph(flights):
#     graph = defaultdict(list)
#     for src, dst, cost in flights:
#         graph[src].append((dst, cost))
#     return graph

# # Función para encontrar la ruta más barata usando Dijkstra
# def find_cheapest_route(graph, destinations, start, end, has_visa):
#     heap = [(0, start, [])]
#     visited = set()

#     while heap:
#         cost, node, path = heapq.heappop(heap)
#         if node in visited:
#             continue
#         path = path + [node]
#         visited.add(node)
        
#         if node == end:
#             return cost, path
        
#         for neighbor, price in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (cost + price, neighbor, path))
    
#     return float("inf"), []

# # Función para encontrar la ruta con menos escalas usando Dijkstra
# def find_shortest_route(graph, destinations, start, end, has_visa):
#     heap = [(0, start, [])]  # (number of stops, current node, path)
#     visited = set()

#     while heap:
#         stops, node, path = heapq.heappop(heap)
#         if node in visited:
#             continue
#         path = path + [node]
#         visited.add(node)
        
#         if node == end:
#             total_cost = sum(graph[path[i]][j][1] for i in range(len(path)-1) for j in range(len(graph[path[i]])) if graph[path[i]][j][0] == path[i+1])
#             return stops, path, total_cost
        
#         for neighbor, _ in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (stops + 1, neighbor, path))
    
#     return float("inf"), [], 0

# # Función para mostrar el menú
# def show_menu(root, destinations, flights, graph):
#     root.title("Metro Travel")
#     root.geometry("400x300")

#     tk.Label(root, text="Bienvenido a Metro Travel", font=("Arial", 16)).pack(pady=10)

#     def print_destinations():
#         dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
#         print(dest_str)

#     def print_flights():
#         flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
#         print(flights_str)

#     def draw_graph(canvas, graph, destinations, path=[], route_info=""):
#         canvas.delete("all")
#         nodes = list(destinations.keys())
#         pos = {}
#         # Aumentar el tamaño del área de dibujo para mejorar la visibilidad
#         width, height = 800, 600
#         canvas.config(width=width, height=height)
#         for node in nodes:
#             pos[node] = (random.randint(50, width - 50), random.randint(50, height - 50))
        
#         for node, neighbors in graph.items():
#             x1, y1 = pos[node]
#             canvas.create_oval(x1-10, y1-10, x1+10, y1+10, fill="skyblue")
#             canvas.create_text(x1, y1, text=node, fill="black")
#             for neighbor, cost in neighbors:
#                 x2, y2 = pos[neighbor]
#                 if (node in path and neighbor in path and 
#                     abs(path.index(node) - path.index(neighbor)) == 1):
#                     canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
#                 else:
#                     canvas.create_line(x1, y1, x2, y2, fill="gray")
#                 mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
#                 canvas.create_text(mid_x, mid_y, text=f"${cost:.2f}", fill="red")
        
#         if route_info:
#             canvas.create_text(width / 2, height - 20, text=route_info, fill="blue", font=("Arial", 10, "bold"))

#     def print_graph_gui(path=[], route_info=""):
#         graph_window = tk.Toplevel(root)
#         graph_window.title("Grafo de vuelos")
#         graph_window.geometry("800x600")  # Ajustar el tamaño de la ventana para que coincida con el tamaño del lienzo

#         canvas = tk.Canvas(graph_window, width=800, height=600, bg="white")
#         canvas.pack()

#         draw_graph(canvas, graph, destinations, path, route_info)

#     def search_route():
#         while True:
#             start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
#             if start not in destinations:
#                 messagebox.showerror("Error", "Código de aeropuerto de origen no válido. Vuelve a ingresar un código existente.")
#                 continue

#             end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
#             if end not in destinations:
#                 messagebox.showerror("Error", "Código de aeropuerto de destino no válido. Vuelve a ingresar un código existente.")
#                 continue

#             break

#         has_visa = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

#         route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

#         if route_type == "costo":
#             cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
#             if cost == float("inf"):
#                 route_info = "No hay ruta disponible que cumpla con los requisitos."
#             else:
#                 route_info = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
#             print_graph_gui(cheapest_path, route_info)
#         elif route_type == "escalas":
#             stops, shortest_path, total_cost = find_shortest_route(graph, destinations, start, end, has_visa)
#             if stops == float("inf"):
#                 route_info = "No hay ruta disponible que cumpla con los requisitos."
#             else:
#                 route_info = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}\nCosto total: ${total_cost:.2f}"
#             print_graph_gui(shortest_path, route_info)
#         else:
#             messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

#     tk.Button(root, text="Imprimir destinos cargados", width=30, command=print_destinations).pack(pady=10)
#     tk.Button(root, text="Imprimir vuelos cargados", width=30, command=print_flights).pack(pady=10)
#     tk.Button(root, text="Imprimir grafo de vuelos", width=30, command=print_graph_gui).pack(pady=10)
#     tk.Button(root, text="Buscar ruta", width=30, command=search_route).pack(pady=10)
#     tk.Button(root, text="Salir", width=30, command=root.destroy).pack(pady=10)

# # Función principal
# def main():
#     # Cargar destinos y vuelos desde el archivo
#     destinations, flights = load_data('flights.txt')
#     graph = build_graph(flights)

#     root = tk.Tk()

#     show_menu(root, destinations, flights, graph)

#     root.mainloop()

# if __name__ == "__main__":
#     main()


# import heapq
# from collections import defaultdict
# import tkinter as tk
# from tkinter import simpledialog
# import random

# # Función para cargar destinos y vuelos desde un archivo
# def load_data(filename):
#     destinations = {}
#     flights = []
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#         mode = None
#         for line in lines:
#             line = line.strip()
#             if line == "# Destinos":
#                 mode = "destinos"
#                 continue
#             elif line == "# Vuelos":
#                 mode = "vuelos"
#                 continue

#             if mode == "destinos" and line:
#                 code, name, visa_required = line.split(',')
#                 destinations[code] = {"name": name, "visa_required": visa_required == "Yes"}
#             elif mode == "vuelos" and line:
#                 src, dst, cost = line.split(',')
#                 flights.append((src, dst, float(cost)))
#                 flights.append((dst, src, float(cost)))  # Asumimos vuelos bidireccionales
#     return destinations, flights

# # Función para construir el grafo de vuelos
# def build_graph(flights):
#     graph = defaultdict(list)
#     for src, dst, cost in flights:
#         graph[src].append((dst, cost))
#     return graph

# # Función para encontrar la ruta más barata usando Dijkstra
# def find_cheapest_route(graph, destinations, start, end, has_visa):
#     heap = [(0, start, [])]
#     visited = set()

#     while heap:
#         cost, node, path = heapq.heappop(heap)
#         if node in visited:
#             continue
#         path = path + [node]
#         visited.add(node)
        
#         if node == end:
#             return cost, path
        
#         for neighbor, price in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (cost + price, neighbor, path))
    
#     return float("inf"), []

# # Función para encontrar la ruta con menos escalas usando Dijkstra
# def find_shortest_route(graph, destinations, start, end, has_visa):
#     heap = [(0, start, [])]  # (number of stops, current node, path)
#     visited = set()

#     while heap:
#         stops, node, path = heapq.heappop(heap)
#         if node in visited:
#             continue
#         path = path + [node]
#         visited.add(node)
        
#         if node == end:
#             total_cost = sum(graph[path[i]][j][1] for i in range(len(path)-1) for j in range(len(graph[path[i]])) if graph[path[i]][j][0] == path[i+1])
#             return stops, path, total_cost
        
#         for neighbor, _ in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (stops + 1, neighbor, path))
    
#     return float("inf"), [], 0

# # Función para mostrar el menú
# def show_menu(root, destinations, flights, graph):
#     menu_window = tk.Toplevel(root)
#     menu_window.title("Metro Travel")
#     menu_window.geometry("400x300")

#     tk.Label(menu_window, text="Bienvenido a Metro Travel", font=("Arial", 16)).pack(pady=10)

#     def print_destinations():
#         dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
#         print(dest_str)

#     def print_flights():
#         flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
#         print(flights_str)

#     def draw_graph(canvas, graph, destinations, path=[], route_info=""):
#         canvas.delete("all")
#         nodes = list(destinations.keys())
#         pos = {}
#         # Aumentar el tamaño del área de dibujo para mejorar la visibilidad
#         width, height = 800, 600
#         canvas.config(width=width, height=height)
#         for node in nodes:
#             pos[node] = (random.randint(50, width - 50), random.randint(50, height - 50))
        
#         for node, neighbors in graph.items():
#             x1, y1 = pos[node]
#             canvas.create_oval(x1-10, y1-10, x1+10, y1+10, fill="skyblue")
#             canvas.create_text(x1, y1, text=node, fill="black")
#             for neighbor, cost in neighbors:
#                 x2, y2 = pos[neighbor]
#                 if (node in path and neighbor in path and 
#                     abs(path.index(node) - path.index(neighbor)) == 1):
#                     canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
#                 else:
#                     canvas.create_line(x1, y1, x2, y2, fill="gray")
#                 mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
#                 canvas.create_text(mid_x, mid_y, text=f"${cost:.2f}", fill="red")
        
#         if route_info:
#             canvas.create_text(width / 2, height - 20, text=route_info, fill="blue", font=("Arial", 10, "bold"))

#     def print_graph_gui(path=[], route_info=""):
#         graph_window = tk.Toplevel(root)
#         graph_window.title("Grafo de vuelos")
#         graph_window.geometry("800x600")  # Ajustar el tamaño de la ventana para que coincida con el tamaño del lienzo

#         canvas = tk.Canvas(graph_window, width=800, height=600, bg="white")
#         canvas.pack()

#         draw_graph(canvas, graph, destinations, path, route_info)

#     def search_route():
#         while True:
#             start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
#             if start not in destinations:
#                 tk.messagebox.showerror("Error", "Código de aeropuerto de origen no válido. Vuelve a ingresar un código existente.")
#                 continue

#             end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
#             if end not in destinations:
#                 tk.messagebox.showerror("Error", "Código de aeropuerto de destino no válido. Vuelve a ingresar un código existente.")
#                 continue

#             break

#         has_visa = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

#         route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

#         if route_type == "costo":
#             cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
#             if cost == float("inf"):
#                 route_info = "No hay ruta disponible que cumpla con los requisitos."
#             else:
#                 route_info = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
#             print_graph_gui(cheapest_path, route_info)
#         elif route_type == "escalas":
#             stops, shortest_path, total_cost = find_shortest_route(graph, destinations, start, end, has_visa)
#             if stops == float("inf"):
#                 route_info = "No hay ruta disponible que cumpla con los requisitos."
#             else:
#                 route_info = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}\nCosto total: ${total_cost:.2f}"
#             print_graph_gui(shortest_path, route_info)
#         else:
#             tk.messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

#     tk.Button(menu_window, text="Imprimir grafo de vuelos", width=30, command=print_graph_gui).pack(pady=10)
#     tk.Button(menu_window, text="Buscar ruta", width=30, command=search_route).pack(pady=10)
#     tk.Button(menu_window, text="Salir", width=30, command=menu_window.destroy).pack(pady=10)

# # Función principal
# def main():
#     # Cargar destinos y vuelos desde el archivo
#     destinations, flights = load_data('flights.txt')
#     graph = build_graph(flights)

#     root = tk.Tk()
#     root.title("Metro Travel")
#     root.geometry("400x300")

#     show_menu(root, destinations, flights, graph)

#     root.mainloop()

# if __name__ == "__main__":
#     main()



# import heapq
# from collections import defaultdict
# import tkinter as tk
# from tkinter import simpledialog
# import random

# # Función para cargar destinos y vuelos desde un archivo
# def load_data(filename):
#     destinations = {}
#     flights = []
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#         mode = None
#         for line in lines:
#             line = line.strip()
#             if line == "# Destinos":
#                 mode = "destinos"
#                 continue
#             elif line == "# Vuelos":
#                 mode = "vuelos"
#                 continue

#             if mode == "destinos" and line:
#                 code, name, visa_required = line.split(',')
#                 destinations[code] = {"name": name, "visa_required": visa_required == "Yes"}
#             elif mode == "vuelos" and line:
#                 src, dst, cost = line.split(',')
#                 flights.append((src, dst, float(cost)))
#                 flights.append((dst, src, float(cost)))  # Asumimos vuelos bidireccionales
#     return destinations, flights

# # Función para construir el grafo de vuelos
# def build_graph(flights):
#     graph = defaultdict(list)
#     for src, dst, cost in flights:
#         graph[src].append((dst, cost))
#     return graph

# # Función para encontrar la ruta más barata usando Dijkstra
# def find_cheapest_route(graph, destinations, start, end, has_visa):
#     heap = [(0, start, [])]
#     visited = set()

#     while heap:
#         cost, node, path = heapq.heappop(heap)
#         if node in visited:
#             continue
#         path = path + [node]
#         visited.add(node)
        
#         if node == end:
#             return cost, path
        
#         for neighbor, price in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (cost + price, neighbor, path))
    
#     return float("inf"), []

# # Función para encontrar la ruta con menos escalas usando Dijkstra
# def find_shortest_route(graph, destinations, start, end, has_visa):
#     heap = [(0, start, [])]  # (number of stops, current node, path)
#     visited = set()

#     while heap:
#         stops, node, path = heapq.heappop(heap)
#         if node in visited:
#             continue
#         path = path + [node]
#         visited.add(node)
        
#         if node == end:
#             total_cost = sum(graph[path[i]][j][1] for i in range(len(path)-1) for j in range(len(graph[path[i]])) if graph[path[i]][j][0] == path[i+1])
#             return stops, path, total_cost
        
#         for neighbor, _ in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (stops + 1, neighbor, path))
    
#     return float("inf"), [], 0

# # Función para mostrar el menú
# def show_menu(root, destinations, flights, graph):
#     menu_window = tk.Toplevel(root)
#     menu_window.title("Metro Travel")
#     menu_window.geometry("400x300")

#     tk.Label(menu_window, text="Bienvenido a Metro Travel", font=("Arial", 16)).pack(pady=10)

#     def print_destinations():
#         dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
#         print(dest_str)

#     def print_flights():
#         flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
#         print(flights_str)

#     def draw_graph(canvas, graph, destinations, path=[], route_info=""):
#         canvas.delete("all")
#         nodes = list(destinations.keys())
#         pos = {}
#         # Aumentar el tamaño del área de dibujo para mejorar la visibilidad
#         width, height = 800, 600
#         canvas.config(width=width, height=height)
#         for node in nodes:
#             pos[node] = (random.randint(50, width - 50), random.randint(50, height - 50))
        
#         for node, neighbors in graph.items():
#             x1, y1 = pos[node]
#             canvas.create_oval(x1-10, y1-10, x1+10, y1+10, fill="skyblue")
#             canvas.create_text(x1, y1, text=node, fill="black")
#             for neighbor, cost in neighbors:
#                 x2, y2 = pos[neighbor]
#                 if (node in path and neighbor in path and 
#                     abs(path.index(node) - path.index(neighbor)) == 1):
#                     canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
#                 else:
#                     canvas.create_line(x1, y1, x2, y2, fill="gray")
#                 mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
#                 canvas.create_text(mid_x, mid_y, text=f"${cost:.2f}", fill="red")
        
#         if route_info:
#             canvas.create_text(width / 2, height - 20, text=route_info, fill="blue", font=("Arial", 10, "bold"))

#     def print_graph_gui(path=[], route_info=""):
#         graph_window = tk.Toplevel(root)
#         graph_window.title("Grafo de vuelos")
#         graph_window.geometry("800x600")  # Ajustar el tamaño de la ventana para que coincida con el tamaño del lienzo

#         canvas = tk.Canvas(graph_window, width=800, height=600, bg="white")
#         canvas.pack()

#         draw_graph(canvas, graph, destinations, path, route_info)

#     def search_route():
#         start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
#         end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
#         has_visa = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

#         if start not in destinations or end not in destinations:
#             print("Código de aeropuerto no válido.")
#             return

#         route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

#         if route_type == "costo":
#             cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
#             if cost == float("inf"):
#                 route_info = "No hay ruta disponible que cumpla con los requisitos."
#             else:
#                 route_info = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
#             print_graph_gui(cheapest_path, route_info)
#         elif route_type == "escalas":
#             stops, shortest_path, total_cost = find_shortest_route(graph, destinations, start, end, has_visa)
#             if stops == float("inf"):
#                 route_info = "No hay ruta disponible que cumpla con los requisitos."
#             else:
#                 route_info = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}\nCosto total: ${total_cost:.2f}"
#             print_graph_gui(shortest_path, route_info)
#         else:
#             print("Opción no válida. Por favor, elija 'costo' o 'escalas'.")

#     # tk.Button(menu_window, text="Imprimir destinos cargados", width=30, command=print_destinations).pack(pady=10)
#     # tk.Button(menu_window, text="Imprimir vuelos cargados", width=30, command=print_flights).pack(pady=10)
#     tk.Button(menu_window, text="Imprimir grafo de vuelos", width=30, command=print_graph_gui).pack(pady=10)
#     tk.Button(menu_window, text="Buscar ruta", width=30, command=search_route).pack(pady=10)
#     tk.Button(menu_window, text="Salir", width=30, command=menu_window.destroy).pack(pady=10)

# # Función principal
# def main():
#     # Cargar destinos y vuelos desde el archivo
#     destinations, flights = load_data('flights.txt')
#     graph = build_graph(flights)

#     root = tk.Tk()
#     root.title("Metro Travel")
#     root.geometry("400x300")

#     show_menu(root, destinations, flights, graph)

#     root.mainloop()

# if __name__ == "__main__":
#     main()




