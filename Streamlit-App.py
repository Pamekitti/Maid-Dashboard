import streamlit as st 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta, datetime
import pytz

st.set_page_config(layout='wide')

def PauseTime_Calculation(pause_list_string): # Calculate pause time from pause and continue list
  if pause_list_string == "0" :
    return 0
  else :
    pause_list = eval(pause_list_string)
    durations = []
    for i in pause_list:
      if i[0] != None and i[1] != None :
        pause_time = datetime.strptime(i[0], '%Y-%m-%dT%H:%M:%S.%fZ')
        continue_time = datetime.strptime(i[1], '%Y-%m-%dT%H:%M:%S.%fZ')
        duration = (continue_time - pause_time).total_seconds()/60
        durations.append(duration)
      return sum(durations)

def RemoveOutlier_Series(series) : # Get series that remove outliers
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    return series[(series >= lower_bound) & (series <= upper_bound)]

def BurnupByRatio_Visualization(df, date_select) :  # Create burnup by ratio figure
    # Prepare data
    list10 = []
    list20 = []
    list30 = []
    list40 = []
    list50 = []
    list60 = []
    list70 = []
    list80 = []
    list90 = []
    list100 = []
    dayarray = np.array(date_select)

    for d in date_select:
        df_spec = df[df["Date"] == d]

        n = df_spec.shape[0]

        df_spec.sort_values("Started At",inplace = True)
        df_spec["Ratio"] = range(n)
        df_spec["Ratio"] += 1
        df_spec["Ratio"] /= n

        percentile10 = df_spec[df_spec["Ratio"] <= 0.1].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile20 = df_spec[df_spec["Ratio"] <= 0.2].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile30 = df_spec[df_spec["Ratio"] <= 0.3].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile40 = df_spec[df_spec["Ratio"] <= 0.4].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile50 = df_spec[df_spec["Ratio"] <= 0.5].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile60 = df_spec[df_spec["Ratio"] <= 0.6].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile70 = df_spec[df_spec["Ratio"] <= 0.7].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile80 = df_spec[df_spec["Ratio"] <= 0.8].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile90 = df_spec[df_spec["Ratio"] <= 0.9].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)
        percentile100 = df_spec[df_spec["Ratio"] <= 1].iloc[-1]["Started At"].replace(day = 1, month = 1, year = 2022)

        list10.append(percentile10)
        list20.append(percentile20)
        list30.append(percentile30)
        list40.append(percentile40)
        list50.append(percentile50)
        list60.append(percentile60)
        list70.append(percentile70)
        list80.append(percentile80)
        list90.append(percentile90)
        list100.append(percentile100)

    array10 = np.array(list10)
    array20 = np.array(list20)
    array30 = np.array(list30)
    array40 = np.array(list40)
    array50 = np.array(list50)
    array60 = np.array(list60)
    array70 = np.array(list70)
    array80 = np.array(list80)
    array90 = np.array(list90)
    array100 = np.array(list100)

    # Visualize
    layout = go.Layout(title = "Cleaning Time By Ratio", height = 700, width = 1200)

    fig = go.Figure(layout = layout)

    fig.add_trace(go.Scatter(x = dayarray, y = array100, name="100%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array90, name="90%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array80, name="80%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array70, name="70%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array60, name="60%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array50, name="50%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array40, name="40%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array30, name="30%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array20, name="20%"))
    fig.add_trace(go.Scatter(x = dayarray, y = array10, name="10%"))

    fig.update_xaxes(tickangle = 90)

    return fig

def StartTimeByCleaningType_Visualization(df, date_select) : # Create boxplot for start time by cleaning type
    df_spec = df[df["Date"].isin(date_select)]

    fig = px.box(df_spec, x = "Date", y = "Time", color = "Cleaning_type", height = 590, width = 600, title = "Start Cleaning Time By Cleaning Type")

    fig.update_xaxes(tickangle = 90)

    return fig

