# import heapq
# from collections import defaultdict
# import tkinter as tk
# from tkinter import messagebox, simpledialog
# from PIL import Image, ImageTk
# import tempfile
# import os
# import graphviz

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
#             return stops, path
        
#         for neighbor, _ in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (stops + 1, neighbor, path))
    
#     return float("inf"), []

# # Función para mostrar el menú
# def show_menu(root, destinations, flights, graph):
#     menu_window = tk.Toplevel(root)
#     menu_window.title("Metro Travel")
#     menu_window.geometry("400x300")

#     tk.Label(menu_window, text="Bienvenido a Metro Travel", font=("Arial", 16)).pack(pady=10)

#     def print_destinations():
#         dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
#         messagebox.showinfo("Destinos cargados", dest_str)

#     def print_flights():
#         flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
#         messagebox.showinfo("Vuelos cargados", flights_str)

#     def render_and_show_graph():
#         dot = graphviz.Digraph()
#         for src, edges in graph.items():
#             for dst, cost in edges:
#                 dot.edge(src, dst, label=f"${cost:.2f}")

#         # Renderizar el gráfico como imagen temporal
#         graph_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#         dot.render(graph_file.name, format='png', engine='dot', quiet=True)

#         # Mostrar la imagen en una ventana emergente
#         image = Image.open(graph_file.name)
#         photo = ImageTk.PhotoImage(image)
#         graph_window = tk.Toplevel(menu_window)
#         graph_window.title("Grafo de vuelos")
#         graph_label = tk.Label(graph_window, image=photo)
#         graph_label.image = photo
#         graph_label.pack(padx=10, pady=10)

#         # Cerrar y eliminar el archivo temporal después de mostrar la imagen
#         graph_file.close()
#         os.unlink(graph_file.name)

#     def search_route():
#         start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
#         end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
#         has_visa = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

#         if start not in destinations or end not in destinations:
#             messagebox.showerror("Error", "Código de aeropuerto no válido.")
#             return

#         route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

#         if route_type == "costo":
#             cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
#             if cost == float("inf"):
#                 messagebox.showinfo("Ruta más barata", "No hay ruta disponible que cumpla con los requisitos.")
#             else:
#                 route_str = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
#                 messagebox.showinfo("Ruta más barata", route_str)
#         elif route_type == "escalas":
#             stops, shortest_path = find_shortest_route(graph, destinations, start, end, has_visa)
#             if stops == float("inf"):
#                 messagebox.showinfo("Ruta con menos escalas", "No hay ruta disponible que cumpla con los requisitos.")
#             else:
#                 route_str = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}"
#                 messagebox.showinfo("Ruta con menos escalas", route_str)
#         else:
#             messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

#     tk.Button(menu_window, text="Imprimir destinos cargados", width=30, command=print_destinations).pack(pady=10)
#     tk.Button(menu_window, text="Imprimir vuelos cargados", width=30, command=print_flights).pack(pady=10)
#     tk.Button(menu_window, text="Mostrar grafo de vuelos", width=30, command=render_and_show_graph).pack(pady=10)
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






import heapq
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt

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
            return stops, path
        
        for neighbor, _ in graph[node]:
            if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
                heapq.heappush(heap, (stops + 1, neighbor, path))
    
    return float("inf"), []

