from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Map (Url)', validators=[DataRequired(), URL(require_tld=True, allow_ip=True, message="Invalid Url")])
    op_time = StringField('Opening Time eg: 8 AM', validators=[DataRequired()])
    cl_time = StringField('Closing Time eg: 5:30 PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee rating', choices=[('☕️'),('☕️☕️'),('☕️☕️☕️'),('☕️☕️☕️☕️'),('☕️☕️☕️☕️☕️')])
    wifi_strength = SelectField('Wifi Strength rating', choices=[('✘'),('💪'),('💪💪️'),('💪💪💪'),('💪💪💪💪'),('💪💪💪💪💪')])
    power = SelectField('Power Socket Availability', choices=[('✘'),('🔌'),('🔌🔌️'),('🔌🔌🔌'),('🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([form.cafe.data, form.location.data, form.op_time.data,
                             form.cl_time.data, form.coffee_rating.data, form.wifi_strength.data,
                             form.power.data])
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding='utf-8', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
