import pandas as pd
import streamlit as st
import plotly.express as px

from dataPrepFunctions import data_prep_functions
from clusteringFunctions import clustering_functions
from introductionFunctions import introduction_functions
from yieldFunctions import yield_functions

data_prep = data_prep_functions()
introduction = introduction_functions()
clustering = clustering_functions()
yield_ = yield_functions()

data = pd.read_csv("dataset/Product Information - 2023-06-25.csv")
(data_lmt, data_ulmt, data_apps), (scaled_data_lmt, scaled_data_ulmt, scaled_data_apps) = data_prep.prepare_data(data)

scaled_data_lmt = data_prep.PCA_decomposition(scaled_data_lmt, 2)
scaled_data_ulmt = data_prep.PCA_decomposition(scaled_data_ulmt, 2)
scaled_data_apps = data_prep.PCA_decomposition(scaled_data_apps, 2)

data_with_clusters, data_lmt, data_ulmt, data_apps, center_lmt, center_ulmt, center_apps = clustering.create_clusters(data_lmt, data_ulmt, data_apps, scaled_data_lmt, scaled_data_ulmt, scaled_data_apps)


convert = {
        'High Main (1)':1,
        'Medium Main (2)':2,
        'Low Main (3)':3,
        'Low Unlimited (4)':4,
        'High Unlimited (5)':5,
        '80:20 High Main and App (6)':6,
        '50:50 Low Main and App (7)':7,
        '20:80 Medium Main and App (8)':8
}

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="XL's Data Product Market Position", page_icon=":reminder_ribbon:", layout="wide")
tab1, tab2, tab3, tab4 = st.tabs(['Introduction', 'Clustering Analysis', 'Yield Analysis', 'Appendixes'])

with tab1:
    with st.container():
        st.markdown("<h1 style='text-align: center; color: black;'>Analyzing Product Data From Every Operators</h1>", unsafe_allow_html=True)

    with st.container():
        st.write('---')
        fup_quota_product = introduction.visualize_product_type(data_with_clusters)
        st.plotly_chart(fup_quota_product, use_container_width = True)

    with st.container():
        st.write('---')
        mean_operators_product_price = introduction.visualize_mean_operators_product_price(data_with_clusters)
        st.plotly_chart(mean_operators_product_price, use_container_width = True)

with tab2:
    with st.container():
        obj, kpi = st.columns((3, 1), gap='small')
        with obj:
            st.header("Objective")
            st.subheader(
                """
                Understanding XL's Data Products Compared to Other Operators in the National's Data Product Market
                """
            )
        with kpi :
            st.header("KPIs")
            st.subheader("Clusters & Yields")

    with st.container():
        st.write('---')
        limited_quota_vis, unlimited_quota_vis, internet_apps_quota_vis = clustering.visualize_clusters(center_lmt, center_ulmt, center_apps)
        st.plotly_chart(limited_quota_vis, use_container_width = True)
        st.plotly_chart(unlimited_quota_vis, use_container_width = True)
        st.plotly_chart(internet_apps_quota_vis, use_container_width = True)

    with st.container():
        st.write('---')
        count_each_clusters_vis = clustering.visualize_count_each_clusters(data_with_clusters)
        st.plotly_chart(count_each_clusters_vis, use_container_width = True)

    with st.container():
        cluster_proportions = clustering.visualize_clusters_proportions(data_with_clusters)
        st.write('---')
        st.plotly_chart(cluster_proportions, use_container_width = True)

    with st.container():
        st.write('---')
        cluster_label = st.selectbox('Select a Cluster', convert.keys())
        st.subheader("Quota and Price Comparison between Operators in each Cluster")
        cluster = convert[cluster_label]
        left_col, _, right_col = st.columns((10, 1, 10), gap='small')
        quota_vis, harga_vis = clustering.visualize_cluster_char_in_operator(data_with_clusters, cluster)
        with left_col:
            st.plotly_chart(quota_vis, use_container_width = True)
        with right_col:
            st.plotly_chart(harga_vis, use_container_width = True)

