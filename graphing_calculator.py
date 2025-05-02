import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, FloatSlider, IntSlider, VBox
import ipywidgets as widgets
from IPython.display import display
from IPython.display import clear_output

# Function 1: Display graph and table of values for any y= equation
def graph_and_table():
    x = sp.symbols('x')
    eq_input = widgets.Text(description='y =', placeholder='e.g. x**2 + 2*x + 1')

    def update_graph(eq_str):
        plt.clf()
        try:
            y_expr = sp.sympify(eq_str)
        except:
            print("Invalid equation.")
            return

        print("\nTable of Values")
        print("x\t\ty")
        for i in range(-5, 6):
            y_val = y_expr.subs(x, i)
            print(f"{i}\t\t{y_val}")

        def plot_with_zoom(zoom):
            x_vals = np.linspace(-zoom, zoom, 400)
            y_vals = [float(y_expr.subs(x, val)) for val in x_vals]
            plt.plot(x_vals, y_vals, label=f"y = {y_expr}")
            plt.fill_between(x_vals, y_vals, y2=max(y_vals), alpha=0.1, color='blue')
            plt.axhline(0, color='gray', linewidth=1)
            plt.axvline(0, color='gray', linewidth=1)
            plt.grid(True)
            plt.legend()
            plt.title("Graph of y = " + str(y_expr))
            plt.xlabel("x")
            plt.ylabel("y")
            plt.show()

        display(interactive(plot_with_zoom, zoom=IntSlider(min=5, max=30, step=1, value=10)))

    display(eq_input)
    eq_input.on_submit(lambda change: update_graph(change.value))

# Function 2: Solve a system of two equations without graphing
def solve_system_algebraically():
    eq1_input = widgets.Text(description='Eq1:')
    eq2_input = widgets.Text(description='Eq2:')
    solve_button = widgets.Button(description='Solve')
    output = widgets.Output()

    def solve(_):
        x, y = sp.symbols('x y')
        with output:
            output.clear_output()
            try:
                eq1 = sp.sympify(eq1_input.value)
                eq2 = sp.sympify(eq2_input.value)
                sol = sp.solve([eq1, eq2], (x, y))
                print("\nSolution:", sol)
            except:
                print("Invalid equations.")

    solve_button.on_click(solve)
    display(VBox([eq1_input, eq2_input, solve_button, output]))

# Function 3: Graph two equations and plot the point of intersection
def graph_system_and_intersection():
    m1 = FloatSlider(description='m1', min=-10, max=10, step=0.1, value=1)
    b1 = FloatSlider(description='b1', min=-10, max=10, step=0.1, value=0)
    m2 = FloatSlider(description='m2', min=-10, max=10, step=0.1, value=-1)
    b2 = FloatSlider(description='b2', min=-10, max=10, step=0.1, value=0)

    def plot(m1, b1, m2, b2, zoom):
        x_vals = np.linspace(-zoom, zoom, 400)
        y1 = m1 * x_vals + b1
        y2 = m2 * x_vals + b2

        xs = sp.Symbol('x')
        eq = sp.Eq(m1 * xs + b1, m2 * xs + b2)
        x_int = sp.solve(eq, xs)[0]
        y_int = m1 * x_int + b1

        plt.plot(x_vals, y1, label=f"y = {m1}x + {b1}", color='blue')
        plt.plot(x_vals, y2, label=f"y = {m2}x + {b2}", color='green')
        plt.fill_between(x_vals, y1, y2, where=(y1 > y2), interpolate=True, alpha=0.1, color='purple')
        plt.plot([float(x_int)], [float(y_int)], 'ro', label=f"Intersection ({x_int:.2f}, {y_int:.2f})")
        plt.axhline(0, color='gray')
        plt.axvline(0, color='gray')
        plt.grid(True)
        plt.legend()
        plt.title("System of Equations")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    display(interactive(plot, m1=m1, b1=b1, m2=m2, b2=b2, zoom=IntSlider(min=5, max=30, step=1, value=10)))

# Function 4: Plot roots and vertex of a quadratic equation
def quadratic_roots_and_vertex():
    a = FloatSlider(description='a', min=-10, max=10, step=0.1, value=1)
    b = FloatSlider(description='b', min=-10, max=10, step=0.1, value=0)
    c = FloatSlider(description='c', min=-10, max=10, step=0.1, value=0)

    def plot_quad(a, b, c, zoom):
        if a == 0:
            print("'a' cannot be zero in a quadratic function.")
            return

        x = sp.symbols('x')
        y_expr = a*x**2 + b*x + c
        vertex_x = -b / (2*a)
        vertex_y = y_expr.subs(x, vertex_x)
        discriminant = b**2 - 4*a*c
        roots = []
        if discriminant >= 0:
            root1 = (-b + sp.sqrt(discriminant)) / (2*a)
            root2 = (-b - sp.sqrt(discriminant)) / (2*a)
            roots = [root1, root2]

        print("\nVertex:", (vertex_x, vertex_y))
        if roots:
            print("Roots:", roots)
        else:
            print("No real roots.")

        x_vals = np.linspace(vertex_x - zoom, vertex_x + zoom, 400)
        y_vals = a*x_vals**2 + b*x_vals + c
        plt.plot(x_vals, y_vals, label=f"y = {a}x² + {b}x + {c}")
        plt.plot(vertex_x, vertex_y, 'ro', label="Vertex")
        for r in roots:
            plt.plot(float(r), 0, 'go', label=f"Root: {r:.2f}")
        plt.axhline(0, color='gray')
        plt.axvline(0, color='gray')
        plt.grid(True)
        plt.legend()
        plt.title("Quadratic Function")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    display(interactive(plot_quad, a=a, b=b, c=c, zoom=IntSlider(min=5, max=30, step=1, value=10)))

# Main Menu
menu_input = widgets.Dropdown(
    options=[('Select one', 0),
             ('1. Graph and table', 1),
             ('2. Solve system', 2),
             ('3. Graph system and intersection', 3),
             ('4. Quadratic solver', 4)],
    description='Menu:',
)

def run_selection(change):
    clear_output(wait=True)
    display(menu_input)

    choice = change['new']
    if choice == 1:
        graph_and_table()
    elif choice == 2:
        solve_system_algebraically()
    elif choice == 3:
        graph_system_and_intersection()
    elif choice == 4:
        quadratic_roots_and_vertex()

# Attach observer only once
menu_input.observe(run_selection, names='value')
display(menu_input)
