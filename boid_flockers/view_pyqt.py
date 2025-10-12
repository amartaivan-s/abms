# view_pyqt.py
from PyQt6 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
import random

class BoidQtViewer(QtWidgets.QMainWindow):
    """
    PyQtGraph-based viewer for Mesa continuous-space models.
    Automatically detects swarms (clusters) based on proximity
    and colors them with distinct hues each frame.
    """
    def __init__(self, model, fps=30, point_size=6.0, swarm_radius=5.0, parent=None):
        super().__init__(parent)
        self.model = model
        self.ms_per_frame = int(1000 / max(1, fps))
        self.swarm_radius = swarm_radius
        self.setWindowTitle("Boid Flockers — PyQtGraph (Dynamic Swarm Coloring)")
        self.resize(1000, 800)

        # Set up PyQtGraph canvas
        self.canvas = pg.GraphicsLayoutWidget(show=True)
        self.setCentralWidget(self.canvas)
        self.plot = self.canvas.addPlot()
        self.plot.setAspectLocked(True)
        self.plot.showGrid(x=True, y=True, alpha=0.3)

        # Space boundaries
        sxmin = getattr(self.model.space, "x_min", 0.0)
        sxmax = getattr(self.model.space, "x_max", 100.0)
        symin = getattr(self.model.space, "y_min", 0.0)
        symax = getattr(self.model.space, "y_max", 100.0)
        self.plot.setXRange(sxmin, sxmax)
        self.plot.setYRange(symin, symax)

        # Scatter plot for agents
        self.scatter = pg.ScatterPlotItem(pxMode=False, size=point_size, name="Agents")
        self.plot.addItem(self.scatter)

        # Timer for continuous stepping
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._step_and_render)
        self.timer.start(self.ms_per_frame)

    
    # --- Swarm detection and visualization -------------
    
    def _detect_swarms(self, positions, radius=5.0):
        """
        Basic clustering by distance (union-find / BFS).
        positions: Nx2 numpy array.
        Returns array of cluster labels for each agent.
        """
        N = len(positions)
        labels = np.full(N, -1, dtype=int)
        cluster_id = 0

        for i in range(N):
            if labels[i] != -1:
                continue
            labels[i] = cluster_id
            stack = [i]
            while stack:
                j = stack.pop()
                # Distance-based neighbors
                dists = np.linalg.norm(positions[j] - positions, axis=1)
                neighbors = np.where((labels == -1) & (dists < radius))[0]
                labels[neighbors] = cluster_id
                stack.extend(neighbors)
            cluster_id += 1
        return labels

    def _make_group_colors(self, n_groups):
        """Generate visually distinct RGB colors."""
        random.seed(42)
        return [
            (
                int(random.randint(50, 255)),
                int(random.randint(50, 255)),
                int(random.randint(50, 255)),
            )
            for _ in range(n_groups)
        ]

    
    # --- Main step & render loop ------------------------
    
    def _step_and_render(self):
        # Advance simulation
        self.model.step()

        agents = list(getattr(self.model.schedule, "agents", []))
        if not agents:
            return

        # Collect agent positions
        positions = np.array([a.pos for a in agents])
        xs, ys = positions[:, 0], positions[:, 1]

        # Detect clusters
        labels = self._detect_swarms(positions, radius=self.swarm_radius)
        n_clusters = len(np.unique(labels))
        colors = self._make_group_colors(n_clusters)

        # Assign color per label
        brushes = [pg.mkBrush(colors[l % n_clusters]) for l in labels]
        self.scatter.setData(xs, ys, brush=brushes)
