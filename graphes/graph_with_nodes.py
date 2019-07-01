import pandas as pd
import networkx as nx 

from bokeh.io import output_file, show
from bokeh.models import CustomJSTransform, LabelSet
from bokeh.models.graphs import from_networkx

from bokeh.plotting import figure



df = pd.read_csv('rel2.csv',dtype=str)

df = df.rename(columns={'subject':'source', 'object':"target", 'relation':'weight'})
df = df.drop_duplicates(['source', 'target']).reset_index().dropna()


G = nx.from_pandas_edgelist(df.dropna(), "source", 'target')


p = figure(x_range=(-3.5,3.5), y_range=(-3.5,3.5),  plot_height=1000, plot_width=1800) 
p.grid.grid_line_color = None

r = from_networkx(G, nx.spring_layout, scale=3, center=(0,0))
r.node_renderer.glyph.size=15
r.edge_renderer.glyph.line_alpha=0.2

p.renderers.append(r)


from bokeh.transform import transform    

# add the labels to the node renderer data source
source = r.node_renderer.data_source


code = """
    var result = new Float64Array(xs.length)
    for (var i = 0; i < xs.length; i++) {
        result[i] = provider.graph_layout[xs[i]][%s]
    }
    return result
"""
xcoord = CustomJSTransform(v_func=code % "0", args=dict(provider=r.layout_provider))
ycoord = CustomJSTransform(v_func=code % "1", args=dict(provider=r.layout_provider))

# Use the transforms to supply coords to a LabelSet 
labels = LabelSet(x=transform('index', xcoord),
                  y=transform('index', ycoord),
                  text='index', text_font_size="12px",
                  x_offset=5, y_offset=5,
                  source=source, render_mode='canvas')

p.add_layout(labels)


output_file('graph.html')
show(p)
