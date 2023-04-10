from flask import Flask, render_template, request
import pandas as pd
from geopy import geocoders
import geopy.distance as geod

gn = geocoders.GeoNames(username="sebasg")

companies_df = pd.read_csv('companies_df.csv')
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/find_closest_company', methods=['POST'])
def find_closest_company():
    user_input = request.form['city']
    company = closest_surveillance_company(user_input, companies_df, geod)
    return render_template("ClosestCompany.html")
    return f"The closest surveillance company to {user_input} is {company['company_name']}. Their headquarters are located in {company['hq_city']} at ({company['hq_latitude']}, {company['hq_longitude']})."

def closest_surveillance_company(user_input_name, companies_df, geod):
    list_of_coords = list(zip(companies_df.hq_latitude, companies_df.hq_longitude))
    user_city = gn.geocode(user_input_name, exactly_one=False)[0]
    user_city_coord = (user_city.latitude, user_city.longitude)
    distance_dict = dict()
    for position,coord in enumerate(list_of_coords):
        try:
            coord_distance = geod.distance(user_city_coord, coord).km
            distance_dict[position] = coord_distance
        except ValueError:
            pass
    index_lowest = min(distance_dict, key=distance_dict.get)
    entry = companies_df.iloc[index_lowest]
    return entry

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)