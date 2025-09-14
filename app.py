import streamlit as st
from pypdf import PdfReader, PdfWriter
from copy import deepcopy
import io

st.set_page_config(page_title="PDF Splitter", page_icon="✂️")

st.title("✂️ Разрезать PDF пополам")
st.write("Загрузи PDF, и каждая страница будет разделена на **правую и левую половину** в одинарном порядке.")

uploaded_file = st.file_uploader("📂 Загрузите PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # правая половина
        right_page = deepcopy(page)
        right_page.mediabox.lower_left = (width / 2, 0)
        right_page.mediabox.upper_right = (width, height)
        writer.add_page(right_page)

        # левая половина
        left_page = deepcopy(page)
        left_page.mediabox.lower_left = (0, 0)
        left_page.mediabox.upper_right = (width / 2, height)
        writer.add_page(left_page)

    # сохраняем в память
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    st.success("✅ PDF успешно обработан!")
    st.download_button(
        "📥 Скачать готовый PDF",
        data=output,
        file_name="split.pdf",
        mime="application/pdf"
    )
