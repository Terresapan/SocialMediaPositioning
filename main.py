from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from prompts import EVALUATE_PROMPT, ANALYSIS_PROMPT, POSITIONING_PROMPT

class PositioningState(TypedDict):
    """State for the positioning analysis workflow"""
    messages: List[dict]
    core_value_provided: str
    target_audience: str
    monetization: str
    persona: str
    aligned: bool

class EvaluateAgent:
    def __init__(self, model):
        self.model = model

    def evaluate_alignment(self, state: PositioningState):
        """Evaluates alignment between core value, target audience, persona, and monetization"""
        prompt = EVALUATE_PROMPT.format(
            core_value_provided=state["core_value_provided"],
            target_audience=state["target_audience"],
            persona=state["persona"],
            monetization=state["monetization"]
        )
        
        response = self.model.invoke(prompt)
        is_aligned = "YES" in response.content.upper()
        
        new_state = state.copy()
        new_state["aligned"] = is_aligned
        # new_state["messages"] = state["messages"] + [{"role": "assistant", "content": response.content}]
        return new_state
        
class AnalysisAgent:
    def __init__(self, model):
        self.model = model

    def analyze_alignment(self, state: PositioningState):
        """Analyzes why elements are aligned and provides refined version"""
        if not state["aligned"]:
            return state
            
        prompt = ANALYSIS_PROMPT.format(
            core_value_provided=state["core_value_provided"],
            target_audience=state["target_audience"],
            persona=state["persona"],
            monetization=state["monetization"],
            aligned="YES"
        )
        
        response = self.model.invoke(prompt)
        new_state = state.copy()
        new_state["messages"] = state["messages"] + [{"role": "assistant", "content": response.content}]
        return new_state

class PositioningAgent:
    def __init__(self, model):
        self.model = model

    def refine_positioning(self, state: PositioningState):
        """Provides analysis of misalignment and suggests aligned combinations"""
        if state["aligned"]:
            return state
            
        prompt = POSITIONING_PROMPT.format(
            core_value_provided=state["core_value_provided"],
            target_audience=state["target_audience"],
            persona=state["persona"],
            monetization=state["monetization"],
            aligned="NO"
        )
        
        response = self.model.invoke(prompt)
        new_state = state.copy()
        new_state["messages"] = state["messages"] + [{"role": "assistant", "content": response.content}]
        return new_state

def create_graph(model):
    """Creates and returns a compiled StateGraph with the given model"""
    graph = StateGraph(PositioningState)
    
    # Initialize agents with the provided model
    evaluate_agent = EvaluateAgent(model)
    analysis_agent = AnalysisAgent(model)
    positioning_agent = PositioningAgent(model)
    
    # Add nodes
    graph.add_node("evaluate", evaluate_agent.evaluate_alignment)
    graph.add_node("analyze", analysis_agent.analyze_alignment)
    graph.add_node("position", positioning_agent.refine_positioning)
    
    # Set entry point
    graph.set_entry_point("evaluate")
    
    # Add conditional edges
    def router(state: PositioningState):
        return "analyze" if state["aligned"] else "position"
    
    graph.add_conditional_edges(
        "evaluate",
        router,
        {
            "analyze": "analyze",
            "position": "position"
        }
    )
    
    # Add edges to END
    graph.add_edge("analyze", END)
    graph.add_edge("position", END)
    
    return graph.compile()