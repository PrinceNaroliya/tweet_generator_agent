from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGroq(
    model = "llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

from typing import TypedDict, Literal, Annotated
import operator

class Tweet():
    tweet: str
    topic: str
    tone: str
    response: Literal['APPROVED','REJECTED']
    feedback: Annotated[list[str], operator.add]
    iteration: int
    maximum_iteration: int

from pydantic import BaseModel

class Structure(BaseModel):
    response: Literal['APPROVED','REJECTED']
    feedback: Annotated[list[str], operator.add]

structured_model = model.with_structured_output(Structure)

from langchain_core.output_parsers import StrOutputParser

def tweet_gen(state: Tweet):

    prompt = ChatPromptTemplate.from_messages([
        ('system','You are a viral Twitter expert. Your Tone is {tone}.'),
        ('human','Write a tweet about {topic}.')
    ])

    parser = StrOutputParser()

    chain = prompt | model | parser

    response = chain.invoke(state)

    return {
        'tweet': response
    }

def tweet_approval(state: Tweet):

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional Twitter Editor. 
        Evaluate the tweet based on:
        1. Length: Must be under 280 characters.
        2. Relevance: Does it talk about {topic}?
        3. Viral Factor: Is the {tone} tone maintained?
        
        If it's good, start your response with 'APPROVED'.
        If not, start with 'REJECTED' and give a feedback about the tweet why it is not so good and write issues in the feedback """),
        ("human", "Analyze this tweet: {tweet}")
    ])

    chain = prompt | structured_model

    response = chain.invoke(state)

    return {
        'response': response.response,
        'feedback': response.feedback
    }

def tweet_optimizer(state: Tweet):

    current_iter = state.get('iteration', 0)

    if state['iteration'] < state['maximum_iteration']:
    
        prompt = ChatPromptTemplate.from_messages([
            ('system','You are a proffessional viral Twitter expert and you have to improve a previous Tweet according to the {feedback}.'),
            ('human','Improve this tweet. \n\n{tweet} and do not write anything else.')
        ])

        parser = StrOutputParser()

        chain = prompt | model | parser

        new_tweet = chain.invoke(state)

        return {
            'tweet': new_tweet,
            'iteration': current_iter + 1
        }

    else:
        return {
            'tweet': state['tweet']
        }

def route_after_approval(state: Tweet):
    
    if "APPROVED" in state['response'].upper():
        return "end"
    elif state['iteration'] >= state['maximum_iteration']:
        return "end"
    else:
        return "optimize"

from langgraph.graph import StateGraph, START, END

graph = StateGraph(Tweet)

graph.add_node('tweet_gen', tweet_gen)
graph.add_node('tweet_approval', tweet_approval)
graph.add_node('tweet_optimizer', tweet_optimizer)

graph.add_edge(START, 'tweet_gen')
graph.add_edge('tweet_gen', 'tweet_approval')
graph.add_conditional_edges('tweet_approval', route_after_approval, {
    'end': END,
    'optimize': 'tweet_optimizer'
})

graph.add_edge('tweet_optimizer', 'tweet_approval')

workflow = graph.compile()

workflow

initial_state = {
    'topic': 'DeepLearning',
    'tone': 'funny',
    'iteration': 0,
    'maximum_iteration': 5
}

result = workflow.invoke(initial_state)

print(f"Final Tweet: {result['tweet']}")
print(f"Total Iterations: {result['iteration']}")
print(f"Feedback: {result['feedback']}")