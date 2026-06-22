#!/usr/bin/env python3
"""Graph Coloring — greedy algorithm for register allocation."""

def greedy_color(graph):
    colors = {}
    for node in sorted(graph):
        used = {colors[n] for n in graph[node] if n in colors}
        color = 0
        while color in used: color += 1
        colors[node] = color
    return colors

def chromatic_number(graph):
    return max(greedy_color(graph).values()) + 1

if __name__ == "__main__":
    graph = {"A":["B","C"],"B":["A","C","D"],"C":["A","B","D"],"D":["B","C","E"],"E":["D"]}
    colors = greedy_color(graph)
    print("Graph Coloring (greedy):")
    for node, color in sorted(colors.items()):
        print(f"  {node}: color {color}")
    print(f"Colors used: {chromatic_number(graph)}")\n