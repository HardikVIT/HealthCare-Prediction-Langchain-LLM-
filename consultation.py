from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv ()
class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str

    def __init__(self,
                 model_name: str,
                 openai_api_key: str = os.getenv('OPENROUTER_API_KEY'),
                 openai_api_base: str = "https://openrouter.ai/api/v1",
                 **kwargs):
        openai_api_key = openai_api_key or os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name, **kwargs)
        

llm = ChatOpenRouter(
    model_name="deepseek/deepseek-r1:free"
)
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
template_predicted=ChatPromptTemplate.from_template("""
Input:
    Disease: {disease}

Response Structure:
    Summary
    "{disease} is a common condition. Here's a quick medical brief:"

Diagnosis
    Key symptoms
    Common causes

Basic test (if relevant)
    Treatment
    First-line meds (OTC/prescription)
Home care tips
When to see a doctor
Urgent Signs

List 2–3 symptoms needing ER care
Disclaimer
"Consult a licensed doctor for accurate diagnosis and care."
""")                                              
template_medical = ChatPromptTemplate.from_template("""
MEDICAL CONSULTATION TEMPLATE                                                   

Patient Information Summary:
- Age: {age}
- Gender: {gender}
- Primary Concern: {query}

Consultation Guidelines for AI Response:
1. Express empathy and understanding in opening statement
2. Analyze symptom patterns and potential risk factors
3. Identify 3-4 common conditions associated with reported symptoms
4. Provide differentiated self-care options based on symptom severity
5. Specify multiple clear indicators for urgent care needs
6. Include symptom monitoring recommendations
7. Maintain formal but approachable tone

Response Framework:

1. Initial Evaluation
Acknowledge the patient's concern and summarize key symptoms. Note any concerning patterns or missing information that would help assessment.

Example: "Thank you for sharing your health concerns. Based on the description of [symptoms], which have persisted for [duration], there are several potential considerations..."

2. Potential Health Considerations
List 3-4 possible conditions that align with symptoms, including:
- Typical presentation patterns
- Common risk factors
- Frequency in patient's age group
- Environmental/lifestyle connections

3. Care Recommendations
Tiered suggestions based on symptom severity:
Mild Symptoms:
- Specific OTC medications with dosage notes
- Environmental modifications
- Monitoring techniques
- Dietary considerations

Moderate Symptoms:
- Warning signs to watch for
- Telehealth options
- Urgent care vs ER guidance

4. Immediate Care Indicators
List specific scenarios requiring urgent attention:
- Cardiovascular warning signs
- Neurological red flags
- Respiratory emergencies
- Systemic symptoms (e.g., high fever ranges)

5. Follow-Up Guidance
- Recommended specialists if symptoms persist
- Diagnostic tests to request
- Preparation tips for clinical visits

6. Professional Disclaimer
"This preliminary analysis represents potential health considerations based on limited information. Individual medical histories and physical examinations are essential for accurate diagnosis. Please consult licensed healthcare providers for personalized assessment, particularly if symptoms progress or concerning signs develop."

Sample Response Opening:
"I appreciate you reaching out with these health concerns. Let's carefully examine the symptoms you've described..." 

[Proceed with structured analysis using above framework]

This format removes markdown while adding clinical depth through:
- Expanded symptom analysis categories
- Tiered care recommendations
- Specific clinical indicators
- Enhanced patient guidance elements
- Clear information hierarchy through spacing and indentation
""")

