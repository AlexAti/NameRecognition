import pandas as pd

def ExtraFields(df_screen, adjacency_matrix, df_party, score_factor, threshold, key_screen, key_party):
    if adjacency_matrix.shape[0] == 0:
        adjacency_matrix = pd.DataFrame(columns = [
            'key_screen',
            'key_party',
            'score',
            'birth_country_hit',
            'birth_date_hit',
            'identifier_hit',
            'gender_hit'
        ])
        return(adjacency_matrix)
    adjacency_matrix = pd.merge(
        left = adjacency_matrix,
        right = df_screen,
        how = 'left',
        on = key_screen
    ).rename({
        'birth_date': 'birth_date_screen',
        'birth_country': 'birth_country_screen',
        'identifier': 'identifier_screen',
        'gender': 'gender_screen'
    }, axis = 1)
    adjacency_matrix = pd.merge(
        left = adjacency_matrix,
        right = df_party,
        how = 'left',
        on = key_party
    ).rename({
        'birth_date': 'birth_date_party',
        'birth_country': 'birth_country_party',
        'identifier': 'identifier_party',
        'gender': 'gender_party'
    }, axis = 1)
    adjacency_matrix['birth_country_hit'] = adjacency_matrix['birth_country_party'] == adjacency_matrix['birth_country_screen']
    adjacency_matrix['birth_date_hit'] = adjacency_matrix['birth_date_party'] == adjacency_matrix['birth_date_screen']
    adjacency_matrix['identifier_hit'] = adjacency_matrix['identifier_party'] == adjacency_matrix['identifier_screen']
    adjacency_matrix['gender_hit'] = adjacency_matrix['gender_party'] == adjacency_matrix['gender_screen']

    adjacency_matrix['global_score'] = adjacency_matrix['birth_country_hit'] * score_factor['birth_country_factor']
    adjacency_matrix['global_score'] += adjacency_matrix['birth_date_hit'] * score_factor['birth_date_factor'] 
    adjacency_matrix['global_score'] += adjacency_matrix['identifier_hit'] * score_factor['identifier_factor'] 
    adjacency_matrix['global_score'] += adjacency_matrix['score'] * 100 * score_factor['value_factor']
    print(adjacency_matrix.head(5))
    return(adjacency_matrix)