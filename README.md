# Optimal Network Routing Program

## Overview
This program computes optimal network routes based on user-defined criteria such as minimized latency or maximized bandwidth. It also visualizes network graphs to highlight optimal paths using efficient backtracking logic.

## Features
- **Optimal Route Computation:** Calculates the most efficient network routes based on criteria like minimized latency or maximized bandwidth.
- **Network Visualization:** Displays network graphs using NetworkX and Matplotlib, emphasizing optimal paths for clear analysis.
- **Modular & Scalable Framework:** Supports dynamic input of routers, connections (edges), and weights, making it adaptable to various network configurations.
- **No Transit Packets Policy:** Allows users to select routers where transit packets are not permitted. The program dynamically recalculates alternative paths to maintain network efficiency.

## Example 
- **Minimizing latency and Allowing all transit packets:**
  ![minLatencyAllowAllTransitPackets (1)](https://github.com/user-attachments/assets/fb634478-6d03-44a0-aa93-ac2c2129981f)

