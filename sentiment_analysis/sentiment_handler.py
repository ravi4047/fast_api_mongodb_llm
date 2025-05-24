from typing_extensions import TypedDict
import random
from langgraph.graph import StateGraph,START,END
from langgraph.constants import Send
import operator
from typing import Annotated
from pydantic import BaseModel
from pyspark.sql import Row
row_list = []

# Setting up Data

for i in range(1,11):  
  row = Row(id=i, score=float(random.random()))
  row_list.append(row)
df = spark.createDataFrame(row_list)
df.show()

def getGraph():

  import operator
  from typing import Annotated
  from pydantic import BaseModel

  class ParentState(TypedDict):
    #scores: list  #gets list of scores as input to Parent Graph
    sentiment_scores: list # Same scores are provided as input to subgraph
    sentiments: Annotated[list, operator.add]# sentiments 
    result: list

  class SentimentState(TypedDict):    
    sentiment_scores: list 
    sentiment_score: Annotated[float,operator.add] #mapper will iterate through each of the score 
    sentiments: Annotated[list, operator.add]# sentiments 
    #result: list

   
  def getScores_agent(state: SentimentState):   
    return {"sentiment_scores" : state["sentiment_scores"]}

  def sentiment_decider_agent(state: SentimentState):   
    senti = ""
    result = {}
    score = state["sentiment_score"]
    if score < 0.5:
        senti = "Sad"        
    else:
        senti = "Happy"
        
    result[score] = senti
    return {"sentiments":[result]}
  
  def continue_to_sentiment(state: SentimentState):
    return [Send("SentimentGraph",{"sentiment_score":s}) for s in state["sentiment_scores"]]

  def sentiment_generator_agent(state: SentimentState):
    sentiments = state["sentiments"]   
    return {"result":sentiments}
 
  sub_graph_builder = StateGraph(SentimentState)
  sub_graph_builder.add_node("SentimentDecider",sentiment_decider_agent) 
  sub_graph_builder.add_edge(START,"SentimentDecider")
  sub_graph_builder.add_edge("SentimentDecider",END)
  sub_graph = sub_graph_builder.compile()

  parent_graph_builder = StateGraph(ParentState) 
  parent_graph_builder.add_node("GetScores",getScores_agent)
  parent_graph_builder.add_node("SentimentGraph",sub_graph)# sub-graph is added as a node
  parent_graph_builder.add_node("SentimentGenerator",sentiment_generator_agent) # Reducer
  parent_graph_builder.add_edge(START,"GetScores")
  parent_graph_builder.add_conditional_edges("GetScores", continue_to_sentiment,["SentimentGraph"]) #Map to do parallel processing
  parent_graph_builder.add_edge("SentimentGraph","SentimentGenerator")
  parent_graph_builder.add_edge("SentimentGenerator",END)
  graph = parent_graph_builder.compile()   
  return graph
def getSentiment_mappartition(partData):
  
  scores = []
  if partData is None:
    print("Part Data is None")
  else:
    
    for row in partData:
      scores.append(row.score)    

    graph = getGraph()      
    input = {"sentiment_scores":scores}
    response = graph.invoke(input)  
    sentiments = response["result"]   
    for sentiment in sentiments:
      for key,value in sentiment.items(): 
        yield [key,value]
df_result = df.rdd.mapPartitions(getSentiment_mappartition).toDF(["sentiment_score","sentiment"])
df_result.show()