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
        'prac_seventh_help': "Applies only to the Major (Ionian) scale.",
        'caged_explorer': "Enable CAGED Explorer (Advanced)",
        'caged_help': "The CAGED system applies to Standard tuning and tunings with standard intervals (e.g., Eb Standard, D Standard).",
        'caged_expander': "Explore all CAGED shapes for {0} ⮟",
        'caged_note': "💡 *Practical Guitar Tip:* Full C-shape and G-shape barre chords require wide finger stretches. Guitarists usually play them as 3- or 4-note partial voicings.",
        'caged_unsupported': "ℹ️ CAGED templates are not defined for this chord quality.",
        'omitted_warning': "⚠️ Note: Some chord tones omitted due to physical tuning constraints.",
        'highlight_degree': "Highlight Fretboard for Chord Degree:",
        'all_scale_notes': "All Scale Notes (Full Scale)",
        'fretboard_legend': "Legend: **Blue (●)** = Active chord tones | **Purple** = Other scale notes",
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
        'prac_seventh_help': "仅适用于大调 (Major / Ionian) 音阶。",
        'caged_explorer': "启用 CAGED 探索 (进阶)",
        'caged_help': "CAGED 系统适用于标准调弦及具有相同琴弦音程关系的调弦（如降E或D标准调弦）。",
        'caged_expander': "探索 {0} 的所有 CAGED 指法 ⮟",
        'caged_note': "💡 *实用吉他小贴士：* 完整的 C 型和 G 型横按和弦跨度较大。在实际演奏中，吉他手通常仅弹奏其中 3 到 4 个音的局部指法。",
        'caged_unsupported': "ℹ️ 暂无该和弦类型的 CAGED 模板。",
        'omitted_warning': "⚠ 注意：由于物理调弦限制，省略了部分和弦音。",
        'highlight_degree': "在指板上高亮显示和弦级数 (Chord Degree):",
        'all_scale_notes': "所有音阶音 (完整音阶)",
        'fretboard_legend': "图例：**蓝色 (●)** = 当前和弦内音 | **紫色** = 其余音阶内音",
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
        'prac_seventh_help': "S'applique uniquement à la gamme Majeure (Ionien).",
        'caged_explorer': "Activer l'Explorateur CAGED (Avancé)",
        'caged_help': "Le système CAGED s'applique à l'accordage standard et aux accordages avec des intervalles standards (ex. Mib Standard, Ré Standard).",
        'caged_expander': "Explorer toutes les formes CAGED pour {0} ⮟",
        'caged_note': "💡 *Astuce Pratique :* Les accords barrés complets en forme de Do (C) et de Sol (G) nécessitent de grands écarts de doigts. Les guitaristes les jouent généralement sous forme de voicings partiels de 3 ou 4 notes.",
        'caged_unsupported': "ℹ️ Aucun modèle CAGED n'est défini pour cette qualité d'accord.",
        'omitted_warning': "⚠ Remarque : Certaines notes de l'accord ont été omises en raison de contraintes physiques liées à l'accordage.",
        'highlight_degree': "Mettre en évidence le Degré de l'Accord sur le manche :",
        'all_scale_notes': "Toutes les Notes de la Gamme",
        'fretboard_legend': "Légende : **Bleu (●)** = Notes de l'accord actif | **Violet** = Autres notes de la gamme",
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

BASE_LETTERS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
MAJOR_SEMITONES = [0, 2, 4, 5, 7, 9, 11]

# --- 1. Music Theory Logic ---

chromatic_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chromatic_flats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

def get_chromatic_list(root_note, scale_type='Major'):
    if 'b' in root_note:
        return chromatic_flats

    major_flat_keys = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    minor_flat_keys = ['D', 'G', 'C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']

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
    if not note_str:
        return -1
    base = note_str[0]
    val = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}.get(base, 0)
    for acc in note_str[1:]:
        if acc == '#':
            val += 1
        elif acc == 'x':
            val += 2
        elif acc == 'b':
            val -= 1
    return val % 12

def get_interval_label(note_str, root_str, use_spelling=True):
    actual_semi = (get_pitch(note_str) - get_pitch(root_str)) % 12
    if use_spelling and note_str and root_str and note_str[0] in BASE_LETTERS and root_str[0] in BASE_LETTERS:
        letter_dist = (BASE_LETTERS.index(note_str[0]) - BASE_LETTERS.index(root_str[0])) % 7
        expected_semi = MAJOR_SEMITONES[letter_dist]
        diff = (actual_semi - expected_semi + 6) % 12 - 6
        prefixes = {-2: 'bb', -1: 'b', 0: '', 1: '#', 2: 'x'}
        if diff in prefixes:
            return f"{prefixes[diff]}{letter_dist + 1}"
    return interval_names[actual_semi]

