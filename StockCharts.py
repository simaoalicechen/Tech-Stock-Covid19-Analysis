from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Blues8
from bokeh.embed import components
from bokeh.transform import dodge
import pandas 

# Read in csv 
df = pandas.read_csv('stocks.csv') 
df = df.sort_values(by="August7", ascending=False)

# Convert String fields to numeric
df['Feb21'] = df['Feb21'].astype(int)
df['March12'] = df['March12'].astype(int)
df['August7'] = df['August7'].astype(int)

# Calculate Crash Percentage and Rise Percentage

CrashPercentage = (df['March12']-df['Feb21'])/df['Feb21']*100
RisePercentage = (df['August7']-df['March12'])/df['March12']*100

# Add new CrashPercentage and RisePercentage in csv 
df["CrashPercentage"] = CrashPercentage
df.to_csv("stocks.csv", index=False)

df['RisePercentage'] = RisePercentage
df.to_csv("stocks.csv", index=False)

# Create ColumnDataSource from data frome 
source = ColumnDataSource(df)

output_file('index.html')

# Stock List 

stock_list = source.data['Stock'].tolist()

# Add plot 

p= figure(
  y_range = stock_list, 
  plot_width = 800,
  plot_height = 600,
  title = 'stock prices', 
  x_axis_label = 'Feb21',
  tools = "pan, box_select, zoom_in, zoom_out, save, reset" 
)

# Render glyph 

p.hbar(
  y = 'Stock', 
  right = 'August7',
  left = 0, 
  height = 0.4, 
  color = 'orange', 
  fill_color = factor_cmap(
    'Stock', 
    palette = Blues8, 
    factors = stock_list
  ), 
  fill_alpha = 0.9, 
  source = source, 
  legend_field = 'Stock'
)


# Add Legend 
p.legend.orientation = 'vertical' 
p.legend.location = 'top_right'
p.legend.label_text_font_size = '10px'

# Add Tooltips 

hover = HoverTool()
hover.tooltips = """
  <div> 
    <h3>@Stock</h3> 
    <div><strong>Feb21: </strong>@Feb21</div>
    <div><strong>March12: </strong>@March12</div>
    <div><strong>August7: </strong>@August7</div>
    <div><strong>CrashPercentage: </strong>@CrashPercentage%</div>
    <div><strong>CrashPercentage: </strong>@RisePercentage%</div>
    <div><img src="@Logo" alt="" width = "200"/></div>
  </div> 

"""
p.add_tools(hover)

# Show results 
show(p)
# Save file 
# save(p)

# Print out div and script 
# script, div = components(p)
# print(div)
# print(script) 
