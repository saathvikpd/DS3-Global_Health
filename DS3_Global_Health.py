import plotly.express as px
import numpy as np
import pandas as pd
import streamlit as st
import math
from regression import predictor
from PIL import Image
#read csv and processe
LifeExp_vs_year = pd.read_csv("LifeExp_vs_Year.csv")
LifeExp_vs_liver_death = pd.read_csv("LifeExp_vs_liver_death.csv")
Gdp_vs_femaleH = pd.read_csv("GDP_vs_femaleinthehouse.csv")
LiteracyRate_vs_year = pd.read_csv("literacy_v_year.csv")
SatRate_vs_year = pd.read_csv("satisfaction_v_year.csv")
fm_year_avg = pd.read_csv("female_male_year copy.csv")
df_male_country = pd.read_csv("male_country copy.csv")

merged_final_pop = pd.read_csv("bmi_population_income.csv")
merged_year_avg = pd.read_csv("bmi_year_avg.csv")

life_vs_lungcancer = pd.read_csv("LifeExpectancy_vs_lungCancerDeath")
emp_vs_lungcancer = pd.read_csv("lungCancerDeath_vs_employmentRate")

# # set up sidebar
a = st.sidebar
a.title("Indicators to Explore")
choice = a.radio("Navigation", ["LifeExpectancy", "Liver Cancer Death", "Lung Cancer Death", "BMI and Income", "Literacy", "Satisfaction", "%female in The House", "Try our predictor!", "Run AB test!"])
# Setting up titles
st.write("""
# Global Health Trend of Several Indicators between Male & Female across Continents
""")
if choice == "LifeExpectancy":
    example = LifeExp_vs_year.groupby(['Year','Indicator Name'])[['LifeExpectancy','Pop']].mean().reset_index()

    # discussion for life expectency
    st.write("""
    ##### Female tends to have higher life expectency than male. With the support from the research papers(linked on the poster), female hormone build the strong immune system, and help them to live longer. 
    """)
    
    st.write("""
    ### Example: Overall Average Life Expectancy VS Year between Male and Female
    """)
    # the same way as you would draw in jupyter notebook
    LifeExp_AVG_fig = px.scatter(example,x="Year", y="LifeExpectancy",
                 size="Pop", color= "Indicator Name",symbol = "Indicator Name",
                     hover_name="Indicator Name", size_max=60)
    # streamlit function to dispaly plotly drawing. Check the correct function for matplotlib or others.
    st.plotly_chart(LifeExp_AVG_fig)

    # adding interactive selectbox so users can explore
    st.write("""
    ### Explore Life Expectancy Between Genders for a Specific Country
    """)
    Country = st.selectbox("Country: ",np.array(LifeExp_vs_year.country.unique()))
    df = LifeExp_vs_year[LifeExp_vs_year["country"] == Country]
    LifeExp_Year_figure = px.scatter(df,x="Year", y="LifeExpectancy",
    	         size="Pop", color= "Indicator Name", symbol = "Region",
                     hover_name="country", log_x=True, size_max=60)
    st.plotly_chart(LifeExp_Year_figure)

    st.write("""
    ### Explore Life Expectancy Between Genders across regions
    """)
    gender_selection = ["All Genders","Population, female", "Population, male"]
    region_selection = np.append(["All Regions"], np.array(LifeExp_vs_year.Region.unique()))
    Gender = st.selectbox("Gender: ", gender_selection)
    Region = st.selectbox("Region:" , region_selection)
    for i in gender_selection:
        if i == Gender:
            if i == "All Genders":
                df = LifeExp_vs_year
            else:
                df = LifeExp_vs_year[LifeExp_vs_year["Indicator Name"] == i]
            break
    for j in region_selection:
        if j == Region:
            if j == "All Regions":
                df = df
            else:
                df = df[df['Region'] == j]
            break
    if i ==  'All Genders' and j != 'All Regions' :
        LifeExp_Year_figure = px.scatter(df, x="Year", y="LifeExpectancy",
                                         size="Pop", color="Indicator Name",
                                         hover_name="country", log_x=True, size_max=60)

    elif j == 'All Regions' and i != 'All Genders' or j == 'All Regions' and i == 'All Genders':
        LifeExp_Year_figure = px.scatter(df, x="Year", y="LifeExpectancy",
                                         size="Pop", color="Region",
                                         hover_name="country", log_x=True, size_max=60)
    else: 
        LifeExp_Year_figure = px.scatter(df, x="Year", y="LifeExpectancy",
                                         size="Pop", color="country",
                                         hover_name="country", log_x=True, size_max=60)


    st.plotly_chart(LifeExp_Year_figure)

