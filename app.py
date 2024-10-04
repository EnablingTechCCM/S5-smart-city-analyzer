from flask import Flask, jsonify, request
from difflib import SequenceMatcher
import csv

app = Flask(__name__)

# Function to load keywords from a CSV file
def load_keywords_from_csv(file_path):
    keywords = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keywords.append(row['Keyword'].lower())  # Ensure all keywords are in lowercase for matching
    return keywords

# Load keywords from separate CSV files
s5_keywords = {
    "Smart": load_keywords_from_csv('smart.csv'),
    "Sensing": load_keywords_from_csv('sensing.csv'),
    "Sustainable": load_keywords_from_csv('sustainable.csv'),
    "Social": load_keywords_from_csv('social.csv'),
    "Safe": load_keywords_from_csv('safe.csv')
}

# Pre-defined solutions
solutions = [
    {
        "solution_id": 1,
        "name": "Didactic Solar Umbrella",
        "description": "An outdoor umbrella equipped with flexible solar panels and weather monitoring tools.",
        "s5_features": {
            "Smart": "Uses cloud services for energy management, offering real-time personalized insights on energy use.",
            "Sensing": "Monitors solar energy in real-time to optimize performance and provide data.",
            "Sustainable": "Umbrella with solar panels reduces carbon footprint and supports sustainability.",
            "Social": "Encourages renewable energy, community engagement, and hands-on solar learning.",
            "Safe": "Follows strict safety standards, ensuring a secure and trustworthy environment.",
            "Associated Personality Traits": "Extraversion and neuroticism. Environmentally conscious individuals likely to be interested in sustainability, eager to learn about renewable energy, and appreciate convenient amenities for daily use."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
        {
        "solution_id": 2,
        "name": "Electric Bicycle with Regenerative Charge",
        "description": "A solar-powered bicycle equipped with regenerative charging for urban commuting.",
        "s5_features": {
            "Smart": "Optimizes energy use and navigation with cloud services and adaptive features.",
            "Sensing": "Monitors battery levels and energy use for real-time data and efficiency.",
            "Sustainable": "Uses solar energy to cut environmental impact and reduce resource dependency.",
            "Social": "Provides a sustainable, eco-friendly transportation option for community well-being.",
            "Safe": "Ensures rider and pedestrian safety with protocols and accident prevention systems.",
            "Associated Personality Traits": "Extraversion and neuroticism: Eco-conscious individuals likely to be open to innovation, motivated by environmental benefits, and appreciate efficient, multifunctional transportation solutions."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 3,
        "name": "Fruit Inspection Using Artificial Vision",
        "description": "AI-powered vision system for urban agriculture, enhancing crop monitoring and management.",
        "s5_features": {
            "Smart": "Uses AI to detect diseases and measure fruit parameters efficiently.",
            "Sensing": "Employs cameras for real-time data on fruit health and conditions.",
            "Sustainable": "Uses eco-friendly methods to minimize resource use and environmental impact.",
            "Social": "Enhances agricultural productivity and crop quality for farming communities.",
            "Safe": "Ensures safety for farmers and consumers by preventing inaccurate assessments.",
            "Associated Personality Traits": "Extraversion and neuroticism: Innovative farmers and urban agriculturalists are interested in advanced technology for improving crop health and yield."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 4,
        "name": "Robot Designed for Teaching Mathematics in Elementary Schools",
        "description": "A LEGO robot system designed to improve elementary-level math education using LabVIEW.",
        "s5_features": {
            "Smart": "Applies AI and robotics in LabVIEW to adapt lessons and engagement.",
            "Sensing": "Uses sensors for real-time feedback and personalized learning experiences.",
            "Sustainable": "Promotes resource efficiency, reducing waste and supporting ecological balance.",
            "Social": "Makes math interactive and fun, fostering collaboration and positive interactions.",
            "Safe": "Ensures a safe learning environment, protecting students' privacy.",
            "Associated Personality Traits": "Agreeableness and neuroticism: Enthusiastic educators, students, and those who are motivated by educational advancement and practical application of STEM concepts."
        },
        "personality_traits": ["Agreeableness", "Neuroticism"]
    },
    {
        "solution_id": 5,
        "name": "Tailored Interfaces for Energy Reduction",
        "description": "Gamified platforms that use AI-driven decision systems to motivate users to reduce energy consumption.",
        "s5_features": {
            "Smart": "Uses cloud services for autonomous energy optimization and efficiency.",
            "Sensing": "Offers real-time data on energy use and environmental conditions.",
            "Sustainable": "Reduces ecological footprints through efficient energy management.",
            "Social": "Boosts community well-being by promoting energy-saving and its benefits.",
            "Safe": "Ensures robust data security and risk management to protect users.",
            "Associated Personality Traits": "Extraversion and Agreeableness: Tech-savvy urban dwellers interested in energy conservation, eager to reduce their environmental impact through engaging and effective methods."
        },
        "personality_traits": ["Extraversion", "Agreeableness"]
    },
    {
        "solution_id": 6,
        "name": "Adaptive Rooftop Shading System",
        "description": "A static rooftop shading system that adapts to seasonal solar angles, optimizing indoor comfort.",
        "s5_features": {
            "Smart": "Uses cloud services to analyze shading configurations from environmental data.",
            "Sensing": "Adapts to solar changes for maximum energy savings and comfort.",
            "Sustainable": "Optimizes solar shading to reduce energy use and support conservation.",
            "Social": "Ensures inclusive thermal comfort for well-being and productivity in communities.",
            "Safe": "Applies strict safety protocols to protect users and environments.",
            "Associated Personality Traits": "Extraversion and neuroticism: Environmentally conscious homeowners and building managers interested in reducing energy costs and improving indoor comfort using long-term solutions for enhancing urban living conditions."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 7,
        "name": "Enhancing Engagement and Efficiency Through ISO 37120, AI, and Gamification",
        "description": "A smart campus model that integrates ISO 37120 indicators, real-time energy monitoring, and gamification.",
        "s5_features": {
            "Smart": "Integrates AI and gamification to create intelligent, engaging city systems.",
            "Sensing": "Enhances responsiveness with real-time insights for data-driven decisions.",
            "Sustainable": "Uses eco-friendly, resource-efficient technologies to reduce environmental impact.",
            "Social": "Fosters community participation in energy management.",
            "Safe": "Ensures safety protocols and data security to protect residents and information.",
            "Associated Personality Traits": "Extraversion, Agreeableness and neuroticism: Students, faculty, and staff likely to be engaged by gamified, tech-forward solutions that promote energy efficiency and contribute to a more sustainable campus environment."
        },
        "personality_traits": ["Extraversion", "Agreeableness", "Neuroticism"]
    },
    {
        "solution_id": 8,
        "name": "AI and Vision for Garments and Activities Detection",
        "description": "AI-powered vision system to optimize thermostat functionality by detecting clothing insulation and user activities.",
        "s5_features": {
            "Smart": "Adapts garments with AI to individual thermal needs and activities.",
            "Sensing": "Uses sensors and cameras for real-time monitoring of thermal comfort.",
            "Sustainable": "Supports ecological balance by optimizing resources through efficient design.",
            "Social": "Enhances well-being with tailored clothing solutions, reducing resource waste.",
            "Safe": "Ensures user well-being through intelligent design and risk management.",
            "Associated Personality Traits": "Extraversion, Agreeableness and neuroticism: Environmentally conscious city dwellers and tech-savvy individuals who value advanced technology and sustainable living practices to enhance their home and building environments."
        },
        "personality_traits": ["Extraversion", "Agreeableness", "Neuroticism"]
    },
    {
        "solution_id": 9,
        "name": "Interfaces Development for Effective Human-Machine Interaction",
        "description": "A hands-free interface system that assists individuals with limited mobility in controlling devices through voice, head movement, and eye gestures.",
        "s5_features": {
            "Smart": "Adapts interfaces with AI to improve efficiency and user experience.",
            "Sensing": "Uses sensors for real-time data on actions like eye-tracking or body movements.",
            "Sustainable": "Focuses on long-term resource conservation and minimizing waste.",
            "Social": "Promotes inclusivity with ethical interactions for diverse users.",
            "Safe": "Ensures safety, data security, and ergonomic design to reduce risks.",
            "Associated Personality Traits": "Openness, Extraversion, and Neuroticism: Individuals facing disabilities, caregivers, healthcare professionals, and tech enthusiasts who prioritize tools that enhance accessibility and independence."
        },
        "personality_traits": ["Openness", "Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 10,
        "name": "Semi-Autonomous Assisting Robot in Children Autism Therapy",
        "description": "A semi-autonomous robot designed to assist children with autism spectrum disorder during therapy.",
        "s5_features": {
            "Smart": "Personalizes therapy with AI, improving outcomes over time.",
            "Sensing": "Uses sensors for real-time data, optimizing therapy effectiveness.",
            "Sustainable": "Promotes sustainable practices to reduce resource consumption.",
            "Social": "Enhances social interaction by supporting diverse autism therapy needs.",
            "Safe": "Prioritizes privacy to build trust with users and caregivers.",
            "Associated Personality Traits": "Openness, Extraversion, and Neuroticism: Therapists, caregivers, and parents of children with ASD. Additionally, professionals interested in innovative technologies and data-driven approaches."
        },
        "personality_traits": ["Openness", "Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 11,
        "name": "Smart Portable Greenhouse for Hydroponic Cultivation",
        "description": "A portable AI-controlled greenhouse for urban hydroponic farming, optimized for high-humidity environments.",
        "s5_features": {
            "Smart": "Enhances efficiency with AI, optimizing conditions and interactions.",
            "Sensing": "Monitors environmental variables, providing real-time data for control.",
            "Sustainable": "Uses renewable energy and eco-friendly practices to reduce environmental impact.",
            "Social": "Supports local food production and community engagement in urban areas.",
            "Safe": "Ensures safety with secure data handling and reliable system operation.",
            "Associated Personality Traits": "Extraversion and Agreeableness: Urban gardeners, tech-savvy individuals, and environmentally conscious residents interested in precise, autonomous systems for managing plant health."
        },
        "personality_traits": ["Extraversion", "Agreeableness"]
    },
    {
        "solution_id": 12,
        "name": "Energy Management Using Digital Twins",
        "description": "A digital twin framework that integrates BIM with VR to optimize building energy management in urban environments.",
        "s5_features": {
            "Smart": "Adapts energy use with AI for comfort and efficiency.",
            "Sensing": "Offers real-time data for predictive monitoring and informed decisions.",
            "Sustainable": "Reduces energy waste and promotes conservation through optimization.",
            "Social": "Ensures inclusivity with adaptable environments for diverse users.",
            "Safe": "Prioritizes occupant well-being and reliable energy systems.",
            "Associated Personality Traits": "Extraversion, Agreeableness, and Neuroticism: Architects, urban planners, and tech-savvy building managers who value resource efficiency and innovative solutions for optimizing building performance."
        },
        "personality_traits": ["Extraversion", "Agreeableness", "Neuroticism"]
    },
    {
        "solution_id": 13,
        "name": "Collaborative Experience Using Digital Technologies",
        "description": "A multiplayer VR platform for architectural education and exploration in urban settings.",
        "s5_features": {
            "Smart": "Personalizes interactions with AI to enhance virtual reality experiences.",
            "Sensing": "Uses sensors for real-time insights to improve user experience.",
            "Sustainable": "Minimizes environmental impact with energy-efficient technologies in exhibitions.",
            "Social": "Enhances social connectivity through accessible and interactive architectural experiences.",
            "Safe": "Ensures a secure, reliable virtual environment prioritizing user well-being.",
            "Associated Personality Traits": "Conscientiousness and Agreeableness: Art educators, architecture enthusiasts, and students who value engaging platforms for architectural exploration and experiential learning."
        },
        "personality_traits": ["Conscientiousness", "Agreeableness"]
    },
    {
        "solution_id": 14,
        "name": "ROBOCOV: Multipurpose Modular Robotic Platform",
        "description": "A modular robotic platform designed for disinfection, public safety, and clinical care, particularly in response to the COVID-19 pandemic.",
        "s5_features": {
            "Smart": "Enhances efficiency with AI and IoT for intelligent functionalities.",
            "Sensing": "Uses sensors for real-time data, optimizing performance and safety.",
            "Sustainable": "Reduces resource consumption with eco-friendly operations.",
            "Social": "Provides accessible telepresence for community well-being in remote areas.",
            "Safe": "Ensures human safety with rigorous standards in dangerous environments.",
            "Associated Personality Traits": "Extraversion and Neuroticism: Public health officials, urban safety managers, and healthcare providers prioritize technology that addresses public health challenges."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 15,
        "name": "Robotic Arm for Assisting Individuals with Limb Loss",
        "description": "A robotic arm designed to assist individuals with upper limb loss, enabling them to perform everyday tasks more effectively.",
        "s5_features": {
            "Smart": "Enhances grasping with AI and machine learning for continuous improvement.",
            "Sensing": "Sensors optimize grasp accuracy, user comfort, and ensure safety.",
            "Sustainable": "Uses eco-friendly materials to minimize waste and promote circular economy.",
            "Social": "Fosters community integration for differently-abled individuals.",
            "Safe": "Ensures safety and reliability with rigorous testing and data security.",
            "Associated Personality Traits": "Extraversion and Neuroticism: Individuals with upper limb loss, prosthetists, and rehabilitation specialists interested in advanced prosthetic solutions."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 16,
        "name": "Obstructive Sleep Apnea (OSA) Detection Using Machine Learning",
        "description": "A cost-effective system that uses machine learning to monitor and diagnose Obstructive Sleep Apnea (OSA) during sleep.",
        "s5_features": {
            "Smart": "AI improves diagnostic precision and provides personalized health insights.",
            "Sensing": "Advanced sensors collect and analyze ECG and sleep data in real-time.",
            "Sustainable": "Uses eco-friendly materials to minimize waste in monitoring devices.",
            "Social": "Enhances community well-being with accessible, early diagnosis for diverse needs.",
            "Safe": "Ensures medical standards and data security, minimizing patient risk.",
            "Associated Personality Traits": "Extraversion and Neuroticism: Healthcare providers, sleep specialists, and city residents seeking cost-effective, accurate solutions for sleep disorder diagnostics."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 17,
        "name": "Smart Power Wheelchair for Assisting People with Mobility Challenges",
        "description": "An electric wheelchair with obstacle avoidance technology using fuzzy logic, designed for individuals with severe mobility limitations.",
        "s5_features": {
            "Smart": "Uses AI and IoT for adaptive, personalized mobility assistance.",
            "Sensing": "Sensors optimize performance and safety by monitoring user and environment.",
            "Sustainable": "Supports environmental stewardship with minimal waste wheelchair design.",
            "Social": "Enhances independence with ethical, inclusive mobility solutions.",
            "Safe": "Ensures safety and trust through rigorous testing and robust standards.",
            "Associated Personality Traits": "Openness, Extraversion, and Neuroticism: Individuals with severe mobility limitations, their caregivers, and rehabilitation specialists seeking advanced, user-friendly wheelchair technologies."
        },
        "personality_traits": ["Openness", "Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 18,
        "name": "Sensing Platform for Weather and Air Quality Monitoring",
        "description": "A low-cost, open-source weather station for real-time environmental monitoring of temperature, humidity, CO2 concentration, and particulate matter.",
        "s5_features": {
            "Smart": "Analyzes data with cloud services for predictive insights and adjustments.",
            "Sensing": "Collects real-time environmental data for informed decision-making.",
            "Sustainable": "Reduces waste and conserves resources using eco-friendly materials and practices.",
            "Social": "Improves public health with accessible, accurate data for community well-being.",
            "Safe": "Ensures data security and safety with rigorous protocols and risk mitigation.",
            "Associated Personality Traits": "Extraversion and Agreeableness: Environmental enthusiasts, community organizers, and small-scale researchers who value real-time data for informed decision-making."
        },
        "personality_traits": ["Extraversion", "Agreeableness"]
    },
    {
        "solution_id": 19,
        "name": "Smart Hydroponic Greenhouse",
        "description": "An intelligent hydroponic greenhouse system for urban agriculture, focused on optimizing tomato production using advanced technology.",
        "s5_features": {
            "Smart": "Enhances crop production with AI, robotics, and automation.",
            "Sensing": "Sensors monitor performance and conditions for data-driven efficiency.",
            "Sustainable": "Uses renewable resources, minimizes waste, and conserves energy.",
            "Social": "Supports fair labor, community well-being, and local engagement.",
            "Safe": "Protects workers and communities with safety protocols and data security.",
            "Associated Personality Traits": "Extraversion, Agreeableness, and Neuroticism: Urban farmers, agricultural technology enthusiasts seeking high-tech systems for optimizing crop production and enhancing local food supply."
        },
        "personality_traits": ["Extraversion", "Agreeableness", "Neuroticism"]
    },
    {
        "solution_id": 20,
        "name": "Automobile Security and Health Monitoring Using Driver Behavior Analysis",
        "description": "A system that monitors and analyzes driver behavior using AI and signal detection theory to improve road safety and driving efficiency.",
        "s5_features": {
            "Smart": "Uses AI for adaptive driving assistance tailored to individual behaviors.",
            "Sensing": "Analyzes driving patterns and feedback to improve driver safety.",
            "Sustainable": "Reduces environmental impact by encouraging eco-friendly driving habits.",
            "Social": "Promotes safe driving through ethical treatment, awareness, and education.",
            "Safe": "Ensures safety with robust collision mitigation and personalized alerts.",
            "Associated Personality Traits": "Extraversion and Neuroticism: Urban drivers who value personalized solutions for reducing accidents, and health professionals interested in preventive care."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 21,
        "name": "Smart Grids Laboratory for Education on Sustainable Energy Solutions",
        "description": "A platform integrating real and virtual scenarios for research, education, and training in smart grid technology and alternative energy sources.",
        "s5_features": {
            "Smart": "Enhances system intelligence for integrating alternative energy sources.",
            "Sensing": "Monitors grid performance and energy usage with sensors.",
            "Sustainable": "Promotes renewable resources and sustainable practices.",
            "Social": "Offers inclusive education and training for renewable energy workforce development.",
            "Safe": "Ensures safety and reliability in the learning environment.",
            "Associated Personality Traits": "Extraversion, Agreeableness, and Neuroticism: Educators and researchers with a strong interest in sustainable energy solutions and smart grid technology."
        },
        "personality_traits": ["Extraversion", "Agreeableness", "Neuroticism"]
    },
    {
        "solution_id": 22,
        "name": "Energy Management Systems and Microgrid Design for Sustainable Energy Consumption",
        "description": "A system that explores the role of microgrids and energy management systems in integrating renewable energy sources in urban environments.",
        "s5_features": {
            "Smart": "Enhances operations with AI and automation in gamified interfaces.",
            "Sensing": "Optimizes efficiency with real-time performance monitoring and data-driven decisions.",
            "Sustainable": "Reduces ecological impact with resource conservation and renewable energy.",
            "Social": "Promotes inclusivity and community well-being with fair labor practices.",
            "Safe": "Safeguards individuals by improving thermal comfort in communities.",
            "Associated Personality Traits": "Extraversion and Neuroticism: Environmentally conscious urban planners, researchers, and energy professionals who appreciate data-driven insights for sustainable urban energy management."
        },
        "personality_traits": ["Extraversion", "Neuroticism"]
    },
    {
        "solution_id": 23,
        "name": "Energy Optimization for Residential HVAC Systems",
        "description": "A system that integrates serious gaming with predictive technology to optimize the usability of residential HVAC systems and reduce energy consumption.",
        "s5_features": {
            "Smart": "Enhances operations with AI and automation in gamified interfaces.",
            "Sensing": "Optimizes efficiency with real-time data and data-driven decisions.",
            "Sustainable": "Reduces ecological impact through conservation and waste reduction.",
            "Social": "Promotes inclusivity and community well-being with fair labor practices.",
            "Safe": "Improves safety and comfort for individuals and communities.",
            "Associated Personality Traits": "Extraversion, Agreeableness, and Neuroticism: Tech-savvy homeowners who enjoy interactive tools for optimizing home comfort and energy use."
        },
        "personality_traits": ["Extraversion", "Agreeableness", "Neuroticism"]
    }
]

# Function to calculate similarity score between two strings
def calculate_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Function to suggest personality traits based on product name and description
def suggest_personality_traits(product_name, product_description, solutions):
    best_match = None
    highest_score = 0
    
    for solution in solutions:
        # Calculate similarity between input and existing solutions
        name_similarity = calculate_similarity(product_name, solution['name'])
        description_similarity = calculate_similarity(product_description, solution['description'])
        
        # Average the two similarity scores
        avg_similarity = (name_similarity + description_similarity) / 2
        
        # Track the best match
        if avg_similarity > highest_score:
            highest_score = avg_similarity
            best_match = solution
    
    if best_match:
        return best_match['personality_traits']
    else:
        return "No relevant match found."

# Route to analyze and suggest personality traits based on input
@app.route('/suggest_personality_traits', methods=['POST'])
def suggest_personality_traits_route():
    data = request.json
    product_name = data.get('product_name')
    description = data.get('description')
    
    personality_traits = suggest_personality_traits(product_name, description, solutions)
    
    return jsonify({"personality_traits": personality_traits})

@app.route('/solutions', methods=['GET'])
def get_solutions():
    return jsonify(solutions), 200

@app.route('/analyze', methods=['POST'])
def analyze_product():
    data = request.json
    product_name = data.get('product_name')
    description = data.get('description')
    features = [feature.lower() for feature in data.get('features')]  # Lowercase for matching

    # Function to check if any feature matches keywords for a specific S5 category
    def check_s5_category(features, category):
        return any(keyword in feature for feature in features for keyword in s5_keywords[category])

    # Analyze the product based on S5 categories
    s5_analysis = {
        "Smart": check_s5_category(features, "Smart"),
        "Sensing": check_s5_category(features, "Sensing"),
        "Sustainable": check_s5_category(features, "Sustainable"),
        "Social": check_s5_category(features, "Social"),
        "Safe": check_s5_category(features, "Safe")
    }

    return jsonify({
        "product_name": product_name,
        "s5_analysis": s5_analysis
    }), 200

@app.route('/personalize', methods=['POST'])
def personalize():
    data = request.json
    openness = data.get('openness')
    conscientiousness = data.get('conscientiousness')
    extraversion = data.get('extraversion')
    agreeableness = data.get('agreeableness')
    neuroticism = data.get('neuroticism')

    # Define a function to calculate a match score
    def calculate_match(solution_traits, user_traits):
        match_score = 0
        for trait, score in user_traits.items():
            if trait in solution_traits:
                match_score += score  # Increase score for matching traits
        return match_score

    # Create a dictionary of user traits
    user_traits = {
        "Openness": openness,
        "Conscientiousness": conscientiousness,
        "Extraversion": extraversion,
        "Agreeableness": agreeableness,
        "Neuroticism": neuroticism
    }

    # Rank solutions based on how well they match the user's personality traits
    ranked_solutions = sorted(
        solutions,
        key=lambda sol: calculate_match(sol['personality_traits'], user_traits),
        reverse=True  # Highest match scores first
    )

    # Return the top recommendations
    return jsonify({
        "recommended_solutions": ranked_solutions[:7]  # Top 5 matches
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
