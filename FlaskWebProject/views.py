"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from flask import request
from sergey import get_recommendations


@app.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
    if request.method == 'POST':
	print request.form
        uid = request.form['uid']
        target_city = request.form['to']
        start_city = request.form['from']
        profiles = get_recommendations(uid, start_city, target_city)

	return render_template(
		'recommendations.html',
		title="Recommendations",
		profiles=profiles.to_dict(orient = 'records')
	)
    else:
        return render_template(
            'index.html',
            title='Home Page',
            year=datetime.now().year,
        )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
