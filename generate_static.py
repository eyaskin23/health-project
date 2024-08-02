from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Mock data for static site generation
    data = [
        {"Test": "WBC", "Value": 6.13, "Image": "WBC.svg"},
        {"Test": "RBC", "Value": 4.86, "Image": "RBC.svg"},
        {"Test": "HGB", "Value": 13.3, "Image": "HGB.svg"},
        {"Test": "HCT", "Value": 41.0, "Image": "HCT.svg"},
        {"Test": "MCV", "Value": 84.4, "Image": "MCV.svg"},
        {"Test": "MCH", "Value": 27.4, "Image": "MCH.svg"},
        {"Test": "MCHC", "Value": 32.4, "Image": "MCHC.svg"},
        {"Test": "RDW", "Value": 13.7, "Image": "RDW.svg"},
        {"Test": "PLATELET COUNT", "Value": 227, "Image": "PLATELET_COUNT.svg"},
        {"Test": "Hemoglobin A1c", "Value": 5.2, "Image": "Hemoglobin_A1c.svg"},
        {"Test": "Glucose", "Value": 99, "Image": "Glucose.svg"},
        {"Test": "Fresno Air Quality", "Value": "75", "Image": "fresno_air_quality.svg"},
        {"Test": "California Population", "Value": "38866193", "Image": "california_population.svg"}
    ]
    return render_template('dashboard.html', data=data)

@app.route('/social_determinants')
def social_determinants():
    # Mock data for static site generation
    data = [
        {"Test": "Fresno Air Quality", "Value": "75", "Image": "fresno_air_quality.svg"},
        {"Test": "California Population", "Value": "38866193", "Image": "california_population.svg"}
    ]
    return render_template('social_determinants.html', data=data)

def build_static_site():
    with app.test_request_context():
        pages = {
            '/': 'index.html',
            '/social_determinants': 'social_determinants.html'
        }

        if not os.path.exists('static_site'):
            os.makedirs('static_site')

        for route, filename in pages.items():
            try:
                rendered = app.test_client().get(route)
                if rendered.status_code != 200:
                    print(f"Error: Failed to render {route}, status code {rendered.status_code}")
                    with open(f'static_site/{filename}', 'w') as f:
                        f.write(rendered.get_data(as_text=True))
                else:
                    with open(f'static_site/{filename}', 'w') as f:
                        f.write(rendered.get_data(as_text=True))
            except Exception as e:
                print(f"Error processing {route}: {e}")

if __name__ == '__main__':
    build_static_site()
