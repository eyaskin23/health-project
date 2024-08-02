from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/social_determinants')
def social_determinants():
    return render_template('social_determinants.html')

def build_static_site():
    with app.test_request_context():
        # Render templates
        os.makedirs('static_site', exist_ok=True)
        for template in ['index.html', 'social_determinants.html']:
            rendered = app.view_functions[template.split('.')[0]]()
            with open(os.path.join('static_site', template), 'w') as f:
                f.write(rendered)

if __name__ == "__main__":
    build_static_site()