def get_tuning_intervals(tuning):
    intervals = []
    for i in range(5):
        p1 = get_pitch(tuning[i])
        p2 = get_pitch(tuning[i + 1])
        diff = (p2 - p1) % 12
        intervals.append(diff)
    return intervals

def is_caged_compatible(tuning):
    # Standard tuning intervals: P4, P4, P4, M3, P4
    return get_tuning_intervals(tuning) == [5, 5, 5, 4, 5]

def enforce_diatonic_spelling(scale, root_note):
    if len(scale) != 7:
        return scale

    start_idx = BASE_LETTERS.index(root_note[0])
    expected_letters = [BASE_LETTERS[(start_idx + i) % 7] for i in range(7)]

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

def get_chord_name(chord_notes):
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

def _is_valid_fret_list(frets):
    return frets is not None and all((f is None or f >= 0) for f in frets)

def _effective_root_pitch(chord_name, tuning, capo_fret=0):
    clean_name = chord_name.split(" (")[0]
    parts = clean_name.split(" ", 1)
    r_str = parts[0]
    qual = parts[1] if len(parts) > 1 else "Major"

    # Account for both open tuning and capo transposition
    offset = (get_pitch(tuning[0]) + capo_fret - get_pitch('E')) % 12
    effective_pitch = (get_pitch(r_str) - offset) % 12
    return effective_pitch, qual

def get_standard_shape(chord_name, tuning, capo_fret=0):
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
        "F maj7": [None, None, 3, 2, 1, 0],
        "F# minor": [2, 4, 4, 2, 2, 2],
        "G Major": [3, 2, 0, 0, 0, 3],
        "G minor": [3, 5, 5, 3, 3, 3],
        "G 7": [3, 2, 0, 0, 0, 1],
        "A Major": [None, 0, 2, 2, 2, 0],
        "A minor": [None, 0, 2, 2, 1, 0],
        "A 7": [None, 0, 2, 0, 2, 0],
        "A m7": [None, 0, 2, 0, 1, 0],
        "B Major": [None, 2, 4, 4, 4, 2],
        "B minor": [None, 2, 4, 4, 3, 2],
        "B 7": [None, 2, 1, 2, 0, 2],
    }

    effective_pitch, qual = _effective_root_pitch(chord_name, tuning, capo_fret)

    for name, frets in open_shapes.items():
        n_parts = name.split(" ", 1)
        n_pitch = get_pitch(n_parts[0])
        n_qual = n_parts[1] if len(n_parts) > 1 else "Major"
        if n_pitch == effective_pitch and n_qual == qual:
            return frets

    e_fret = (effective_pitch - 4) % 12
    a_fret = (effective_pitch - 9) % 12
    d_fret = (effective_pitch - 2) % 12

    a_shapes = {
        "Major": [None, a_fret, a_fret + 2, a_fret + 2, a_fret + 2, a_fret],
        "minor": [None, a_fret, a_fret + 2, a_fret + 2, a_fret + 1, a_fret],
        "maj7": [None, a_fret, a_fret + 2, a_fret + 1, a_fret + 2, a_fret],
        "m7": [None, a_fret, a_fret + 2, a_fret, a_fret + 1, a_fret],
        "7": [None, a_fret, a_fret + 2, a_fret, a_fret + 2, a_fret],
        "dim": [None, a_fret, a_fret + 1, a_fret + 2, a_fret + 1, None],
        "m7b5": [None, a_fret, a_fret + 1, a_fret, a_fret + 1, None],
        "dim7": [None, a_fret, a_fret + 1, a_fret - 1, a_fret + 1, None] if a_fret >= 1 else None,
        "aug": [None, a_fret, a_fret + 3, a_fret + 2, a_fret + 2, None],
        "m(maj7)": [None, a_fret, a_fret + 2, a_fret + 1, a_fret + 1, a_fret],
        "maj7#5": [None, a_fret, a_fret + 3, a_fret + 1, a_fret + 2, None],
    }

    e_shapes = {
        "Major": [e_fret, e_fret + 2, e_fret + 2, e_fret + 1, e_fret, e_fret],
        "minor": [e_fret, e_fret + 2, e_fret + 2, e_fret, e_fret, e_fret],
        "maj7": [e_fret, None, e_fret + 1, e_fret + 1, e_fret, None],
        "m7": [e_fret, e_fret + 2, e_fret, e_fret, e_fret, e_fret],
        "7": [e_fret, e_fret + 2, e_fret, e_fret + 1, e_fret, e_fret],
        "dim": [e_fret, e_fret + 1, e_fret + 2, e_fret, None, None],
        "m7b5": [e_fret, e_fret + 1, e_fret, e_fret, None, None],
        "dim7": [e_fret, None, e_fret - 1, e_fret, e_fret - 1, None] if e_fret >= 1 else None,
        "aug": [e_fret, e_fret + 3, e_fret + 2, e_fret + 1, None, None],
        "m(maj7)": [e_fret, e_fret + 2, e_fret + 1, e_fret, e_fret, e_fret],
        "maj7#5": [e_fret, None, e_fret + 1, e_fret + 1, e_fret + 1, None],
    }

    d_shapes = {
        "dim7": [None, None, d_fret, d_fret + 1, d_fret, d_fret + 1],
    }

    candidates = [(a_fret, a_shapes.get(qual)), (e_fret, e_shapes.get(qual))]
    if qual in d_shapes:
        candidates.append((d_fret, d_shapes[qual]))

    valid = [(pos, sh) for pos, sh in candidates if _is_valid_fret_list(sh)]
    if valid:
        valid.sort(key=lambda item: item[0])
        return valid[0][1]

    return None

