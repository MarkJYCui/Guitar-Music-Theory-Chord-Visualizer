import pandas as pd
import streamlit as st
import itertools

# MUST be the first Streamlit command executed
st.set_page_config(page_title="Guitar Theory Visualizer", layout="wide")

# --- Custom Acoustic Guitar Icon (Minimalist Taylor Grand Auditorium Cutaway) ---
# Uses currentColor to perfectly adapt to both Dark Mode and Light Mode natively.
acoustic_guitar_icon = """
<svg width="38" height="38" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg" style="vertical-align: -10px; margin-right: 8px;">
  <g transform="rotate(-45 50 50)">
    <!-- Headstock (Taylor Style Crown) -->
    <path d="M44.5 9 Q50 3 55.5 9 L56 18 L44 18 Z" />
    <!-- Neck -->
    <rect x="47.5" y="19" width="5" height="28" />
    <!-- Body with Venetian Cutaway & Soundhole Mask -->
    <path fill-rule="evenodd" clip-rule="evenodd" d="
      M 47.5 47 
      C 30 47 27 58 37 66 
      C 24 78 27 96 50 96 
      C 73 96 76 78 63 66 
      C 70 56 62 47 55 47 
      C 54 47 53 48 52.5 49 
      L 52.5 47 
      Z 
      M 50 67.5 C 45.858 67.5 42.5 64.142 42.5 60 C 42.5 55.858 45.858 52.5 50 52.5 C 54.142 52.5 57.5 55.858 57.5 60 C 57.5 64.142 54.142 67.5 50 67.5 Z
    "/>
  </g>
</svg>
""".replace('\n', '')

