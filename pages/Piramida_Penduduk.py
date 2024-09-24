import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import requests

st.set_page_config(layout='wide')

geojson_data = requests.get(
    "https://raw.githubusercontent.com/firmanh3200/batas-administrasi-indonesia/refs/heads/master/Kab_Kota/kabkot32.json"
).json()

data = pd.read_csv(
    'dukcapil/piramida_penduduk.csv', sep=',',
    dtype={'kode_kabupaten_kota':'str', 'kelompok_umur':'str', 'tahun':'str', 'jumlah_penduduk':'float'}
)

data['KODE_KK'] = data['kode_kabupaten_kota'].astype(str).str.slice(0, 2) + '.' + \
                   data['kode_kabupaten_kota'].astype(str).str.slice(2, 4)

# Pilihan tema warna
warna_options = {
    'Viridis_r': px.colors.sequential.Viridis_r,
    'Viridis': px.colors.sequential.Viridis,
    'Greens': px.colors.sequential.Greens,
    'Inferno': px.colors.sequential.Inferno,
    'Blues': px.colors.sequential.Blues,
    'Reds': px.colors.sequential.Reds,
    'YlGnBu': px.colors.sequential.YlGnBu,
    'YlOrRd': px.colors.sequential.YlOrRd,
    'RdBu': px.colors.diverging.RdBu,
    'Spectral': px.colors.diverging.Spectral
}

jumlahpenduduk = data.groupby(['nama_provinsi', 'nama_kabupaten_kota', 'kelompok_umur', 'tahun'])['jumlah_penduduk'].sum().reset_index()
jumlahpenduduk['tahun'] = jumlahpenduduk['tahun'].astype(str)

st.title("Visualisasi Open Data Kependudukan Jawa Barat")
st.subheader("", divider='rainbow')

with st.container(border=True):
    kolom1, kolom2, kolom3 = st.columns(3)
    datapenduduk = data.sort_values(by=['tahun', 'kelompok_umur'], ascending=[False, True])
    pilihantahun = datapenduduk['tahun'].unique()
    pilihanjenis = datapenduduk['kelompok_umur'].unique()
    
    with kolom1:
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
    
    with kolom2:
        jenisterpilih = st.selectbox("Filter Kelompok Umur", pilihanjenis)
    
    with kolom3:
        pilihwarna = st.selectbox("Pilih Tema Warna:", options=list(warna_options.keys()))
            
if tahunterpilih and jenisterpilih:
    df = datapenduduk[(datapenduduk['tahun'] == tahunterpilih) & (datapenduduk['kelompok_umur'] == jenisterpilih)]
    with st.container(border=True):
        st.subheader(f"Sebaran Penduduk Jawa Barat :blue[Berumur {jenisterpilih} Tahun], :green[Tahun {tahunterpilih}]")

    with st.container(border=True):
        kol1, kol2 = st.columns([2,1])
        with kol1:
            fig2 = px.choropleth_mapbox(
                data_frame=df,
                geojson=geojson_data,
                locations="KODE_KK",
                color="jumlah_penduduk",
                color_continuous_scale=warna_options[pilihwarna],
                opacity=0.7,
                featureidkey="properties.KODE_KK",
                zoom=7,
                center={"lat": -6.914845, "lon": 107.609836},
                mapbox_style="carto-positron",
                hover_name="nama_kabupaten_kota",
                hover_data=['tahun', 'jumlah_penduduk']
            )

            fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig2, use_container_width=True)
        
        with kol2:
            fig3 = px.sunburst(df, 
                       path=['nama_provinsi', 'nama_kabupaten_kota', 'jenis_kelamin'],
                       values='jumlah_penduduk', 
                       color_discrete_sequence=warna_options[pilihwarna])
    
            fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig3.update_traces(textinfo='label+value')
            st.plotly_chart(fig3, use_container_width=True)

    with st.container(border=True):
        kol3, kol4 = st.columns(2)
        with kol3:
            pie_penduduk = px.pie(df, 
                            values='jumlah_penduduk', names='nama_kabupaten_kota', 
                            color_discrete_sequence=warna_options[pilihwarna])
            pie_penduduk.update_layout(showlegend=False,
                                      margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(pie_penduduk, use_container_width=True)
        
        with kol4:
            trimep_penduduk = px.treemap(df, 
                            values='jumlah_penduduk', path=['nama_provinsi', 'nama_kabupaten_kota', 'jenis_kelamin'], 
                            color_discrete_sequence=warna_options[pilihwarna])
            trimep_penduduk.update_layout(showlegend=False,
                                      margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(trimep_penduduk, use_container_width=True)
    
    with st.container(border=True):
        st.subheader(f"Perkembangan Penduduk Jawa Barat :blue[Berumur {jenisterpilih}] menurut Kabupaten/Kota")
        kol5, kol6 = st.columns(2)
        with kol5:
            perkembangan = px.line(jumlahpenduduk[jumlahpenduduk['kelompok_umur'] == jenisterpilih], x='tahun', y='jumlah_penduduk', line_shape='spline',
                                color='nama_kabupaten_kota')
            st.plotly_chart(perkembangan, use_container_width=True)
        
        with kol6:
            sketer = px.scatter(jumlahpenduduk[jumlahpenduduk['kelompok_umur'] == jenisterpilih],
                                x='tahun', y='jumlah_penduduk',
                                size='jumlah_penduduk',
                                color='nama_kabupaten_kota')    
            st.plotly_chart(sketer, use_container_width=True)
    
        

st.subheader("", divider='rainbow')

kol1, kol2, kol3, kol4, kol5 = st.columns(5)
with kol1:
    st.link_button("Sumber Data", url="https://opendata.jabarprov.go.id/id/dataset/jumlah-penduduk-berdasarkan-kelompok-umur-dan-kabupatenkota-di-jawa-barat")
with kol2:
    st.link_button("Sumber Peta Dasar", url="https://github.com/Alf-Anas/batas-administrasi-indonesia") 
with kol3:
    st.link_button("Inspirasi Grafik", url="https://plotly.com/python")
with kol4:
    st.link_button("Framework", url="https://streamlit.io")
with kol5:
    st.link_button("Pengolah Data", url="https://pandas.pydata.org/")
st.subheader("", divider='rainbow')
