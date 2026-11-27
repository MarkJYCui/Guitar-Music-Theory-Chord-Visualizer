# Guitar Music Theory & Chord Visualizer

This tool helps guitarists explore scales, map out the fretboard across different tunings and capo positions, and find playable chord voicings.

## Live Application
The app is hosted online on Streamlit Community Cloud, so you can use it directly in your browser without downloading or running any code locally:

[Open Guitar Music Theory & Chord Visualizer](https://guitar-music-theory-chord-visualizer-h4zgzqyisvfgs98lapfwjb.streamlit.app/)

## Core Features
- **Full Fretboard Mapping:** Displays full scales across the fretboard in either Note or Interval mode, with accurate diatonic spelling and highlighting for the selected chord degree.
- **Tunings and Capo Support:** Includes standard and alternate tunings (such as Drop D, DADGAD, and Open G), custom string configurations, and capo transposition up to fret 12.
- **Diatonic Chords and Progressions:** Builds triads and 7th chords for 7-note scales, includes a practical V7 option in Major keys, and lets you view common progressions (Pop, Classic Rock, and Jazz/R&B).
- **Playable Chord Voicings:** Uses standard open and barre shapes for standard-interval tunings, and falls back to a Python `itertools` search to calculate playable voicings for alternate and custom tunings.
- **CAGED System Explorer:** Maps CAGED chord shapes across standard and compatible tunings (adjusted for capo position) for triads and 7th chords.
- **Multilingual Support:** The interface is available in English, Chinese (中文), and French (Français).

## Running the Application Locally
If you want to run this tool on your own computer, follow these steps:
1. Make sure you have Python installed.
2. Install the required packages by running: `pip install -r requirements.txt`
3. Start the app with the command: `streamlit run app.py`

## Disclaimer on Music Theory Accuracy
Please note that the code and underlying logic for this application were generated with AI. While the tool has been reviewed and updated to work as a reliable visualizer, the music theory logic has not been independently checked by professional musicians or music theorists. You are welcome to use this app as a learning aid, while keeping in mind that minor theoretical inaccuracies may still appear.