with tab3:
    with st.container():
        obj, kpi = st.columns((3, 1), gap='small')
        with obj:
            st.header("Objective")
            st.subheader(
                """
                Understanding XL's Data Products Compared to Other Operators in the National's Data Product Market
                """
            )
        with kpi :
            st.header("KPIs")
            st.subheader("Clusters & Yields")
    with st.container():
        st.write('---')
        operators_yield_type1 = yield_._visualize_operators_yield(data_with_clusters, 'apps')
        operators_yield_type2 = yield_._visualize_operators_yield(data_with_clusters, 'non_apps')
        st.plotly_chart(operators_yield_type1, use_container_width = True)
        st.plotly_chart(operators_yield_type2, use_container_width = True)
        
    with st.container():
        st.write('---')
        operators_yield_type1 = yield_._visualize_all_cluster_yield(data_with_clusters, 'apps')
        operators_yield_type2 = yield_._visualize_all_cluster_yield(data_with_clusters, 'non_apps')
        st.plotly_chart(operators_yield_type1, use_container_width = True)
        st.plotly_chart(operators_yield_type2, use_container_width = True)

    with st.container():
        st.write('---')
        cluster_label = st.selectbox('Pick a Cluster', convert.keys())
        cluster = convert[cluster_label]
        # no_outliers_data_with_clusters = data_prep.clean_outliers(data_with_clusters)
        # data_with_clusters_yield = yield_._non_apps_yield_data(no_outliers_data_with_clusters)
        cluster_yield_type1 = yield_._visualize_cluster_yield(data_with_clusters, cluster, 'apps', cluster_label)
        cluster_yield_type2 = yield_._visualize_cluster_yield(data_with_clusters, cluster, 'non-apps', cluster_label)
        st.plotly_chart(cluster_yield_type1, use_container_width = True)
        st.plotly_chart(cluster_yield_type2, use_container_width = True)

with tab4:
    with st.container():
        score_lmt = clustering.calculate_fpc(scaled_data_lmt, 1.3)
        score_lmt = clustering.set_figure(score_lmt, 'Main Quota Product FPC C-Means Clusters Score')
        score_ulmt = clustering.calculate_fpc(scaled_data_ulmt, 1.3)
        score_ulmt = clustering.set_figure(score_ulmt, 'Unlimited Quota Product FPC C-Means  Clusters Score')
        score_app = clustering.calculate_fpc(scaled_data_apps, 1.1)
        score_app = clustering.set_figure(score_app, 'Main and App Quota Product FPC C-Means Clusters Score')
        st.plotly_chart(score_lmt)
        st.plotly_chart(score_ulmt)
        st.plotly_chart(score_app)

    with st.container():
        st.write('---')
        store_data = [data_lmt, data_ulmt, data_apps]
        store_x = ['Kuota Utama (GB)', 'Fair Usage Policy (GB)', 'Kuota Utama (GB)']
        store_size = ['Masa Berlaku (Hari)', 'Masa Berlaku (Hari)', 'Kuota Aplikasi (GB)']
        store_color = [None, None, 'Kuota Aplikasi (GB)']
        store_title = ['Visualize Each Main Quota Product', 'Visualize Each Unlimited Quota Product', 'Visualize Each Main and App Quota Product']
        for data, x, color, size, title in zip(store_data, store_x, store_color, store_size, store_title):
            data['Cluster'] = data['Cluster'].astype('string')
            vis = px.scatter(
                data,
                x=x,
                y='Harga',
                size=size,
                color='Cluster',
            )
            vis = clustering.set_figure(vis, title)
            st.plotly_chart(vis)
        
        data_apps['Cluster'] = data_apps['Cluster'].astype('string')
        vis = px.scatter(
                data_apps,
                x='Kuota Utama (GB)',
                y='Kuota Aplikasi (GB)',
                size='Masa Berlaku (Hari)',
                color='Cluster'
            )
        vis = clustering.set_figure(vis, 'Visualize Each Main and App Quota Product')
        st.plotly_chart(vis)