# --- Translation Dictionary ---
texts = {
    'en': {
        'app_title': "Guitar Music Theory & Chord Visualizer",
        'about': "About This App",
        'about_desc': "Welcome to the **Guitar Music Theory & Chord Visualizer**! \n\nThis tool is designed to help guitarists explore scales, map out fretboards across various tunings, and dynamically generate playable chord voicings.",
        'created_by': "**Created by:** Mark Cui",
        'co_created_by': "**Co-created by:** AI (Gemini)",
        'powered_by': (
            "**Powered by:**\n"
            "- 🐍 Python (Core Logic)\n"
            "- 🐼 Pandas (Data Grids)\n"
            "- 🎈 Streamlit (UI Framework)\n"
            "- 🧮 Itertools (Algorithmic Voicing)\n"
            "- <img src=\"https://github.githubassets.com/favicons/favicon.svg\" width=\"18\" style=\"vertical-align:-3px; margin-right:2px; background-color: white; border-radius: 50%;\"> GitHub (Version Control)\n"
            "- :streamlit: Streamlit Community Cloud (Hosting)"
        ),
        'display_mode': "Display Mode:",
        'notes': "Notes (C, E, G)",
        'intervals': "Intervals (1, 3, 5)",
        'choose_root': "Choose a Root Note / Key:",
        'choose_scale': "Choose a Scale / Mode Type:",
        'show_sevenths': "Show 7th Chords",
        'prac_seventh': "Practical 7th (Replace Major vii° with V7)",
        'caged_explorer': "Enable CAGED Explorer (Advanced)",
        'caged_help': "The CAGED system applies to Standard tuning and tunings with standard intervals (e.g., Eb Standard, D Standard).",
        'caged_expander': "Explore all CAGED shapes for {0} ⮟",
        'caged_note': "💡 *Practical Guitar Tip:* Full C-shape and G-shape barre chords require wide finger stretches. Guitarists usually play them as 3- or 4-note partial voicings.",
        'omitted_warning': "⚠️ Note: Some chord tones omitted due to physical tuning constraints.",
        'highlight_degree': "Highlight Fretboard for Chord Degree:",
        'results_for': "Results for",
        'highlighting_degree': "Highlighting Degree",
        'practical': "Practical",
        'scale_notes': "Scale Notes:",
        'choose_tuning': "Choose Tuning:",
        'capo_pos': "Capo Position (Fret 0 = No Capo):",
        'full_fretboard': "1. Full Fretboard Map",
        'diatonic_chords': "2. Diatonic Chords & Progressions",
        'progression': "Select Progression:",
        'prog_all': "All 7 Diatonic Chords",
        'prog_pop': "Pop / Modern (I - V - vi - IV)",
        'prog_rock': "Classic Rock (I - IV - V)",
        'prog_jazz': "Jazz / R&B (ii - V - I)",
        'degree': "Degree",
        'open_0': "Open (0)",
        'capo': "Capo",
        'fret_fmt': "Fret {0}",
        'str_fmt': "Str {0}",
        'custom': "Custom...",
        'interval_clarification_title': "💡 Key vs. Chord Root Interval Clarification",
        'interval_clarification_body': (
            "• **Full Fretboard Map:** Intervals are displayed relative to the **Key Root ({key})** "
            "(e.g., in C Major: C=1, D=2, E=3, F=4, G=5, A=6, B=7).\n"
            "• **Chord Voicings & CAGED Shapes:** Intervals are displayed relative to each **Chord's Root** "
            "(e.g., for a D minor chord, D=1, F=b3, A=5)."
        ),
        'scale_types': {
            'Major': 'Major (Ionian)', 
            'Natural Minor': 'Natural Minor (Aeolian)',
            'Harmonic Minor': 'Harmonic Minor',
            'Melodic Minor': 'Melodic Minor',
            'Dorian': 'Dorian Mode',
            'Phrygian': 'Phrygian Mode',
            'Lydian': 'Lydian Mode',
            'Mixolydian': 'Mixolydian Mode',
            'Locrian': 'Locrian Mode',
            'Major Pentatonic': 'Major Pentatonic',
            'Minor Pentatonic': 'Minor Pentatonic'
        }
    },
    'zh': {
        'app_title': "吉他乐理与和弦可视化工具",
        'about': "关于本应用",
        'about_desc': "欢迎使用**吉他乐理与和弦可视化工具**！\n\n本工具旨在帮助吉他手探索音阶，映射不同调弦下的指板，并动态生成真实可弹奏的吉他和弦指法。",
        'created_by': "**原作者：** Mark Cui",
        'co_created_by': "**共同创作者：** AI (Gemini)",
        'powered_by': (
            "**技术支持：**\n"
            "- 🐍 Python (核心逻辑)\n"
            "- 🐼 Pandas (数据网格)\n"
            "- 🎈 Streamlit (界面框架)\n"
            "- 🧮 Itertools (算法和弦声部)\n"
            "- <img src=\"https://github.githubassets.com/favicons/favicon.svg\" width=\"18\" style=\"vertical-align:-3px; margin-right:2px; background-color: white; border-radius: 50%;\"> GitHub (代码版本控制)\n"
            "- :streamlit: Streamlit Community Cloud (云端托管与部署)"
        ),
        'display_mode': "显示模式 (Display Mode):",
        'notes': "音名 (Notes)",
        'intervals': "级数/音程 (Intervals)",
        'choose_root': "选择根音 / 调 (Root Note / Key):",
        'choose_scale': "选择音阶/调式类型 (Scale Type):",
        'show_sevenths': "显示七和弦",
        'prac_seventh': "实用七级 (大调中将 vii° 替换为 V7)",
        'caged_explorer': "启用 CAGED 探索 (进阶)",
        'caged_help': "CAGED 系统适用于标准调弦及具有相同琴弦音程关系的调弦（如降E或D标准调弦）。",
        'caged_expander': "探索 {0} 的所有 CAGED 指法 ⮟",
        'caged_note': "💡 *实用吉他小贴士：* 完整的 C 型和 G 型横按和弦跨度较大。在实际演奏中，吉他手通常仅弹奏其中 3 到 4 个音的局部指法。",
        'omitted_warning': "⚠ 注意：由于物理调弦限制，省略了部分和弦音。",
        'highlight_degree': "在指板上高亮显示和弦级数 (Chord Degree):",
        'results_for': "分析结果：",
        'highlighting_degree': "当前高亮级数",
        'practical': "实用替换",
        'scale_notes': "音阶包含音 (Scale Notes):",
        'choose_tuning': "选择调弦 (Tuning):",
        'capo_pos': "变调夹位置 (0品 = 不使用变调夹):",
        'full_fretboard': "1. 完整指板音名分布图",
        'diatonic_chords': "2. 顺阶和弦与常见进行",
        'progression': "选择和弦进行 (Select Progression):",
        'prog_all': "所有7个顺阶和弦 (I - VII)",
        'prog_pop': "流行乐 (I - V - vi - IV)",
        'prog_rock': "经典摇滚 (I - IV - V)",
        'prog_jazz': "爵士/R&B (ii - V - I)",
        'degree': "级数",
        'open_0': "空弦 (0)",
        'capo': "变调夹",
        'fret_fmt': "{0}品",
        'str_fmt': "{0}弦",
        'custom': "自定义 (Custom)...",
        'interval_clarification_title': "💡 调性根音 vs 和弦根音音程说明",
        'interval_clarification_body': (
            "• **完整指板音名分布图：** 音程相对于**调性根音 (Key Root: {key})** 计算"
            "（例如在 C 大调中：C=1, D=2, E=3, F=4, G=5, A=6, B=7）。\n"
            "• **和弦指法与 CAGED 框图：** 音程相对于**该和弦自身的根音 (Chord Root)** 计算"
            "（例如在 D minor (ii) 和弦中：D=1, F=b3, A=5）。"
        ),
        'scale_types': {
            'Major': '大调 (Major / Ionian)', 
            'Natural Minor': '自然小调 (Natural Minor / Aeolian)',
            'Harmonic Minor': '和声小调 (Harmonic Minor)',
            'Melodic Minor': '旋律小调 (Melodic Minor)',
            'Dorian': '多利亚调式 (Dorian)',
            'Phrygian': '弗里吉亚调式 (Phrygian)',
            'Lydian': '利底亚调式 (Lydian)',
            'Mixolydian': '混合利底亚调式 (Mixolydian)',
            'Locrian': '洛克里亚调式 (Locrian)',
            'Major Pentatonic': '大调五声音阶 (Major Pentatonic)',
            'Minor Pentatonic': '小调五声音阶 (Minor Pentatonic)'
        }
    },
    'fr': {
        'app_title': "Visualiseur de Théorie Musicale et d'Accords",
        'about': "À Propos de cette Application",
        'about_desc': "Bienvenue dans le **Visualiseur de Théorie Musicale et d'Accords** ! \n\nCet outil est conçu pour aider les guitaristes à explorer les gammes, à cartographier le manche sur différents accordages et à générer dynamiquement des voicings d'accords jouables.",
        'created_by': "**Créé par :** Mark Cui",
        'co_created_by': "**Co-créé par :** l'IA (Gemini)",
        'powered_by': (
            "**Propulsé par :**\n"
            "- 🐍 Python (Logique de base)\n"
            "- 🐼 Pandas (Grilles de données)\n"
            "- 🎈 Streamlit (Interface utilisateur)\n"
            "- 🧮 Itertools (Algorithme de Voicing)\n"
            "- <img src=\"https://github.githubassets.com/favicons/favicon.svg\" width=\"18\" style=\"vertical-align:-3px; margin-right:2px; background-color: white; border-radius: 50%;\"> GitHub (Contrôle de version)\n"
            "- :streamlit: Streamlit Community Cloud (Hébergement)"
        ),
        'display_mode': "Mode d'affichage :",
        'notes': "Notes (Do, Mi, Sol)",
        'intervals': "Intervalles (1, 3, 5)",
        'choose_root': "Choisissez une Fondamentale / Tonalité :",
        'choose_scale': "Choisissez un Type de Gamme / Mode :",
        'show_sevenths': "Afficher les Accords de 7ème",
        'prac_seventh': "7ème Pratique (Remplace vii° Majeur par V7)",
        'caged_explorer': "Activer l'Explorateur CAGED (Avancé)",
        'caged_help': "Le système CAGED s'applique à l'accordage standard et aux accordages avec des intervalles standards (ex. Mib Standard, Ré Standard).",
        'caged_expander': "Explorer toutes les formes CAGED pour {0} ⮟",
        'caged_note': "💡 *Astuce Pratique :* Les accords barrés complets en forme de Do (C) et de Sol (G) nécessitent de grands écarts de doigts. Les guitaristes les jouent généralement sous forme de voicings partiels de 3 ou 4 notes.",
        'omitted_warning': "⚠ Remarque : Certaines notes de l'accord ont été omises en raison de contraintes physiques liées à l'accordage.",
        'highlight_degree': "Mettre en évidence le Degré de l'Accord sur le manche :",
        'results_for': "Résultats pour",
        'highlighting_degree': "Mise en évidence du Degré",
        'practical': "Pratique",
        'scale_notes': "Notes de la Gamme :",
        'choose_tuning': "Choisissez l'Accordage :",
        'capo_pos': "Position du Capodastre (Case 0 = Aucun) :",
        'full_fretboard': "1. Carte Complète du Manche",
        'diatonic_chords': "2. Accords Diatoniques et Progressions",
        'progression': "Sélectionnez une Progression :",
        'prog_all': "Les 7 Accords Diatoniques",
        'prog_pop': "Pop / Moderne (I - V - vi - IV)",
        'prog_rock': "Rock Classique (I - IV - V)",
        'prog_jazz': "Jazz / R&B (ii - V - I)",
        'degree': "Degré",
        'open_0': "À vide (0)",
        'capo': "Capo",
        'fret_fmt': "Case {0}",
        'str_fmt': "Crd {0}",
        'custom': "Personnalisé...",
        'interval_clarification_title': "💡 Précision sur les Intervalles : Tonalité vs Fondamentale de l'Accord",
        'interval_clarification_body': (
            "• **Carte Complète du Manche :** Les intervalles sont affichés par rapport à la **Fondamentale de la Tonalité ({key})** "
            "(ex. en Do Majeur : Do=1, Ré=2, Mi=3, Fa=4, Sol=5, La=6, Si=7).\n"
            "• **Voicings et Formes CAGED :** Les intervalles sont affichés par rapport à la **Fondamentale de chaque accord** "
            "(ex. pour un accord de Ré mineur, Ré=1, Fa=b3, La=5)."
        ),
        'scale_types': {
            'Major': 'Majeure (Ionien)', 
            'Natural Minor': 'Mineure Naturelle (Éolien)',
            'Harmonic Minor': 'Mineure Harmonique',
            'Melodic Minor': 'Mineure Mélodique',
            'Dorian': 'Mode Dorien',
            'Phrygian': 'Mode Phrygien',
            'Lydian': 'Mode Lydien',
            'Mixolydian': 'Mode Mixolydien',
            'Locrian': 'Mode Locrien',
            'Major Pentatonic': 'Pentatonique Majeure',
            'Minor Pentatonic': 'Pentatonique Mineure'
        }
    }
}

