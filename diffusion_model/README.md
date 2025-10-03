# Diffusion Model (Mesa 2.x)

This is a simple **Agent-Based Model** implemented with [Mesa 2.x](https://mesa.readthedocs.io/).
It demonstrates how diffusion processes (such as **virus infection, innovation adoption, or news spread**) 
emerge from local interactions of agents.

## 🚀 Features
- Randomly moving agents on a 2D grid
- Infection spread by local interactions
- Adjustable parameters (number of agents, infection rate, grid size)
- Visualization with CanvasGrid + ChartModule

## 📦 Installation
Clone the repo and install dependencies (recommend using a virtual environment):

```bash
git clone https://github.com/amartaivan-s/abms/diffusion-model.git
cd diffusion-model
pip install -r requirements.txt
```

## ▶️ Run

Launch the server:

```bash
python server.py
```

Then open `http://127.0.0.1:8521` in your browser.

## �� Reference

* Schelling, T. C. (1971). *Dynamic Models of Segregation*. Journal of Mathematical Sociology, 1(2), 143–186.
* Epstein, J. M., & Axtell, R. (1996). *Growing Artificial Societies*. Brookings Institution Press.
