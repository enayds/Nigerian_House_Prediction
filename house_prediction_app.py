import streamlit as st
import joblib
from house_functions import House
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


st.title(' Egbuna\'s House Prediction App')
st.write('## Welcome to the place of Prediction')
location = st.selectbox('State',['Abuja', 'Lagos', 'Imo', 'Rivers', 'Anambra', 'Others'])
rooms = st.selectbox('Bedrooms', [1,2,3,4,5,'Others'])
bathrooms = st.selectbox('Bathrooms', [1,2,3,4,5,'Others'])
house_type = st.selectbox('type of house', ['Apartment', 'Flat', 'Duplex', 'House', 'Bungalow', 'Penthouse', 'Condo', 'Studio Apartment'])
house_facilities = st.multiselect('House Facilities: (you can choose more than one option)', ['Aircondition',
     'Dinning Area',  'Dishwasher', 'Chandelier', 'Prepaid Meter'])
house_condition = st.selectbox('House Condition', ['Newly Built', 'Fairly Used'])
furnish = st.selectbox('Furnishing', ['Unfurnished', 'Semi_Furnished', 'Furnished'])
area = st.selectbox('Type of Area', ['Urban', 'Semi_Urban', 'Rural'])
estate = st.checkbox('in estate?')

## encoding all the categorical values into numerical values
location = House.location(location)
rooms = House.bedrooms(rooms)
bathrooms = House.bath(bathrooms)
estate = House.estate(estate)
house_type = House.house_type(house_type)
house_facilities = House.facilities(house_facilities)
furnish = House.furnish(furnish)
house_condition = House.house_condition(house_condition)
area = House.area(area)



## extracting all the selected facilties
dishwasher = House.check('Dishwasher', house_facilities)
kitchen_shelves = House.check('Kitchen Shelves', house_facilities)
wardrobe = House.check('wardrobe', house_facilities)
prepaid_meter = House.check('Prepaid Meter', house_facilities)
dinning_area = House.check('Dinning Area', house_facilities)
balcony = House.check('Balcony', house_facilities)
air_conditioning = House.check('Air Conditioning', house_facilities)
chandelier = House.check('Chandelier', house_facilities)
steady_electricity = House.check('Steady Electricity', house_facilities)

## creating a dictionary to keep my info
series = [{'house_type':house_type, 'rooms':rooms, 'bathrooms':bathrooms,
 'condition': house_condition, 'furnishing': furnish, 'area' : area, 'dishwasher': dishwasher,
  'prepaid_meter': prepaid_meter, 'dinning_area': dinning_area,
   'air conditioning': air_conditioning, 'chandelier': chandelier,
  'state': location, 'estate':estate}]



## creating a pandas dataframe so my i can visualize it
data = pd.DataFrame(series)

st.write(data.head())


#st.dataframe(House.scaled(data))

classifier = joblib.load('jiji_prediction_model_new.pkl')
predict = classifier.predict(data)

st.write(np.round(np.exp(np.exp(predict))))



