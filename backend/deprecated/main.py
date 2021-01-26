import matlab.engine

eng = matlab.engine.start_matlab()

print(eng.sqrt(11.0))
