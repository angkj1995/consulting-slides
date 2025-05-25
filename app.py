import streamlit as st
import pandas as pd
import os
from PIL import Image
import ast
from collections import Counter

#### 0. Data and other things ####
st.set_page_config(layout='wide')

df = pd.read_csv('slidestart.csv')
# Convert the string representation of lists in 'tags' column to actual lists
if 'tags' in df.columns:
    df['tags'] = df['tags'].apply(ast.literal_eval)
# Convert image_id into ref urls
df['image_id'] = ['https://raw.githubusercontent.com/angkj1995/consulting-slides/refs/heads/main/New%20folder/' + x for x in df['image_id'].tolist()]

# Initialize session state for gallery display confirmation
if 'display_gallery_confirmed' not in st.session_state:
    st.session_state.display_gallery_confirmed = False
if 'last_filtered_df_hash' not in st.session_state:
    st.session_state.last_filtered_df_hash = None





#### 1. Filter the dataframe ####
st.subheader('Filters')
filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

with filter_col1:
    # Inject CSS to change selectbox text size
    st.markdown("""
        <style>
        div[data-baseweb="select"] * {
            font-size: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Selection box
    company_list = list(set(df['company'].tolist()))
    company_list.sort()
    company_option = st.selectbox(
        "Company",
        company_list,
        index=None,
        placeholder="Choose a company"
    )

with filter_col2:
    # Inject CSS to change selectbox text size
    st.markdown("""
        <style>
        div[data-baseweb="select"] * {
            font-size: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Selection box
    slide_type_list = list(set(df['slide_type'].tolist()))
    slide_type_list.sort()
    slide_type_option = st.selectbox(
        "Slide type",
        slide_type_list,
        index=None,
        placeholder="Choose a slide type"
    )

with filter_col3:
    # Inject CSS to change selectbox text size
    st.markdown("""
        <style>
        div[data-baseweb="select"] * {
            font-size: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Selection box
    industry_list = list(set(df['industry'].tolist()))
    industry_list.sort()
    industry_option = st.selectbox(
        "Industry",
        industry_list,
        index=None,
        placeholder="Choose an industry"
    )

with filter_col4:
    # Inject CSS to change selectbox text size
    st.markdown("""
        <style>
        div[data-baseweb="select"] * {
            font-size: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Selection box
    use_case_list = list(set(df['use_case'].tolist()))
    use_case_list.sort()
    use_case_option = st.selectbox(
        "Use case",
        use_case_list,
        index=None,
        placeholder="Choose a use case"
    )

with filter_col5:
    # Inject CSS to change selectbox text size
    st.markdown("""
        <style>
        div[data-baseweb="select"] * {
            font-size: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Selection box
    all_tags = set()
    for tag_list in df['tags']:
        all_tags.update(tag_list)
    tag_list = sorted(list(all_tags))
    tag_option = st.selectbox(
        "Tag",
        tag_list,
        index=None,
        placeholder="Choose a tag"
    )

# Apply filters
filters = {
    'company': company_option,
    'slide_type': slide_type_option,
    'industry': industry_option,
    'use_case': use_case_option
}

# Make a copy
filtered_df = df.copy()

# Special filter for tags (do first)
if tag_option is not None:
    filtered_df = filtered_df[filtered_df['tags'].apply(lambda x: tag_option in x if isinstance(x, list) else False)]

# Begin filtering. If empty, it's ok
for col, val in filters.items():
    if val is not None:
        filtered_df = filtered_df[filtered_df[col] == val]






#### 2. Dynamic Summary Statistics ####
st.subheader("Summary Statistics")
st.markdown(f"<p style='color: #DC267F;'>Total slides: {filtered_df.shape[0]}</p>", unsafe_allow_html=True)
summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = st.columns(5)

with summary_col1:
    st.markdown("<p style='font-size:14px; font-weight: bold;'>Company Counts</p>", unsafe_allow_html=True)
    company_counts = filtered_df['company'].value_counts().reset_index()
    company_counts.columns = ['Company', 'Count']
    styled_company_counts = company_counts.style.set_table_attributes('style="font-size:12px"').hide(axis='index')
    st.markdown(styled_company_counts.to_html(escape=False), unsafe_allow_html=True)

with summary_col2:
    st.markdown("<p style='font-size:14px; font-weight: bold;'>Slide Type Counts</p>", unsafe_allow_html=True)
    slide_type_counts = filtered_df['slide_type'].value_counts().reset_index()
    slide_type_counts.columns = ['Slide Type', 'Count']
    styled_slide_type_counts = slide_type_counts.style.set_table_attributes('style="font-size:12px"').hide(axis='index')
    st.markdown(styled_slide_type_counts.to_html(escape=False), unsafe_allow_html=True)

with summary_col3:
    st.markdown("<p style='font-size:14px; font-weight: bold;'>Industry Counts</p>", unsafe_allow_html=True)
    industry_counts = filtered_df['industry'].value_counts().reset_index()
    industry_counts.columns = ['Industry', 'Count']
    styled_industry_counts = industry_counts.style.set_table_attributes('style="font-size:12px"').hide(axis='index')
    st.markdown(styled_industry_counts.to_html(escape=False), unsafe_allow_html=True)

with summary_col4:
    st.markdown("<p style='font-size:14px; font-weight: bold;'>Use Case Counts</p>", unsafe_allow_html=True)
    use_case_counts = filtered_df['use_case'].value_counts().reset_index()
    use_case_counts.columns = ['Use Case', 'Count']
    styled_use_case_counts = use_case_counts.style.set_table_attributes('style="font-size:12px"').hide(axis='index')
    st.markdown(styled_use_case_counts.to_html(escape=False), unsafe_allow_html=True)

with summary_col5:
    st.markdown("<p style='font-size:14px; font-weight: bold;'>Tag Counts</p>", unsafe_allow_html=True)
    # Tag collector
    all_tags_in_filtered_df = []
    for tag_list in filtered_df['tags']:
        if isinstance(tag_list, list):
            all_tags_in_filtered_df.extend(tag_list)

    # Tag counter
    tag_counts = Counter(all_tags_in_filtered_df)
    tag_counts_df = pd.DataFrame(tag_counts.items(), columns=['Tag', 'Count'])
    tag_counts_df = tag_counts_df.sort_values(by='Count', ascending=False).reset_index(drop=True)

    styled_tag_counts = tag_counts_df.style.set_table_attributes('style="font-size:12px"').hide(axis='index')
    st.markdown(styled_tag_counts.to_html(escape=False), unsafe_allow_html=True)





#### 3. Slide Gallery ####
st.subheader('Slide Gallery')

current_row_count = filtered_df.shape[0]
current_df_hash = hash(frozenset(filtered_df.index)) # A simple hash of the index for change detection

# Check if the filtered DataFrame has changed since last display/button press
if st.session_state.last_filtered_df_hash != current_df_hash:
    st.session_state.display_gallery_confirmed = False # Reset confirmation if data changed
    st.session_state.last_filtered_df_hash = current_df_hash

if current_row_count > 300:
    if not st.session_state.display_gallery_confirmed:
        st.warning(f"Displaying {current_row_count} slides may cause the application to lag.")
        if st.button("Continue displaying gallery"):
            st.session_state.display_gallery_confirmed = True
            st.rerun() # the script is halted - no more statements will be run, and the script will be queued to re-run from the top
    else:
        # If confirmed, display the dataframe
        if not filtered_df.empty:
            st.dataframe(filtered_df.iloc[:,[8,0,1,2,3,4,5,6]],
                        column_config={
                            'company': st.column_config.TextColumn('company', width='small'),
                            'details': st.column_config.TextColumn('details', width='medium'),
                            'description': st.column_config.TextColumn('description', width='medium'),
                            'use_case': st.column_config.TextColumn('use_case', width=137),
                            'image_id': st.column_config.ImageColumn('image_id', width='small')
                        },
                        hide_index=True, row_height=60)
        else:
            st.info("No matching data based on the selected filters.")
else:
    # If row count is <= 300, always display and set confirmed to True
    st.session_state.display_gallery_confirmed = True
    if not filtered_df.empty:
        st.dataframe(filtered_df.iloc[:,[8,0,1,2,3,4,5,6]],
                     column_config={
                         'company': st.column_config.TextColumn('company', width='small'),
                         'details': st.column_config.TextColumn('details', width='medium'),
                         'description': st.column_config.TextColumn('description', width='medium'),
                         'use_case': st.column_config.TextColumn('use_case', width=137),
                         'image_id': st.column_config.ImageColumn('image_id', width='small')
                     },
                     hide_index=True, row_height=60)
    else:
        st.info("No matching data based on the selected filters.")
