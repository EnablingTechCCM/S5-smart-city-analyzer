import streamlit as st
import requests
import csv
import matplotlib.pyplot as plt
import numpy as np

API_URL = "https://IsabelMendez.pythonanywhere.com"

st.title("Smart City Pentagon Framework Analyzer")

# Function to load keywords and levels from a CSV file
def load_keywords_and_levels_from_csv(file_path):
    keywords_levels = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keyword = row['Keyword'].lower()  # Ensure all keywords are in lowercase for matching
            level = int(row['Level'])  # Read the level as an integer
            keywords_levels[keyword] = level  # Store keyword with its level as a dictionary
    return keywords_levels

# Load keywords and levels for each S5 feature from the corresponding CSV files
smart_keywords = load_keywords_and_levels_from_csv('smart.csv')
sensing_keywords = load_keywords_and_levels_from_csv('sensing.csv')
sustainable_keywords = load_keywords_and_levels_from_csv('sustainable.csv')
social_keywords = load_keywords_and_levels_from_csv('social.csv')
safe_keywords = load_keywords_and_levels_from_csv('safe.csv')

# Analyze the combined product name, description, and features using keywords from CSV files
def analyze_combined_input(product_name, description, features):
    combined_input = product_name.lower() + " " + description.lower() + " " + " ".join(features).lower()
    
    def get_keywords_by_level(keywords):
        level_dict = {1: [], 2: [], 3: []}
        for keyword, level in keywords.items():
            if keyword in combined_input:
                level_dict[level].append(keyword)
        return level_dict
    
    analysis = {
        "Smart": get_keywords_by_level(smart_keywords),
        "Sensing": get_keywords_by_level(sensing_keywords),
        "Sustainable": get_keywords_by_level(sustainable_keywords),
        "Social": get_keywords_by_level(social_keywords),
        "Safe": get_keywords_by_level(safe_keywords),
    }
    
    return analysis

# Calculate the average score for each S5 feature
def calculate_average(levels):
    total_keywords = sum(len(keywords) for keywords in levels.values())
    weighted_sum = sum(level * len(keywords) for level, keywords in levels.items())
    if total_keywords == 0:
        return 0
    return (weighted_sum / (3 * total_keywords)) * 100

# Provide feedback based on missing S5 features
def provide_s5_feedback(s5_analysis):
    feedback = {
        "Smart": "Consider adding AI, IoT, or cloud integration to make the product smarter.",
        "Sensing": "You could add sensors or data collection to improve monitoring capabilities.",
        "Sustainable": "Incorporate renewable energy sources or make your product more eco-friendly.",
        "Social": "Think about adding community engagement or social inclusion elements.",
        "Safe": "Ensure the product is secure and follows safety protocols."
    }
    feedback_messages = {}
    for s5, keywords in s5_analysis.items():
        if not any(keywords.values()):
            feedback_messages[s5] = feedback[s5]
    return feedback_messages

# Function to plot radar chart based on S5 analysis
def plot_radar_chart(s5_analysis):
    labels = ['Smart', 'Sensing', 'Sustainable', 'Social', 'Safe']
    values = []

    for label in labels:
        levels = s5_analysis[label]
        score = sum(level * len(keywords) for level, keywords in levels.items())
        max_score = 3 * sum(len(keywords) for keywords in levels.values())
        values.append(score / max_score if max_score > 0 else 0)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='cyan', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    st.pyplot(fig)

# Suggest personality traits based on product name and description
def suggest_personality_traits(product_name, description):
    data = {
        "product_name": product_name,
        "description": description
    }
    response = requests.post(f"{API_URL}/suggest_personality_traits", json=data)
    return response.json().get('personality_traits', [])

# Adjust sliders based on personality trait suggestions
def adjust_sliders_based_on_suggestions(suggested_traits):
    openness, conscientiousness, extraversion, agreeableness, neuroticism = 0.0, 0.0, 0.0, 0.0, 0.0
    for trait in suggested_traits:
        if trait == "Openness":
            openness = 1.0
        elif trait == "Conscientiousness":
            conscientiousness = 1.0
        elif trait == "Extraversion":
            extraversion = 1.0
        elif trait == "Agreeableness":
            agreeableness = 1.0
        elif trait == "Neuroticism":
            neuroticism = 1.0
    return openness, conscientiousness, extraversion, agreeableness, neuroticism

# Initialize session state for sliders, analysis result, and button click
if 's5_analysis_result' not in st.session_state:
    st.session_state['s5_analysis_result'] = None