def InspectionTimeByDate_Visualization(df, date_select) : # Create line chart for inspection time by date
    df_spec = df[df["Status"] == "done"]
    df_spec = df_spec[df_spec["Cleaning_type"] == "C/O"]
    
    layout = go.Layout(title = "Inspection Time By Date", height = 700, width = 1200)

    fig = go.Figure(layout = layout) 

    for d in date_select :

        df_spec_date = df_spec[df_spec["Date"] == d]

        df_spec_date_cleaning = df_spec_date[["Cleaning Finished At"]]
        df_spec_date_cleaning.sort_values("Cleaning Finished At", inplace = True)
        df_spec_date_cleaning["Order"] = range(df_spec_date_cleaning.shape[0])
        df_spec_date_cleaning["Order"] += 1

        df_spec_date_inspection = df_spec_date[["End At"]]
        df_spec_date_inspection.sort_values("End At", inplace = True)
        df_spec_date_inspection["Order"] = range(df_spec_date_inspection.shape[0])
        df_spec_date_inspection["Order"] += 1

        df_spec_merge = df_spec_date_cleaning.merge(df_spec_date_inspection, on = "Order", how = "inner")
        df_spec_merge["Inspection Duration"] = (df_spec_merge["End At"] - df_spec_merge["Cleaning Finished At"]).dt.total_seconds() / 60
        df_spec_merge["Time"] = df_spec_merge["Cleaning Finished At"].apply(lambda x : x.replace(day = 1, month = 1, year = 2000))

        fig.add_trace(go.Scatter(x = df_spec_merge["Time"], y = df_spec_merge["Inspection Duration"], mode = "lines", name = d))

    return fig

def RoomAmountByDate_Visualization(df, date_select) : # Create bar chart for room amount by cleaning type
    df_spec = df[df["Date"].isin(date_select)]
     
    df_spec_group = df_spec.groupby(["Date","Cleaning_type"])["Cleaning_type"].count().reset_index(name = "Count")

    fig = px.bar(df_spec_group, x = "Date", y = "Count", color = "Cleaning_type", text_auto = True, height = 590, width = 600, title = "Room Amount By Cleaning Type")

    fig.update_xaxes(tickangle = 90)

    return fig

def RoomAmountPerMaidByDate_Visualization(df, df_people, date_select) : # Create bar chart for room amount per maid by cleaning type
    df_spec = df[df["Date"].isin(date_select)]
    
    df_spec_group = df_spec.groupby(["Date","Cleaning_type"])["Cleaning_type"].count().reset_index(name = "Count")
    
    df_spec_merge = pd.merge(df_spec_group, df_people, on = "Date", how = "inner")
    
    df_spec_merge["Count_per_maid"] = df_spec_merge["Count"] / df_spec_merge["Total_Maid"]
    df_spec_merge["Count_per_maid"] = df_spec_merge['Count_per_maid'].apply(lambda x: round(x, 2))
    
    fig = px.bar(df_spec_merge, x = "Date", y = "Count_per_maid", color = "Cleaning_type", text_auto = True, height = 590, width = 600, title = "Room Amount Per Maid By Cleaning Type")

    fig.update_xaxes(tickangle = 90)

    return fig

def MaidCleaningTime_Visualization(df, date_select, starttime, endtime) : # Create boxplot for maid cleaning time by cleaning type
    df_spec = df[df["Date"].isin(date_select)]
    df_spec = df_spec[(df_spec["Time"] > starttime) & (df_spec["Time"] < endtime)]

    fig = px.box(df_spec, x = "Assigned To", y = "Total_cleaning_time", color = "Cleaning_type", points = "all", hover_data = ["Room"], height = 700, width = 1200, title = "Maid Cleaning Time By Cleaning Type")

    return fig

def BurnupByFloor_ListVisualization(df, date_select, floor_select) : # Create burnup by floor 
    df_spec = df[df["Date"].isin(date_select)]

    figlist = []  
    
    for d in date_select :
        fig = make_subplots(rows = 1, cols = 2)
        fig.update_layout(height = 590, width = 1200, title_text = d)

        for f in floor_select :
            df_spec = df[df["Date"] == d]
            df_spec = df_spec[df_spec["Floor"] == f]

            df_spec.sort_values("Started At", inplace = True)

            df_spec["Order"] = range(df_spec.shape[0])
            df_spec["Order"] += 1

            # Burnup
            fig.append_trace(go.Scatter(x = df_spec["Started At"], y = df_spec["Order"], name = "Floor" + str(f), line_shape = "spline", mode = "lines"), row = 1, col = 1)

        # Room Amount
        df_spec = df[df["Date"] == d]
        df_spec_group = df_spec.groupby(["Floor","Cleaning_type"])["Cleaning_type"].count().reset_index(name = "Count")

        df_spec_type = df_spec_group[df_spec_group["Cleaning_type"] == "C/O"]
        fig.append_trace(go.Bar(x = df_spec_type["Floor"], y = df_spec_type["Count"], name = "C/O"), row = 1, col = 2)

        df_spec_type = df_spec_group[df_spec_group["Cleaning_type"] == "OD"]
        fig.append_trace(go.Bar(x = df_spec_type["Floor"], y = df_spec_type["Count"], name = "OD"), row = 1, col = 2)

        df_spec_type = df_spec_group[df_spec_group["Cleaning_type"] == "VC"]
        fig.append_trace(go.Bar(x = df_spec_type["Floor"], y = df_spec_type["Count"], name = "VC"), row = 1, col = 2)

        figlist.append(fig)
    
    return figlist

