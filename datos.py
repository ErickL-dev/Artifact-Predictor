from flask import Flask, request, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

attribute_ranges = {
    'HP': [209, 239, 269, 299],
    'ATK': [14, 16, 18, 19],
    'DEF': [16, 19, 21, 23],
    'HP%': [4.1, 4.7, 5.3, 5.3],
    'ATK%': [4.1, 4.7, 5.3, 5.8],
    'DEF%': [5.1, 5.8, 6.6, 7.3],
    'Elemental Mastery': [16, 21, 23, 29],
    'Energy Recharge%': [4.5, 5.2, 5.8, 6.5],
    'CRIT Rate%': [2.7, 3.1, 3.5, 3.9],
    'CRIT DMG%': [5.4, 6.2, 7.0, 7.8]
}

def normalize_stat_name(stat_name):
    stat_name = stat_name.strip().lower()
    normalized_names = {
        'hp': 'HP',
        'atk': 'ATK',
        'def': 'DEF',
        'hp%': 'HP%',
        'atk%': 'ATK%',
        'def%': 'DEF%',
        'elemental mastery': 'Elemental Mastery',
        'energy recharge%': 'Energy Recharge%',
        'crit rate%': 'CRIT Rate%',
        'crit dmg%': 'CRIT DMG%'
    }
    return normalized_names.get(stat_name, stat_name)

def predecir_cuarta_subestadistica(sub_stats, attribute_ranges):
    if len(sub_stats) >= 3:
        tercer_sub_estadistica = normalize_stat_name(sub_stats[2].rsplit(' ', 1)[0])
        tercer_sub_estadistica_valor_str = sub_stats[2].rsplit(' ', 1)[1].replace('%', '')

        try:
            tercer_sub_estadistica_valor = float(tercer_sub_estadistica_valor_str)
        except ValueError:
            return "Error: no se pudo convertir el valor de la tercera estadística a un número."

        max_value = max(attribute_ranges[tercer_sub_estadistica])
        min_value = min(attribute_ranges[tercer_sub_estadistica])
        probabilidad_base = 0.55

        if tercer_sub_estadistica_valor == max_value:
            probabilidad_base += 0.20

        if random.random() <= probabilidad_base:
            posibles_subestadisticas = list(attribute_ranges.keys())
            for stat in sub_stats:
                stat_name = normalize_stat_name(stat.rsplit(' ', 1)[0])
                if stat_name in posibles_subestadisticas:
                    posibles_subestadisticas.remove(stat_name)
            if 'CRIT Rate%' in posibles_subestadisticas:
                posibles_subestadisticas.remove('CRIT Rate%')
            if 'CRIT DMG%' in posibles_subestadisticas:
                posibles_subestadisticas.remove('CRIT DMG%')
            cuarta_sub_estadistica = random.choice(posibles_subestadisticas)
        else:
            posibles_subestadisticas = list(attribute_ranges.keys())
            for stat in sub_stats:
                stat_name = normalize_stat_name(stat.rsplit(' ', 1)[0])
                if stat_name in posibles_subestadisticas:
                    posibles_subestadisticas.remove(stat_name)
            cuarta_sub_estadistica = random.choice(posibles_subestadisticas)

        return cuarta_sub_estadistica + " " + str(random.choice(attribute_ranges[cuarta_sub_estadistica]))

    else:
        return "Error: no hay suficientes subestadísticas."

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sub_stats = data.get('sub_stats', [])
    resultado_prediccion = predecir_cuarta_subestadistica(sub_stats, attribute_ranges)
    return jsonify({'result': resultado_prediccion})

if __name__ == '__main__':
    app.run(debug=True)