interval_names = {
    0: '1', 1: 'b2', 2: '2', 3: 'b3', 4: '3', 
    5: '4', 6: 'b5', 7: '5', 8: 'b6', 9: '6', 
    10: 'b7', 11: '7'
}

# --- 1. Music Theory Logic ---

chromatic_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chromatic_flats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

def get_chromatic_list(root_note, scale_type='Major'):
    major_flat_keys = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    minor_flat_keys = ['D', 'G', 'C', 'F', 'Bb', 'Eb', 'Ab']

    if 'Minor' in scale_type and root_note in minor_flat_keys:
        return chromatic_flats
    elif 'Major' in scale_type and root_note in major_flat_keys:
        return chromatic_flats
    elif scale_type in ['Dorian', 'Phrygian', 'Locrian'] and root_note in minor_flat_keys:
        return chromatic_flats
    elif scale_type in ['Lydian', 'Mixolydian'] and root_note in major_flat_keys:
        return chromatic_flats
    else:
        return chromatic_sharps

def get_pitch(note_str):
    if not note_str: return -1
    base = note_str[0]
    val = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}.get(base, 0)
    for acc in note_str[1:]:
        if acc == '#': val += 1
        elif acc == 'x': val += 2 
        elif acc == 'b': val -= 1
    return val % 12

def get_tuning_intervals(tuning):
    intervals = []
    for i in range(5):
        p1 = get_pitch(tuning[i])
        p2 = get_pitch(tuning[i+1])
        diff = (p2 - p1) % 12
        intervals.append(diff)
    return intervals

def is_caged_compatible(tuning):
    # Standard tuning intervals: P4, P4, P4, M3, P4
    return get_tuning_intervals(tuning) == [5, 5, 5, 4, 5]

def enforce_diatonic_spelling(scale, root_note):
    if len(scale) != 7:
        return scale
        
    base_letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    start_idx = base_letters.index(root_note[0])
    expected_letters = [base_letters[(start_idx + i) % 7] for i in range(7)]
    
    corrected_scale = []
    for i, note in enumerate(scale):
        actual_pitch = get_pitch(note)
        exp_letter = expected_letters[i]
        exp_pitch = get_pitch(exp_letter)
        
        diff = (actual_pitch - exp_pitch) % 12
        
        if diff == 0:
            corrected_scale.append(exp_letter)
        elif diff == 1:
            corrected_scale.append(exp_letter + '#')
        elif diff == 2:
            corrected_scale.append(exp_letter + 'x')
        elif diff == 11:
            corrected_scale.append(exp_letter + 'b')
        elif diff == 10:
            corrected_scale.append(exp_letter + 'bb')
        else:
            corrected_scale.append(note)
            
    return corrected_scale

scale_intervals = {
    'Major': [0, 2, 4, 5, 7, 9, 11],
    'Natural Minor': [0, 2, 3, 5, 7, 8, 10],
    'Harmonic Minor': [0, 2, 3, 5, 7, 8, 11],
    'Melodic Minor': [0, 2, 3, 5, 7, 9, 11],
    'Dorian': [0, 2, 3, 5, 7, 9, 10],
    'Phrygian': [0, 1, 3, 5, 7, 8, 10],
    'Lydian': [0, 2, 4, 6, 7, 9, 11],
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'Locrian': [0, 1, 3, 5, 6, 8, 10],
    'Major Pentatonic': [0, 2, 4, 7, 9],
    'Minor Pentatonic': [0, 3, 5, 7, 10],
}

def get_scale(root_note, scale_type):
    chromatic = get_chromatic_list(root_note, scale_type)
    start_index = get_pitch(root_note)
    intervals = scale_intervals[scale_type]
    raw_scale = [chromatic[(start_index + interval) % 12] for interval in intervals]
    
    if len(intervals) == 7:
        return enforce_diatonic_spelling(raw_scale, root_note)
    return raw_scale

def get_chord_from_scale(scale, degree, include_seventh=False):
    scale_length = len(scale)
    root_idx = (degree - 1) % scale_length
    third_idx = (root_idx + 2) % scale_length
    fifth_idx = (root_idx + 4) % scale_length
    
    chord = [scale[root_idx], scale[third_idx], scale[fifth_idx]]
    
    if include_seventh:
        seventh_idx = (root_idx + 6) % scale_length
        chord.append(scale[seventh_idx])
        
    return chord

