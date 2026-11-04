pip install snakeviz
python -m cProfile -o sim_stats.prof main.py
snakeviz sim_stats.prof