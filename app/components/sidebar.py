import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space


def sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] a p {
                font-size: 18px !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        st.title(" Analysis Panel")
        st.divider()
        st.page_link("main.py", label=" Home", icon="🏠", use_container_width=True)
        add_vertical_space(2)
        st.page_link("pages/01_dashboard.py", label=" -> Dashboard")
        st.page_link("pages/02_clientes.py", label=" -> Clients")
        st.page_link("pages/03_productos.py", label=" -> Products")
        st.page_link("pages/04_ordenes.py", label="-> Orders")