def get_note_on_fret(open_note, fret_number, root_note, scale_type='Major'):
    chromatic = get_chromatic_list(root_note, scale_type)
    pitch = (get_pitch(open_note) + fret_number) % 12
    return chromatic[pitch]

def get_spelled_note_if_in_chord(pitch, chord_notes):
    for cn in chord_notes:
        if get_pitch(cn) == pitch:
            return cn
    return None

def get_chord_name(chord_notes, root_key, scale_type='Major'):
    root_pitch = get_pitch(chord_notes[0])
    third_pitch = get_pitch(chord_notes[1])
    fifth_pitch = get_pitch(chord_notes[2])

    third_dist = (third_pitch - root_pitch) % 12
    fifth_dist = (fifth_pitch - root_pitch) % 12
    
    if len(chord_notes) == 4:
        seventh_pitch = get_pitch(chord_notes[3])
        seventh_dist = (seventh_pitch - root_pitch) % 12
        
        if third_dist == 4 and fifth_dist == 7 and seventh_dist == 11:
            return f"{chord_notes[0]} maj7"
        elif third_dist == 4 and fifth_dist == 7 and seventh_dist == 10:
            return f"{chord_notes[0]} 7"
        elif third_dist == 3 and fifth_dist == 7 and seventh_dist == 11:
            return f"{chord_notes[0]} m(maj7)" 
        elif third_dist == 3 and fifth_dist == 7 and seventh_dist == 10:
            return f"{chord_notes[0]} m7"
        elif third_dist == 3 and fifth_dist == 6 and seventh_dist == 10:
            return f"{chord_notes[0]} m7b5"
        elif third_dist == 3 and fifth_dist == 6 and seventh_dist == 9:
            return f"{chord_notes[0]} dim7"
        elif third_dist == 4 and fifth_dist == 8 and seventh_dist == 11:
            return f"{chord_notes[0]} maj7#5" 
        elif third_dist == 4 and fifth_dist == 8 and seventh_dist == 10:
            return f"{chord_notes[0]} aug7"   

    if third_dist == 4 and fifth_dist == 7:
        return f"{chord_notes[0]} Major"
    elif third_dist == 3 and fifth_dist == 7:
        return f"{chord_notes[0]} minor"
    elif third_dist == 3 and fifth_dist == 6:
        return f"{chord_notes[0]} dim"
    elif third_dist == 4 and fifth_dist == 8:
        return f"{chord_notes[0]} aug"
        
    return f"{chord_notes[0]}"


# --- ERGONOMIC CHORD LOGIC & CAGED SHAPES ---

def get_standard_shape(chord_name, tuning):
    clean_name = chord_name.split(" (")[0]
    
    open_shapes = {
        "C Major": [None, 3, 2, 0, 1, 0],
        "C minor": [None, 3, 5, 5, 4, 3], 
        "C 7": [None, 3, 2, 3, 1, 0],
        "C maj7": [None, 3, 2, 0, 0, 0],
        "C# minor": [None, 4, 6, 6, 5, 4],
        "D Major": [None, None, 0, 2, 3, 2],
        "D minor": [None, None, 0, 2, 3, 1],
        "D 7": [None, None, 0, 2, 1, 2],
        "D m7": [None, None, 0, 2, 1, 1],
        "E Major": [0, 2, 2, 1, 0, 0],
        "E minor": [0, 2, 2, 0, 0, 0],
        "E 7": [0, 2, 0, 1, 0, 0],
        "E m7": [0, 2, 0, 0, 0, 0],
        "F Major": [1, 3, 3, 2, 1, 1], 
        "F minor": [1, 3, 3, 1, 1, 1],
        "F maj7": [None, 3, 3, 2, 1, 0],
        "F# minor": [2, 4, 4, 2, 2, 2],
        "G Major": [3, 2, 0, 0, 0, 3],
        "G minor": [3, 5, 5, 3, 3, 3],
        "G 7": [3, 2, 0, 0, 0, 1],
        "A Major": [None, 0, 2, 2, 2, 0],
        "A minor": [None, 0, 2, 2, 1, 0],
        "A 7": [None, 0, 2, 0, 2, None], 
        "A m7": [None, 0, 2, 0, 1, 0],
        "B Major": [None, 2, 4, 4, 4, 2],
        "B minor": [None, 2, 4, 4, 3, 2],
        "B 7": [None, 2, 4, 2, 4, 2]
    }
    
    offset = (get_pitch(tuning[0]) - get_pitch('E')) % 12
    
    parts = clean_name.split(" ", 1)
    r_str = parts[0]
    qual = parts[1] if len(parts) > 1 else "Major"
    
    r_pitch = get_pitch(r_str)
    effective_pitch = (r_pitch - offset) % 12
    
    for name, frets in open_shapes.items():
        n_parts = name.split(" ", 1)
        n_pitch = get_pitch(n_parts[0])
        n_qual = n_parts[1] if len(n_parts) > 1 else "Major"
        if n_pitch == effective_pitch and n_qual == qual:
            return frets
    
    e_fret = (effective_pitch - 4) % 12
    if e_fret < 0: e_fret += 12
    
    a_fret = (effective_pitch - 9) % 12
    if a_fret < 0: a_fret += 12
    
    if a_fret < e_fret:
        if qual == "Major": return [None, a_fret, a_fret+2, a_fret+2, a_fret+2, a_fret]
        elif qual == "minor": return [None, a_fret, a_fret+2, a_fret+2, a_fret+1, a_fret]
        elif qual == "maj7": return [None, a_fret, a_fret+2, a_fret+1, a_fret+2, a_fret]
        elif qual == "m7": return [None, a_fret, a_fret+2, a_fret, a_fret+1, a_fret]
        elif qual == "7": return [None, a_fret, a_fret+2, a_fret, a_fret+2, a_fret]
        elif qual in ["dim", "m7b5"]: return [None, a_fret, a_fret+1, a_fret, a_fret+1, None]
    else:
        if qual == "Major": return [e_fret, e_fret+2, e_fret+2, e_fret+1, e_fret, e_fret]
        elif qual == "minor": return [e_fret, e_fret+2, e_fret+2, e_fret, e_fret, e_fret]
        elif qual == "maj7": return [e_fret, e_fret+2, e_fret+1, e_fret+1, e_fret, e_fret]
        elif qual == "m7": return [e_fret, e_fret+2, e_fret, e_fret, e_fret, e_fret]
        elif qual == "7": return [e_fret, e_fret+2, e_fret, e_fret+1, e_fret, e_fret]
        elif qual in ["dim", "m7b5"]: return [e_fret, None, e_fret, e_fret, e_fret-1, None]
        
    return None

