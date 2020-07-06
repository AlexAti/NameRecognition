import os

os.environ['NAME_RECOGNITION_SQL_DIALECT'] = 'postgresql'
os.environ['NAME_RECOGNITION_SQL_USER'] = 'postgres'
os.environ['NAME_RECOGNITION_SQL_PASSWORD'] = 'password'
os.environ['NAME_RECOGNITION_SQL_URL'] = 'localhost'
os.environ['NAME_RECOGNITION_SQL_PORT'] = '5432'
os.environ['NAME_RECOGNITION_PORT'] = '5000'
os.environ['NAME_RECOGNITION_DEBUG'] = 'true'
os.environ['NAME_RECOGNITION_QUERY_SCREEN'] = 'SELECT * FROM WLF.screening limit 1000;'
os.environ['NAME_RECOGNITION_SCORE_FACTOR'] = 'key_0'
os.environ['NAME_RECOGNITION_THRESHOLD'] = 'key_0'