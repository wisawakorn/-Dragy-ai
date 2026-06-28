from main import HTML_TEMPLATE, q_core

data = q_core.collapse_state('Sakon Nakhon, TH')
try:
    html = HTML_TEMPLATE.format(
        status=data['status'],
        location=data['location_resonance'],
        timestamp=data['timestamp'],
        news_html=''
    )
    print('OK', len(html))
except Exception as exc:
    import traceback
    traceback.print_exc()