def BurnupByDate_ListVisualization(df, date_select, floor_select) : # Create burnup by date 
    df_spec = df[df["Date"].isin(date_select)]

    figlist = []  
    
    for f in floor_select :
        fig = make_subplots(rows = 1, cols = 2)
        fig.update_layout(height = 590, width = 1200, title_text = "Floor " + str(f))

        for d in date_select :
            df_spec = df[df["Floor"] == f]
            df_spec = df_spec[df_spec["Date"] == d]

            df_spec.sort_values("Started At", inplace = True)

            df_spec["Order"] = range(df_spec.shape[0])
            df_spec["Order"] += 1

            # Burnup
            fig.append_trace(go.Scatter(x = df_spec["Time"], y = df_spec["Order"], name = str(d), line_shape = "spline", mode = "lines"), row = 1, col = 1)

        # Room Amount
        df_spec = df[df["Floor"] == f]
        df_spec_group = df_spec.groupby(["Date","Cleaning_type"])["Cleaning_type"].count().reset_index(name = "Count")

        df_spec_type = df_spec_group[df_spec_group["Cleaning_type"] == "C/O"]
        fig.append_trace(go.Bar(x = df_spec_type["Date"], y = df_spec_type["Count"], name = "C/O"), row = 1, col = 2)

        df_spec_type = df_spec_group[df_spec_group["Cleaning_type"] == "OD"]
        fig.append_trace(go.Bar(x = df_spec_type["Date"], y = df_spec_type["Count"], name = "OD"), row = 1, col = 2)

        df_spec_type = df_spec_group[df_spec_group["Cleaning_type"] == "VC"]
        fig.append_trace(go.Bar(x = df_spec_type["Date"], y = df_spec_type["Count"], name = "VC"), row = 1, col = 2)

        fig.update_xaxes(tickangle = 90)

        figlist.append(fig)
    
    return figlist

def FloorCleaningAmount_Visualization(df, date_select, startroom, endroom) : # Create bar chart for room amount per floor by cleaning type
    df_spec = df[df["Date"].isin(date_select)]
    df_spec = df_spec[(df_spec["Room_num"] >= startroom) & (df_spec["Room_num"] <= endroom)]

    df_spec_group = df_spec.groupby(["Floor","Cleaning_type"])["Cleaning_type"].count().reset_index(name = "Count")
    
    fig = px.bar(df_spec_group, x = "Floor", y = "Count", color = "Cleaning_type", height = 590, width = 400, title = "Room Amount")

    return fig

def FloorCleaningTime_Visualization(df, date_select, startroom, endroom) : # Create bar chart for total cleaning time per floor by cleaning type
    df_spec = df[df["Date"].isin(date_select)]
    df_spec = df_spec[(df_spec["Room_num"] >= startroom) & (df_spec["Room_num"] <= endroom)]

    df_spec_group = df_spec.groupby(["Floor","Cleaning_type"])["Total_cleaning_time"].sum().reset_index(name = "Cleaning_time")
    
    fig = px.bar(df_spec_group, x = "Floor", y = "Cleaning_time", color = "Cleaning_type", height = 590, width = 400, title = "Cleaning Time")

    return fig

def FloorMedianCleanigTime_Visualization(df, date_select, startroom, endroom) : # Create bar chart for median cleaning time per floor by cleaning type
    df_spec = df[df["Date"].isin(date_select)]
    df_spec = df_spec[(df_spec["Room_num"] >= startroom) & (df_spec["Room_num"] <= endroom)]

    df_spec_group = df_spec.groupby(["Floor","Cleaning_type"])["Total_cleaning_time"].median().reset_index(name = "Cleaning_time")
    
    fig = px.bar(df_spec_group, x = "Floor", y = "Cleaning_time", color = "Cleaning_type", barmode = "group", height = 590, width = 480, title = "Median Cleaning Time")

    return fig

