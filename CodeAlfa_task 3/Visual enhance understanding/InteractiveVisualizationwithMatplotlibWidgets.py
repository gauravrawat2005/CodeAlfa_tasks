from matplotlib.widgets import Slider, Button, CheckButtons
import matplotlib.gridspec as gridspec

# Create interactive visualization
fig = plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(3, 3, height_ratios=[3, 1, 1])

# Main plot
ax_main = plt.subplot(gs[0, :])
# Control panel
ax_slider = plt.subplot(gs[1, :])
ax_button = plt.subplot(gs[2, 0])
ax_check = plt.subplot(gs[2, 1:])

# Sample time series data
years = np.arange(2010, 2024)
base_data = np.array([100, 120, 150, 170, 190, 210, 250, 280, 
                      310, 340, 380, 410, 450, 480])
noise = np.random.normal(0, 20, len(years))
data = base_data + noise

# Initial plot
line, = ax_main.plot(years, data, 'b-', linewidth=2, label='Actual')
trend_line, = ax_main.plot(years, base_data, 'r--', linewidth=1.5, 
                           alpha=0.7, label='Trend')
ax_main.set_xlabel('Year')
ax_main.set_ylabel('Value')
ax_main.set_title('Interactive Time Series Analysis')
ax_main.legend()
ax_main.grid(True, alpha=0.3)

# Create slider
ax_slider.clear()
slider_color = 'lightgoldenrodyellow'
ax_slider.set_facecolor(slider_color)
smooth_slider = Slider(
    ax=ax_slider,
    label='Smoothing Factor',
    valmin=1,
    valmax=20,
    valinit=1,
    valstep=1
)

# Create check buttons
ax_check.clear()
check = CheckButtons(
    ax=ax_check,
    labels=['Show Trend', 'Show Grid', 'Show Markers'],
    actives=[True, True, False]
)

# Create reset button
ax_button.clear()
reset_button = Button(ax_button, 'Reset', color=slider_color, hovercolor='gold')

# Update function
def update(val):
    smooth_factor = int(smooth_slider.val)
    smoothed = np.convolve(data, np.ones(smooth_factor)/smooth_factor, mode='same')
    line.set_ydata(smoothed)
    fig.canvas.draw_idle()

def reset(event):
    smooth_slider.reset()
    line.set_ydata(data)
    trend_line.set_visible(True)
    ax_main.grid(True)
    line.set_marker('')
    fig.canvas.draw_idle()

def check_clicked(label):
    if label == 'Show Trend':
        trend_line.set_visible(not trend_line.get_visible())
    elif label == 'Show Grid':
        ax_main.grid(not ax_main.grid)
    elif label == 'Show Markers':
        line.set_marker('o' if line.get_marker() == '' else '')
    fig.canvas.draw_idle()

# Connect callbacks
smooth_slider.on_changed(update)
reset_button.on_clicked(reset)
check.on_clicked(check_clicked)

plt.tight_layout()
plt.show()