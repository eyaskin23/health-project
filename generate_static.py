import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/social_determinants')
def social_determinants():
    data = {
        'fresno_aqi': 75,
        'california_population': 38866193,
        'unemployment_rate': 3.8
    }
    return render_template('social_determinants.html', data=data)

def build_static_site():
    with app.app_context():
        # Define data for social determinants page
        data = {
            'fresno_aqi': 75,
            'california_population': 38866193,
            'unemployment_rate': 3.8
        }
        
        templates = ['index.html', 'social_determinants.html']
        for template in templates:
            if template == 'social_determinants.html':
                rendered = render_template(template, data=data)
            else:
                rendered = render_template(template)
            
            output_path = os.path.join('static_site', template)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(rendered)

if __name__ == '__main__':
    build_static_site()
