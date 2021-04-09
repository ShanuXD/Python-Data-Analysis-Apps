import pandas as pd
import plotly.express as px


desired_width = 320

pd.set_option('display.width', desired_width)

# np.set_printoption(linewidth=desired_width)

pd.set_option('display.max_columns', 20)

# Show numeric output in decimal format e.g., 2.15
pd.options.display.float_format = '{:,.2f}'.format

df_app = pd.read_csv('apps.csv')
# print(df_app.sample(5))
"""DELETE COLS"""
# del df_app['Last_Updated']
df_app.drop(['Last_Updated', 'Android_Ver'], axis=1, inplace=True)
# print(df_app.Rating.isna())

"""Drop NAN values"""
df_app_clean = df_app.dropna()
# print(df_app_clean.shape)

"""Check Duplicate"""
# print(df_app_clean.duplicated())
# duplicated_rows = df_app_clean[df_app_clean.duplicated()]
# print(duplicated_rows.head())
# print(duplicated_rows.shape)
# df_app_clean = df_app_clean.drop_duplicates()
df_app_clean = df_app_clean.drop_duplicates(subset=['App', 'Type', 'Price'])
# print(df_app_clean.shape)
"""Sort according to rating"""
# print(df_app_clean.sort_values('Rating', ascending=False))

"""Show max size app"""
# print(df_app_clean[df_app_clean.Size_MBs == df_app_clean.Size_MBs.max()])
# df_apps_clean.sort_values('Size_MBs', ascending=False).head()

"""Max Review app"""
# print(df_app_clean[df_app_clean.Reviews == df_app_clean.Reviews.max()])

"""Max number of Review, check any paid apps among top 50"""
# print(df_app_clean.sort_values('Reviews', ascending=False).head(50))

"""Content Rating"""
ratings = df_app_clean['Content_Rating'].value_counts()
# print(ratings)
"""Pie Dig"""
# fig = px.pie(labels=ratings.index,
#              values=ratings.values,
#              title="Content Rating",
#              names=ratings.index,
#              )
# fig.update_traces(textposition='outside', textinfo='percent+label')
# fig.show()
"""Hole dig"""
# fig = px.pie(labels=ratings.index,
#              values=ratings.values,
#              title="Content Rating",
#              names=ratings.index,
#              hole=0.6,
#              )
# fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
#
# fig.show()

# print(df_app_clean['Installs'].value_counts())
# print(df_app_clean.Installs.describe())
# print(df_app_clean.info())

df_app_clean.Installs = df_app_clean.Installs.astype(str).str.replace(',', "")
df_app_clean.Installs = pd.to_numeric(df_app_clean.Installs)
# print(df_app_clean[['App', 'Installs']].groupby('Installs').count())
# print(df_app_clean)

df_app_clean['Price'] = df_app_clean['Price'].astype(str).str.replace('$', '', regex=True)
df_app_clean['Price'] = pd.to_numeric(df_app_clean.Price)
# print(df_app_clean)
# print(df_app_clean.sort_values('Price', ascending=False).head(20))
"""Removing False or incorrect Data"""
df_app_clean = df_app_clean[df_app_clean['Price'] < 250]
# print(df_app_clean.sort_values('Price', ascending=False).head(5))

"""Top Paid App Revenue"""
df_app_clean['Revenue_Estimate'] = df_app_clean.Installs.mul(df_app_clean.Price)
# print(df_app_clean.sort_values('Revenue_Estimate', ascending=False)[:10])

# print(df_app_clean.Category.nunique())  --> total 33 umique categories
top10_category = df_app_clean.Category.value_counts()[:10]
# print(top10_category)
"""Plot Graph of top10 Categories"""
# bar = px.bar(x=top10_category.index,
#              y=top10_category.values)
#
# bar.show()
"""Most Downloaded Category"""
category_installs = df_app_clean.groupby('Category').agg({'Installs': pd.Series.sum})
category_installs.sort_values('Installs', ascending=True, inplace=True)
# print(category_installs)
# h_bar = px.bar(x=category_installs.Installs,
#                y=category_installs.index,
#                orientation='h',
#                title='Category Popularity')
#
# h_bar.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')
# h_bar.show()

category_number = df_app_clean.groupby('Category').agg({'App': pd.Series.count})
# print(category_number)
"""Merging two DF category_number, category_installs"""
category_merge_df = pd.merge(category_number, category_installs, on="Category", how="inner")
# print(category_merge_df)

category_merge_df.sort_values('Installs', ascending=False, inplace=True)
# print(category_merge_df)
# print(df_app.sample())
"""Scatter dig of Merge DF"""
# scatter = px.scatter(category_merge_df,
#                      x="App",
#                      y="Installs",
#                      title='Category Concentration',
#                      size='App',
#                      hover_name=category_merge_df.index,
#                      color='Installs')
#
# scatter.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
#                       yaxis_title="Installs",
#                       yaxis=dict(type='log'))
#
# scatter.show()

"""Fixing Nested Columns"""
stack = df_app_clean['Genres'].str.split(';', expand=True).stack()
number_of_genres = stack.value_counts()
# print(number_of_genres)
#
# bar = px.bar(x=number_of_genres.index,
#              y=number_of_genres.values,
#              title='Top Genres',
#              hover_name=number_of_genres.index,
#              color=number_of_genres.values,
#              color_continuous_scale='Agsunset'
#              )
# bar.update_layout(xaxis_title='Genre',
#                   yaxis_title='Number of Apps',
#                   coloraxis_showscale=False)
#
# bar.show()
"""Free vs Paid"""
# print(df_app_clean['Type'].value_counts())

df_free_vs_paid = df_app_clean.groupby(["Category", "Type"], as_index=False).agg({'App': pd.Series.count})
print(df_free_vs_paid)

# g_bar = px.bar(df_free_vs_paid,
#                x='Category',
#                y='App',
#                title='Free vs Paid Apps by Category',
#                color='Type',
#                barmode='group')
#
# g_bar.update_layout(xaxis_title='Category',
#                     yaxis_title='Number of Apps',
#                     xaxis={'categoryorder': 'total descending'},
#                     yaxis=dict(type='log'))
#
# g_bar.show()
"""How Many Download are Paid Apps Giving up?"""
# box = px.box(df_app_clean,
#              y="Installs",
#              x='Type',
#              color='Type',
#              notched=True,
#              points='all',
#              title="How Many Download are Paid Apps Giving up?")
#
# box.update_layout(yaxis=dict(type='log'))
#
# box.show()

"""How Much Paid App Earns?"""
df_paid_apps = df_app_clean[df_app_clean['Type'] == 'Paid']
# box = px.box(df_paid_apps,
#              x='Category',
#              y='Revenue_Estimate',
#              title='How Much Paid App Earns?',
#              )
# box.update_layout(xaxis_title='Category',
#                   yaxis_title='Paid App Ballpark Revenue',
#                   xaxis={'categoryorder': 'min ascending'},
#                   yaxis=dict(type='log'))
# box.show()

"""Price per Categories"""
# median price of android app = 22.9
# print(df_paid_apps.Price.median())
print(df_paid_apps)
box = px.box(df_paid_apps,
             x='Category',
             y="Price",
             title='Price per Category')

box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Price',
                  xaxis={'categoryorder': 'max descending'},
                  yaxis=dict(type='log'))

box.show()

