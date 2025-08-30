import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Interactive CSV Visualizer", layout="wide")

# --- Sidebar for User Inputs ---
st.sidebar.header("Visualization Settings")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Main panel
st.title("Interactive CSV Data Visualizer")

# Conditional logic: only proceed if a file is uploaded
if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        st.stop() # Stop execution if file can't be read

    # --- Sidebar Widgets (only show if file is uploaded) ---
    st.sidebar.subheader("Plot Configuration")

    # Selectbox for plot type
    plot_type = st.sidebar.selectbox(
        "Select Plot Type",
        ["Scatter Plot", "Line Plot", "Bar Chart", "Histogram", "Box Plot"]
    )

    # Get column names for selectboxes
    column_names = df.columns.tolist()

    # Widgets for selecting columns based on plot type
    if plot_type in ["Scatter Plot", "Line Plot", "Bar Chart", "Box Plot"]:
        x_axis = st.sidebar.selectbox("Select X-axis", options=column_names, index=0)

        # For Line Plot, allow multiple Y-axes (Bonus Challenge)
        if plot_type == "Line Plot":
            y_axis = st.sidebar.multiselect("Select Y-axis (or axes)", options=column_names, default=column_names[1:2])
        elif plot_type == "Box Plot":
             y_axis = st.sidebar.selectbox("Select Y-axis", options=column_names, index=1)
        else: # For Scatter and Bar
            y_axis = st.sidebar.selectbox("Select Y-axis", options=column_names, index=1)

    elif plot_type == "Histogram":
        x_axis = st.sidebar.selectbox("Select Column for Histogram", options=column_names, index=0)
        y_axis = None # Histogram only needs one column

    # --- Plot Customization (Bonus Challenge) ---
    st.sidebar.subheader("Plot Customization")
    plot_title = st.sidebar.text_input("Plot Title", f"{plot_type} of {uploaded_file.name}")
    x_label = st.sidebar.text_input("X-axis Label", x_axis)

    if y_axis:
        # Create a default label for single or multiple y-axes
        y_label_default = y_axis[0] if isinstance(y_axis, list) and len(y_axis) > 0 else y_axis
        y_label = st.sidebar.text_input("Y-axis Label", y_label_default)
    else:
        y_label = "Frequency"


    # --- Display Data and Plot ---
    st.subheader("Uploaded Data")
    st.write(df)

    # Display Summary Statistics (Bonus Challenge)
    if st.sidebar.checkbox("Show Summary Statistics"):
        st.subheader("Summary Statistics")
        st.write(df.describe())


    # Generate and display the plot
    st.subheader("Generated Plot")

    fig = None # Initialize fig to None
    try:
        if plot_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, title=plot_title, labels={'x': x_label, 'y': y_label})
        elif plot_type == "Line Plot":
            # Plotly Express can handle multiple y-columns directly if the data is melted
            # For simplicity here, we plot each selected y-column
            df_melted = df.melt(id_vars=[x_axis], value_vars=y_axis, var_name='Variable', value_name='Value')
            fig = px.line(df_melted, x=x_axis, y='Value', color='Variable', title=plot_title, labels={'x': x_label, 'Value': y_label})
        elif plot_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, title=plot_title, labels={'x': x_label, 'y': y_label})
        elif plot_type == "Histogram":
            fig = px.histogram(df, x=x_axis, title=plot_title, labels={'x': x_label})
        elif plot_type == "Box Plot":
            fig = px.box(df, x=x_axis, y=y_axis, title=plot_title, labels={'x': x_label, 'y': y_label})

        if fig:
            # Update layout for custom labels
            fig.update_xaxes(title_text=x_label)
            fig.update_yaxes(title_text=y_label)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Could not generate plot. Please check your selections.")

    except Exception as e:
        st.error(f"An error occurred while generating the plot: {e}")
        st.info("Please ensure you have selected columns with compatible data types for the chosen plot.")


else:
    st.info("Awaiting for CSV file to be uploaded.")
    st.markdown("""
        **Welcome to the Interactive CSV Visualizer!**

        This tool allows you to upload a CSV file and create various plots to explore your data.

        **How to use:**
        1.  Click on **"Browse files"** in the sidebar to upload your CSV file.
        2.  Once uploaded, configure your plot using the options in the sidebar.
        3.  View the raw data and the generated plot in the main area.
    """)