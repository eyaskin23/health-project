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
    with app.app_context():
        if not os.path.exists('static_site'):
            os.makedirs('static_site')
        templates = ['index.html', 'social_determinants.html']
        for template in templates:
            rendered = render_template(template)
            with open(f'static_site/{template}', 'w') as f:
                f.write(rendered)

if __name__ == "__main__":
    build_static_site()