if choice == "Liver Cancer Death":
    
    # discussion for Liver cancer death
    st.write("""
    ##### Females tend to have less liver cancer rate than males. Female lives approximately live 5 years longer than male with 0.004% lower liver cancer death rate. Both gender have increased life expectancy and liver cancer rate along the years. 
    """)
    
    st.write("""
    ### Explore Life Expectancy VS Average Liver Cancer Death between Genders
    """)
    liver_lifeExp_avg = LifeExp_vs_liver_death.groupby(['Year','Indicator Name'])[['liver_death','LifeExpectancy','Pop']].mean().reset_index()
    df = liver_lifeExp_avg

    fig = px.scatter(df, x= "liver_death", y="LifeExpectancy",
                 size="Pop", color= "Indicator Name",symbol = "Indicator Name",
                     hover_name="Year", log_x=True, size_max=20)
    fig.update_layout(xaxis_title="liver_death in %")
    st.plotly_chart(fig)
    #
    #
    st.write("""
    ### Explore Life Expectancy VS Liver Cancer Death between Gender for a specific country
    """)
    #
    Country = st.selectbox("Country: ",np.array(LifeExp_vs_liver_death['Country Name'].unique()))
    #
    df = LifeExp_vs_liver_death[LifeExp_vs_liver_death['Country Name'] == Country]
    #
    fig = px.scatter(df,x="liver_death", y="LifeExpectancy",
                 size="Pop", color= "Indicator Name", symbol = "Region",
                     hover_name="Country Name", size_max=40, animation_frame = 'Year')
    fig.update_layout(xaxis_title = "liver_death in %",
                      xaxis_range=(np.min(df['liver_death']), np.max(df['liver_death']) * 1.2 ),
                     yaxis_range=(0, 100))
    st.plotly_chart(fig)
    #
    #
    st.write("""
    ### Explore Life Expectancy VS Liver Cancer Death Between Genders across regions
    """)
    gender_selection = ["All Genders","Population, female", "Population, male"]
    region_selection = np.append(["All Regions"], np.array(LifeExp_vs_liver_death.Region.unique()))
    Gender_liver = st.selectbox("Gender : ", gender_selection)
    Region_liver = st.selectbox("Region :" , region_selection)
    for i in gender_selection:
        if i == Gender_liver:
            if i == "All Genders":
                df = LifeExp_vs_liver_death
            else:
                df = LifeExp_vs_liver_death[LifeExp_vs_liver_death["Indicator Name"] == i]
            break
    for j in region_selection :
        if j == Region_liver:
            if j == "All Regions":
                df = df
            else:
                df = df[df['Region'] == j]
            break
    fig = px.scatter(df,x="liver_death", y="LifeExpectancy",
                 size="Pop", color= "Indicator Name", symbol = "Region",
                     hover_name="Country Name", size_max=60, animation_frame ='Year')
    fig.update_layout(xaxis_title = "liver_death in %",
                      xaxis_range=(np.min(df['liver_death'])*0.5, np.max(df['liver_death']) * 1.2 ),
                     yaxis_range=(0, 100))

    st.plotly_chart(fig)