def get_all_caged_shapes(chord_name, tuning, capo_fret=0):
    effective_pitch, qual = _effective_root_pitch(chord_name, tuning, capo_fret)

    e_fret = (effective_pitch - 4) % 12
    a_fret = (effective_pitch - 9) % 12
    d_fret = (effective_pitch - 2) % 12

    c_root = a_fret if a_fret >= 3 else a_fret + 12
    g_root = e_fret if e_fret >= 3 else e_fret + 12
    g_root_4 = e_fret if e_fret >= 4 else e_fret + 12
    a_root_1 = a_fret if a_fret >= 1 else a_fret + 12
    e_root_1 = e_fret if e_fret >= 1 else e_fret + 12

    shapes = {}

    # C-Shape (root on 5th string)
    if qual == "Major":
        shapes['C-Shape'] = [None, c_root, c_root - 1, c_root - 3, c_root - 2, c_root - 3]
    elif qual == "maj7":
        shapes['C-Shape'] = [None, c_root, c_root - 1, c_root - 3, c_root - 3, c_root - 3]
    elif qual == "minor":
        shapes['C-Shape'] = [None, c_root, c_root - 2, c_root - 3, c_root - 2, None]
    elif qual == "m7":
        shapes['C-Shape'] = [None, c_root, c_root - 2, c_root, c_root - 2, None]
    elif qual == "7":
        shapes['C-Shape'] = [None, c_root, c_root - 1, c_root, c_root - 2, c_root - 3]
    elif qual == "dim":
        shapes['C-Shape'] = [None, c_root, c_root - 2, None, c_root - 2, c_root - 1]
    elif qual == "m7b5":
        shapes['C-Shape'] = [None, c_root, c_root - 2, c_root, c_root - 2, c_root - 1]
    elif qual == "dim7":
        shapes['C-Shape'] = [None, c_root, c_root - 2, c_root - 1, c_root - 2, c_root - 1]
    elif qual == "aug":
        shapes['C-Shape'] = [None, c_root, c_root - 1, c_root - 2, c_root - 2, None]
    elif qual == "m(maj7)":
        shapes['C-Shape'] = [None, c_root, c_root - 2, c_root - 3, c_root - 3, None]
    elif qual == "maj7#5":
        shapes['C-Shape'] = [None, c_root, c_root - 1, c_root - 2, c_root - 3, None]

    # A-Shape (root on 5th string)
    if qual == "Major":
        shapes['A-Shape'] = [None, a_fret, a_fret + 2, a_fret + 2, a_fret + 2, a_fret]
    elif qual == "minor":
        shapes['A-Shape'] = [None, a_fret, a_fret + 2, a_fret + 2, a_fret + 1, a_fret]
    elif qual == "maj7":
        shapes['A-Shape'] = [None, a_fret, a_fret + 2, a_fret + 1, a_fret + 2, a_fret]
    elif qual == "m7":
        shapes['A-Shape'] = [None, a_fret, a_fret + 2, a_fret, a_fret + 1, a_fret]
    elif qual == "7":
        shapes['A-Shape'] = [None, a_fret, a_fret + 2, a_fret, a_fret + 2, a_fret]
    elif qual == "dim":
        shapes['A-Shape'] = [None, a_fret, a_fret + 1, a_fret + 2, a_fret + 1, None]
    elif qual == "m7b5":
        shapes['A-Shape'] = [None, a_fret, a_fret + 1, a_fret, a_fret + 1, None]
    elif qual == "dim7":
        shapes['A-Shape'] = [None, a_root_1, a_root_1 + 1, a_root_1 - 1, a_root_1 + 1, None]
    elif qual == "aug":
        shapes['A-Shape'] = [None, a_fret, a_fret + 3, a_fret + 2, a_fret + 2, None]
    elif qual == "m(maj7)":
        shapes['A-Shape'] = [None, a_fret, a_fret + 2, a_fret + 1, a_fret + 1, a_fret]
    elif qual == "maj7#5":
        shapes['A-Shape'] = [None, a_fret, a_fret + 3, a_fret + 1, a_fret + 2, None]

    # G-Shape (root on 6th / 1st / 3rd strings)
    if qual == "Major":
        shapes['G-Shape'] = [g_root, g_root - 1, g_root - 3, g_root - 3, g_root - 3, g_root]
    elif qual == "minor":
        shapes['G-Shape'] = [g_root, g_root - 2, g_root - 3, g_root - 3, None, g_root]
    elif qual == "maj7":
        shapes['G-Shape'] = [g_root, g_root - 1, g_root - 3, g_root - 3, g_root - 3, g_root - 1]
    elif qual == "m7":
        shapes['G-Shape'] = [g_root, g_root - 2, g_root - 3, g_root - 3, None, g_root - 2]
    elif qual == "7":
        shapes['G-Shape'] = [g_root, g_root - 1, g_root - 3, g_root - 3, g_root - 3, g_root - 2]
    elif qual == "dim":
        shapes['G-Shape'] = [g_root, g_root - 2, None, g_root - 3, g_root - 1, None]
    elif qual == "m7b5":
        shapes['G-Shape'] = [None, None, g_root_4 - 4, g_root_4 - 3, g_root_4 - 4, g_root_4 - 2]
    elif qual == "dim7":
        shapes['G-Shape'] = [None, None, g_root_4 - 4, g_root_4 - 3, g_root_4 - 4, g_root_4 - 3]
    elif qual == "aug":
        shapes['G-Shape'] = [None, g_root - 1, g_root - 2, g_root - 3, g_root - 3, None]
    elif qual == "m(maj7)":
        shapes['G-Shape'] = [g_root, g_root - 2, g_root - 3, g_root - 3, None, g_root - 1]
    elif qual == "maj7#5":
        shapes['G-Shape'] = [None, g_root - 1, g_root - 2, g_root - 3, g_root - 3, g_root - 1]

    # E-Shape (root on 6th string)
    if qual == "Major":
        shapes['E-Shape'] = [e_fret, e_fret + 2, e_fret + 2, e_fret + 1, e_fret, e_fret]
    elif qual == "minor":
        shapes['E-Shape'] = [e_fret, e_fret + 2, e_fret + 2, e_fret, e_fret, e_fret]
    elif qual == "maj7":
        shapes['E-Shape'] = [e_fret, None, e_fret + 1, e_fret + 1, e_fret, None]
    elif qual == "m7":
        shapes['E-Shape'] = [e_fret, e_fret + 2, e_fret, e_fret, e_fret, e_fret]
    elif qual == "7":
        shapes['E-Shape'] = [e_fret, e_fret + 2, e_fret, e_fret + 1, e_fret, e_fret]
    elif qual == "dim":
        shapes['E-Shape'] = [e_fret, e_fret + 1, e_fret + 2, e_fret, None, None]
    elif qual == "m7b5":
        shapes['E-Shape'] = [e_fret, e_fret + 1, e_fret, e_fret, None, None]
    elif qual == "dim7":
        shapes['E-Shape'] = [e_root_1, None, e_root_1 - 1, e_root_1, e_root_1 - 1, None]
    elif qual == "aug":
        shapes['E-Shape'] = [e_fret, e_fret + 3, e_fret + 2, e_fret + 1, None, None]
    elif qual == "m(maj7)":
        shapes['E-Shape'] = [e_fret, e_fret + 2, e_fret + 1, e_fret, e_fret, e_fret]
    elif qual == "maj7#5":
        shapes['E-Shape'] = [e_fret, None, e_fret + 1, e_fret + 1, e_fret + 1, None]

    # D-Shape (root on 4th string)
    if qual == "Major":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 2, d_fret + 3, d_fret + 2]
    elif qual == "maj7":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 2, d_fret + 2, d_fret + 2]
    elif qual == "minor":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 2, d_fret + 3, d_fret + 1]
    elif qual == "m7":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 2, d_fret + 1, d_fret + 1]
    elif qual == "7":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 2, d_fret + 1, d_fret + 2]
    elif qual == "dim":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 1, d_fret + 3, d_fret + 1]
    elif qual == "m7b5":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 1, d_fret + 1, d_fret + 1]
    elif qual == "dim7":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 1, d_fret, d_fret + 1]
    elif qual == "aug":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 3, d_fret + 3, d_fret + 2]
    elif qual == "m(maj7)":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 2, d_fret + 2, d_fret + 1]
    elif qual == "maj7#5":
        shapes['D-Shape'] = [None, None, d_fret, d_fret + 3, d_fret + 2, d_fret + 2]

    return {name: frets for name, frets in shapes.items() if _is_valid_fret_list(frets)}

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

    rows_labels = [texts[lang]['str_fmt'].format(6 - i) for i in range(5, -1, -1)]
    chord_root = chord_notes[0]

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
                in_chord = spelled is not None
                if not in_chord:
                    spelled = note

                if display_mode == 'Intervals':
                    display_val = get_interval_label(spelled, chord_root, use_spelling=in_chord)
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
    search_frets = 5  # capo_fret .. capo_fret + 5
    lowest_root_string = None

    for s_idx in range(6):
        open_note = tuning[s_idx]
        for fret in range(capo_fret, capo_fret + search_frets + 1):
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
            for fret in range(capo_fret, capo_fret + search_frets + 1):
                note = get_note_on_fret(tuning[s_idx], fret, root_note, scale_type)
                if get_pitch(note) == root_target_pitch:
                    root_opts.append((fret, root_target))
            string_options.append(root_opts if root_opts else [None])
        else:
            opts = []
            for fret in range(capo_fret, capo_fret + search_frets + 1):
                note = get_note_on_fret(tuning[s_idx], fret, root_note, scale_type)
                spelled_note = get_spelled_note_if_in_chord(get_pitch(note), chord_notes)
                if spelled_note:
                    opts.append((fret, spelled_note))
            # Always allow muting so awkward strings can be skipped for a cleaner stretch
            opts.append(None)
            string_options.append(opts)

    best_full_combo = None
    best_full_score = float('inf')

    best_partial_combo = None
    best_partial_key = (-1, float('inf'))  # (distinct chord tones, score)

    for combo in itertools.product(*string_options):
        played_items = [item for item in combo if item is not None]
        if not played_items:
            continue

        played_notes = set(item[1] for item in played_items)
        distinct_count = sum(1 for cn in chord_notes if cn in played_notes)
        fretted = [item[0] for item in played_items if item[0] > capo_fret]
        span = (max(fretted) - min(fretted)) if fretted else 0

        # Penalize wide stretches (>3 frets = >4-fret box) and internal muted strings
        played_indices = [i for i, item in enumerate(combo) if item is not None]
        internal_mutes = sum(
            1 for i in range(played_indices[0], played_indices[-1]) if combo[i] is None
        )
        muted_upper = sum(
            1 for i in range(played_indices[0], 6) if combo[i] is None
        )

        score = (
            sum(item[0] - capo_fret for item in played_items)
            + span * 12
            + internal_mutes * 18
            + muted_upper * 4
        )
        if span > 3:
            score += 200 * (span - 3)

        if distinct_count == len(chord_notes):
            if score < best_full_score:
                best_full_score = score
                best_full_combo = combo
        else:
            # Prefer more distinct chord tones; break ties by lower ergonomic score
            partial_key = (distinct_count, -score)
            if partial_key > (best_partial_key[0], -best_partial_key[1]):
                best_partial_key = (distinct_count, score)
                best_partial_combo = combo

    if best_full_combo is not None:
        chosen_combo = best_full_combo
        is_omitted = False
    else:
        chosen_combo = best_partial_combo if best_partial_combo is not None else [None] * 6
        is_omitted = True

    rel_frets = [(item[0] - capo_fret if item is not None else None) for item in chosen_combo]
    df = build_fret_dataframe(
        rel_frets, tuning, chord_notes, root_note, scale_type,
        capo_fret, lang=lang, display_mode=display_mode
    )
    return df, is_omitted