if 'feedback_messages' not in st.session_state:
    st.session_state['feedback_messages'] = None
if 'analyze_clicked' not in st.session_state:
    st.session_state['analyze_clicked'] = False

# Analyze User Product
product_name = st.text_input("Product Name")
description = st.text_area("Product Description")
features = st.text_input("Product Features (comma-separated)")

# Button to analyze product
if st.button("Analyze Product"):
    if not product_name or not description or not features:
        st.markdown("**:red[Please fill in the Product Name, Description, and Features fields.]**")
    elif ";" in features:
        st.markdown("**:red[Please use a comma to separate the features, not a semicolon.]**")
    else:
        features_list = features.split(',')
        s5_analysis_result = analyze_combined_input(product_name, description, features_list)
        st.session_state['s5_analysis_result'] = s5_analysis_result
        feedback_messages = provide_s5_feedback(s5_analysis_result)
        st.session_state['feedback_messages'] = feedback_messages
        personality_traits = suggest_personality_traits(product_name, description)
        st.session_state['personality_traits'] = personality_traits
        st.session_state['openness'], st.session_state['conscientiousness'], st.session_state['extraversion'], st.session_state['agreeableness'], st.session_state['neuroticism'] = adjust_sliders_based_on_suggestions(personality_traits)
        st.session_state['analyze_clicked'] = True

# Display S5 Analysis and radar chart if the "Analyze Product" button was clicked
if st.session_state['analyze_clicked']:
    st.write(f"S5 Analysis for {product_name}")

    # Display analysis results with average percentage values
    for s5, levels in st.session_state['s5_analysis_result'].items():
        average = calculate_average(levels)
        level_output = []
        for level, keywords in levels.items():
            if keywords:
                level_output.append(f"Level {level}: {', '.join(keywords)}")
        st.write(f"{s5} ({average:.0f}%): {', '.join(level_output) if level_output else 'No relevant keywords found'}")

    # Provide feedback for missing S5 features
    st.subheader("Enhancing Your Product for S5 Compliance")
    for s5, levels in st.session_state['s5_analysis_result'].items():
        if not any(levels.values()):
            st.write(f"Suggestion to improve {s5}: {st.session_state['feedback_messages'][s5]}")
    
    # Display radar chart
    st.subheader("S5 Features Radar Chart")
    plot_radar_chart(st.session_state['s5_analysis_result'])

    # Improvement button
    st.markdown(
        """
        <a href="https://chatgpt.com/g/g-7SqJsJoeF-smart-city-s5-compliance-assistant" target="_blank">
            <button style="background-color:Green;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
                Improve your product's S5 features
            </button>
        </a>
        """, unsafe_allow_html=True
    )
    
    # Sliders for personality traits
    st.subheader("Adjust Personality Traits Sliders Based on Suggestions")
    openness = st.slider("Openness", 0.0, 1.0, st.session_state.get('openness', 0.5))
    conscientiousness = st.slider("Conscientiousness", 0.0, 1.0, st.session_state.get('conscientiousness', 0.5))
    extraversion = st.slider("Extraversion", 0.0, 1.0, st.session_state.get('extraversion', 0.5))
    agreeableness = st.slider("Agreeableness", 0.0, 1.0, st.session_state.get('agreeableness', 0.5))
    neuroticism = st.slider("Neuroticism", 0.0, 1.0, st.session_state.get('neuroticism', 0.5))

    # Button to exemplify other solutions based on personality traits
    if st.button("Exemplify other solutions based on Personality Traits"):
        data = {
            "openness": openness,
            "conscientiousness": conscientiousness,
            "extraversion": extraversion,
            "agreeableness": agreeableness,
            "neuroticism": neuroticism
        }
        
        response = requests.post(f"{API_URL}/personalize", json=data)
        recommendations = response.json().get('recommended_solutions', [])
        
        st.write("S5 Exemplification Solutions:")
        for rec in recommendations:
            st.subheader(rec['name'])
            st.write(f"Description: {rec['description']}")
            
            # Display detailed S5 features in the same order as they are defined in the main app
            st.write("S5 Features:")
            s5_features = rec['s5_features']
            for feature in ["Smart", "Sensing", "Sustainable", "Social", "Safe", "Associated Personality Traits"]:
                if feature in s5_features:
                    st.write(f"**{feature}:** {s5_features[feature]}")
            
            st.write("---")