def get_all_caged_shapes(chord_name, tuning):
    clean_name = chord_name.split(" (")[0]
    parts = clean_name.split(" ", 1)
    r_str = parts[0]
    qual = parts[1] if len(parts) > 1 else "Major"
    
    offset = (get_pitch(tuning[0]) - get_pitch('E')) % 12
    r_pitch = get_pitch(r_str)
    effective_pitch = (r_pitch - offset) % 12
    
    e_fret = (effective_pitch - 4) % 12
    if e_fret < 0: e_fret += 12
    a_fret = (effective_pitch - 9) % 12
    if a_fret < 0: a_fret += 12
    d_fret = (effective_pitch - 2) % 12
    if d_fret < 0: d_fret += 12
    
    c_root = a_fret if a_fret >= 3 else a_fret + 12
    g_root = e_fret if e_fret >= 3 else e_fret + 12

    shapes = {}
    
    # C-Shape
    if qual == "Major": shapes['C-Shape'] = [None, c_root, c_root-1, c_root-3, c_root-2, c_root-3]
    elif qual == "maj7": shapes['C-Shape'] = [None, c_root, c_root-1, c_root-3, c_root-3, c_root-3]
    elif qual == "minor": shapes['C-Shape'] = [None, c_root, c_root-2, c_root-3, c_root-2, None]
    elif qual == "m7": shapes['C-Shape'] = [None, c_root, c_root-2, c_root-3, c_root-4, None] if c_root >= 4 else None
    elif qual == "7": shapes['C-Shape'] = [None, c_root, c_root-1, c_root, c_root-2, c_root-3]
    elif qual in ["dim", "m7b5"]: shapes['C-Shape'] = [None, c_root, c_root-2, c_root-4, c_root-2, None] if c_root >= 4 else None
    else: shapes['C-Shape'] = [None, c_root, c_root-1, c_root-3, c_root-2, c_root-3]

    # A-Shape 
    if qual == "Major": shapes['A-Shape'] = [None, a_fret, a_fret+2, a_fret+2, a_fret+2, a_fret]
    elif qual == "minor": shapes['A-Shape'] = [None, a_fret, a_fret+2, a_fret+2, a_fret+1, a_fret]
    elif qual == "maj7": shapes['A-Shape'] = [None, a_fret, a_fret+2, a_fret+1, a_fret+2, a_fret]
    elif qual == "m7": shapes['A-Shape'] = [None, a_fret, a_fret+2, a_fret, a_fret+1, a_fret]
    elif qual == "7": shapes['A-Shape'] = [None, a_fret, a_fret+2, a_fret, a_fret+2, a_fret]
    elif qual in ["dim", "m7b5"]: shapes['A-Shape'] = [None, a_fret, a_fret+1, a_fret, a_fret+1, None]
    else: shapes['A-Shape'] = [None, a_fret, a_fret+2, a_fret+2, a_fret+2, a_fret]

    # G-Shape
    if qual == "Major": shapes['G-Shape'] = [g_root, g_root-1, g_root-3, g_root-3, g_root-3, g_root]
    elif qual == "minor": shapes['G-Shape'] = [g_root, g_root-2, g_root-3, g_root-3, g_root-4, g_root] if g_root >= 4 else None
    elif qual == "maj7": shapes['G-Shape'] = [g_root, g_root-1, g_root-3, g_root-3, g_root-3, g_root-1] if g_root >= 3 else None
    elif qual == "m7": shapes['G-Shape'] = [g_root, g_root-2, g_root-3, g_root-3, g_root-4, g_root-2] if g_root >= 4 else None
    elif qual == "7": shapes['G-Shape'] = [g_root, g_root-1, g_root-3, g_root-3, g_root-3, g_root-2] if g_root >= 3 else None
    elif qual in ["dim", "m7b5"]: shapes['G-Shape'] = [g_root, g_root-2, g_root-3, g_root-4, None, None] if g_root >= 4 else None
    else: shapes['G-Shape'] = [g_root, g_root-1, g_root-3, g_root-3, g_root-3, g_root]

    # E-Shape 
    if qual == "Major": shapes['E-Shape'] = [e_fret, e_fret+2, e_fret+2, e_fret+1, e_fret, e_fret]
    elif qual == "minor": shapes['E-Shape'] = [e_fret, e_fret+2, e_fret+2, e_fret, e_fret, e_fret]
    elif qual == "maj7": shapes['E-Shape'] = [e_fret, e_fret+2, e_fret+1, e_fret+1, e_fret, e_fret]
    elif qual == "m7": shapes['E-Shape'] = [e_fret, e_fret+2, e_fret, e_fret, e_fret, e_fret]
    elif qual == "7": shapes['E-Shape'] = [e_fret, e_fret+2, e_fret, e_fret+1, e_fret, e_fret]
    elif qual in ["dim", "m7b5"]: shapes['E-Shape'] = [e_fret, None, e_fret, e_fret, e_fret-1, None]
    else: shapes['E-Shape'] = [e_fret, e_fret+2, e_fret+2, e_fret+1, e_fret, e_fret]

    # D-Shape 
    if qual == "Major": shapes['D-Shape'] = [None, None, d_fret, d_fret+2, d_fret+3, d_fret+2]
    elif qual == "maj7": shapes['D-Shape'] = [None, None, d_fret, d_fret+2, d_fret+2, d_fret+2]
    elif qual == "minor": shapes['D-Shape'] = [None, None, d_fret, d_fret+2, d_fret+3, d_fret+1]
    elif qual == "m7": shapes['D-Shape'] = [None, None, d_fret, d_fret+2, d_fret+1, d_fret+1]
    elif qual == "7": shapes['D-Shape'] = [None, None, d_fret, d_fret+2, d_fret+1, d_fret+2]
    elif qual in ["dim", "m7b5"]: shapes['D-Shape'] = [None, None, d_fret, d_fret+1, d_fret+1, d_fret+1]
    else: shapes['D-Shape'] = [None, None, d_fret, d_fret+2, d_fret+3, d_fret+2]

    # Filter out None shapes or shapes containing invalid negative frets
    valid_shapes = {}
    for name, frets in shapes.items():
        if frets is not None and all((f is None or f >= 0) for f in frets):
            valid_shapes[name] = frets

    return valid_shapes

