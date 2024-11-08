import plotly.graph_objects as go


# Add data
diff =  [-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3]
err =   [-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3]

four =  [0,   0,  0.5,1,1,1,1,1,1,1,0.5,0,0]
one =   [0,0,0,0,0,0.5,1,0.5,0,0,0,0,0]

fig = go.Figure()

# Create and style traces
fig.add_trace(go.Scatter(x=err, y=diff, name='differences',
                         line=dict(color='royalblue', width=4)))

fig.add_trace(go.Scatter(x=err, y=one, name='1 pixel line',
                         line=dict(color='firebrick', width=4)))

fig.add_trace(go.Scatter(x=err, y=four, name='4 pixel line',
                         line=dict(color='green', width=4)))

#plt.title('Colour Change with Line Widths \nand Distance from Theoretical Line')
#plt.ylabel('Relative Colour Intensity')
#plt.xlabel('Distance from Theoretical Line')

# Edit the layout
fig.update_layout(title='Colour Change with Line Widths \nand Distance from Theoretical Line',
                   xaxis_title='Distance from Theoretical Line',
                   yaxis_title='Relative Colour Intensity'
                   )
fig.update_traces(textposition="bottom right")

#fig.write_html(file='thick_lines.html', auto_open=True)
fig.show()