def get_optimal_voicing(tuning, chord_notes, chord_name, root_note, scale_type, capo_fret=0, lang='en', display_mode='Notes'):
    if is_caged_compatible(tuning):
        frets = get_standard_shape(chord_name, tuning, capo_fret=capo_fret)
        if frets is not None:
            return build_fret_dataframe(frets, tuning, chord_notes, root_note, scale_type, capo_fret, lang, display_mode), False

    return get_algorithmic_voicing(tuning, chord_notes, root_note, scale_type, capo_fret, lang, display_mode)


def get_fretboard_dataframe(
    tuning, scale_notes, root_note, scale_type, capo_fret=0, num_frets=12,
    lang='en', display_mode='Notes', highlight_notes=None
):
    max_fret = capo_fret + num_frets
    is_seven_note = len(scale_notes) == 7
    highlight_pitches = {get_pitch(n) for n in highlight_notes} if highlight_notes else set()

    columns = []
    for f in range(capo_fret, max_fret + 1):
        if f == capo_fret:
            columns.append(f"{texts[lang]['capo']} {capo_fret}" if capo_fret > 0 else texts[lang]['open_0'])
        else:
            columns.append(str(f - capo_fret))

    grid = []
    row_labels = []

    for i in range(5, -1, -1):
        open_note = tuning[i]
        string_number = 6 - i
        capo_note = get_note_on_fret(open_note, capo_fret, root_note, scale_type)
        row_labels.append(f"{texts[lang]['str_fmt'].format(string_number)} ({capo_note})")

        row_data = []
        for fret in range(capo_fret, max_fret + 1):
            note = get_note_on_fret(open_note, fret, root_note, scale_type)
            pitch = get_pitch(note)

            spelled_note = get_spelled_note_if_in_chord(pitch, scale_notes)
            if spelled_note:
                if display_mode == 'Intervals':
                    display_val = get_interval_label(spelled_note, root_note, use_spelling=is_seven_note)
                else:
                    display_val = spelled_note

                if highlight_pitches and pitch in highlight_pitches:
                    row_data.append(f"● {display_val}")
                else:
                    row_data.append(display_val)
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

