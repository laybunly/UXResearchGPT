from __future__ import annotations
import re
from typing import Optional, Tuple, List, Union, Literal
import base64
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import os
import openai
import graphviz
from dataclasses import dataclass, asdict
from textwrap import dedent
from streamlit_agraph import agraph, Node, Edge, Config

# set title of page (will be seen in tab) and the width
st.set_page_config(page_title="User Flow Visualizer", layout="wide")

COLOR = "cyan"
FOCUS_COLOR = "red"
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'

@dataclass
class Message:
    """A class that represents a message in a ChatGPT conversation."""
    content: str
    role: Literal["user", "system", "assistant"]

    def __post_init__(self):
        self.content = dedent(self.content).strip()

START_CONVERSATION = [
    Message("""
        You are a user flow visualizer AI that can generate user flow graphs based on given inputs or instructions.
    """, role="system"),
    Message("""
        You have the ability to perform the following actions given a request to construct or modify a user flow graph:

        1. add(screen1, screen2) - add a connection between screen1 and screen2
        2. delete(screen1, screen2) - delete the connection between screen1 and screen2
        3. delete(screen1) - delete the screen and all its connections

        Note that the graph is a directed graph, representing the flow from one screen to another.
        The answer should only include the actions to perform, nothing else. If the instructions are vague
        or even if only a single word is provided, still generate a graph of multiple screens and connections
        that could make sense in the situation. Remember to think step by step and debate pros and cons before
        settling on an answer to accomplish the request as well as possible.

        Here is my first request: Add a user flow for an e-commerce app.
    """, role="user"),
    Message("""
        add("Home", "Product Listing")
        add("Product Listing", "Product Details")
        add("Product Details", "Add to Cart")
        add("Product Details", "Back to Product Listing")
        add("Add to Cart", "Checkout")
        add("Checkout", "Payment")
        add("Payment", "Order Confirmation")
    """, role="assistant"),
    Message("""
        Remove the connection between "Product Listing" and "Product Details".
    """, role="user"),
    Message("""
        delete("Product Listing", "Product Details")
    """, role="assistant")
]

def ask_chatgpt(conversation: List[Message]) -> Tuple[str, List[Message]]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[asdict(c) for c in conversation]
    )
    msg = Message(**response["choices"][0]["message"])
    return msg.content, conversation + [msg]

class UserFlowVisualizer:
    """A class that represents a user flow visualizer."""

    def __init__(self, connections: Optional[List[Tuple[str, str]]] = None, screens: Optional[List[str]] = None) -> None:
        self.connections = [] if connections is None else connections
        self.screens = [] if screens is None else screens
        self.save()

    @classmethod
    def load(cls) -> UserFlowVisualizer:
        if "user_flow_visualizer" in st.session_state:
            return st.session_state["user_flow_visualizer"]
        return cls()

    def save(self) -> None:
        st.session_state["user_flow_visualizer"] = self

    def is_empty(self) -> bool:
        return len(self.connections) == 0

    def ask_for_initial_flow(self, query: str) -> None:
        conversation = START_CONVERSATION + [
            Message(f"""
                Great, now ignore all previous screens and connections and restart from scratch.
                I now want you to do the following:

                {query}
            """, role="user")
        ]

        output, self.conversation = ask_chatgpt(conversation)
        self.parse_and_include_connections(output, replace=True)

    def ask_for_extended_flow(self, selected_screen: Optional[str] = None, text: Optional[str] = None) -> None:
        if (selected_screen is None and text is None):
            return

        if selected_screen is not None:
            conversation = self.conversation + [
                Message(f"""
                    add new connections to new screens, starting from the screen "{selected_screen}"
                """, role="user")
            ]
            st.session_state.last_expanded = selected_screen
        else:
            conversation = self.conversation + [Message(text, role="user")]

        output, self.conversation = ask_chatgpt(conversation)
        self.parse_and_include_connections(output, replace=False)

    def parse_and_include_connections(self, output: str, replace: bool = True) -> None:
        pattern1 = r'(add|delete)\("([^()"]+)",\s*"([^()"]+)"\)'
        pattern2 = r'(delete)\("([^()"]+)"\)'

        matches = re.findall(pattern1, output) + re.findall(pattern2, output)

        new_connections = []
        remove_connections = set()
        remove_screens = set()
        for match in matches:
            op, *args = match
            add = op == "add"
            if add or (op == "delete" and len(args) == 2):
                a, b = args
                if a == b:
                    continue
                if add:
                    new_connections.append((a, b))
                else:
                    remove_connections.add((a, b))
            else:
                remove_screens.add(args[0])

        if replace:
            connections = new_connections
        else:
            connections = self.connections + new_connections

        added = set()
        for conn in connections:
            if conn in added or conn[0] in remove_screens or conn in remove_connections:
                continue
            added.add(conn)

        self.connections = list(added)
        self.screens = list(set([s for conn in self.connections for s in conn]))
        self.save()

    def _delete_screen(self, screen) -> None:
        self.connections = [conn for conn in self.connections if screen not in conn]
        self.screens = list(set([s for conn in self.connections for s in conn]))
        self.conversation.append(Message(
            f'delete("{screen}")',
            role="user"
        ))
        self.save()

    def _add_expand_delete_buttons(self, screen) -> None:
        st.sidebar.subheader(screen)
        cols = st.sidebar.columns(2)
        cols[0].button(
            label="Expand",
            on_click=self.ask_for_extended_flow,
            key=f"expand_{screen}",
            kwargs={"selected_screen": screen}
        )
        cols[1].button(
            label="Delete",
            on_click=self._delete_screen,
            type="primary",
            key=f"delete_{screen}",
            args=(screen,)
        )

    def visualize(self) -> None:
        selected = st.session_state.get("last_expanded")
        vis_nodes = [
            Node(
                id=s,
                label=s,
                size=10 + 10 * (s == selected),
                color=COLOR if s != selected else FOCUS_COLOR
            )
            for s in self.screens
        ]
        vis_edges = [Edge(source=a, target=b) for a, b in self.connections]
        config = Config(width="100%", height=600, directed=True, physics=True, hierarchical=False)
        clicked_screen = agraph(nodes=vis_nodes, edges=vis_edges, config=config)
        if clicked_screen is not None:
            self._add_expand_delete_buttons(clicked_screen)
        return

def main():
    user_flow_visualizer = UserFlowVisualizer.load()

    st.sidebar.title("User Flow Visualizer")

    empty = user_flow_visualizer.is_empty()
    reset = empty or st.sidebar.checkbox("Reset user flow", value=False)
    query = st.sidebar.text_area(
        "Describe your user flow" if reset else "Describe how to change your user flow",
        value=st.session_state.get("flow-input", ""),
        key="flow-input",
        height=200
    )
    submit = st.sidebar.button("Submit")

    valid_submission = submit and query != ""

    if empty and not valid_submission:
        return

    with st.spinner(text="Loading user flow graph..."):
        if valid_submission:
            if reset:
                user_flow_visualizer.ask_for_initial_flow(query=query)
            else:
                user_flow_visualizer.ask_for_extended_flow(text=query)
            st.experimental_rerun()
        else:
            user_flow_visualizer.visualize()

if __name__ == "__main__":
    main()
