import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("students_data.csv")


dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
records = []
for _, row in df.iterrows():
    for d in dates:
        records.append({
            "Student_ID": row["Student_ID"],
            "Name": row["Name"],
            "Date": d,
            "Attendance (%)": np.clip(np.random.normal(row["Attendance (%)"], 5), 50, 100)
        })

attendance_df = pd.DataFrame(records)

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")


st.title(" Advanced Student Performance Dashboard")


st.sidebar.header(" Filters")
course = st.sidebar.selectbox("Course", ["All"] + sorted(df["Course"].unique()))
city = st.sidebar.multiselect("City", sorted(df["City"].unique()))
min_marks = st.sidebar.slider("Minimum Marks", 0, 100, 50)
gender = st.sidebar.radio("Gender", ["All", "Male", "Female"])
reset = st.sidebar.button(" Reset Filters")

filtered = df.copy()

if reset:
    filtered = df.copy()
else:
    if course != "All":
        filtered = filtered[filtered.Course == course]
    if city:
        filtered = filtered[filtered.City.isin(city)]
    if gender != "All":
        filtered = filtered[filtered.Gender == gender]
    filtered = filtered[filtered.Marks >= min_marks]


tab1, tab2, tab3, tab4 = st.tabs(["⬤ Dashboard", "⬤ Student Explorer", "⬤ Visual Analytics", "⬤ Summary & Actions"])


with tab1:
    st.subheader(" Filtered Student Records")
    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(" Download Filtered Data", csv, "filtered_students.csv")

    avg_marks = round(filtered["Marks"].mean(), 2)
    avg_att = round(filtered["Attendance (%)"].mean(), 2)
    total = len(filtered)

    c1, c2, c3 = st.columns(3)
    c1.metric(" Average Marks", avg_marks)
    c2.metric(" Average Attendance", f"{avg_att}%")
    c3.metric(" Total Students", total)

    if avg_marks > 85:
        st.success(" Excellent overall performance!")
        
    elif avg_marks > 70:
        st.info(" Good performance, keep improving!")
    else:
        st.warning(" Needs Improvement — focus on weak areas.")


with tab2:
    st.subheader(" Search Student")
    name = st.text_input("Enter student name:")
    
    if name:
        result = df[df.Name.str.contains(name, case=False)]
        if not result.empty:
            row = result.iloc[0]
            st.write(f"###  Student Profile: {row['Name']}")
            st.write(f"""
             ID: {row['Student_ID']}
             Course: {row['Course']}
             City: {row['City']}
             Marks: {row['Marks']}
             Attendance: {row['Attendance (%)']}%
             Gender: {row['Gender']}
            """)
        else:
            st.error("No student found ")

with tab3:
    st.subheader(" Marks Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered["Marks"], bins=8)
    ax.set_xlabel("Marks")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.subheader("Gender Distribution")
    g = filtered["Gender"].value_counts()
    st.pyplot(g.plot.pie(autopct="%1.1f%%").figure)

    st.subheader(" Attendance Trend (Last 10 Days)")
    selected = filtered["Name"].unique().tolist()
    trend = attendance_df[attendance_df["Name"].isin(selected)]

    if not trend.empty:
        pivot = trend.pivot_table(index="Date", columns="Name", values="Attendance (%)")
        st.line_chart(pivot)
    else:
        st.info("No attendance data available.")

with tab4:
    st.subheader(" Quick Actions")

    if st.button("Show Top Performers (>90 Marks)"):
        top = df[df.Marks > 90]
        st.success(" Top Achievers")
        st.dataframe(top)

    if st.button("Show All Data"):
        st.info(" Complete Student Dataset")
        st.dataframe(df)

st.image("pngwing.com.png", caption="Powered by Streamlit", use_container_width=True)

st.write("---")
st.caption("Developed by Pawan — Enhanced Streamlit Dashboard UI for Student Performance Monitoring")
