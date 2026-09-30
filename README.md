# Guitar Music Theory & Chord Visualizer

This tool is designed to help guitarists explore scales, map out fretboards across various tunings, and dynamically generate playable chord voicings. 

## Live Application
To make this tool as accessible as possible, it is hosted online via Streamlit Community Cloud. You can access and interact with the application directly from your browser without needing to download or run any code locally:

**[Insert your Streamlit App URL here]*

## Core Features
- **Dynamic Fretboard Mapping:** Visualizes scales and intervals across the entire fretboard, adapting to the user's chosen root note and scale type.
- **Custom and Alternate Tunings:** Supports standard and alternate tunings (such as Drop D, DADGAD, Open G), as well as entirely custom string configurations.
- **Algorithmic Chord Voicing:** Utilizes Python's Itertools to dynamically calculate physically playable, ergonomic chord shapes based on string intervals and standard human finger stretches.
- **CAGED System Explorer:** Maps traditional CAGED chord shapes automatically for standard and compatible tunings to help users bridge the gap between theory and practical playing.
- **Multilingual Support:** The interface is fully accessible in English, Chinese (中文), and French (Français).

## Running the Application Locally
If you wish to run this tool on your own machine, please follow these steps:
1. Ensure you have Python installed.
2. Install the necessary dependencies by running: `pip install -r requirements.txt`
3. Launch the application with the command: `streamlit run app.py`

## Disclaimer on Music Theory Accuracy
Please note that the codebase and the underlying logic for this application were generated entirely by AI. While the tool has been refined to serve as a reliable visualizer, the music theory frameworks within have not been independently verified by professional musicians or theorists. I encourage you to use this app as a supplementary learning aid, but please proceed at your own risk, keeping in mind the possibility of encountering theoretical inaccuracies.
