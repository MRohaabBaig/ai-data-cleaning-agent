import os
import pandas as pd
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, START
from config import llm

# 1. Define the State
class AgentState(TypedDict):
    input_data: str
    user_prompt: str
    initial_cleaned_data: str
    llm_instructions: str
    final_processed_data: str
    report: str

# 2. Define the Nodes

def data_cleaning_node(state: AgentState):
    print("--- Node: Initial Data Cleaning ---")
    data = state["input_data"]
    # Simple heuristic cleaning: remove extra whitespace and empty lines
    cleaned = "\n".join([line.strip() for line in data.splitlines() if line.strip()])
    return {"initial_cleaned_data": cleaned}

def llm_integration_node(state: AgentState):
    print("--- Node: LLM Integration ---")
    prompt = f"""
    You are a data expert. Based on the following user prompt and data,
    provide specific Python cleaning instructions to process this data.

    User Prompt: {state['user_prompt']}
    Data Sample: {state['input_data'][:500]}

    Provide only the Python logic or steps needed to clean this data.
    """
    response = llm.invoke(prompt)
    return {"llm_instructions": response.content}

def python_cleaning_node(state: AgentState):
    print("--- Node: Python Cleaning Execution ---")
    # This node simulates executing the instructions from the LLM
    # In a production agent, you might use a PythonREPLTool here.
    # For this implementation, we will combine initial cleaning with LLM guidance.

    initial = state["initial_cleaned_data"]
    instructions = state["llm_instructions"]

    # Simulate processing: here we just append the LLM's guidance to show it was used
    processed = f"Processed Data:\n{initial}\n\nApplied Logic: {instructions}"
    return {"final_processed_data": processed}

def final_report_node(state: AgentState):
    print("--- Node: Final Report ---")
    report_prompt = f"""
    Generate a final report based on the following:
    User Prompt: {state['user_prompt']}
    Final Processed Data: {state['final_processed_data']}

    Ensure the report is professional and directly answers the user's request.
    """
    response = llm.invoke(report_prompt)
    return {"report": response.content}

# 3. Build the Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("initial_cleaning", data_cleaning_node)
workflow.add_node("llm_integration", llm_integration_node)
workflow.add_node("python_cleaning", python_cleaning_node)
workflow.add_node("final_report", final_report_node)

# Define Edges
workflow.add_edge(START, "initial_cleaning")
workflow.add_edge("initial_cleaning", "llm_integration")
workflow.add_edge("llm_integration", "python_cleaning")
workflow.add_edge("python_cleaning", "final_report")
workflow.add_edge("final_report", END)

# Compile
app = workflow.compile()

if __name__ == "__main__":
    print("\nWelcome to the AI Data Cleaning Agent!")

    input_data = ""
    while not input_data:
        print("\nHow would you like to provide the data?")
        print("1. Direct Text")
        print("2. CSV File")
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == '1':
            input_data = input("Please enter the data text:\n").strip()
            if not input_data:
                print("Error: Input data cannot be empty.")
        elif choice == '2':
            filename = input("Please enter the CSV filename: ").strip()
            if os.path.exists(filename):
                try:
                    df = pd.read_csv(filename)
                    if df.empty:
                        print("Error: The CSV file is empty.")
                    else:
                        input_data = df.to_string(index=False)
                except Exception as e:
                    print(f"Error reading CSV: {e}")
            else:
                print(f"Error: File '{filename}' not found.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

    user_prompt = ""
    while not user_prompt:
        user_prompt = input("\nPlease enter your custom instructions: ").strip()
        if not user_prompt:
            print("Error: Custom instructions cannot be empty.")

    inputs = {
        "input_data": input_data,
        "user_prompt": user_prompt
    }

    final_state = app.invoke(inputs)
    print("\n" + "="*30 + "\nFINAL REPORT\n" + "="*30)
    print(final_state["report"])