def CleaningTimeByWeek(df, date_select) : # Create line graph for cleaning time by week and cleaning type
    df_spec = df[df["Date"].isin(date_select)]
    df_spec_group = df_spec.groupby(["Date", "Cleaning_type"])["Total_cleaning_time"].median().reset_index(name = "Median")
    df_spec_group_co = df_spec_group[df_spec_group["Cleaning_type"] == "C/O"]
    df_spec_group_od = df_spec_group[df_spec_group["Cleaning_type"] == "OD"]

    layout = go.Layout(height = 550, width = 1200)

    fig = go.Figure(layout = layout)
    
    i = 1
    week = 1

    for row in range(df_spec_group_co.shape[0]) :
        if i == 1 :
            cleaningtime_list = [df_spec_group_co.iloc[row]["Median"]]
            i += 1
        
        if 1 < i < 7 :
            cleaningtime_list.append(df_spec_group_co.iloc[row]["Median"])
            i += 1
        
        else : # i == 7
            cleaningtime_list.append(df_spec_group_co.iloc[row]["Median"])

            fig.add_trace(go.Scatter(x = [1, 2, 3, 4, 5, 6, 7], y = cleaningtime_list, mode = "lines", name = "C/O Week" + str(week)))
          
            i = 1
            week += 1

    i = 1
    week = 1
            
    for row in range(df_spec_group_od.shape[0]) :
        if i == 1 :
            cleaningtime_list = [df_spec_group_od.iloc[row]["Median"]]
            i += 1
        
        if 1 < i < 7 :
            cleaningtime_list.append(df_spec_group_od.iloc[row]["Median"])
            i += 1
        
        else : # i == 7
            cleaningtime_list.append(df_spec_group_od.iloc[row]["Median"])

            fig.add_trace(go.Scatter(x = [1, 2, 3, 4, 5, 6, 7], y = cleaningtime_list, mode = "lines", name = "OD Week" + str(week)))
          
            i = 1
            week += 1
    
    return fig

def CleaningTimeByCleaningType_Visualization(df, date_select) : # Create boxplot for cleaning time on date by cleaning type
    df_spec = df[df["Date"].isin(date_select)]
    
    df_spec_group = df_spec.groupby(["Date", "Cleaning_type"])["Total_cleaning_time"]

    layout = go.Layout(title = "Cleaning Duration By Cleaning Type", height = 590, width = 590)

    fig = go.Figure(layout = layout)
    
    df_group_co = pd.DataFrame({"Date" : [], "Total_cleaning_time" : []})
    df_group_od = pd.DataFrame({"Date" : [], "Total_cleaning_time" : []})
    df_group_vc = pd.DataFrame({"Date" : [], "Total_cleaning_time" : []})
    
    for (date, cleaning_type), group_value in df_spec_group :
        
        group_value = RemoveOutlier_Series(group_value)

        group_df = pd.DataFrame({"Date" : [date] * len(group_value), "Total_cleaning_time" : group_value})

        if cleaning_type == "C/O" :
            df_group_co = pd.concat([df_group_co, group_df], axis = 0)
        elif cleaning_type == "OD" :
            df_group_od = pd.concat([df_group_od, group_df], axis = 0)
        elif cleaning_type == "VC" :
            df_group_vc = pd.concat([df_group_vc, group_df], axis = 0)

    fig.add_trace(go.Box(x = df_group_co["Date"], y = df_group_co["Total_cleaning_time"], boxpoints = False, name = "C/O"))
    fig.add_trace(go.Box(x = df_group_od["Date"], y = df_group_od["Total_cleaning_time"], boxpoints = False, name = "OD"))
    fig.add_trace(go.Box(x = df_group_vc["Date"], y = df_group_vc["Total_cleaning_time"], boxpoints = False, name = "VC"))

    fig.update_layout(boxmode = "group", xaxis_title = "Date", yaxis_title = "Cleaning Duration")
    fig.update_xaxes(tickangle = 90)

    return fig