def render_dataframe(styled_df):
    try:
        ver = tuple(int(x) for x in st.__version__.split(".")[:2])
        if ver >= (1, 50):
            st.dataframe(styled_df, width="stretch")
            return
    except Exception:
        pass
    st.dataframe(styled_df, use_container_width=True)


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
            note = st.selectbox(f"{t['str_fmt'].format(6 - i)}", chromatic, index=default_index, key=f"str_{i}")
            custom_tuning.append(note)
    selected_tuning = custom_tuning
else:
    selected_tuning = tunings[selected_tuning_name]

caged_compat = is_caged_compatible(selected_tuning)
is_major_scale = (selected_scale_type == 'Major')

st.markdown("---")
display_mode_choice = st.radio(
    t['display_mode'],
    ["Notes", "Intervals"],
    format_func=lambda x: t['notes'] if x == "Notes" else t['intervals'],
    horizontal=True
)

# Key vs. Chord Root Interval Clarification
if display_mode_choice == "Intervals":
    st.info(
        f"**{t['interval_clarification_title']}**\n\n"
        + t['interval_clarification_body'].format(key=selected_root),
        icon="ℹ️"
    )

col1, col2, col3 = st.columns(3)
with col1:
    show_sevenths = st.checkbox(t['show_sevenths'], value=False)