if choice == "%female in The House":
    
    # discussion for female in the house
    st.write("""
    ##### Aggregating every country’s data, the percentage of female in the government is increasing by years pass. However, even as of today, on average it’s still less than 30%, which tells us that the political area is still dominated by male. Female voice isn’t represented enough.
    """)
    
    st.write("""
    ### Example: Overall Percentage of female in The House VS Year
    """)
    example = Gdp_vs_femaleH.groupby(['Year', 'Indicator Name'])[['GDPs','%female in the house']].mean().reset_index()
    fig = px.scatter(example, x="Year", y="%female in the house",
                     size="GDPs", color="Indicator Name",
                     hover_name="Year", log_x=True, size_max=60)
    fig.update_layout(yaxis_title="%female in The House")
    st.plotly_chart(fig)

    st.write("""
       ### Explore % of female in The House for a specific country
       """)

    Country = st.selectbox("Country: ", np.array(Gdp_vs_femaleH['Country Name'].unique()))

    df = Gdp_vs_femaleH[Gdp_vs_femaleH['Country Name'] == Country]

    fig = px.scatter(df, x="GDPs", y="%female in the house",
                     size="GDPs", color="Indicator Name", symbol="Region",
                     hover_name="Country Name", size_max=40, animation_frame='Year')
    fig.update_layout(yaxis_title="%female in The House",
                      xaxis_range=(np.min(df['GDPs']) * 0.5, np.max(df['GDPs']) * 1.2),
                      yaxis_range=(np.min(df['%female in the house']) * 0.5, np.max(df['%female in the house']) * 1.2))
    st.plotly_chart(fig)


    st.write("""
    ### Explore % of female in The House for a specific region
    """)
    region_selection = np.append(np.array(Gdp_vs_femaleH.Region.unique()), ["All Regions"])
    Region_female = st.selectbox("Region:" , region_selection)
    if Region_female == "All Regions":
        df = Gdp_vs_femaleH
    else:
        df = Gdp_vs_femaleH[Gdp_vs_femaleH['Region'] == Region_female]


    fig = px.scatter(df, x="GDPs", y="%female in the house",
                     size="GDPs", color="Country Name",
                     hover_name="Country Name", size_max=40)
    fig.update_layout(yaxis_title="%female in The House",
                      xaxis_range=(np.min(df['GDPs']) * 0.5, np.max(df['GDPs']) * 1.2),
                      yaxis_range=(np.min(df['%female in the house'])-10, np.max(df['%female in the house']) * 1.2))
    st.plotly_chart(fig)

if choice == "Literacy":
    
    # discussion for literacy
    st.write("""
    ##### Males tend to have higher literacy rate than females, even though global literacy rates have generally increased in both genders.
    """)
    
    example = LiteracyRate_vs_year.groupby(['Year','Indicator Name'])[['Lit','Pop']].mean().reset_index()

    st.write("""
    ### Example: Overall Average Literacy Rate by Subregion VS Year between Male and Female
    """)
    # the same way as you would draw in jupyter notebook
    LitRate_AVG_fig = px.scatter(example,x="Year", y="Lit",
                 size="Pop", color= "Indicator Name",symbol = "Indicator Name",
                     hover_name="Indicator Name", size_max=60)
    # streamlit function to dispaly plotly drawing. Check the correct function for matplotlib or others.
    st.plotly_chart(LitRate_AVG_fig)

    # adding interactive selectbox so users can explore
    st.write("""
    ### Explore Literacy Rate Between Genders for a Specific Subregion
    """)
    Subregion = st.selectbox("Subregion: ",np.array(LiteracyRate_vs_year.Subregion.unique()))
    df = LiteracyRate_vs_year[LiteracyRate_vs_year["Subregion"] == Subregion]
    LitRate_Year_figure = px.scatter(df,x="Year", y="Lit",
    	         size="Pop", color= "Indicator Name", symbol = "Subregion",
                     hover_name="Subregion", log_x=True, size_max=20)
    st.plotly_chart(LitRate_Year_figure)

    st.write("""
    ### Explore Literacy Rate Between Genders across subregions
    """)
    gender_selection = ["All Genders", "Population, female", "Population, male"]
    Gender = st.selectbox("Gender: ", gender_selection)
    for i in gender_selection:
        if i == Gender:
            if i == "All Genders":
                df = LiteracyRate_vs_year
            else:
                df = LiteracyRate_vs_year[LiteracyRate_vs_year["Indicator Name"] == i]
            break
    LitRate_Year_figure = px.scatter(df, x="Year", y="Lit",
                                         size="Pop", color="Indicator Name", symbol="Subregion",
                                         hover_name="Subregion", log_x=True, size_max=60)
    st.plotly_chart(LitRate_Year_figure)

