import pandas as pd
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, FactorRange
from bokeh.transform import factor_cmap

def age_group_survival(df):
    # categorise by age
    df['AgeGroup'] = df['Age'].apply(categorise_age_groups)

    # calculate the percentage of passengers who survived within each group
    survival_rate = df.groupby('AgeGroup')['Survived'].mean() * 100
    df['SurvivalRate'] = df['AgeGroup'].map(survival_rate)

    # survival rate by age group bar chart 
    age_groups = survival_rate.index.tolist()
    rate = survival_rate.values
    p = figure(x_range=age_groups, title="Age Group Survival Rate", x_axis_label="Age Group", y_axis_label="Survival Rate")
    p.vbar(x = age_groups, top=rate, width=0.5)
    p.add_tools(HoverTool(tooltips=[("Age Group", "@x"), ("Survival Rate", "@top%")]))
    output_file("age_group_survival.html")
    show(p)

def class_gender(df):
    # survival rate by class gender
    survival_rate_class_gender = df.groupby(['Pclass', 'Sex'])['Survived'].mean()
    class_gender = [ (str(pair[0]), pair[1]) for pair in survival_rate_class_gender.keys() ]

    p2 = figure(x_range=FactorRange(*class_gender), title="Survival Rate by Class and Gender")
    rates = survival_rate_class_gender.values * 100
    p2.vbar(x=class_gender, top=rates, width=0.5)
    p2.add_tools(HoverTool(tooltips=[("PClass, Gender", "@x"), ("Survival Rate", "@top%")]))
    output_file("class_gender.html")
    show(p2)

def fare_survival(df):
    factors = [ str(pair) for pair in df['Pclass'].unique() ]

    # 1. Map 0 and 1 to "Not Survived" and "Survived"
    # fucking amazing, colors works only on strings, WOW
    df['Pclass'] = df['Pclass'].astype(str)
    df['SurvivalStatus'] = df['Survived'].map({0: 'Not Survived', 1: 'Survived'})
    # Create a ColumnDataSource from the first 20 rows
    # took only 20 because another way is a mess
    source = ColumnDataSource(df.head(20))

    p3 = figure(title="Scatter plot: Fare vs Survival Status by Class", 
                x_axis_label="Fare", y_axis_label="Survival Status",
                width=700, height=500)

    # use factor_cmap to map the 'Pclass' to colors
    p3.circle(x='Fare', y='Survived', size=40, alpha=0.6, source=source,
                color=factor_cmap('Pclass', palette=['green', 'blue','yellow'], factors=factors))

    p3.add_tools(HoverTool(tooltips=[
        ("Fare", "@Fare"),
        ("Survived", "@SurvivalStatus"),
        ("Class", "@Pclass")]))

    output_file("fare_vs_survival.html")
    # Display the plot
    show(p3)

def categorise_age_groups(age):
        if age < 13:
            return "Child"
        elif age < 28:
            return "Young Adult"
        elif age < 60:
            return "Adult"
        else:
            return "Senior"
        
def main():
    df = pd.read_csv('Titanic-Dataset.csv')

    # handle missing values
    fill_values = {
        'Age': df['Age'].median(),
        'Cabin': 'Unknown',
        'Embarked': 'Unknown'  
    }
    df.fillna(value=fill_values, inplace=True)
    
    age_group_survival(df)
    class_gender(df)
    fare_survival(df)


if __name__ == '__main__':
    main()