# Función para mostrar el menú
def show_menu(root, destinations, flights, graph):
    menu_window = tk.Toplevel(root)
    menu_window.title("Metro Travel")
    menu_window.geometry("400x300")

    tk.Label(menu_window, text="Bienvenido a Metro Travel", font=("Arial", 16)).pack(pady=10)

    def print_destinations():
        dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
        messagebox.showinfo("Destinos cargados", dest_str)

    def print_flights():
        flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
        messagebox.showinfo("Vuelos cargados", flights_str)

    def print_graph_gui():
        print_graph(graph, destinations)

    def search_route():
        start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
        end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
        has_visa = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

        if start not in destinations or end not in destinations:
            messagebox.showerror("Error", "Código de aeropuerto no válido.")
            return

        route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

        if route_type == "costo":
            cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
            if cost == float("inf"):
                messagebox.showinfo("Ruta más barata", "No hay ruta disponible que cumpla con los requisitos.")
            else:
                route_str = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
                messagebox.showinfo("Ruta más barata", route_str)
        elif route_type == "escalas":
            stops, shortest_path = find_shortest_route(graph, destinations, start, end, has_visa)
            if stops == float("inf"):
                messagebox.showinfo("Ruta con menos escalas", "No hay ruta disponible que cumpla con los requisitos.")
            else:
                route_str = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}"
                messagebox.showinfo("Ruta con menos escalas", route_str)
        else:
            messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

    tk.Button(menu_window, text="Imprimir destinos cargados", width=30, command=print_destinations).pack(pady=10)
    tk.Button(menu_window, text="Imprimir vuelos cargados", width=30, command=print_flights).pack(pady=10)
    tk.Button(menu_window, text="Imprimir grafo de vuelos", width=30, command=print_graph_gui).pack(pady=10)
    tk.Button(menu_window, text="Buscar ruta", width=30, command=search_route).pack(pady=10)
    tk.Button(menu_window, text="Salir", width=30, command=menu_window.destroy).pack(pady=10)


    def print_destinations():
        dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
        messagebox.showinfo("Destinos cargados", dest_str)

    def print_flights():
        flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
        messagebox.showinfo("Vuelos cargados", flights_str)

    def print_graph(graph, destinations):
        G = nx.Graph()

        for node, neighbors in graph.items():
            G.add_node(node, label=destinations[node]["name"])
            for neighbor, cost in neighbors:
                G.add_edge(node, neighbor, weight=cost)

        pos = nx.spring_layout(G, seed=42)  # Layout para posicionar los nodos

        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)

        # Dibujar etiquetas de nodos
        nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=10, font_color='black')

        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1.0, alpha=0.5, edge_color='gray')

        # Dibujar etiquetas de aristas (costos)
        edge_labels = {(node1, node2): f"${cost:.2f}" for node1, node2, cost in G.edges(data='weight')}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Grafo de vuelos")
        plt.axis('off')
        plt.show()

    def search_route():
        start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
        end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
        has_visa = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

        if start not in destinations or end not in destinations:
            messagebox.showerror("Error", "Código de aeropuerto no válido.")
            return

        route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

        if route_type == "costo":
            cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
            if cost == float("inf"):
                messagebox.showinfo("Ruta más barata", "No hay ruta disponible que cumpla con los requisitos.")
            else:
                route_str = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
                messagebox.showinfo("Ruta más barata", route_str)
        elif route_type == "escalas":
            stops, shortest_path = find_shortest_route(graph, destinations, start, end, has_visa)
            if stops == float("inf"):
                messagebox.showinfo("Ruta con menos escalas", "No hay ruta disponible que cumpla con los requisitos.")
            else:
                route_str = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}"
                messagebox.showinfo("Ruta con menos escalas", route_str)
        else:
            messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

    tk.Button(menu_window, text="Imprimir destinos cargados", width=30, command=print_destinations).pack(pady=10)
    tk.Button(menu_window, text="Imprimir vuelos cargados", width=30, command=print_flights).pack(pady=10)
    tk.Button(menu_window, text="Imprimir grafo de vuelos", width=30, command=print_graph).pack(pady=10)
    tk.Button(menu_window, text="Buscar ruta", width=30, command=search_route).pack(pady=10)
    tk.Button(menu_window, text="Salir", width=30, command=menu_window.destroy).pack(pady=10)

# Función principal
def main():
    # Cargar destinos y vuelos desde el archivo
    destinations, flights = load_data('flights.txt')
    graph = build_graph(flights)

    root = tk.Tk()
    root.title("Metro Travel")
    root.geometry("400x300")

    show_menu(root, destinations, flights, graph)

    root.mainloop()

if __name__ == "__main__":
    main()





# import heapq
# from collections import defaultdict
# import tkinter as tk
# from tkinter import messagebox, simpledialog

# # Aquí va todo el código de las funciones load_data, build_graph, find_cheapest_route, find_shortest_route y main que ya tienes
# # ...
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
#             return stops, path
        
#         for neighbor, _ in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (stops + 1, neighbor, path))
    
#     return float("inf"), []
# # Función para mostrar el menú y manejar la entrada del usuario
# def show_menu():
#     print("\nBienvenido a Metro Travel")
#     print("1. Imprimir destinos cargados")
#     print("2. Imprimir vuelos cargados")
#     print("3. Imprimir grafo de vuelos")
#     print("4. Buscar ruta")
#     print("5. Salir")

# def print_destinations(destinations):
#     dest_str = "\n".join([f"{code}: {data['name']} {'(Requiere Visa)' if data['visa_required'] else ''}" for code, data in destinations.items()])
#     messagebox.showinfo("Destinos cargados", dest_str)

# def print_flights(flights):
#     flights_str = "\n".join([f"{src} -> {dst}: ${cost:.2f}" for src, dst, cost in flights])
#     messagebox.showinfo("Vuelos cargados", flights_str)

