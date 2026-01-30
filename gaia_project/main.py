import streamlit as st
import plotly.express as px
from db import execute_query

st.set_page_config(page_title="Gaia Star Explorer", layout="wide")

st.title("🌌 Исследование данных космического телескопа Gaia")
st.markdown("Этот дашборд визуализирует данные о звездах, полученные из архива Gaia DR3.")
with st.expander("📖 Справочник параметров (что значат графики?)"):
    st.write("""
    * **RA / Dec**: Небесные координаты (аналог долготы и широты).
    * **Distance (pc)**: Расстояние в парсеках. 1 парсек ≈ 3.26 световых года.
    * **Brightness (G-mag)**: Видимая звездная величина. Чем МЕНЬШЕ число, тем ЯРЧЕ звезда.
    * **Temperature (K)**: Температура поверхности в Кельвинах. Солнце ≈ 5778 K.
    """)

try:
    df = execute_query('gaia_project/queries/main_query.sql')
    
    st.sidebar.header("Настройки фильтрации")
    
    max_dist = float(df['distance_pc'].max())
    dist_range = st.sidebar.slider(
        "Расстояние до звезды (парсек)", 
        0.0, max_dist, (0.0, 500.0)
    )
    
    min_bright = float(df['brightness'].min())
    max_bright = float(df['brightness'].max())
    bright_filter = st.sidebar.slider(
        "Яркость (чем меньше число, тем ярче)", 
        min_bright, max_bright, (min_bright, max_bright)
    )

    mask = (df['distance_pc'].between(dist_range[0], dist_range[1])) & \
           (df['brightness'].between(bright_filter[0], bright_filter[1]))
    filtered_df = df[mask]

    st.subheader("📊 Ключевые показатели")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    m_col1.metric("Звезд в выборке", len(filtered_df))
    m_col2.metric("Ср. расстояние", f"{filtered_df['distance_pc'].mean():.1f} пк")
    m_col3.metric("Ср. температура", f"{filtered_df['temperature'].mean():.0f} K")
    
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        # 1. Карта неба
        st.subheader("🔭 Положение звезд на небе (RA/Dec)")
        fig1 = px.scatter(filtered_df, x="ra", y="dec", color="brightness", 
                 hover_data={"source_id": True, "ra": ":.2f", "dec": ":.2f"},
                 title="Карта прямого восхождения и склонения")
        st.plotly_chart(fig1, use_container_width=True)

        # 2. Гистограмма температур
        st.subheader("🌡️ Распределение температур звезд")
        fig2 = px.histogram(filtered_df, x="temperature", nbins=30, 
                           color_discrete_sequence=['orange'], title="Количество звезд по температуре (K)")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # 3. Диаграмма яркость vs расстояние
        st.subheader("📏 Яркость и Расстояние")
        fig3 = px.scatter(filtered_df, x="distance_pc", y="brightness", 
                 hover_data={"source_id": True, "distance_pc": ":.1f", "temperature": ":.0f"},
                 title="Зависимость видимой величины от дистанции")
        st.plotly_chart(fig3, use_container_width=True)

        # 4. График скоростей
        st.subheader("🚀 Лучевые скорости")
        fig4 = px.box(filtered_df, y="radial_velocity", 
                     title="Разброс скоростей движения звезд")
        st.plotly_chart(fig4, use_container_width=True)

    st.info(f"Найдено объектов по вашим критериям: {len(filtered_df)}")

except Exception as e:
    st.error(f"Ошибка при загрузке данных: {e}")
    st.warning("Убедитесь, что вы запустили 'python ddl.py' для создания базы данных.")
