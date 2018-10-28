categories = ('adult', 'child', 'infant')
calculate_rules = {
    'equal': {'adult': 1, 'child': 1, 'infant': 1},
    'preferential': {'adult': 1, 'child': 0.6, 'infant': 0},
}