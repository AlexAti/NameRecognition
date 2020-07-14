import pandas as pd

def ExtraFields(df_screen, adjacency_matrix, df_party, score_factor, threshold, key_screen, key_party):
    if adjacency_matrix.shape[0] == 0:
        adjacency_matrix = pd.DataFrame(columns = [
            'key_screen',
            'key_party',
            'score',
            'birth_country_hit',
            'birth_date_hit',
            'identifier_hit'
        ])
        return(adjacency_matrix)
    # Aplicación de los score_factor
    adjacency_matrix = pd.merge(
        left = adjacency_matrix,
        right = df_screen,
        how = 'left',
        on = key_screen
    ).rename({
        'birth_date': 'birth_date_screen',
        'birth_country': 'birth_country_screen',
        'identifier': 'identifier_screen'
    }, axis = 1)
    adjacency_matrix = pd.merge(
        left = adjacency_matrix,
        right = df_party,
        how = 'left',
        on = key_party
    ).rename({
        'birth_date': 'birth_date_party',
        'birth_country': 'birth_country_party',
        'identifier': 'identifier_party'
    }, axis = 1)
    adjacency_matrix['birth_country_hit'] = adjacency_matrix['birth_country_party'] == adjacency_matrix['birth_country_screen']
    adjacency_matrix['birth_date_hit'] = adjacency_matrix['birth_date_party'] == adjacency_matrix['birth_date_screen']
    adjacency_matrix['identifier_hit'] = adjacency_matrix['identifier_party'] == adjacency_matrix['identifier_screen']
    adjacency_matrix['global_score'] = adjacency_matrix['birth_country_hit'] * score_factor['birth_country_factor'] + adjacency_matrix['birth_date_hit'] * score_factor['birth_date_factor'] + adjacency_matrix['identifier_hit'] * score_factor['identifier_factor'] + adjacency_matrix['score'] * 100 * score_factor['value_factor']
    print(adjacency_matrix.head(5))
    return(adjacency_matrix)


    """screen['global_score'] = screen.apply(
        lambda row: 
            (score_factor['birth_country_factor'] * (row['birth_country_party'] == row['birth_country_screen'])) +
            (score_factor['identifier_factor'] * (row['identifier_party'] == row['identifier_screen'])) +
            (score_factor['value_factor'] * (row['score'] * 100))
    , axis = 1)
    screen.drop(screen.columns.difference(
        ['key_screen','key_party','score','global_score']
    ), axis = 1, inplace = True)
    # Fitro puntuación global
    screen.drop(
        screen[screen['global_score'] < threshold['global_threshold']].index
    , axis = 0, inplace = True)
    # Filtro de aparicion
    ids = set(screen[key_party])
    df.drop(
        df[df[key_party].apply(lambda key: key not in ids)].index
    , inplace = True, axis = 0)
    # Calculo de score
    df = pd.merge(
        left = df,
        right = screen.groupby([key_party])['score'].max().reset_index(),
        how = 'inner',
        on = key_party
    )
    print('columns: ',df.columns)"""