# def print_graph(graph):
#     graph_str = "\n".join([f"{node} -> {neighbors}" for node, neighbors in graph.items()])
#     messagebox.showinfo("Grafo de vuelos", graph_str)

# def search_route(destinations, graph):
#     start = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de origen: ").strip().upper()
#     end = simpledialog.askstring("Buscar ruta", "Ingrese el código del aeropuerto de destino: ").strip().upper()
#     has_visa = simpledialog.askstring("Buscar ruta", "¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

#     if start not in destinations or end not in destinations:
#         messagebox.showerror("Error", "Código de aeropuerto no válido.")
#         return

#     route_type = simpledialog.askstring("Buscar ruta", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

#     if route_type == "costo":
#         cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
#         if cost == float("inf"):
#             messagebox.showinfo("Ruta más barata", "No hay ruta disponible que cumpla con los requisitos.")
#         else:
#             route_str = f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es:\n{' -> '.join(cheapest_path)}"
#             messagebox.showinfo("Ruta más barata", route_str)
#     elif route_type == "escalas":
#         stops, shortest_path = find_shortest_route(graph, destinations, start, end, has_visa)
#         if stops == float("inf"):
#             messagebox.showinfo("Ruta con menos escalas", "No hay ruta disponible que cumpla con los requisitos.")
#         else:
#             route_str = f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es:\n{' -> '.join(shortest_path)}"
#             messagebox.showinfo("Ruta con menos escalas", route_str)
#     else:
#         messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

# def main():
#     # Cargar destinos y vuelos desde el archivo
#     destinations, flights = load_data('flights.txt')
#     graph = build_graph(flights)

#     while True:
#         show_menu()
#         choice = simpledialog.askinteger("Menú", "Seleccione una opción (1-5): ")

#         if choice == 1:
#             print_destinations(destinations)
#         elif choice == 2:
#             print_flights(flights)
#         elif choice == 3:
#             print_graph(graph)
#         elif choice == 4:
#             search_route(destinations, graph)
#         elif choice == 5:
#             messagebox.showinfo("Salir", "Gracias por preferir nuestra agencia Metro Travel. ¡Hasta luego!")
#             break
#         else:
#             messagebox.showerror("Error", "Opción no válida. Por favor, intente de nuevo.")

# if __name__ == "__main__":
#     main()





# import heapq
# from collections import defaultdict
# import tkinter as tk
# from tkinter import simpledialog, messagebox
# import networkx as nx
# import matplotlib.pyplot as plt

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
#             return stops, path
        
#         for neighbor, _ in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (stops + 1, neighbor, path))
    
#     return float("inf"), []

# # Función para construir y mostrar el subgrafo de la ruta
# def build_subgraph(graph, path):
#     subgraph = defaultdict(list)
#     for i in range(len(path) - 1):
#         for neighbor, cost in graph[path[i]]:
#             if neighbor == path[i + 1]:
#                 subgraph[path[i]].append((neighbor, cost))
#                 break
#     return subgraph

# # Función para mostrar el subgrafo con networkx y matplotlib
# def show_graph(graph):
#     G = nx.DiGraph()
#     for src, dsts in graph.items():
#         for dst, cost in dsts:
#             G.add_edge(src, dst, weight=cost)

#     pos = nx.spring_layout(G)
#     edge_labels = {(src, dst): f"${cost:.2f}" for src, dsts in graph.items() for dst, cost in dsts}

#     nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
#     plt.show()

# # Función para manejar la búsqueda de rutas y mostrar los resultados
# def search_route(destinations, flights, graph):
#     start = simpledialog.askstring("Input", "Ingrese el código del aeropuerto de origen:").strip().upper()
#     end = simpledialog.askstring("Input", "Ingrese el código del aeropuerto de destino:").strip().upper()
#     has_visa = simpledialog.askstring("Input", "¿El pasajero tiene visa? (si/no):").strip().lower() == "si"

#     if start not in destinations or end not in destinations:
#         messagebox.showerror("Error", "Código de aeropuerto no válido.")
#         return

#     route_type = simpledialog.askstring("Input", "¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas):").strip().lower()

#     if route_type == "costo":
#         cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
#         if cost == float("inf"):
#             messagebox.showinfo("Resultado", "No hay ruta disponible que cumpla con los requisitos.")
#         else:
#             subgraph = build_subgraph(graph, cheapest_path)
#             messagebox.showinfo("Resultado", f"La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es: {' -> '.join(cheapest_path)}")
#             show_graph(subgraph)
#     elif route_type == "escalas":
#         stops, shortest_path = find_shortest_route(graph, destinations, start, end, has_visa)
#         if stops == float("inf"):
#             messagebox.showinfo("Resultado", "No hay ruta disponible que cumpla con los requisitos.")
#         else:
#             subgraph = build_subgraph(graph, shortest_path)
#             messagebox.showinfo("Resultado", f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es: {' -> '.join(shortest_path)}")
#             show_graph(subgraph)
#     else:
#         messagebox.showerror("Error", "Opción no válida. Por favor, elija 'costo' o 'escalas'.")

