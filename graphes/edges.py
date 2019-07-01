import pandas as pd
df = pd.read_csv('rel2.csv',dtype=str)
df = df.rename(columns={'subject':'source', 'object':"target", 'relation':'weight'})
df = df.drop_duplicates(['source', 'target']).reset_index().dropna()

G = nx.from_pandas_edgelist(df.dropna(), "source", 'target')


import networkx as nx

from bokeh.io import output_file, show
from bokeh.models import CustomJSTransform, LabelSet
from bokeh.models.graphs import from_networkx

from bokeh.plotting import figure

#G=nx.nx.barbell_graph(3,2)

p = figure(x_range=(-3.5,3.5), y_range=(-3.5,3.5),  plot_height=1000, plot_width=1800)
p.grid.grid_line_color = None

r = from_networkx(G, nx.spring_layout, scale=3, center=(0,0))
r.node_renderer.glyph.size=15
r.edge_renderer.glyph.line_alpha=0.2

p.renderers.append(r)

from bokeh.transform import transform

# add the labels to the edge renderer data source
source = r.edge_renderer.data_source
#source.data['names'] = ["{x}-{y}".format(x=x, y=y) for (x,y) in zip(source.data['start'], source.data['end'])]
source.data['names'] = df['weight'].values
# create a transform that can extract and average the actual x,y positions
code = """
    var result = new Float64Array(xs.length)
    coords = provider.get_edge_coordinates(source)[%s]
    for (var i = 0; i < xs.length; i++) {
        result[i] = (coords[i][0] + coords[i][1])/2
    }
    return result
"""
xcoord = CustomJSTransform(v_func=code % "0", args=dict(provider=r.layout_provider, source=source))
ycoord = CustomJSTransform(v_func=code % "1", args=dict(provider=r.layout_provider, source=source))

# Use the transforms to supply coords to a LabelSet
labels = LabelSet(x=transform('start', xcoord),
                  y=transform('start', ycoord),
                  text='names', text_font_size="12px",
                  x_offset=5, y_offset=5,
                  source=source, render_mode='canvas')

p.add_layout(labels)
output_file('edges.html')
show(p)
