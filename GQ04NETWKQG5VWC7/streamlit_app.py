# Import python packages
import streamlit as st
import os


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Example Streamlit App (vNext) :balloon:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:")

st.markdown("""
- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
""")

# get_active_session() does not work in vNext yet, so we use the connection API instead
conn = st.connection("snowflake")
session = conn.session()
session.use_warehouse(os.environ.get('SNOWFLAKE_WAREHOUSE'))

# Use an interactive slider to get user input
hifives_val = st.slider(
    "Number of high-fives in Q3",
    min_value=0,
    max_value=90,
    value=60,
    help="Use this to enter the number of high-fives you gave in Q3",
)

#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
created_dataframe = session.create_dataframe(
    [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
    schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
)

# Execute the query and convert it into a Pandas dataframe
queried_data = created_dataframe.to_pandas()

# Create a simple bar chart
# See docs.streamlit.io for more types of charts
st.subheader("Number of high-fives")
st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

st.subheader("Underlying data")
st.dataframe(queried_data, use_container_width=True)
