import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(50)
start_date = datetime(2025,9,1)
dates = [start_date+timedelta(i) for i in range(60)]
products = ['A','B','C']
regions = ['north','south','east','west']
data = {
    "date" : np.random.choice(dates,size=200),
    "product" : np.random.choice(products,size=200),
    "region" : np.random.choice(regions,size=200),
    "quantity":np.random.randint(1,20,size=200),
    "unit_price" : np.random.randint(50,200,size=200)
}
df = pd.DataFrame(data)
df.to_csv("unclean_sales_data.csv", index=False)

#total sales per products
total_sales_product = df.groupby("product")['unit_price'].sum().reset_index()
#total sales per region
total_sales_region = df.groupby("region")['unit_price'].sum().reset_index()
#top 3 selling products
top_products = total_sales_product.sort_values('unit_price',ascending=False).head(3)
#day with highest total sales
total_sales_date = df.groupby('date')['unit_price'].sum().reset_index()
highest_sales_date = total_sales_date.sort_values('unit_price',ascending=False).head(1)
highest_sales_date['date'] = highest_sales_date['date'].dt.strftime('%Y-%m-%d')

sales_array = df['unit_price'].to_numpy()
numpy_summary = pd.DataFrame({
    "metric" : ["average_sale","maximum_sale","minimum_sale"],
    "unit_price" : [np.mean(sales_array),np.max(sales_array),np.min(sales_array)]
})


df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.weekday
df['day'] = df['date'].dt.day_name()
weekdays_sales = df[df["day_of_week"] < 5]["unit_price"].sum()
weekends_sales = df[df["day_of_week"] >= 5]["unit_price"].sum()
week_summary = pd.DataFrame({
    "metric": ["weekdays_sales", "weekends_sales"],
    "unit_price": [weekdays_sales, weekends_sales]
})

def standardize(df, category, metric=None, product=None, region=None, date=None):
    return pd.DataFrame({
        "category": [category] * len(df),
        "metric": df.get("metric", [metric] * len(df)),
        "product": df.get("product", [product] * len(df)),
        "region": df.get("region", [region] * len(df)),
        "date": df.get("date", [date] * len(df)),
        "unit_price": df["unit_price"]
    })

s1 = standardize(total_sales_product, "total sales product")
s2 = standardize(total_sales_region, "total sales region")
s3 = standardize(top_products, "Top 3 products")
s4 = standardize(highest_sales_date, "Highest sales day")
s5 = standardize(numpy_summary, "numpy summary")
s6 = standardize(week_summary, "week_summary")

final_summary = pd.concat([s1,s2,s3,s4,s5,s6],ignore_index=True)
final_summary.to_csv("final_summary.csv", index=False)