template_mental = ChatPromptTemplate.from_template("""
MENTAL HEALTH SUPPORT TEMPLATE

Client Profile Overview:  
- Age: {age}  
- Gender: {gender}  
- Reported Stress Level (1-10): {stress_level}  
- Sleep Pattern Description: {sleep_quality}  
- Emotional State: {current_mood}  
- Primary Concerns: {thoughts}  

Therapeutic Response Guidelines:  
1. Establish emotional safety through compassionate acknowledgment  
2. Practice active listening through reflective paraphrasing  
3. Incorporate trauma-informed communication principles  
4. Offer 2-3 evidence-based interventions per concern category  
5. Include psychoeducation components when appropriate  
6. Maintain cultural sensitivity regarding emotional expression  
7. Provide escalation paths for crisis situations  

Response Framework:  

1. Emotional Acknowledgement  
Demonstrate understanding of stated experiences using validating language.  
Example: "I hear you're experiencing [specific emotion] around [situation]. Many people find these circumstances challenging, and your feelings are completely valid."

2. Contextual Exploration  
Include 2-3 reflective prompts to deepen self-awareness:  
  "How has this situation impacted your daily routines?"  
  "What moments bring slight relief from these feelings?"  
  "How does this compare to previous challenges you've navigated?"

3. Tiered Support Strategies  
A. Stress Management (Customized to reported level 1-10):  
For 1-4: Mindfulness exercises (5 senses grounding technique)  
For 5-7: Structured worry time + progressive muscle relaxation  
For 8-10: Crisis containment strategies (temperature modulation, safe space visualization)  

B. Sleep Optimization:  
  Circadian rhythm adjustment techniques  
  Sensory reduction checklist for sleep environments  
  Wind-down routine development guidelines  

C. Mood Support:  
  Emotional tracking worksheet suggestions  
  Behavioral activation planning templates  
  Social connection micro-goals  

4. Progress Monitoring Guidance  
  Recommended self-check intervals (e.g., daily mood journaling)  
  Progress measurement indicators (e.g., sleep efficiency tracking)  
  Warning sign documentation (escalation patterns to watch for)  

5. Professional Support Pathways  
  Indicators for considering therapy (specific functional impairments)  
  Types of specialists (CBT practitioners vs. somatic therapists)  
  Preparation checklist for first therapy session  

6. Ongoing Support Reminders  
  Community resource suggestions (support groups, helplines)  
  Micro-self-care rituals (60-second breathing sequences)  
  Emergency contact information for crisis situations  

7. Closing Reinforcement  
Personalized affirmation recognizing client strengths:  
Your willingness to address these challenges shows remarkable resilience. Each small effort contributes to meaningful change.

Professional Note:  
This supportive guidance does not constitute medical advice or formal therapy. Individual experiences vary significantly, and persistent difficulties should be addressed with licensed mental health professionals. If you experience thoughts of self-harm or harm to others, please contact [local emergency services] immediately.

Sample Opening:  
Thank you for trusting me with these personal experiences. Let's work together to explore constructive ways to navigate this situation...

[Proceed with structured support using above framework]

This version enhances clinical value through:  
  Trauma-informed care principles  
  Tiered intervention strategies  
  Progress monitoring systems  
  Crisis resource integration  
  Cultural competence considerations  
  Clear information hierarchy through spacing and section breaks 
                                                   

""")
predicted_chain=template_predicted |llm
medical_chain = template_medical | llm
mental_chain = template_mental | llm

def predicted_consultation(disease):    
    predict = predicted_chain.invoke({
        "disease": f'{disease}'
    })
    print("Diaganose | prediction received.")
    return predict.content.replace('*', '').replace('#', '')

def medical_consultation(age, gender, query):
    print(f"Invoking medical consultation")
    medical = medical_chain.invoke({
        "age": f'{age}',
        "gender": f'{gender}',
        "query": f'{query}'
    })
    print("Medical consultation response received.")
    return medical.content.replace('*', '').replace('#', '')

def mental_consultation(age, gender, stress_level, sleep_quality, current_mood, thoughts):
    print(f"Invoking mental consultation")
    mental = mental_chain.invoke({
        "age": f'{age}',
        "gender": f'{gender}',
        "stress_level": f'{stress_level}',
        "sleep_quality": f'{sleep_quality}',
        "current_mood": f'{current_mood}',
        "thoughts": f'{thoughts}'
    })
    print("Mental consultation response received.")
    return mental.content.replace('*', '').replace('#', '')
