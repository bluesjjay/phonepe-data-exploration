import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json

#DataFrame Creation
#sql connection

mydb=psycopg2.connect(host= "localhost",
                      user= "postgres",
                      port="5432",
                      database= "phpnepe_data",
                      password= "Jesse")
cursor= mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Year","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Year","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Year","Quarter","Brands",
                                             "Transaction_count","percentage"))


#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Year","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))


#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Year","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))


#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Year","Quarter","Districts",
                                             "RegisteredUsers","AppOpens"))


#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Year","Quarter","pincodes",
                                             "Transaction_count","Transaction_amount"))



#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States","Year","Quarter","pincodes",
                                             "Transaction_count","Transaction_amount"))



#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Year","Quarter","pincodes",
                                             "RegisteredUsers"))



def Transaction_amount_count_Y(df,year):

    tacy=df[df["Year"] == year]
    tacy.reset_index(drop= True, inplace= True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States",y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(tacyg, x="States",y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)


    col1,col2= st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1, locations= "States", featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States",title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg,geojson= data1, locations= "States", featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States",title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy


def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True, inplace= True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States",y="Transaction_amount", title=f"{tacy["Year"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(tacyg, x="States",y="Transaction_count", title=f"{tacy["Year"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1, locations= "States", featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States",title=f"{tacy["Year"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States",title=f"{tacy["Year"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy


#Transaction_Type
def Aggre_Tran_Transaction_type(df, state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop= True, inplace= True)
    
    tacyga=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyga.reset_index(inplace=True)


    fig_pie_1= px.pie(data_frame=tacyga, names= "Transaction_type", values="Transaction_amount",
                    width=600, title= f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
    st.plotly_chart(fig_pie_1)

    fig_pie_2= px.pie(data_frame=tacyga, names= "Transaction_type", values="Transaction_count",
                    width=600, title=  f"{state.upper()} TRANSACTION COUNT", hole=0.5)
    st.plotly_chart(fig_pie_2)

# Aggre_User_Analysis_1
def Aggre_user_plot_1(df, year):
    aguy=df[df["Year"]==  year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1 = px.bar(aguyg, x= "Brands", y="Transaction_count", title = f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 800, color_discrete_sequence= px.colors.sequential.haline, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy 

# Aggre_user_analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq=df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1 = px.bar(aguyqg, x= "Brands", y="Transaction_count", title = f"{quarter} QUARTER,BRANDS AND TRANSACTION COUNT",
                    width= 800, color_discrete_sequence= px.colors.sequential.haline, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

# Aggre_user_analysis_3
def Aggre_user_plot_3(df, state):

    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=800, markers= True)
    st.plotly_chart(fig_line_1)



#Map_Insurance_District
def Map_insurance_Districts(df, state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop= True, inplace= True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_bar_1= px.bar(tacyg, x="Transaction_amount", y="Districts", orientation="h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Oranges_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x="Transaction_count", y="Districts", orientation="h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df,year):
    muy=df[df["Year"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{year} REGISTERED USERS, APPOPENS", width=1000,height=800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{df ["Year"].min()} YEAR {quarter} QUARTER REGISTERED USERS, APPOPENS", width=1000,height=800, markers= True,
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

# map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== 'Bihar']
    muyqs.reset_index(drop= True, inplace= True)

    fig_map_user_bar_1= px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation= "h",
                            title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence = px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2= px.bar(muyqs, x="AppOpens", y="Districts", orientation= "h",
                            title= f"{states.upper()} APPOPENS USER", height= 800, color_discrete_sequence = px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_map_user_bar_2)


# top_insurance_plot_1 
def Top_insurance_plot_1(df, state):
    tiy=df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_Top_insur_bar_1= px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data="pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width=600, color_discrete_sequence = px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_Top_insur_bar_1)

    with col2:

        fig_Top_insur_bar_2= px.bar(tiy, x="Quarter", y="Transaction_count", hover_data="pincodes",
                                title= "TRANSACTION COUNT", height= 650,width=600, color_discrete_sequence = px.colors.sequential.Blugrn_r)
        st.plotly_chart(fig_Top_insur_bar_2)

# top_user_plot_1
def top_user_plot_1(df, year):
    tuy=df[df["Year"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["pincodes"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1 =px.bar(tuyg, x= "States", y= "pincodes", color= "Quarter",width=1000, height=800,
                        color_discrete_sequence=px.colors.sequential.Blues,hover_name= "States",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

# top_user_plot_2
def top_user_plot_2(df, state):
    tuys=df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2 = px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height=800, color="RegisteredUsers", hover_data= "pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)




# sql connection
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port="5432",
                        database= "phpnepe_data",
                        password= "Jesse")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''select states, sum(transaction_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("states", "transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
    
        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title= "TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, sum(transaction_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount
                limit 10'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("states", "transaction_amount"))

    with col2:
    
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title= "LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select states, avg(transaction_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title= "AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Redor_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)



# sql connection
def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port="5432",
                        database= "phpnepe_data",
                        password= "Jesse")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''select states, sum(transaction_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("states", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="transaction_count", title= "TOP 10 0F TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, sum(transaction_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count
                limit 10'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("states", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title= "LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select states, avg(transaction_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title= "AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Redor_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)

# sql connection
def top_chart_registered_user(table_name, state):
    mydb=psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port="5432",
                        database= "phpnepe_data",
                        password= "Jesse")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''select districts, sum(registeredusers) as registeredusers
                from {table_name}
                where states= '{state}'
                group by districts
                order by registeredusers desc  
                limit 10'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("districts", "registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registeredusers", title= "TOP 10 OF REGISTERED USERS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts, sum(registeredusers) as registeredusers
                from {table_name}
                where states= '{state}'
                group by districts
                order by registeredusers
                limit 10'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("districts", "registeredusers"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registeredusers", title= "LAST 10 REGISTERED USERS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select districts, avg(registeredusers) as registeredusers
                from {table_name}
                where states= '{state}'
                group by districts
                order by registeredusers'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("districts", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="districts", x="registeredusers", title= "AVERAGE OF REGISTERED USERS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Redor_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


# sql connection
def top_chart_appopens(table_name, state):
    mydb=psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port="5432",
                        database= "phpnepe_data",
                        password= "Jesse")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states= '{state}'
                group by districts
                order by appopens desc  
                limit 10'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("districts", "appopens"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="appopens", title= "TOP 10 OF APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states= '{state}'
                group by districts
                order by appopens
                limit 10'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("districts", "appopens"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title= "LAST 10 APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select districts, avg(appopens) as appopens
                from {table_name}
                where states= '{state}'
                group by districts
                order by appopens'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title= "AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Redor_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


# sql connection
def top_chart_registered_users(table_name):
    mydb=psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port="5432",
                        database= "phpnepe_data",
                        password= "Jesse")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns= ("states", "registeredusers"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="registeredusers", title= "TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers
                limit 10'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns= ("states", "registeredusers"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title= "LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select states, avg(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns= ("states", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title= "AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Redor_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#streamlit part 

st.set_page_config(layout="wide")
st.title("PHONEPE VISUALISATION AND EXPLORATION")

with st.sidebar:


    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])
if select== "HOME":
    
    col1,col2= st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.header("INDIA'S BEST TRANSACTION APP")
        st.header("scan QR Code and Pay")
        st.header("Split Bills Between People")
        st.header("Experience the Phonepe Advantage")
        st.download_button("DOWNLOAD THE APP NOW",  "https://www.phonepe.com/app-download/")
    with col2:
        st.image(r"C:\Users\THINKPAD\Desktop\New folder\Phonepeproject\New-Project.png")
        

elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_ia",Aggre_insurance["Year"].min(),Aggre_insurance["Year"].max(),Aggre_insurance["Year"].min())
            tac_Y = Transaction_amount_count_Y(Aggre_insurance, years)


            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())

            Transaction_amount_count_Y_Q( tac_Y,quarters)
 
        elif method == "Transaction Analysis":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_at",Aggre_transaction["Year"].min(),Aggre_transaction["Year"].max(),Aggre_transaction["Year"].min())
            Aggre_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_at", Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter", Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(), Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q( Aggre_tran_tac_Y,quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_t", Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)    


        elif method == "User Analysis":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_ua",Aggre_user["Year"].min(),Aggre_user["Year"].max(),Aggre_user["Year"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)
            
            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())

            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)



    with tab2:

        method2 = st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year",Map_insurance["Year"].min(),Map_insurance["Year"].max(),Map_insurance["Year"].min())
            map_insur_tac_Y = Transaction_amount_count_Y(Map_insurance, years)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_map", map_insur_tac_Y["States"].unique())

            Map_insurance_Districts(map_insur_tac_Y, states)


            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter_mi", map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(), map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_t", map_insur_tac_Y_Q["States"].unique())

            Map_insurance_Districts(map_insur_tac_Y_Q, states)


        elif method2 == "Map Transaction":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year",Map_transaction["Year"].min(),Map_transaction["Year"].max(),Map_transaction["Year"].min())
            map_tran_tac_Y = Transaction_amount_count_Y(Map_transaction, years)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_map", map_tran_tac_Y["States"].unique())

            Map_insurance_Districts(map_tran_tac_Y, states)


            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter_mt", map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(), map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y,quarters)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_t", map_tran_tac_Y_Q["States"].unique())

            Map_insurance_Districts(map_tran_tac_Y_Q, states)


        elif method2 == "Map User":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_mu",Map_user["Year"].min(),Map_user["Year"].max(),Map_user["Year"].min())
            map_user_Y = map_user_plot_1(Map_user, years)

            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter_mu", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y,quarters)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mu", map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)



    with tab3:

        method3 = st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method3 == "Top Insurance":

            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_ti",Top_insurance["Year"].min(),Top_insurance["Year"].max(),Top_insurance["Year"].min())
            Top_insur_tac_Y = Transaction_amount_count_Y(Top_insurance, years)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_ti", Top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(Top_insur_tac_Y, states)


            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter_mu", Top_insur_tac_Y["Quarter"].min(), Top_insur_tac_Y["Quarter"].max(), Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Top_insur_tac_Y,quarters)
            

        elif method3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_tt",Top_transaction["Year"].min(),Top_transaction["Year"].max(),Top_transaction["Year"].min())
            Top_tran_tac_Y = Transaction_amount_count_Y(Top_transaction, years)


            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tt", Top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(Top_tran_tac_Y, states)


            col1,col2 = st.columns(2)
            with col1:

                quarters=st.slider("Select The Quarter_tt", Top_tran_tac_Y["Quarter"].min(), Top_tran_tac_Y["Quarter"].max(), Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Top_tran_tac_Y,quarters)

        elif method3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years=st.slider("Select The Year_tu",Top_user["Year"].min(),Top_user["Year"].max(),Top_user["Year"].min())
            Top_user_Y = top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tu", Top_user_Y["States"].unique())

            top_user_plot_2(Top_user_Y, states)



elif select == "TOP CHARTS":
    
    question= st.selectbox("select the question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                 "2. Transaction Amount and Count of Map Insurance",
                                                 "3. Transaction Amount and Count of Top Insurance",
                                                 "4. Transaction Amount and Count of Aggregated Transaction",
                                                 "5. Transaction Amount and Count of Map Transaction",
                                                 "6. Transaction Amount and Count of Top Transaction",
                                                 "7. Transaction Count of Aggregated User",
                                                 "8. Registered Users of Map User",
                                                 "9. App opens of Map User",
                                                 "10. Registered Users of Top User",
                                                 ])
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered Users of Map User":

        states= st.selectbox("Select the State", Map_user["States"].unique())   
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":

        states= st.selectbox("Select the State", Map_user["States"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "10. Registered Users of Top User":
   
        st.subheader("REGISTERED USER")
        top_chart_registered_users("top_user")

    

    