if choice == "Satisfaction":
    example = SatRate_vs_year.groupby(['Year','Indicator Name'])[['Sat','Pop']].mean().reset_index()

    # discussion for satisfaction
    st.write("""
    ##### From the visualization, male and female have same trending. No significant difference detected.
    """)
    
    st.write("""
    ### Example: Overall Average Satisfaction Rate by Subregion VS Year between Male and Female
    """)
    # the same way as you would draw in jupyter notebook
    SatRate_AVG_fig = px.scatter(example,x="Year", y="Sat",
                 size="Pop", color= "Indicator Name",symbol = "Indicator Name",
                     hover_name="Indicator Name", size_max=60)
    # streamlit function to dispaly plotly drawing. Check the correct function for matplotlib or others.
    st.plotly_chart(SatRate_AVG_fig)

    # adding interactive selectbox so users can explore
    st.write("""
    ### Explore Satisfaction Rate Between Genders for a Specific Subregion
    """)
    Subregion = st.selectbox("Subregion: ",np.array(LiteracyRate_vs_year.Subregion.unique()))
    df = SatRate_vs_year[SatRate_vs_year["Subregion"] == Subregion]
    SatRate_Year_figure = px.scatter(df,x="Year", y='Sat',
    	         size="Pop", color= "Indicator Name", symbol = "Subregion",
                     hover_name="Subregion", log_x=True, size_max=20)
    st.plotly_chart(SatRate_Year_figure)

    st.write("""
    ### Explore Satisfaction Rate Between Genders across subregions
    """)
    gender_selection = ["All Genders", "Population, female", "Population, male"]
    Gender = st.selectbox("Gender: ", gender_selection)
    for i in gender_selection:
        if i == Gender:
            if i == "All Genders":
                df = SatRate_vs_year
            else:
                df = SatRate_vs_year[SatRate_vs_year["Indicator Name"] == i]
            break
    SatRate_Year_figure = px.scatter(df, x="Year", y="Sat",
                                         size="Pop", color="Indicator Name", symbol="Subregion",
                                         hover_name="Subregion", log_x=True, size_max=60)
    st.plotly_chart(SatRate_Year_figure)

