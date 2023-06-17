import os
import pprint


# Dictionary of chord shapes and their corresponding scores
chord_scores = {
    'A': 0,     'Am': 0,
    'A#': 1,    'A#m': 1,
    'B': 1,     'Bm': 1,
    'C': 0,     'Cm': 1,
    'C#': 1,    'C#m': 1,
    'D': 0,     'Dm': 0,
    'D#': 1,    'D#m': 1,
    'E': 0,     'Em': 0,
    'F': 0,     'Fm': 0.5,
    'F#': 0.5,  'F#m': 0.5,
    'G': 0,     'G#': 0.5,
    'G#m': 0.5, 'Gm': 0,
}




# Example usage
input_chords = ['Am', 'C', 'F', 'G']
input_capo = 0

CHORDS = {
    'major': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
    'minor' : ['Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm']
}

def is_minor(chord):
    return chord[-1] == 'm'

def find_capoless_equivalents(input_chords, init_capo):
    res = []
    shifts =  init_capo
    for chord in input_chords:
        CHORD_TYPE = 'minor' if is_minor(chord) else 'major'

        curr_pos = CHORDS[CHORD_TYPE].index(chord)
        if curr_pos < shifts:
            curr_pos += 12
        res.append(CHORDS[CHORD_TYPE][(curr_pos + shifts) % 12])
    return res


def validate_chords(chords_list):
    for chord in chords_list:
        if chord not in chord_scores:
            print(f'Invalid chord: {chord}')
            os._exit(1)

def find_new_shape(original_chord, new_capo_pos):
    """what new chord shape should you play so that it sounds the same as the original chord with the capo on the fret?
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    CHORD_TYPE = 'minor' if is_minor(original_chord) else 'major'
    curr_pos = CHORDS[CHORD_TYPE].index(original_chord)
    if curr_pos < new_capo_pos:
        curr_pos += 12
    return CHORDS[CHORD_TYPE][(curr_pos - new_capo_pos) % 12]

def simplify_chords(chords_list, capo):
    validate_chords(chords_list)
    capoless_equivalents = find_capoless_equivalents(chords_list, capo)

    capo_scores = {}
    for capo_i in range(13):
        capo_scores[capo_i] = {}
        curr_score = 0
        new_shapes = []
        for chord_i in capoless_equivalents:
            new_shape = find_new_shape(chord_i, capo_i)
            new_shapes.append(new_shape)
            curr_score += chord_scores[new_shape]
        capo_scores[capo_i]['score'] = curr_score
        capo_scores[capo_i]['new_shapes'] = new_shapes



    return capo_scores


input_chords = ['Am', 'C', 'F', 'G']

# validate_chords(input_chords)

input_capo = 1



capo_scores = simplify_chords(input_chords, input_capo)
# sort capo scores by score into a sorted dict
capo_scores = {k: v for k, v in sorted(capo_scores.items(), key=lambda item: item[1]['score'])}

sorted_data = sorted(capo_scores.items(), key=lambda x: x[1]['score'])
pprint.pprint(sorted_data)