def build_fret_dataframe(frets, tuning, chord_notes, root_note, scale_type, capo_fret, lang='en', display_mode='Notes'):
    shifted_frets = [(f + capo_fret if f is not None else None) for f in frets]
    valid_frets = [f for f in shifted_frets if f is not None and f > capo_fret]
    
    if valid_frets:
        span_start = min(valid_frets)
        span_len = max(max(valid_frets) - min(valid_frets) + 1, 4)
    else:
        span_start = capo_fret + 1
        span_len = 4
        
    frets_to_show = [capo_fret] + list(range(span_start, span_start + span_len))
    
    cols = []
    for f in frets_to_show:
        if f == capo_fret:
            cols.append(f"{texts[lang]['capo']} {capo_fret}" if capo_fret > 0 else texts[lang]['open_0'])
        else:
            rel_fret = f - capo_fret
            cols.append(texts[lang]['fret_fmt'].format(rel_fret))
            
    rows_labels = [texts[lang]['str_fmt'].format(6-i) for i in range(5, -1, -1)]
    ref_root_pitch = get_pitch(chord_notes[0]) # Chord Root Reference
    
    grid = []
    for i in range(5, -1, -1):
        fret_info = shifted_frets[i]
        row = []
        for fret in frets_to_show:
            if fret_info is None:
                row.append("X" if fret == capo_fret else "—")
            elif fret_info == fret:
                note = get_note_on_fret(tuning[i], fret, root_note, scale_type)
                spelled = get_spelled_note_if_in_chord(get_pitch(note), chord_notes)
                if not spelled: spelled = note 
                
                # Apply Interval Mode Translation (Chord Root Relative)
                if display_mode == 'Intervals':
                    display_val = interval_names[(get_pitch(spelled) - ref_root_pitch) % 12]
                else:
                    display_val = spelled
                    
                row.append(f"○ {display_val}" if fret == capo_fret else f"● {display_val}")
            else:
                row.append("—")
        grid.append(row)
        
    return pd.DataFrame(grid, index=rows_labels, columns=cols)


# --- FALLBACK ALGORITHMIC VOICING ---

def get_algorithmic_voicing(tuning, chord_notes, root_note, scale_type, capo_fret=0, lang='en', display_mode='Notes'):
    root_target = chord_notes[0]
    root_target_pitch = get_pitch(root_target)
    fretting_span = 5 
    lowest_root_string = None
    
    for s_idx in range(6): 
        open_note = tuning[s_idx]
        for fret in range(capo_fret, capo_fret + fretting_span):
            note_str = get_note_on_fret(open_note, fret, root_note, scale_type)
            if get_pitch(note_str) == root_target_pitch:
                lowest_root_string = s_idx
                break
        if lowest_root_string is not None:
            break

    string_options = []
    for s_idx in range(6):
        if lowest_root_string is not None and s_idx < lowest_root_string:
            string_options.append([None]) 
        elif lowest_root_string is not None and s_idx == lowest_root_string:
            root_opts = []
            for fret in range(capo_fret, capo_fret + fretting_span):
                note = get_note_on_fret(tuning[s_idx], fret, root_note, scale_type)
                if get_pitch(note) == root_target_pitch:
                    root_opts.append((fret, root_target))
            string_options.append([root_opts[0]] if root_opts else [None])
        else:
            opts = []
            open_string_note = get_note_on_fret(tuning[s_idx], capo_fret, root_note, scale_type)
            spelled_open = get_spelled_note_if_in_chord(get_pitch(open_string_note), chord_notes)
            if spelled_open:
                opts.append((capo_fret, spelled_open))

            for fret in range(capo_fret + 1, capo_fret + fretting_span):
                note = get_note_on_fret(tuning[s_idx], fret, root_note, scale_type)
                spelled_note = get_spelled_note_if_in_chord(get_pitch(note), chord_notes)
                if spelled_note:
                    opts.append((fret, spelled_note))
                    
            if not opts:
                opts.append(None)
            string_options.append(opts)

    best_combo = None
    best_score = float('inf')
    is_omitted = False
    
    for combo in itertools.product(*string_options):
        played_notes = set(item[1] for item in combo if item is not None)
        has_all_notes = all(cn in played_notes for cn in chord_notes)
        if has_all_notes:
            fretted = [item[0] for item in combo if item is not None and item[0] > capo_fret]
            span = (max(fretted) - min(fretted)) if fretted else 0
            
            # Penalize wide unplayable stretches
            score = sum(item[0] for item in combo if item is not None) + (span * 10)
            if span > 4:
                score += 1000
                
            if score < best_score:
                best_score = score
                best_combo = combo
                
    if best_combo is None:
        best_combo = [opts[0] if opts else None for opts in string_options]
        is_omitted = True

    best_frets = []
    for s_idx in range(5, -1, -1):
        best_frets.append(best_combo[s_idx])

    valid_frets = [f[0] for f in best_frets if f is not None and f[0] > capo_fret]
    if valid_frets:
        span_start = min(valid_frets)
        span_len = max(max(valid_frets) - min(valid_frets) + 1, 4)
    else:
        span_start = capo_fret + 1
        span_len = 4
        
    frets_to_show = [capo_fret] + list(range(span_start, span_start + span_len))
    
    cols = []
    for f in frets_to_show:
        if f == capo_fret:
            cols.append(f"{texts[lang]['capo']} {capo_fret}" if capo_fret > 0 else texts[lang]['open_0'])
        else:
            rel_fret = f - capo_fret
            cols.append(texts[lang]['fret_fmt'].format(rel_fret))

    rows = [texts[lang]['str_fmt'].format(6-i) for i in range(5, -1, -1)]
    ref_root_pitch = get_pitch(chord_notes[0])

    grid = []
    for fret_info in best_frets:
        row = []
        for fret in frets_to_show:
            if fret_info is None:
                row.append("X" if fret == capo_fret else "—")
            elif fret_info[0] == fret:
                if display_mode == 'Intervals':
                    display_val = interval_names[(get_pitch(fret_info[1]) - ref_root_pitch) % 12]
                else:
                    display_val = fret_info[1]
                
                row.append(f"○ {display_val}" if fret == capo_fret else f"● {display_val}")
            else:
                row.append("—")
        grid.append(row)

    return pd.DataFrame(grid, index=rows, columns=cols), is_omitted


