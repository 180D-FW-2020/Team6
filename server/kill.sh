lsof -ti :3356 | xargs --no-run-if-empty kill -9
lsof -ti :5559 | xargs --no-run-if-empty kill -9