# # Función para mostrar el menú y manejar la entrada del usuario en la interfaz gráfica
# def show_menu(destinations, flights, graph):
#     root = tk.Tk()
#     root.title("Metro Travel")

#     tk.Label(root, text="Bienvenido a Metro Travel").pack()

#     tk.Button(root, text="Imprimir destinos cargados", command=lambda: messagebox.showinfo("Destinos cargados", destinations)).pack()
#     tk.Button(root, text="Imprimir vuelos cargados", command=lambda: messagebox.showinfo("Vuelos cargados", flights)).pack()
#     tk.Button(root, text="Imprimir grafo de vuelos", command=lambda: messagebox.showinfo("Grafo de vuelos", dict(graph))).pack()
#     tk.Button(root, text="Buscar ruta", command=lambda: search_route(destinations, flights, graph)).pack()
#     tk.Button(root, text="Salir", command=root.quit).pack()

#     root.mainloop()

# # Función principal
# def main():
#     # Cargar destinos y vuelos desde el archivo
#     destinations, flights = load_data('flights.txt')
#     graph = build_graph(flights)

#     # Mostrar el menú en la interfaz gráfica
#     show_menu(destinations, flights, graph)

# if __name__ == "__main__":
#     main()








# import heapq
# from collections import defaultdict

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
#             return stops, path
        
#         for neighbor, _ in graph[node]:
#             if neighbor not in visited and (not destinations[neighbor]["visa_required"] or has_visa):
#                 heapq.heappush(heap, (stops + 1, neighbor, path))
    
#     return float("inf"), []

# # Función para mostrar el menú y manejar la entrada del usuario
# def show_menu():
#     print("\nBienvenido a Metro Travel")
#     print("1. Imprimir destinos cargados")
#     print("2. Imprimir vuelos cargados")
#     print("3. Imprimir grafo de vuelos")
#     print("4. Buscar ruta")
#     print("5. Salir")

# # Función principal
# def main():
#     # Cargar destinos y vuelos desde el archivo
#     destinations, flights = load_data('flights.txt')
#     graph = build_graph(flights)

#     while True:
#         show_menu()
#         choice = input("Seleccione una opción: ").strip()

#         if choice == '1':
#             print("Destinos cargados:", destinations)
#         elif choice == '2':
#             print("Vuelos cargados:", flights)
#         elif choice == '3':
#             print("Grafo de vuelos:", dict(graph))
#         elif choice == '4':
#             start = input("Ingrese el código del aeropuerto de origen: ").strip().upper()
#             end = input("Ingrese el código del aeropuerto de destino: ").strip().upper()
#             has_visa = input("¿El pasajero tiene visa? (si/no): ").strip().lower() == "si"

#             if start not in destinations or end not in destinations:
#                 print("Código de aeropuerto no válido.")
#                 continue

#             route_type = input("¿Desea la ruta más barata (costo) o la de menor cantidad de escalas (escalas)? (costo/escalas): ").strip().lower()

#             if route_type == "costo":
#                 cost, cheapest_path = find_cheapest_route(graph, destinations, start, end, has_visa)
#                 if cost == float("inf"):
#                     print("No hay ruta disponible que cumpla con los requisitos.")
#                 else:
#                     print(f" \n La ruta más barata de {start} a {end} cuesta ${cost:.2f} y es: {' -> '.join(cheapest_path)} \n")
#             elif route_type == "escalas":
#                 stops, shortest_path = find_shortest_route(graph, destinations, start, end, has_visa)
#                 if stops == float("inf"):
#                     print("No hay ruta disponible que cumpla con los requisitos.")
#                 else:
#                     print(f"La ruta con menos escalas de {start} a {end} tiene {stops} escalas y es: {' -> '.join(shortest_path)}")
#             else:
#                 print("Opción no válida. Por favor, elija 'costo' o 'escalas'.")
#         elif choice == '5':
#             print(" \n Gracias preferir nuestra agencia Metro Travel. ¡Hasta luego 👋 ! \n ")
#             break
#         else:
#             print("Opción no válida. Por favor, intente de nuevo.")

# if __name__ == "__main__":
#     main()