def get_optimal_voicing(tuning, chord_notes, chord_name, root_note, scale_type, capo_fret=0, lang='en', display_mode='Notes'):
    if is_caged_compatible(tuning):
        frets = get_standard_shape(chord_name, tuning)
        if frets is not None:
            return build_fret_dataframe(frets, tuning, chord_notes, root_note, scale_type, capo_fret, lang, display_mode), False
            
    return get_algorithmic_voicing(tuning, chord_notes, root_note, scale_type, capo_fret, lang, display_mode)


def get_fretboard_dataframe(tuning, chord_notes, root_note, scale_type, capo_fret=0, num_frets=12, lang='en', display_mode='Notes'):
    max_fret = capo_fret + num_frets
    
    columns = []
    for f in range(capo_fret, max_fret + 1):
        if f == capo_fret:
            columns.append(f"{texts[lang]['capo']} {capo_fret}" if capo_fret > 0 else texts[lang]['open_0'])
        else:
            columns.append(str(f - capo_fret))
            
    grid = []
    row_labels = []
    ref_root_pitch = get_pitch(root_note) # Key Root Reference

    for i in range(5, -1, -1):
        open_note = tuning[i]
        string_number = 6 - i
        capo_note = get_note_on_fret(open_note, capo_fret, root_note, scale_type)
        row_labels.append(f"{texts[lang]['str_fmt'].format(string_number)} ({capo_note})")

        row_data = []
        for fret in range(capo_fret, max_fret + 1):
            note = get_note_on_fret(open_note, fret, root_note, scale_type)
            pitch = get_pitch(note)
            
            spelled_note = get_spelled_note_if_in_chord(pitch, chord_notes)
            if spelled_note:
                if display_mode == 'Intervals':
                    display_val = interval_names[(pitch - ref_root_pitch) % 12]
                    row_data.append(display_val)
                else:
                    row_data.append(spelled_note)
            else:
                row_data.append("—")
        grid.append(row_data)

    return pd.DataFrame(grid, index=row_labels, columns=columns)


def style_fretboard_cells(val):
    if not isinstance(val, str):
        return ""
    if '●' in val:
        return "background-color: #1f77b4; color: white; font-weight: bold; text-align: center; border-radius: 4px;"
    elif '○' in val:
        return "background-color: #2ca02c; color: white; font-weight: bold; text-align: center; border-radius: 4px;"
    elif val == 'X':
        return "color: #d62728; font-weight: bold; text-align: center;"
    elif val != '—' and val != "":
        return "background-color: #9467bd; color: white; font-weight: bold; text-align: center; border-radius: 4px;"
    else:
        return "color: #aaaaaa; text-align: center;"

def apply_styler(df):
    if hasattr(df.style, 'map'):
        return df.style.map(style_fretboard_cells)
    else:
        return df.style.applymap(style_fretboard_cells)


# --- 2. User Interface ---

lang_choice = st.sidebar.selectbox("Language / 语言 / Langue", ["English", "中文", "Français"])
if lang_choice == "English":
    lang = 'en'
elif lang_choice == "中文":
    lang = 'zh'
else:
    lang = 'fr'

t = texts[lang]

with st.sidebar:
    st.markdown(f"# {acoustic_guitar_icon} {t['about']}", unsafe_allow_html=True)
    st.markdown(t['about_desc'])
    
    st.markdown("---")
    st.markdown(t['created_by'])
    st.markdown(t['co_created_by'])
    st.write("") 
    # Enable HTML for rendering the external standard GitHub favicon/logo safely alongside markdown
    st.markdown(t['powered_by'], unsafe_allow_html=True) 

st.markdown(f"# {acoustic_guitar_icon} {t['app_title']}", unsafe_allow_html=True)

all_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Gb', 'Db', 'C#', 'Ab', 'Eb', 'Bb', 'F']
selected_root = st.selectbox(t['choose_root'], all_keys)

selected_scale_type = st.selectbox(
    t['choose_scale'], 
    list(scale_intervals.keys()), 
    format_func=lambda x: t['scale_types'][x]
)

tunings = {
    "Standard": ['E', 'A', 'D', 'G', 'B', 'E'],
    "Drop D": ['D', 'A', 'D', 'G', 'B', 'E'],
    "Drop C": ['C', 'G', 'C', 'F', 'A', 'D'],
    "Double Drop D": ['D', 'A', 'D', 'G', 'B', 'D'],
    "DADGAD": ['D', 'A', 'D', 'G', 'A', 'D'],
    "Open G": ['D', 'G', 'D', 'G', 'B', 'D'],
    "Open D": ['D', 'A', 'D', 'F#', 'A', 'D'],
    "Open C": ['C', 'G', 'C', 'G', 'C', 'E'],
    "Custom": [],
}

tuning_options = list(tunings.keys())
selected_tuning_name = st.selectbox(
    t['choose_tuning'], 
    tuning_options,
    format_func=lambda x: t['custom'] if x == "Custom" else x
)

if selected_tuning_name == "Custom":
    cols = st.columns(6)
    custom_tuning = []
    default_custom = ['E', 'A', 'D', 'G', 'B', 'E']
    chromatic = chromatic_sharps
    for i in range(6):
        with cols[i]:
            default_index = chromatic.index(default_custom[i]) if default_custom[i] in chromatic else 0
            note = st.selectbox(f"{t['str_fmt'].format(6-i)}", chromatic, index=default_index, key=f"str_{i}")
            custom_tuning.append(note)
    selected_tuning = custom_tuning
else:
    selected_tuning = tunings[selected_tuning_name]

caged_compat = is_caged_compatible(selected_tuning)

st.markdown("---")
display_mode_choice = st.radio(
    t['display_mode'],
    ["Notes", "Intervals"],
    format_func=lambda x: t['notes'] if x == "Notes" else t['intervals'],
    horizontal=True
)

# Key vs. Chord Root Interval Clarification
if display_mode_choice == "Intervals":
    st.info(t['interval_clarification_body'].format(key=selected_root), icon="ℹ️")

col1, col2, col3 = st.columns(3)
with col1:
    show_sevenths = st.checkbox(t['show_sevenths'], value=False)
with col2:
    use_practical_seventh = st.checkbox(t['prac_seventh'], value=False)
with col3:
    enable_caged_checkbox = st.checkbox(
        t['caged_explorer'], 
        value=False, 
        disabled=not caged_compat,
        help=None if caged_compat else t['caged_help']
    )
    
enable_caged = enable_caged_checkbox and caged_compat