def CleaningOverall_PivotTable(df, date_select) : # Create pivot table for statistics by cleaning type
    df_spec = df[df["Date"].isin(date_select)]

    df_spec_group_count = df_spec.groupby(["Date", "Cleaning_type"])["Total_cleaning_time"].count().reset_index(name = "Stat")
    df_spec_group_count["Stat_type"] = np.array(["count"] * len(df_spec_group_count))

    df_spec_group_median = df_spec.groupby(["Date", "Cleaning_type"])["Total_cleaning_time"].median().reset_index(name = "Stat")
    df_spec_group_median["Stat_type"] = np.array(["median"] * len(df_spec_group_median))

    df_spec_group_mean = df_spec.groupby(["Date", "Cleaning_type"])["Total_cleaning_time"].mean().reset_index(name = "Stat")
    df_spec_group_mean["Stat_type"] = np.array(["mean"] * len(df_spec_group_mean))
    
    df_spec_merge = pd.concat([df_spec_group_count, df_spec_group_median], axis = 0)
    df_spec_merge = pd.concat([df_spec_merge, df_spec_group_mean], axis = 0)

    df_spec_pivottable = pd.pivot_table(df_spec_merge, index = ["Cleaning_type", "Stat_type"], columns = "Date", values = "Stat")  

    return df_spec_pivottable

uploaded_file_cleaning = st.file_uploader("Choose a cleaning csv file")
uploaded_file_people = st.file_uploader("Choose a people csv file")

