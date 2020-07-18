import os

os.environ['NAME_RECOGNITION_SQL_URL'] = 'postgresql://postgres:password@localhost:5432'
os.environ['NAME_RECOGNITION_PORT'] = '5000'
os.environ['NAME_RECOGNITION_DEBUG'] = 'true'
os.environ['NAME_RECOGNITION_QUERY_SCREEN'] = 'SELECT * FROM WLF.screening LIMIT 1000;'
os.environ['NAME_RECOGNITION_SCORE_FACTOR'] = 'key_0'
os.environ['NAME_RECOGNITION_THRESHOLD'] = 'key_0'