with col2:
    use_practical_seventh_checkbox = st.checkbox(
        t['prac_seventh'],
        value=False,
        disabled=not is_major_scale,
        help=None if is_major_scale else t['prac_seventh_help']
    )
with col3:
    enable_caged_checkbox = st.checkbox(
        t['caged_explorer'],
        value=False,
        disabled=not caged_compat,
        help=None if caged_compat else t['caged_help']
    )

use_practical_seventh = use_practical_seventh_checkbox and is_major_scale
enable_caged = enable_caged_checkbox and caged_compat

capo_fret = st.slider(t['capo_pos'], min_value=0, max_value=12, value=0)

scale = get_scale(selected_root, selected_scale_type)
is_seven_note = len(scale_intervals[selected_scale_type]) == 7

highlight_notes = None
if is_seven_note:
    chord_degree = st.selectbox(
        t['highlight_degree'],
        [0, 1, 2, 3, 4, 5, 6, 7],
        format_func=lambda x: t['all_scale_notes'] if x == 0 else str(x)
    )

    if chord_degree == 0:
        st.subheader(f"{t['results_for']} {selected_root} {t['scale_types'][selected_scale_type]}")
    else:
        is_practical_selection = (chord_degree == 7 and use_practical_seventh)
        if is_practical_selection:
            highlight_notes = get_chord_from_scale(scale, 5, include_seventh=True)
            chord_name = get_chord_name(highlight_notes) + f" ({t['practical']} V7)"
        else:
            highlight_notes = get_chord_from_scale(scale, chord_degree, include_seventh=show_sevenths)
            chord_name = get_chord_name(highlight_notes)

        st.subheader(
            f"{t['results_for']} {selected_root} {t['scale_types'][selected_scale_type]} "
            f"({t['highlighting_degree']} {chord_degree}: {chord_name})"
        )