if uploaded_file_cleaning is not None :

    df = pd.read_csv(uploaded_file_cleaning, dtype=str ,parse_dates = ["Started At", "Cleaning Finished At", "End At"])

    df = df[df["Status"].isin(["waiting_for_inspection","done"])]
    df = df[~df["Cleaning_type"].isnull()]
    df = df[df["Cleaning_type"].isin(["C/O", "OD", "VC"])]
    
    df["Started At"] += timedelta(hours=7)
    df["Cleaning Finished At"] += timedelta(hours=7)
    df["End At"] += timedelta(hours=7)
    df["Floor"] = df["Room"].str.slice(stop = 1)
    df["Date"] = df["Started At"].dt.strftime("%Y/%m/%d")
    df["Time"] = df["Started At"].apply(lambda x : x.replace(day = 1, month = 1, year = 2000))
    df["Room_num"] = df["Room"].str.slice(1)
    df["Pause Continue At"].fillna("0", inplace = True)
    df["Cleaning_time"] = (df["Cleaning Finished At"]-df["Started At"]).dt.total_seconds()/60
    df["Pause_time"] = df["Pause Continue At"].apply(PauseTime_Calculation)
    df["Total_cleaning_time"] = df["Cleaning_time"] - df["Pause_time"]

    # Choice for date and floor filters
    date_choice = df["Date"].unique()
    date_choice.sort()
    floor_choice = df["Floor"].unique()
    floor_choice.sort()
    room_choice = df["Room_num"].unique()
    room_choice.sort()

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overall Cleaning", "Floor Cleaning", "Maid Cleaning", "Inspection"])

    with tab1 :
        date_select_tab1 = st.multiselect("Date Overall Cleaning", date_choice, date_choice)
        
        st.header("Overall Cleaning Analysis")
        
        fig_tab1_1 = BurnupByRatio_Visualization(df, date_select_tab1)
        fig_tab1_2 = StartTimeByCleaningType_Visualization(df, date_select_tab1)
        fig_tab1_3 = RoomAmountByDate_Visualization(df, date_select_tab1)
        fig_tab1_4 = CleaningTimeByCleaningType_Visualization(df, date_select_tab1)

        st.plotly_chart(fig_tab1_1)

        plot1, plot2 = st.columns(2)

        plot1.plotly_chart(fig_tab1_2)
        plot2.plotly_chart(fig_tab1_3)
        
        plot1.plotly_chart(fig_tab1_4)

        if uploaded_file_people is not None :
            df_people = pd.read_csv(uploaded_file_people)
            df_people["Date"] = pd.to_datetime(df_people["Date"], format = "%d/%m/%Y")
            df_people["Date"] = df_people["Date"].dt.strftime("%Y/%m/%d")
            df_people = df_people[df_people["Hotel"] == df["Site"].iloc[0]]
            
            fig_tab1_5 = RoomAmountPerMaidByDate_Visualization(df, df_people, date_select_tab1)
            
            plot2.plotly_chart(fig_tab1_5)

        fig_tab1_6 = CleaningTimeByWeek(df, date_select_tab1)

        st.header("Median Cleaning Time By Week")
        st.plotly_chart(fig_tab1_6)

        st.header("Cleaning Type Stats")
        st.table(CleaningOverall_PivotTable(df, date_select_tab1))

    with tab2 :
        date_select_tab2 = st.multiselect("Date Floor Cleaning", date_choice, date_choice)
        floor_select_tab2 = st.multiselect("Floor", floor_choice, floor_choice)

        st.header("Floor Cleaning Analysis")

        tab2_1, tab2_2, tab2_3, tab2_4 = st.tabs(["Overall Floor Cleaning", "Burnup By Floor", "Burnup By Date", "Floor Workload"])

        with tab2_1 :
            st.subheader("Overall Floor Cleaning Analysis")

            choice_tab2_1, choice_tab2_2 = st.columns(2)
            startroom = choice_tab2_1.selectbox("Start Room", room_choice)
            endroom = choice_tab2_2.selectbox("End Room", room_choice)

            fig_tab2_1_1 = FloorCleaningAmount_Visualization(df, date_select_tab2, startroom, endroom)
            fig_tab2_1_2 = FloorCleaningTime_Visualization(df, date_select_tab2, startroom, endroom)
            fig_tab2_1_3 = FloorMedianCleanigTime_Visualization(df, date_select_tab2, startroom, endroom)

            plot1, plot2, plot3 = st.columns(3)
            plot1.plotly_chart(fig_tab2_1_1)
            plot2.plotly_chart(fig_tab2_1_2)
            plot3.plotly_chart(fig_tab2_1_3)

        with tab2_2 :
            st.subheader("Burnup By Floor Analysis")

            list_fig_tab2_2_1 = BurnupByFloor_ListVisualization(df, date_select_tab2, floor_select_tab2)

            for fig in list_fig_tab2_2_1:
                st.plotly_chart(fig)
        
        with tab2_3 :
            st.subheader("Burnup By Date Analysis")

            list_fig_tab2_3_1 = BurnupByDate_ListVisualization(df, date_select_tab2, floor_select_tab2)

            for fig in list_fig_tab2_3_1:
                st.plotly_chart(fig)

        with tab2_4 :
            st.subheader("Floor Workload Analysis")
        
            plot1, plot2 = st.columns(2)
        
            floor_select_tab1 = plot1.multiselect("Floor Graph 1", floor_choice, floor_choice)
            floor_select_tab2 = plot2.multiselect("Floor Graph 2", floor_choice, floor_choice)

            df_floor1 = df[df["Floor"].isin(floor_select_tab1)]
            df_floor2 = df[df["Floor"].isin(floor_select_tab2)]

            fig_tab2_4_1 = RoomAmountByDate_Visualization(df_floor1, date_select_tab2)
            fig_tab2_4_2 = RoomAmountByDate_Visualization(df_floor2, date_select_tab2)

            plot1.plotly_chart(fig_tab2_4_1)
            plot2.plotly_chart(fig_tab2_4_2)

            if uploaded_file_people is not None :
                fig_tab2_4_3 = RoomAmountPerMaidByDate_Visualization(df_floor1, df_people, date_select_tab2)
                fig_tab2_4_4 = RoomAmountPerMaidByDate_Visualization(df_floor2, df_people, date_select_tab2)

                plot1.plotly_chart(fig_tab2_4_3)
                plot2.plotly_chart(fig_tab2_4_4)


    with tab3 :
        date_select_tab3 = st.multiselect("Date Maid Cleaning", date_choice, date_choice)

        st.header("Maid Cleaning Analysis")

        tab3_1, tab3_2 = st.tabs(["Overall", "By Maid"])

        with tab3_1 :
            choice_tab3_1, choice_tab3_2 = st.columns(2)
            starthour = choice_tab3_1.selectbox("Start Time", [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
            endhour = choice_tab3_2.selectbox("End Time", [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

            starttime = datetime(2000, 1, 1, starthour, 0, 0, 0, pytz.UTC)
            endtime = datetime(2000, 1, 1, endhour, 0, 0, 0, pytz.UTC)

            fig_tab3_1 = MaidCleaningTime_Visualization(df, date_select_tab3, starttime, endtime)
            st.plotly_chart(fig_tab3_1)
            
    with tab4 :
        date_select_tab4 = st.multiselect("Date Inspection", date_choice)

        st.header("Inspection Analysis")

        fig_tab4_1 = InspectionTimeByDate_Visualization(df, date_select_tab4)
        st.plotly_chart(fig_tab4_1)
