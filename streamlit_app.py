# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import column
import requests  

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie!"""
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on the Smoothie will be: ", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(column('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect(
    "Choose upto 5 Ingredents;"
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        st.subheader(f"{fruit_chosen} Nutritional Information")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}",verify=False)  
        st.dataframe(data=smoothiefroot_response.json(),width='stretch')
    st.write(ingredients_string)
    my_insert_stmt = """insert into smoothies.public.orders (ingredients, name_on_order)
    values ('""" + ingredients_string.strip() + """', '""" + name_on_order + """')"""
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert and ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

