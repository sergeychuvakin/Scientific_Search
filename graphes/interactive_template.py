import pandas as pd
import networkx as nx
df = pd.read_csv('second2.csv',dtype=str)
df = df.rename(columns={'subject':'source', 'object':"target", 'relation':'weight'})
df = df.drop_duplicates(['source', 'target']).reset_index().dropna()

G = nx.from_pandas_edgelist(df.dropna(), "source", 'target')



from bokeh.io import output_file, show
from bokeh.models import CustomJSTransform, LabelSet, Arrow, OpenHead, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx

from bokeh.plotting import figure

#G=nx.nx.barbell_graph(3,2)



p = figure(x_range=(-1.5,1.5), y_range=(-1.5,1.5),  plot_height=1000, plot_width=1800)
p.grid.grid_line_color = None

node_hover_tool = HoverTool(tooltips=[("t", "@utterance")])
p.add_tools(node_hover_tool)

pos = nx.spring_layout(G)

r = from_networkx(G, pos, scale=3, center=(0,0))
r.node_renderer.glyph.size=15
r.edge_renderer.glyph.line_alpha=0.2

from bokeh.transform import transform

source2 = r.node_renderer.data_source
# add the labels to the edge renderer data source
source = r.edge_renderer.data_source

#source.data['names'] = ["{x}-{y}".format(x=x, y=y) for (x,y) in zip(source.data['start'], source.data['end'])]
source.data['names'] = df['weight'].values
source.data['utterance'] = df['utterance'].values
source2.data['utterance'] = df['utterance'].values
p.renderers.append(r)


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
                  text='names', text_font_size="10px",
                  x_offset=5, y_offset=5,
                  source=source, render_mode='canvas', text_color='#ff0000')

p.add_layout(labels)


code2 = """
    var result = new Float64Array(xs.length)
    for (var i = 0; i < xs.length; i++) {
        result[i] = provider.graph_layout[xs[i]][%s]
    }
    return result
"""

xcoord = CustomJSTransform(v_func=code2 % "0", args=dict(provider=r.layout_provider))
ycoord = CustomJSTransform(v_func=code2 % "1", args=dict(provider=r.layout_provider))

# Use the transforms to supply coords to a LabelSet 
labels2 = LabelSet(x=transform('index', xcoord),
                  y=transform('index', ycoord),
                  text='index', text_font_size="12px",
                  x_offset=5, y_offset=5,
                  source=source2, render_mode='canvas')

p.add_layout(labels2)

#p.add_layout(Arrow(end=OpenHead(size=15), source=source, x_start='x_start', y_start='y_start', x_end='x_end', y_end='y_end'))
output_file('second.html')
show(p)