capo_fret = st.slider(t['capo_pos'], min_value=0, max_value=12, value=0)

scale = get_scale(selected_root, selected_scale_type)
is_seven_note = len(scale_intervals[selected_scale_type]) == 7

if is_seven_note:
    chord_degree = st.selectbox(t['highlight_degree'], [1, 2, 3, 4, 5, 6, 7])
    
    is_practical_selection = (chord_degree == 7 and use_practical_seventh and selected_scale_type == 'Major')
    
    if is_practical_selection:
        target_notes = get_chord_from_scale(scale, 5, include_seventh=True)
        chord_name = get_chord_name(target_notes, selected_root, selected_scale_type) + f" ({t['practical']} V7)"
    else:
        target_notes = get_chord_from_scale(scale, chord_degree, include_seventh=show_sevenths)
        chord_name = get_chord_name(target_notes, selected_root, selected_scale_type)
        
    st.subheader(f"{t['results_for']} {selected_root} {t['scale_types'][selected_scale_type]} ({t['highlighting_degree']} {chord_degree}: {chord_name})")
else:
    target_notes = scale
    st.subheader(f"{t['results_for']} {selected_root} {t['scale_types'][selected_scale_type]}")

st.write(f"**{t['scale_notes']}** {', '.join(scale)}")

# --- 3. Displays ---
st.subheader(t['full_fretboard'])

fretboard_df = get_fretboard_dataframe(
    selected_tuning, target_notes, selected_root, selected_scale_type, 
    capo_fret, lang=lang, display_mode=display_mode_choice
)

styled_fretboard = apply_styler(fretboard_df)
st.dataframe(styled_fretboard, use_container_width=True)

if is_seven_note:
    st.subheader(t['diatonic_chords'])
    
    prog_options = {
        t['prog_all']: [1, 2, 3, 4, 5, 6, 7],
        t['prog_pop']: [1, 5, 6, 4],
        t['prog_rock']: [1, 4, 5],
        t['prog_jazz']: [2, 5, 1]
    }
    
    selected_progression = st.selectbox(t['progression'], list(prog_options.keys()))
    degrees_to_show = prog_options[selected_progression]

    chord_cols = st.columns(len(degrees_to_show))
    
    if show_sevenths:
        scale_roman_numerals = {
            'Major': ["Imaj7", "ii7", "iii7", "IVmaj7", "V7", "vi7", "viiø7"],
            'Natural Minor': ["i7", "iiø7", "IIImaj7", "iv7", "v7", "VImaj7", "VII7"],
            'Harmonic Minor': ["i(maj7)", "iiø7", "IIImaj7#5", "iv7", "V7", "VImaj7", "vii°7"],
            'Melodic Minor': ["i(maj7)", "ii7", "IIImaj7#5", "IV7", "V7", "viø7", "viiø7"],
            'Dorian': ["i7", "ii7", "IIImaj7", "IV7", "v7", "viø7", "VIImaj7"],
            'Phrygian': ["i7", "IImaj7", "III7", "iv7", "vø7", "VImaj7", "vii7"],
            'Lydian': ["Imaj7", "II7", "iii7", "ivø7", "Vmaj7", "vi7", "vii7"],
            'Mixolydian': ["I7", "ii7", "iiiø7", "IVmaj7", "v7", "vi7", "VIImaj7"],
            'Locrian': ["iø7", "IImaj7", "iii7", "iv7", "Vmaj7", "VI7", "vii7"]
        }
    else:
        scale_roman_numerals = {
            'Major': ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
            'Natural Minor': ["i", "ii°", "III", "iv", "v", "VI", "VII"],
            'Harmonic Minor': ["i", "ii°", "III+", "iv", "V", "VI", "vii°"],
            'Melodic Minor': ["i", "ii", "III+", "IV", "V", "vi°", "vii°"],
            'Dorian': ["i", "ii", "III", "IV", "v", "vi°", "VII"],
            'Phrygian': ["i", "II", "III", "iv", "v°", "VI", "vii"],
            'Lydian': ["I", "II", "iii", "iv°", "V", "vi", "vii"],
            'Mixolydian': ["I", "ii", "iii°", "IV", "v", "vi", "VII"],
            'Locrian': ["i°", "II", "iii", "iv", "V", "VI", "vii"]
        }
        
    roman_numerals = list(scale_roman_numerals.get(selected_scale_type, ["1", "2", "3", "4", "5", "6", "7"]))

    if use_practical_seventh and selected_scale_type == 'Major':
        roman_numerals[6] = f"V7 ({t['practical']})"

    for idx, degree in enumerate(degrees_to_show):
        is_loop_practical = (degree == 7 and use_practical_seventh and selected_scale_type == 'Major')
        
        if is_loop_practical:
            deg_notes = get_chord_from_scale(scale, 5, include_seventh=True)
            deg_name = get_chord_name(deg_notes, selected_root, selected_scale_type) + " (V7)"
        else:
            deg_notes = get_chord_from_scale(scale, degree, include_seventh=show_sevenths)
            deg_name = get_chord_name(deg_notes, selected_root, selected_scale_type)

        with chord_cols[idx]:
            st.markdown(f"**{t['degree']} {degree} ({roman_numerals[degree-1]})**")
            st.write(f"**{deg_name}**")
            st.caption(f"{deg_notes}")

            deg_voicing, is_omitted = get_optimal_voicing(
                selected_tuning, deg_notes, deg_name, selected_root, selected_scale_type, 
                capo_fret, lang, display_mode=display_mode_choice
            )
            
            styled_voicing = apply_styler(deg_voicing)
            st.dataframe(styled_voicing, use_container_width=True)
            
            if is_omitted:
                st.caption(t['omitted_warning'])
                
            if enable_caged:
                caged_toggle_key = f"caged_toggle_{selected_progression}_{idx}"
                show_caged = st.checkbox(t['caged_expander'].format(deg_name.split(' (')[0]), key=caged_toggle_key)
                
                if show_caged:
                    st.caption(t['caged_note'])
                    caged_shapes = get_all_caged_shapes(deg_name, selected_tuning)
                    for shape_name, frets in caged_shapes.items():
                        st.markdown(f"*{shape_name}*")
                        shape_df = build_fret_dataframe(
                            frets, selected_tuning, deg_notes, selected_root, selected_scale_type, 
                            capo_fret, lang, display_mode=display_mode_choice
                        )
                        st.dataframe(apply_styler(shape_df), use_container_width=True)
