library(shiny)
library(httr)
library(dplyr)
library(plotly)
library(stringdist)  # For string similarity calculation


# Predefined solutions (from your app)
# Define the 23 predefined solutions
solutions <- list(
  list(
    solution_id = 1,
    name = "Didactic Solar Umbrella",
    description = "An outdoor umbrella equipped with flexible solar panels and weather monitoring tools.",
    s5_features = list(
      Smart = "Uses cloud services for energy management, offering real-time personalized insights on energy use.",
      Sensing = "Monitors solar energy in real-time to optimize performance and provide data.",
      Sustainable = "Umbrella with solar panels reduces carbon footprint and supports sustainability.",
      Social = "Encourages renewable energy, community engagement, and hands-on solar learning.",
      Safe = "Follows strict safety standards, ensuring a secure and trustworthy environment."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 2,
    name = "Electric Bicycle with Regenerative Charge",
    description = "A solar-powered bicycle equipped with regenerative charging for urban commuting.",
    s5_features = list(
      Smart = "Optimizes energy use and navigation with cloud services and adaptive features.",
      Sensing = "Monitors battery levels and energy use for real-time data and efficiency.",
      Sustainable = "Uses solar energy to cut environmental impact and reduce resource dependency.",
      Social = "Provides a sustainable, eco-friendly transportation option for community well-being.",
      Safe = "Ensures rider and pedestrian safety with protocols and accident prevention systems."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 3,
    name = "Fruit Inspection Using Artificial Vision",
    description = "AI-powered vision system for urban agriculture, enhancing crop monitoring and management.",
    s5_features = list(
      Smart = "Uses AI to detect diseases and measure fruit parameters efficiently.",
      Sensing = "Employs cameras for real-time data on fruit health and conditions.",
      Sustainable = "Uses eco-friendly methods to minimize resource use and environmental impact.",
      Social = "Enhances agricultural productivity and crop quality for farming communities.",
      Safe = "Ensures safety for farmers and consumers by preventing inaccurate assessments."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 4,
    name = "Robot Designed for Teaching Mathematics in Elementary Schools",
    description = "A LEGO robot system designed to improve elementary-level math education using LabVIEW.",
    s5_features = list(
      Smart = "Applies AI and robotics in LabVIEW to adapt lessons and engagement.",
      Sensing = "Uses sensors for real-time feedback and personalized learning experiences.",
      Sustainable = "Promotes resource efficiency, reducing waste and supporting ecological balance.",
      Social = "Makes math interactive and fun, fostering collaboration and positive interactions.",
      Safe = "Ensures a safe learning environment, protecting students' privacy."
    ),
    personality_traits = c("Agreeableness", "Neuroticism")
  ),
  list(
    solution_id = 5,
    name = "Tailored Interfaces for Energy Reduction",
    description = "Gamified platforms that use AI-driven decision systems to motivate users to reduce energy consumption.",
    s5_features = list(
      Smart = "Uses cloud services for autonomous energy optimization and efficiency.",
      Sensing = "Offers real-time data on energy use and environmental conditions.",
      Sustainable = "Reduces ecological footprints through efficient energy management.",
      Social = "Boosts community well-being by promoting energy-saving and its benefits.",
      Safe = "Ensures robust data security and risk management to protect users."
    ),
    personality_traits = c("Extraversion", "Agreeableness")
  ),
  list(
    solution_id = 6,
    name = "Adaptive Rooftop Shading System",
    description = "A static rooftop shading system that adapts to seasonal solar angles, optimizing indoor comfort.",
    s5_features = list(
      Smart = "Uses cloud services to analyze shading configurations from environmental data.",
      Sensing = "Adapts to solar changes for maximum energy savings and comfort.",
      Sustainable = "Optimizes solar shading to reduce energy use and support conservation.",
      Social = "Ensures inclusive thermal comfort for well-being and productivity in communities.",
      Safe = "Applies strict safety protocols to protect users and environments."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 7,
    name = "Enhancing Engagement and Efficiency Through ISO 37120, AI, and Gamification",
    description = "A smart campus model that integrates ISO 37120 indicators, real-time energy monitoring, and gamification.",
    s5_features = list(
      Smart = "Integrates AI and gamification to create intelligent, engaging city systems.",
      Sensing = "Enhances responsiveness with real-time insights for data-driven decisions.",
      Sustainable = "Uses eco-friendly, resource-efficient technologies to reduce environmental impact.",
      Social = "Fosters community participation in energy management.",
      Safe = "Ensures safety protocols and data security to protect residents and information."
    ),
    personality_traits = c("Extraversion", "Agreeableness", "Neuroticism")
  ),
  list(
    solution_id = 8,
    name = "AI and Vision for Garments and Activities Detection",
    description = "AI-powered vision system to optimize thermostat functionality by detecting clothing insulation and user activities.",
    s5_features = list(
      Smart = "Adapts garments with AI to individual thermal needs and activities.",
      Sensing = "Uses sensors and cameras for real-time monitoring of thermal comfort.",
      Sustainable = "Supports ecological balance by optimizing resources through efficient design.",
      Social = "Enhances well-being with tailored clothing solutions, reducing resource waste.",
      Safe = "Ensures user well-being through intelligent design and risk management."
    ),
    personality_traits = c("Extraversion", "Agreeableness", "Neuroticism")
  ),
  list(
    solution_id = 9,
    name = "Interfaces Development for Effective Human-Machine Interaction",
    description = "A hands-free interface system that assists individuals with limited mobility in controlling devices through voice, head movement, and eye gestures.",
    s5_features = list(
      Smart = "Adapts interfaces with AI to improve efficiency and user experience.",
      Sensing = "Uses sensors for real-time data on actions like eye-tracking or body movements.",
      Sustainable = "Focuses on long-term resource conservation and minimizing waste.",
      Social = "Promotes inclusivity with ethical interactions for diverse users.",
      Safe = "Ensures safety, data security, and ergonomic design to reduce risks."
    ),
    personality_traits = c("Openness", "Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 10,
    name = "Semi-Autonomous Assisting Robot in Children Autism Therapy",
    description = "A semi-autonomous robot designed to assist children with autism spectrum disorder during therapy.",
    s5_features = list(
      Smart = "Personalizes therapy with AI, improving outcomes over time.",
      Sensing = "Uses sensors for real-time data, optimizing therapy effectiveness.",
      Sustainable = "Promotes sustainable practices to reduce resource consumption.",
      Social = "Enhances social interaction by supporting diverse autism therapy needs.",
      Safe = "Prioritizes privacy to build trust with users and caregivers."
    ),
    personality_traits = c("Openness", "Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 11,
    name = "Smart Portable Greenhouse for Hydroponic Cultivation",
    description = "A portable AI-controlled greenhouse for urban hydroponic farming, optimized for high-humidity environments.",
    s5_features = list(
      Smart = "Enhances efficiency with AI, optimizing conditions and interactions.",
      Sensing = "Monitors environmental variables, providing real-time data for control.",
      Sustainable = "Uses renewable energy and eco-friendly practices to reduce environmental impact.",
      Social = "Supports local food production and community engagement in urban areas.",
      Safe = "Ensures safety with secure data handling and reliable system operation."
    ),
    personality_traits = c("Extraversion", "Agreeableness")
  ),
  list(
    solution_id = 12,
    name = "Energy Management Using Digital Twins",
    description = "A digital twin framework that integrates BIM with VR to optimize building energy management in urban environments.",
    s5_features = list(
      Smart = "Adapts energy use with AI for comfort and efficiency.",
      Sensing = "Offers real-time data for predictive monitoring and informed decisions.",
      Sustainable = "Reduces energy waste and promotes conservation through optimization.",
      Social = "Ensures inclusivity with adaptable environments for diverse users.",
      Safe = "Prioritizes occupant well-being and reliable energy systems."
    ),
    personality_traits = c("Extraversion", "Agreeableness", "Neuroticism")
  ),
  list(
    solution_id = 13,
    name = "Collaborative Experience Using Digital Technologies",
    description = "A multiplayer VR platform for architectural education and exploration in urban settings.",
    s5_features = list(
      Smart = "Personalizes interactions with AI to enhance virtual reality experiences.",
      Sensing = "Uses sensors for real-time insights to improve user experience.",
      Sustainable = "Minimizes environmental impact with energy-efficient technologies in exhibitions.",
      Social = "Enhances social connectivity through accessible and interactive architectural experiences.",
      Safe = "Ensures a secure, reliable virtual environment prioritizing user well-being."
    ),
    personality_traits = c("Conscientiousness", "Agreeableness")
  ),
  list(
    solution_id = 14,
    name = "ROBOCOV: Multipurpose Modular Robotic Platform",
    description = "A modular robotic platform designed for disinfection, public safety, and clinical care, particularly in response to the COVID-19 pandemic.",
    s5_features = list(
      Smart = "Enhances efficiency with AI and IoT for intelligent functionalities.",
      Sensing = "Uses sensors for real-time data, optimizing performance and safety.",
      Sustainable = "Reduces resource consumption with eco-friendly operations.",
      Social = "Provides accessible telepresence for community well-being in remote areas.",
      Safe = "Ensures human safety with rigorous standards in dangerous environments."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 15,
    name = "Robotic Arm for Assisting Individuals with Limb Loss",
    description = "A robotic arm designed to assist individuals with upper limb loss, enabling them to perform everyday tasks more effectively.",
    s5_features = list(
      Smart = "Enhances grasping with AI and machine learning for continuous improvement.",
      Sensing = "Sensors optimize grasp accuracy, user comfort, and ensure safety.",
      Sustainable = "Uses eco-friendly materials to minimize waste and promote circular economy.",
      Social = "Fosters community integration for differently-abled individuals.",
      Safe = "Ensures safety and reliability with rigorous testing and data security."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 16,
    name = "Obstructive Sleep Apnea (OSA) Detection Using Machine Learning",
    description = "A cost-effective system that uses machine learning to monitor and diagnose Obstructive Sleep Apnea (OSA) during sleep.",
    s5_features = list(
      Smart = "AI improves diagnostic precision and provides personalized health insights.",
      Sensing = "Advanced sensors collect and analyze ECG and sleep data in real-time.",
      Sustainable = "Uses eco-friendly materials to minimize waste in monitoring devices.",
      Social = "Enhances community well-being with accessible, early diagnosis for diverse needs.",
      Safe = "Ensures medical standards and data security, minimizing patient risk."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 17,
    name = "Smart Power Wheelchair for Assisting People with Mobility Challenges",
    description = "An electric wheelchair with obstacle avoidance technology using fuzzy logic, designed for individuals with severe mobility limitations.",
    s5_features = list(
      Smart = "Uses AI and IoT for adaptive, personalized mobility assistance.",
      Sensing = "Sensors optimize performance and safety by monitoring user and environment.",
      Sustainable = "Supports environmental stewardship with minimal waste wheelchair design.",
      Social = "Enhances independence with ethical, inclusive mobility solutions.",
      Safe = "Ensures safety and trust through rigorous testing and robust standards."
    ),
    personality_traits = c("Openness", "Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 18,
    name = "Sensing Platform for Weather and Air Quality Monitoring",
    description = "A low-cost, open-source weather station for real-time environmental monitoring of temperature, humidity, CO2 concentration, and particulate matter.",
    s5_features = list(
      Smart = "Analyzes data with cloud services for predictive insights and adjustments.",
      Sensing = "Collects real-time environmental data for informed decision-making.",
      Sustainable = "Reduces waste and conserves resources using eco-friendly materials and practices.",
      Social = "Improves public health with accessible, accurate data for community well-being.",
      Safe = "Ensures data security and safety with rigorous protocols and risk mitigation."
    ),
    personality_traits = c("Extraversion", "Agreeableness")
  ),
  list(
    solution_id = 19,
    name = "Smart Hydroponic Greenhouse",
    description = "An intelligent hydroponic greenhouse system for urban agriculture, focused on optimizing tomato production using advanced technology.",
    s5_features = list(
      Smart = "Enhances crop production with AI, robotics, and automation.",
      Sensing = "Sensors monitor performance and conditions for data-driven efficiency.",
      Sustainable = "Uses renewable resources, minimizes waste, and conserves energy.",
      Social = "Supports fair labor, community well-being, and local engagement.",
      Safe = "Protects workers and communities with safety protocols and data security."
    ),
    personality_traits = c("Extraversion", "Agreeableness", "Neuroticism")
  ),
  list(
    solution_id = 20,
    name = "Automobile Security and Health Monitoring Using Driver Behavior Analysis",
    description = "A system that monitors and analyzes driver behavior using AI and signal detection theory to improve road safety and driving efficiency.",
    s5_features = list(
      Smart = "Uses AI for adaptive driving assistance tailored to individual behaviors.",
      Sensing = "Analyzes driving patterns and feedback to improve driver safety.",
      Sustainable = "Reduces environmental impact by encouraging eco-friendly driving habits.",
      Social = "Promotes safe driving through ethical treatment, awareness, and education.",
      Safe = "Ensures safety with robust collision mitigation and personalized alerts."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 21,
    name = "Smart Grids Laboratory for Education on Sustainable Energy Solutions",
    description = "A platform integrating real and virtual scenarios for research, education, and training in smart grid technology and alternative energy sources.",
    s5_features = list(
      Smart = "Enhances system intelligence for integrating alternative energy sources.",
      Sensing = "Monitors grid performance and energy usage with sensors.",
      Sustainable = "Promotes renewable resources and sustainable practices.",
      Social = "Offers inclusive education and training for renewable energy workforce development.",
      Safe = "Ensures safety and reliability in the learning environment."
    ),
    personality_traits = c("Extraversion", "Agreeableness", "Neuroticism")
  ),
  list(
    solution_id = 22,
    name = "Energy Management Systems and Microgrid Design for Sustainable Energy Consumption",
    description = "A system that explores the role of microgrids and energy management systems in integrating renewable energy sources in urban environments.",
    s5_features = list(
      Smart = "Enhances operations with AI and automation in gamified interfaces.",
      Sensing = "Optimizes efficiency with real-time performance monitoring and data-driven decisions.",
      Sustainable = "Reduces ecological impact with resource conservation and renewable energy.",
      Social = "Promotes inclusivity and community well-being with fair labor practices.",
      Safe = "Safeguards individuals by improving thermal comfort in communities."
    ),
    personality_traits = c("Extraversion", "Neuroticism")
  ),
  list(
    solution_id = 23,
    name = "Energy Optimization for Residential HVAC Systems",
    description = "A system that integrates serious gaming with predictive technology to optimize the usability of residential HVAC systems and reduce energy consumption.",
    s5_features = list(
      Smart = "Enhances operations with AI and automation in gamified interfaces.",
      Sensing = "Optimizes efficiency with real-time data and data-driven decisions.",
      Sustainable = "Reduces ecological impact through conservation and waste reduction.",
      Social = "Promotes inclusivity and community well-being with fair labor practices.",
      Safe = "Improves safety and comfort for individuals and communities."
    ),
    personality_traits = c("Extraversion", "Agreeableness", "Neuroticism")
  )
)



# Function to calculate similarity score between two strings
calculate_similarity <- function(a, b) {
  1 - stringdist::stringdist(a, b, method = "jw")  # Jaro-Winkler similarity
}

# Function to load keywords and levels from CSV
load_keywords_and_levels <- function(file_path) {
  data <- read.csv(file_path)
  keywords_levels <- setNames(data$Level, tolower(data$Keyword))
  return(keywords_levels)
}

# Load keywords and levels for each S5 category
s5_keywords <- list(
  Smart = load_keywords_and_levels("smart.csv"),
  Sensing = load_keywords_and_levels("sensing.csv"),
  Sustainable = load_keywords_and_levels("sustainable.csv"),
  Social = load_keywords_and_levels("social.csv"),
  Safe = load_keywords_and_levels("safe.csv")
)

# Function to calculate average level based on matched keywords and return matched keywords with levels
calculate_average_level <- function(text, category_keywords) {
  matched_levels <- c()
  matched_keywords <- list()
  
  for (keyword in names(category_keywords)) {
    if (grepl(keyword, text, ignore.case = TRUE)) {
      matched_levels <- c(matched_levels, category_keywords[[keyword]])
      matched_keywords <- append(matched_keywords, list(list("keyword" = keyword, "level" = category_keywords[[keyword]])))
    }
  }
  
  if (length(matched_levels) > 0) {
    avg_level <- mean(matched_levels)
  } else {
    avg_level <- 0  # Return 0 if no keywords matched
  }
  
  return(list("average" = avg_level, "keywords" = matched_keywords))
}

# Function to suggest personality traits based on product name and description
suggest_personality_traits <- function(product_name, product_description, solutions) {
  best_match <- NULL
  highest_score <- 0
  
  for (solution in solutions) {
    # Calculate similarity between input and existing solutions
    name_similarity <- calculate_similarity(product_name, solution$name)
    description_similarity <- calculate_similarity(product_description, solution$description)
    
    # Average the two similarity scores
    avg_similarity <- (name_similarity + description_similarity) / 2
    
    # Track the best match
    if (avg_similarity > highest_score) {
      highest_score <- avg_similarity
      best_match <- solution
    }
  }
  
  if (!is.null(best_match)) {
    return(best_match$personality_traits)
  } else {
    return(c())  # Return an empty vector if no match is found
  }
}

# Function to suggest products based on personality traits
suggest_products_based_on_traits <- function(user_traits, solutions) {
  calculate_match <- function(solution_traits, user_traits) {
    match_score <- sum(sapply(names(user_traits), function(trait) {
      if (trait %in% solution_traits) user_traits[[trait]] else 0
    }))
    return(match_score)
  }
  
  ranked_solutions <- solutions[order(sapply(solutions, function(sol) {
    calculate_match(sol$personality_traits, user_traits)
  }), decreasing = TRUE)]
  
  return(ranked_solutions[1:7])  # Return top 7 matches
}

# Define the Shiny server logic
server <- function(input, output, session) {
  
  # Reactive value to store analysis results
  s5_analysis_result <- reactiveVal(NULL)
  
  # Perform S5 analysis when button is clicked
  observeEvent(input$analyze_product, {
    product_name <- input$product_name
    product_description <- input$product_description
    features <- unlist(strsplit(input$features, ",\\s*"))  # Split by commas and optional whitespace
    
    # Combine all inputs into a single text block for analysis
    combined_text <- paste(product_name, product_description, paste(features, collapse = " "), sep = " ")
    
    # Perform S5 analysis based on the combined text
    s5_analysis <- lapply(names(s5_keywords), function(category) {
      calculate_average_level(combined_text, s5_keywords[[category]])
    })
    
    # Save the S5 analysis results
    names(s5_analysis) <- names(s5_keywords)  # Assign names to the results for easier access
    s5_analysis_result(s5_analysis)
    
    # Suggest personality traits based on the product name and description
    personality_traits <- suggest_personality_traits(product_name, product_description, solutions)
    
    # Update sliders based on the suggested personality traits
    updateSliderInput(session, "openness", value = ifelse("Openness" %in% personality_traits, 1, 0))
    updateSliderInput(session, "conscientiousness", value = ifelse("Conscientiousness" %in% personality_traits, 1, 0))
    updateSliderInput(session, "extraversion", value = ifelse("Extraversion" %in% personality_traits, 1, 0))
    updateSliderInput(session, "agreeableness", value = ifelse("Agreeableness" %in% personality_traits, 1, 0))
    updateSliderInput(session, "neuroticism", value = ifelse("Neuroticism" %in% personality_traits, 1, 0))
  })
  
  # Display the S5 analysis results with grouped levels and keywords
  output$s5_analysis_output <- renderPrint({
    req(s5_analysis_result())
    s5_results <- s5_analysis_result()
    
    for (category in names(s5_results)) {
      avg_percentage <- round(s5_results[[category]]$average / 3 * 100, 2)
      keywords <- s5_results[[category]]$keywords
      
      if (length(keywords) > 0) {
        # Group keywords by level
        grouped_keywords <- split(sapply(keywords, function(kw) kw$keyword), sapply(keywords, function(kw) kw$level))
        keyword_levels_str <- sapply(names(grouped_keywords), function(level) {
          paste0("Level ", level, ": ", paste(grouped_keywords[[level]], collapse = ", "))
        })
        keyword_levels_str_combined <- paste(keyword_levels_str, collapse = ", ")
        cat(paste0(category, " (", avg_percentage, "%): ", keyword_levels_str_combined, "\n"))
      } else {
        cat(paste0(category, " (", avg_percentage, "%): No relevant keywords found\n"))
      }
    }
  })
  
  # Render the radar chart based on S5 analysis results
  output$s5_radar_chart <- renderPlotly({
    req(s5_analysis_result())
    
    # Labels for the radar chart (categories)
    labels <- names(s5_analysis_result())
    
    # Extract r values from s5_analysis_result (average levels divided by 3)
    values <- round(sapply(s5_analysis_result(), function(res) res$average / 3), 4)  # Round to 2 decimals
    
    
    # Regular polygon for comparison (ideal case where r = 1 for all categories)
    r_regular <- rep(1, length(labels))
    
    # Convert labels to appropriate angles for radar chart (72° intervals)
    theta_deg <- seq(0, 288, by = 72)
    
    # Calculating the area for the evaluated and ideal cases
    calc_area_polar <- function(r, theta) {
      n <- length(r)
      area <- 0
      for (i in 1:(n-1)) {
        area <- area + r[i] * r[i+1] * sin(theta[i+1] - theta[i])
      }
      area <- area + r[n] * r[1] * sin(theta[1] - theta[n])  # Close the polygon
      return(abs(area) / 2)
    }
    
    theta_rad <- theta_deg * (pi / 180)  # Convert angles to radians
    
    # Calculate areas for the ideal and evaluated polygons
    area_regular <- round(calc_area_polar(r_regular, theta_rad), 2)
    area_irregular <- round(calc_area_polar(values, theta_rad), 2)
    
    # Calculate the proportion of the evaluated case compared to the ideal case
    proportion <- round(area_irregular / area_regular, 2)
    
    # Centroid calculation in Cartesian coordinates
    x <- values * cos(theta_rad)
    y <- values * sin(theta_rad)
    centroid_x <- mean(x)
    centroid_y <- mean(y)
    
    # Convert the centroid back to polar coordinates (r, theta)
    centroid_r <- round(sqrt(centroid_x^2 + centroid_y^2), 2)
    centroid_theta_rad <- atan2(centroid_y, centroid_x)
    centroid_theta_deg <- round(centroid_theta_rad * (180 / pi), 2)
    if (centroid_theta_deg < 0) {
      centroid_theta_deg <- centroid_theta_deg + 360
    }
    
    # Create the radar chart using Plotly
    plot_ly(type = 'scatterpolar', mode = 'lines+markers') %>%
      # Ideal Case with area calculation and red dashed line
      add_trace(r = c(r_regular, r_regular[1]), theta = c(theta_deg, theta_deg[1]), 
                line = list(dash = 'dash', color = 'red'), 
                marker = list(size = 8, color = 'orange'), 
                name = paste('Ideal Case (Area:', area_regular, ')')) %>%
      # Evaluated Case with area calculation and filled polygon
      add_trace(r = c(values, values[1]), theta = c(theta_deg, theta_deg[1]), 
                fill = 'toself', fillcolor = 'rgba(54, 163, 141, 0.4)', 
                line = list(color = 'rgba(54, 163, 141, 1)'), 
                marker = list(size = 8, color = 'rgba(54, 163, 141, 1)'), 
                name = paste('Evaluated Case (Area:', area_irregular, ')')) %>%
      # Centroid point on the radar chart
      add_trace(r = centroid_r, theta = centroid_theta_deg, 
                mode = 'markers', marker = list(size = 10, color = 'red'), 
                name = paste('Centroid (r:', centroid_r, ', phi:', centroid_theta_deg, ')')) %>%
      layout(
        title = paste('Penta-S Evaluation\nProportion:', proportion),
        margin = list(t = 100),  # Adjust top margin to avoid title overlap
        polar = list(
          angularaxis = list(
            tickmode = 'array',
            tickvals = c(0, 72, 144, 216, 288),
            ticktext = c('Smart', 'Sensing', 'Sustainable', 'Social', 'Safe')
          )
        )
      )
  })
  
  # Reactive value for recommended solutions
  recommended_solutions <- reactive({
    req(input$analyze_personality)
    
    user_traits <- list(
      Openness = input$openness,
      Conscientiousness = input$conscientiousness,
      Extraversion = input$extraversion,
      Agreeableness = input$agreeableness,
      Neuroticism = input$neuroticism
    )
    
    suggest_products_based_on_traits(user_traits, solutions)
  })
  
  # Display recommended products
  output$recommended_products <- renderUI({
    req(recommended_solutions())
    solution_list <- recommended_solutions()
    tagList(
      lapply(solution_list, function(sol) {
        div(
          h3(sol$name),
          p(strong("Description:"), sol$description),
          h4("S5 Features:"),
          p(strong("Smart:"), sol$s5_features$Smart),
          p(strong("Sensing:"), sol$s5_features$Sensing),
          p(strong("Sustainable:"), sol$s5_features$Sustainable),
          p(strong("Social:"), sol$s5_features$Social),
          p(strong("Safe:"), sol$s5_features$Safe)
        )
      })
    )
  })
}

#observeEvent(input$improve_s5, {
# session$sendCustomMessage(type = 'openURL', message = "https://chatgpt.com/g/g-7SqJsJoeF-smart-city-s5-compliance-assistant")
#})

url<-"https://chatgpt.com/g/g-7SqJsJoeF-smart-city-pentagon-compliance-assistant"

# Shiny UI
ui <- fluidPage(
  
  titlePanel("Smart City Pentagon Framework Analyzer"),
  
  sidebarLayout(
    sidebarPanel(
      textInput("product_name", "Product Name"),
      textAreaInput("product_description", "Product Description"),
      textInput("features", "Product Features (comma-separated)"),
      actionButton("analyze_product", "Analyze Product"),
      br(), br(),
      # Improvement button with the URL
      actionButton("improve_s5", "Improve your product's S5 features", 
                   style = "background-color:Green;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;",
                   onclick = sprintf("window.open('%s')", url)),
      br(), br(),
      sliderInput("openness", "Openness", 0, 1, value = 0.5),
      sliderInput("conscientiousness", "Conscientiousness", 0, 1, value = 0.5),
      sliderInput("extraversion", "Extraversion", 0, 1, value = 0.5),
      sliderInput("agreeableness", "Agreeableness", 0, 1, value = 0.5),
      sliderInput("neuroticism", "Neuroticism", 0, 1, value = 0.5),
      actionButton("analyze_personality", "Get Recommendations")
      
    ),
    
    
    mainPanel(
      # Adjust the width of the verbatimTextOutput by wrapping it in a div
      div(verbatimTextOutput("s5_analysis_output"), style = "width:800px;"),
      # Adjust the size of the plotlyOutput by setting width and height
      plotlyOutput("s5_radar_chart", width = "800px", height = "800px"),  
      uiOutput("recommended_products")
    )
  )
)

# Run the Shiny application
shinyApp(ui = ui, server = server)
