import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import requests

st.set_page_config(layout='wide')

data = pd.read_csv(
    'dukcapil/piramida_penduduk.csv', sep=',',
    dtype={'kode_kabupaten_kota':'str', 'kelompok_umur':'str', 'tahun':'str', 'jumlah_penduduk':'float'}
)

data['kelompok_umur'] = data['kelompok_umur'].str.strip()

# Pilihan tema warna
warna1 = {
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 
    'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 
    'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 
    'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 
    'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 
    'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 
    'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 
    'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 
    'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 
    'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 
    'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 
    'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 
    'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 
    'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 
}
warna2 = {
    'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 
    'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 
    'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 
    'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 
    'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 
    'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 
    'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 
    'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 
    'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 
    'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 
    'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 
    'whitesmoke', 'yellow', 'yellowgreen'
}

penduduk_jabar = data.groupby(['nama_provinsi', 'jenis_kelamin', 'kelompok_umur', 'tahun'])['jumlah_penduduk'].sum().reset_index()
penduduk_jabar = penduduk_jabar.sort_values(by=['tahun', 'kelompok_umur'], ascending=[False, True])

pivot_jabar = penduduk_jabar.pivot_table(
    values='jumlah_penduduk', 
    index=['tahun', 'kelompok_umur'], 
    columns='jenis_kelamin'
).reset_index().sort_values(by=['tahun', 'kelompok_umur'])


pivot_kabkot = data.pivot_table(
    values='jumlah_penduduk', 
    index=['tahun', 'kelompok_umur', 'nama_kabupaten_kota'], 
    columns='jenis_kelamin'
).reset_index().sort_values(by=['tahun', 'kelompok_umur'])

st.title("Visualisasi Open Data Kependudukan Jawa Barat")
st.subheader("", divider='rainbow')

with st.container(border=True):
    kolom1, kolom2, kolom3 = st.columns(3)
    pilihantahun = pivot_jabar['tahun'].unique()
    
    with kolom1:
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
    
    with kolom2:
        pilihwarna1 = st.selectbox("Pilih Tema Warna1:", options=list(warna1), key='warna1')
    
    with kolom3:
        pilihwarna2 = st.selectbox("Pilih Tema Warna2:", options=list(warna2), key='warna2')
            
if tahunterpilih:
    kol1, kol2 = st.columns(2)
    
    with kol1:
        df = pivot_jabar[(pivot_jabar['tahun'] == tahunterpilih)]
        df['LAKI-LAKI'] = pd.to_numeric(df['LAKI-LAKI'], errors='coerce')
        df['LAKI-LAKI'] = df['LAKI-LAKI'] * -1
        df['PEREMPUAN'] = pd.to_numeric(df['PEREMPUAN'], errors='coerce')
        df['kelompok_umur'] = df['kelompok_umur'].astype(object)
        
        with st.container(border=True):
            piramida_jabar = px.bar(df, x=['LAKI-LAKI', 'PEREMPUAN'], 
                                    y='kelompok_umur', labels={'variable':''},
                                orientation='h', 
                                color_discrete_map={'LAKI-LAKI':pilihwarna1, 'PEREMPUAN':pilihwarna2})
            
            # Menempatkan legenda di bawah tengah
            piramida_jabar.update_layout(
                xaxis_title="",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.subheader(f"Piramida Penduduk Jawa Barat :green[Tahun {tahunterpilih}]")
            st.plotly_chart(piramida_jabar, use_container_width=True)
    
    with kol2:
        with st.container(border=True):
            pilihankab = pivot_kabkot['nama_kabupaten_kota'].unique()
            kabterpilih = st.selectbox("Filter Kabupaten/Kota", pilihankab)
            
            df1 = pivot_kabkot[(pivot_kabkot['tahun'] == tahunterpilih) & (pivot_kabkot['nama_kabupaten_kota'] == kabterpilih)]
            df1['LAKI-LAKI'] = df1['LAKI-LAKI'] * -1
        
            piramida_kabkot = px.bar(df1, x=['LAKI-LAKI', 'PEREMPUAN'], 
                                    y='kelompok_umur', labels={'variable':''},
                                orientation='h', 
                                color_discrete_map={'LAKI-LAKI':pilihwarna1, 'PEREMPUAN':pilihwarna2})
            
            # Menempatkan legenda di bawah tengah
            piramida_kabkot.update_layout(
                xaxis_title="",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.subheader(f"Piramida Penduduk :blue[{kabterpilih}], :green[Tahun {tahunterpilih}]")
            st.plotly_chart(piramida_kabkot, use_container_width=True)
    
st.subheader("", divider='rainbow')
baris1, baris2 = st.columns(2)
with baris1:
    with st.container(border=True):
        pivot_jabar['LAKI-LAKI'] = pivot_jabar['LAKI-LAKI'] * -1
        
        animasi_jabar = px.bar(pivot_jabar, x=['LAKI-LAKI', 'PEREMPUAN'], 
                                        y='kelompok_umur', labels={'variable':''},
                                    orientation='h',
                                    animation_frame='tahun', 
                                    color_discrete_map={'LAKI-LAKI':pilihwarna1, 'PEREMPUAN':pilihwarna2})
                
        # Menempatkan legenda di bawah tengah
        animasi_jabar.update_layout(
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.subheader(f"Animasi Piramida Penduduk Jawa Barat")
        st.plotly_chart(animasi_jabar, use_container_width=True)

with baris2:
    with st.container(border=True):
        df2 = pivot_kabkot[(pivot_kabkot['nama_kabupaten_kota'] == kabterpilih)]
        df2['LAKI-LAKI'] = df2['LAKI-LAKI'] * -1
    
        animasi_kabkot = px.bar(df2, x=['LAKI-LAKI', 'PEREMPUAN'], 
                                y='kelompok_umur', labels={'variable':''},
                            orientation='h',
                            animation_frame='tahun', 
                            color_discrete_map={'LAKI-LAKI':pilihwarna1, 'PEREMPUAN':pilihwarna2})
        
        # Menempatkan legenda di bawah tengah
        animasi_kabkot.update_layout(
            xaxis_title="",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.subheader(f"Animasi Piramida Penduduk :blue[{kabterpilih}]")
        st.plotly_chart(animasi_kabkot, use_container_width=True)
                

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
