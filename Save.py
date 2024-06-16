import pickle


def create_save(player_data, current_skin, player_name):
    save = {
        'player_data': player_data,
        'current_skin': current_skin,
        'player_name': player_name
    }

    # Create a save file
    with open('saves/save.pkl', 'wb') as f:
        pickle.dump(save, f)


def load_save():
    # Return if there is no save file
    try:
        with open('saves/save.pkl', 'rb') as f:
            save = pickle.load(f)
    except FileNotFoundError:
        return None

    return save['player_data'], save['current_skin'], save['player_name']