else:
    st.subheader(f"{t['results_for']} {selected_root} {t['scale_types'][selected_scale_type]}")

st.write(f"**{t['scale_notes']}** {', '.join(scale)}")

# --- 3. Displays ---
st.subheader(t['full_fretboard'])
if highlight_notes:
    st.caption(t['fretboard_legend'])

fretboard_df = get_fretboard_dataframe(
    selected_tuning, scale, selected_root, selected_scale_type,
    capo_fret, lang=lang, display_mode=display_mode_choice,
    highlight_notes=highlight_notes
)

render_dataframe(apply_styler(fretboard_df))

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

    if use_practical_seventh:
        roman_numerals[6] = f"V7 ({t['practical']})"

    # Wrap chord cards into rows of at most 4 columns for readability
    max_cols = 4
    for row_start in range(0, len(degrees_to_show), max_cols):
        row_degrees = degrees_to_show[row_start:row_start + max_cols]
        chord_cols = st.columns(len(row_degrees))

        for col_idx, degree in enumerate(row_degrees):
            idx = row_start + col_idx
            is_loop_practical = (degree == 7 and use_practical_seventh)

            if is_loop_practical:
                deg_notes = get_chord_from_scale(scale, 5, include_seventh=True)
                deg_name = get_chord_name(deg_notes) + " (V7)"
            else:
                deg_notes = get_chord_from_scale(scale, degree, include_seventh=show_sevenths)
                deg_name = get_chord_name(deg_notes)

            with chord_cols[col_idx]:
                st.markdown(f"**{t['degree']} {degree} ({roman_numerals[degree - 1]})**")
                st.write(f"**{deg_name}**")
                st.caption(f"{deg_notes}")

                deg_voicing, is_omitted = get_optimal_voicing(
                    selected_tuning, deg_notes, deg_name, selected_root, selected_scale_type,
                    capo_fret, lang, display_mode=display_mode_choice
                )

                render_dataframe(apply_styler(deg_voicing))

                if is_omitted:
                    st.caption(t['omitted_warning'])

                if enable_caged:
                    caged_toggle_key = f"caged_toggle_{selected_progression}_{idx}"
                    show_caged = st.checkbox(
                        t['caged_expander'].format(deg_name.split(' (')[0]),
                        key=caged_toggle_key
                    )

                    if show_caged:
                        caged_shapes = get_all_caged_shapes(deg_name, selected_tuning, capo_fret=capo_fret)
                        if not caged_shapes:
                            st.caption(t['caged_unsupported'])
                        else:
                            st.caption(t['caged_note'])
                            for shape_name, frets in caged_shapes.items():
                                st.markdown(f"*{shape_name}*")
                                shape_df = build_fret_dataframe(
                                    frets, selected_tuning, deg_notes, selected_root, selected_scale_type,
                                    capo_fret, lang=lang, display_mode=display_mode_choice
                                )
                                render_dataframe(apply_styler(shape_df))
