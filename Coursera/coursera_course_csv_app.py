import streamlit as st
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

from random import randint
from time import sleep
from PIL import Image

col1, col2, col3 = st.columns(3)
with col2:
    logo = Image.open("coursera-logo.png")
    st.image(logo, caption="")  # , width=500
col3.write("   ")

st.write("\n\n")

html_temp = """
<div style="background-color:#043471;padding:1.5px">
<h1 style="color:white;text-align:center;">COURSERA COURSE LIST BY CATEGORY</h1>
</div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)


st.write("\n\n"*3)

st.sidebar.subheader('COURSE CATEGORIES')
st.sidebar.write("Select a category and wait for a few seconds. When csv file has ready you can see download button")


category = st.sidebar.radio("Course Category", ("Data Science", "Business", "Computer Science", "Information Technology", "Language Learning", "Health", "Personal Development", "Physical Science and Engineering", "Social Sciences", "Arts and Humanities", "Math and Logic"))

def home(request):
    return HttpResponse('''
        <strong><p>Warning! Please wait a few seconds after clicking. When scraping is finished, you can download CSV file</strong>
        <ul>
            <li><a href='/data-science'>Data Science</a></li>
            <li><a href='/business'>Business</a></li>
            <li><a href='/computer-science'>Computer Science</a></li>
            <li><a href='/information-technology'>Information Technology</a></li>
            <li><a href='/language-learning'>Language Learning</a></li>
            <li><a href='/health'>Health</a></li>
            <li><a href='/personal-development'>Personal Development</a></li>
            <li><a href='/physical-science-and-engineering'>Physical Science and Engineering</a></li>
            <li><a href='/social-sciences'>Social Sciences</a></li>
            <li><a href='/arts-and-humanities'>Arts and Humanities</a></li>
            <li><a href='/math-and-logic'>Math and Logic</a></li>
        </ul>
    ''')

def get_data_from_url(target_url):
    response_data = requests.get(target_url)
    return BeautifulSoup(response_data.text, 'html.parser')

def get_data(request, category):
# Get data from /browse + category
    course_soup = get_data_from_url('https://www.coursera.org/browse/' + category)
    
    for url in course_soup.find_all('a', attrs={'class':'CardText-link'}):
        # To select courses, find urls starts with "learn"
        if url['href'].startswith('/learn'):
            # In Courses:
            course_data = get_data_from_url('https://www.coursera.org' + url['href'])
            
            # Scrap required data from courses
            CourseName = course_data.find('h1', attrs={'class':'banner-title banner-title-without--subtitle m-b-0'}).text
            CourseProvider = course_data.find('h3', attrs={'class':'headline-4-text bold rc-Partner__title'}).text
            # Sleep a random number of seconds (between 5 and 8)
            sleep(randint(5, 8))
            CourseDescription = course_data.find('div', attrs={'class':'content-inner'}).find('p').text
            StudentsEnrolled = course_data.find('div', attrs={'class':'_1fpiay2'}).find('span').text
            Ratings = course_data.find('span', attrs={'data-test':'number-star-rating'}).text

            CourseList, ProviderList, DescriptionList, EnrolledList, RatingsList = [],[],[],[],[]

            for i,j,k,l,m in zip(CourseName, CourseProvider, CourseDescription, StudentsEnrolled, Ratings):
                CourseList.append(i)
                ProviderList.append(j)
                DescriptionList.append(k)
                EnrolledList.append(l)
                RatingsList.append(m)

            courses = pd.DataFrame({
                'Course Name': CourseList,
                'Course Provider': ProviderList,
                'Course Description': DescriptionList,
                'Students Enrolled': EnrolledList,
                'Ratings': RatingsList
            })

            #courses.to_csv((category + ".csv"), encoding='LATIN-1', index=False)
    
    return courses





if st.button("Extract"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        home(request)
        get_data_from_url(target_url)
        get_data(request, category)
    with col3:
        with st.spinner('Wait for it please...'):
            time.sleep(7)
    
    st.write("\n")

    st.table(courses)

    st.write("\n")

    col6, col7, col8 = st.columns(3)
    col6.success(f' {category} csv file is ready to download')
    col7.download_button('Download CSV', courses, f'{category}.csv', 'text/csv')

st.write("\n\n")


