import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def get_itinerary_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are TripMuse, a professional travel assistant.
        
        TASK:
        1. When first asked or when major changes are requested, generate a structured {days}-day itinerary for {location} using these POIs: {poi_list} and with popular places that city has to offer.
        2. If the user asks a follow-up question about the trip, answer conversationally using the provided POIs and the previous history.
        
        OUTPUT FORMAT:
        You must ALWAYS respond with a JSON object containing:
        {{
            "itinerary": [...],
            "travel_tips": "Your conversational response or specific day details here"
        }}"""),
        MessagesPlaceholder(variable_name="history"), 
        ("human", "{user_input}")
    ])
    
    return prompt | llm | JsonOutputParser()


async def generate_itinerary(location, days, poi_df, history, user_input):
    poi_data = poi_df[['name', 'attraction_type']].to_dict(orient='records')
    
    chain = get_itinerary_chain()
    response = await chain.ainvoke({
        "location": location,
        "days": days,
        "poi_list": str(poi_data),
        "history": history,
        "user_input": user_input
    })
    return response