if choice == "Lung Cancer Death":
    example = fm_year_avg.groupby("year").mean().reset_index
    
    # discussion for lung cancer death
    st.write("""
    ##### Males on average have a much higher average amount of deaths from lung cancer compared to females. Furthermore, progressively over years, the number of deaths for both females and males increases. There is a correlation between lung cancer death rate and employment, that as high as the employment rate is higher, the cancer death rate is higher too due to the stressful life event(supported by the research paper).
    """)

    st.write("""
    ### Example: Overall Average death by year for females and males
    """)
    # the same way as you would draw in jupyter notebook
    male_female_deaths_fig = px.scatter(fm_year_avg, x="year", y=fm_year_avg.columns[1:])
    male_female_deaths_fig.update_xaxes(tickangle=45)
    # streamlit function to dispaly plotly drawing. Check the correct function for matplotlib or others.
    st.plotly_chart(male_female_deaths_fig)

    # countries and death
    df_male_cancer_fig = px.bar(df_male_country, x="country", y="deaths")
    st.plotly_chart(df_male_cancer_fig)

    # top 10 countries with deaths --> males
    # top_countries_male = df_male_country[:10]
    # fig_top_male_lc = px.bar(top_countries_male, x="country", y="deaths")
    # st.plotly_chart(fig_top_male_lc)
    
    fig = px.scatter(life_vs_lungcancer, x="Year", y="lung_cancer_death_rate",
                     size="Pop", color="Indicator Name", color_discrete_sequence=['red', 'blue'],
                     symbol="Indicator Name",
                     hover_name="Year", log_x=True, size_max=60)
    st.plotly_chart(fig)

    # lung cancer death vs employment rate

    df = emp_vs_lungcancer
    fig = px.scatter(df, x="employment", y="Lung Cancer Death",
                     size="employment", color="gender",
                     hover_name="gender", size_max=40, animation_frame='Year')
    fig.update_layout(yaxis_title="Lung Cancer Death",
                      xaxis_range=(np.min(df['employment']), np.max(df['employment'])),
                      yaxis_range=(np.min(df['Lung Cancer Death']) * 0.5, np.max(df['Lung Cancer Death']) * 1.2))
    st.plotly_chart(fig)

if choice == "BMI and Income":
    
    # discussion for BMI and Income
    st.write("""
    ##### Males on average have a higher BMI compared to females. Also, the BMI of females and males progressively increased over the years. As easy as people have access to food, the BMI trending is increasing and affecting their health.
    """)
    
    st.write("""
    overall trend for BMI per country over years
    """)
    # the same way as you would draw in jupyter notebook
    df = merged_final_pop
    # fig = px.scatter(df, x="income", y="BMI",
    #                  color="gender", symbol='country', size='population',
    #                  hover_name='country', size_max=20)
    # st.plotly_chart(fig)
    
    region_selection = np.array(df.country.unique())
    Region_bmi = st.selectbox("Country :" , region_selection)
    for j in region_selection :
        if j == Region_bmi:
            df = df[df["country"] == j]
            break
    fig = px.scatter(df,x="income", y="BMI",
                 size="population", color= "gender", symbol = "country",
                     hover_name="country", size_max=30)
    fig.update_layout(xaxis_title = "Income (in thousands of dollars)", 
                      yaxis_title = "BMI")

    st.plotly_chart(fig)

    st.write("""
    Average BMI per year for females and males
    """)

    fig_year_avg = px.scatter(merged_year_avg, x="year", y=merged_year_avg.columns[1:], title=
    "Average BMI per Year", labels={
        "value": "BMI",
    })
    fig_year_avg.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig_year_avg)

if choice == "Try our predictor!":
    st.write("""
    A multiple linear regression using gender, country, and bmi to predict life expectancy
    """)
    gender_selection = ["Female", "Male"]
    country_selection = np.array(LifeExp_vs_year["Country Name"].unique())
    gender = st.selectbox("Gender: ", gender_selection)
    country = st.selectbox("Country: ", country_selection)
    bmi = st.number_input("BMI: ", min_value=0.0, max_value=100.0, value = 23.0, step = 0.1)
    prediction = predictor(gender, country, bmi)
    st.write("Life expectancy: {} year(s)".format(round(prediction, 2)))
    
if choice == "Run AB test!":
    factor = st.selectbox("Choose One Factor", ["Lung Cancer", "Liver Cancer", "BMI", "Literacy", "Life Expectancy"])
    image = Image.open(factor + ".png")
    st.write("P-value is 0, which means the difference between males and females for this factor is statistically significant")
    st.image(image, caption = "AB test for factor {}".format(factor))
   
# fig_year_avg = px.scatter(merged_year_avg, x="year", y=merged_year_avg.columns[1:], title=
# "Average BMI per Year", labels={
#     "value": "BMI",
# })
# fig_year_avg.update_xaxes(tickangle=45)
# fig_year_avg.write_image("fig1.png")

