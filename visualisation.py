import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    df_g = pd.read_csv('global.csv')
    df_d = pd.read_csv('devices.csv')
    
    colors = {
        'primary': '#1E3A8A',     
        'secondary': '#3B82F6',    
        'accent': '#60A5FA',       
        'background': '#0F172A',   
        'card': '#1E293B',         
        'text': '#F8FAFC',         
        'success': '#10B981',      
        'warning': '#F59E0B'       
    }

    fig = make_subplots(
        rows=4, cols=6,
        specs=[
            [{"type": "indicator", "colspan": 2}, None, {"type": "indicator", "colspan": 2}, None, {"type": "indicator", "colspan": 2}, None],
            [{"type": "bar", "colspan": 4}, None, None, None, {"type": "pie", "colspan": 2}, None],
            [{"type": "bar", "colspan": 3}, None, None, {"type": "bar", "colspan": 3}, None, None],
            [{"type": "scatter", "colspan": 6}, None, None, None, None, None]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.07,
        row_heights=[0.2, 0.3, 0.25, 0.25],
        subplot_titles=(
            "<b>🌡️ TEMPÉRATURE GLOBALE</b>", "<b>⚡ CONSOMMATION ÉNERGIE</b>", "<b>🔋 SANTÉ BATTERIE</b>",
            "<b>📊 TEMPÉRATURE PAR CAPTEUR</b>", "<b>📈 RÉPARTITION ÉNERGIE</b>",
            "<b>💧 NIVEAUX D'HUMIDITÉ</b>", "<b>🔋 NIVEAU BATTERIE / DEVICE</b>",
            "<b>📉 SCORE DE PERFORMANCE GLOBAL</b>"
        )
    )


    fig.add_trace(go.Indicator(
        mode="gauge+number", value=df_g['avg_temp_global'][0],
        number={'suffix': "°C", 'font': {'size': 35, 'color': colors['text']}},
        gauge={'axis': {'range': [0, 40]}, 'bar': {'color': colors['secondary']}, 'bgcolor': colors['card']}
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="number+delta", value=df_g['total_energy_consumed'][0],
        delta={'reference': 1000, 'font': {'size': 18}},
        number={'suffix': " kWh", 'font': {'size': 35, 'color': colors['text']}}
    ), row=1, col=3)

    fig.add_trace(go.Indicator(
        mode="gauge+number", value=df_g['avg_battery_global'][0],
        number={'suffix': "%", 'font': {'size': 35, 'color': colors['text']}},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': colors['success']}, 'bgcolor': colors['card']}
    ), row=1, col=5)


    df_temp = df_d.sort_values('avgTemp', ascending=False)
    fig.add_trace(go.Bar(
        x=df_temp['deviceId'], y=df_temp['avgTemp'],
        marker=dict(color=df_temp['avgTemp'], colorscale='Blues'),
        name="Temp"
    ), row=2, col=1)

    fig.add_trace(go.Pie(
        labels=df_d['deviceId'], values=df_d['totalEnergy'],
        hole=0.4, marker=dict(colors=[colors['primary'], colors['secondary'], colors['accent']])
    ), row=2, col=5)


    df_hum = df_d.sort_values('avgHum')
    fig.add_trace(go.Bar(
        x=df_hum['avgHum'], y=df_hum['deviceId'], orientation='h',
        marker_color=colors['accent'], name="Humidité"
    ), row=3, col=1)

    fig.add_trace(go.Bar(
        x=df_d['deviceId'], y=df_d['minBattery'],
        marker_color=colors['secondary'], name="Batterie"
    ), row=3, col=4)


    perf_score = (df_d['minBattery'] * 0.6 + (40 - df_d['avgTemp']) * 1.0)
    fig.add_trace(go.Scatter(
        x=df_d['deviceId'], y=perf_score,
        mode='lines+markers', line=dict(color=colors['success'], width=4),
        fill='tozeroy', name="Performance"
    ), row=4, col=1)

    fig.update_layout(
        title={'text': "<b>🌐 IOT SMART CITY MONITORING</b>", 'x': 0.5, 'y': 0.98, 'font': {'size': 28, 'color': colors['text']}},
        template='plotly_dark',
        height=1300,
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(t=150, b=100, l=80, r=80),
        showlegend=False
    )

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=14, color=colors['text'])
        i['y'] = i['y'] + 0.03  

    fig.show()
    print("✅ Dashboard professionnel généré sans superposition !")

except Exception as e:
    print(f"❌ Erreur : {e}")