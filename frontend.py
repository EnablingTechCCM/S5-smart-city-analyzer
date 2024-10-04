import streamlit as st
import requests
import csv

API_URL = "https://IsabelMendez.pythonanywhere.com"

st.title("Smart City S5 Framework Analyzer")

# Function to load keywords from a CSV file
def load_keywords_from_csv(file_path):
    keywords = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keywords.append(row['Keyword'].lower())  # Ensure all keywords are in lowercase for matching
    return keywords

# Load keywords for each S5 feature from the corresponding CSV files
smart_keywords = load_keywords_from_csv('smart.csv')
sensing_keywords = load_keywords_from_csv('sensing.csv')
sustainable_keywords = load_keywords_from_csv('sustainable.csv')
social_keywords = load_keywords_from_csv('social.csv')
safe_keywords = load_keywords_from_csv('safe.csv')

# Feedback based on missing S5 features
def provide_s5_feedback(s5_analysis):
    feedback = {
        "Smart": "Consider adding AI, IoT, or cloud integration to make the product smarter.",
        "Sensing": "You could add sensors or data collection to improve monitoring capabilities.",
        "Sustainable": "Incorporate renewable energy sources or make your product more eco-friendly.",
        "Social": "Think about adding community engagement or social inclusion elements.",
        "Safe": "Ensure the product is secure and follows safety protocols."
    }
    feedback_messages = {}
    for s5, present in s5_analysis.items():
        if not present:
            feedback_messages[s5] = feedback[s5]
    return feedback_messages

# Analyze the combined product name, description, and features using keywords from CSV files
def analyze_combined_input(product_name, description, features):
    combined_input = product_name.lower() + " " + description.lower() + " " + " ".join(features).lower()
    
    analysis = {
        "Smart": any(keyword in combined_input for keyword in smart_keywords),
        "Sensing": any(keyword in combined_input for keyword in sensing_keywords),
        "Sustainable": any(keyword in combined_input for keyword in sustainable_keywords),
        "Social": any(keyword in combined_input for keyword in social_keywords),
        "Safe": any(keyword in combined_input for keyword in safe_keywords),
    }
    
    return analysis

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

# Initialize session state for sliders and analysis result
if 'openness' not in st.session_state:
    st.session_state['openness'] = 0.5
if 'conscientiousness' not in st.session_state:
    st.session_state['conscientiousness'] = 0.5
if 'extraversion' not in st.session_state:
    st.session_state['extraversion'] = 0.5
if 'agreeableness' not in st.session_state:
    st.session_state['agreeableness'] = 0.5
if 'neuroticism' not in st.session_state:
    st.session_state['neuroticism'] = 0.5
if 's5_analysis_result' not in st.session_state:
    st.session_state['s5_analysis_result'] = None
if 'feedback_messages' not in st.session_state:
    st.session_state['feedback_messages'] = None
if 'personality_traits' not in st.session_state:
    st.session_state['personality_traits'] = None

# Analyze User Product
product_name = st.text_input("Product Name")
description = st.text_area("Product Description")
features = st.text_input("Product Features (comma-separated)")

if st.button("Analyze Product"):
    # Validate that the user has filled all fields
    if not product_name or not description or not features:
        st.markdown("**:red[Please fill in the Product Name, Description, and Features fields.]**")
    elif ";" in features:
        st.markdown("**:red[Please use a comma to separate the features, not a semicolon.]**")
    else:
        features_list = features.split(',')
        
        # Analyze combined product name, description, and features
        s5_analysis_result = analyze_combined_input(product_name, description, features_list)
        st.session_state['s5_analysis_result'] = s5_analysis_result  # Store in session state
        
        # Provide feedback for missing S5 features
        feedback_messages = provide_s5_feedback(s5_analysis_result)
        st.session_state['feedback_messages'] = feedback_messages  # Store in session state
        
        # Suggest Personality Traits based on Product Name and Description
        personality_traits = suggest_personality_traits(product_name, description)
        st.session_state['personality_traits'] = personality_traits  # Store in session state
        
        # Adjust the sliders based on personality traits
        st.session_state['openness'], st.session_state['conscientiousness'], st.session_state['extraversion'], st.session_state['agreeableness'], st.session_state['neuroticism'] = adjust_sliders_based_on_suggestions(personality_traits)

# Display S5 Analysis from session state
if st.session_state['s5_analysis_result']:
    st.write(f"S5 Analysis for {product_name}")
    for s5, value in st.session_state['s5_analysis_result'].items():
        st.write(f"{s5}: {'Yes' if value else 'No'}")
    
    # Provide feedback for missing S5 features
    st.subheader("Enhancing Your Product for S5 Compliance")
    for s5, present in st.session_state['s5_analysis_result'].items():
        if not present:
            st.write(f"Suggestion to improve {s5}: {st.session_state['feedback_messages'][s5]}")

# Display Personality Traits Suggestions
if st.session_state['personality_traits']:
    st.subheader("Personality Traits Suggestions for this Product")
    if st.session_state['personality_traits']:
        st.write(f"Based on the product name, description, and features, we suggest the following personality traits: {', '.join(st.session_state['personality_traits'])}")
    else:
        st.write("No associated personality traits were found based on the product title, description, and features.")
        st.write("You can manually adjust the personality traits sliders to see related solutions.")

# Personalize Recommendations based on Big Five personality traits
st.subheader("Adjust Personality Traits Sliders Based on Suggestions")
openness = st.slider("Openness", 0.0, 1.0, st.session_state['openness'])
conscientiousness = st.slider("Conscientiousness", 0.0, 1.0, st.session_state['conscientiousness'])
extraversion = st.slider("Extraversion", 0.0, 1.0, st.session_state['extraversion'])
agreeableness = st.slider("Agreeableness", 0.0, 1.0, st.session_state['agreeableness'])
neuroticism = st.slider("Neuroticism", 0.0, 1.0, st.session_state['neuroticism'])

if st.button("Show Solutions Based on Personality Traits"):
    data = {
        "openness": openness,
        "conscientiousness": conscientiousness,
        "extraversion": extraversion,
        "agreeableness": agreeableness,
        "neuroticism": neuroticism
    }
    
    response = requests.post(f"{API_URL}/personalize", json=data)
    recommendations = response.json()['recommended_solutions']
    
    st.write("Recommended Solutions:")
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
