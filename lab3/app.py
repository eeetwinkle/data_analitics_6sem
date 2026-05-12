import streamlit as st
import pandas as pd
from agent import run_agent
from injection import sanitize

st.set_page_config(page_title="Agent", layout="wide")
st.title("🤖 Аналитический агент")

up = st.file_uploader("Загрузите CSV или Excel", type=["csv", "xlsx", "xls"])
if up:
    if up.name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(up)
    else:
        try:
            df = pd.read_csv(up, encoding="utf-8")
        except:
            df = pd.read_csv(up, encoding="cp1251")
    st.success(f"{df.shape[0]} строк, {df.shape[1]} колонок")
    st.dataframe(df.head())
    inst = st.text_area("Дополнительная инструкция (необязательно)")
    clean, susp = sanitize(inst)
    if st.button("Запустить анализ"):
        if susp:
            st.warning("Подозрительная инструкция – игнорирую.")
        with st.spinner("Агент работает..."):
            report, imgs = run_agent(clean, df, susp)
        st.markdown("## Отчёт")
        st.markdown(report)
        if imgs:
            st.markdown("## Графики")
            seen = set()
            unique = []
            for img in imgs:
                if img not in seen:
                    seen.add(img)
                    unique.append(img)
            for i, b64 in enumerate(unique[:4]):
                st.image(f"data:image/png;base64,{b64}", caption=f"График {i+1}")
        else:
            st.info("Графики не были созданы.")