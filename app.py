# app.py
import streamlit as st
from underthesea import word_tokenize, pos_tag
import pandas as pd
import base64

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Demo POS Tagging Tiếng Việt",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================
st.title("🧠 Demo POS Tagging Tiếng Việt với Streamlit")
st.write(
    "Nhập một câu tiếng Việt, ứng dụng sẽ tách từ và gán nhãn từ loại."
)

# =========================================================
# INPUT
# =========================================================
text = st.text_area(
    "✍️ Nhập câu tiếng Việt ở đây:",
    "Hệ thống phân loại bình luận tiếng Việt rất chính xác.",
    height=120
)

analyze_clicked = st.button(
    "🔍 Phân tích",
    type="primary",
    use_container_width=True
)

col1, col2 = st.columns(2)

# =========================================================
# POS TAG EXPLANATION
# =========================================================
POS_TAGS_EXPLANATION = {
    "N": "Danh từ",
    "Np": "Danh từ riêng",
    "Nc": "Danh từ chỉ loại",
    "Nu": "Danh từ đơn vị",
    "V": "Động từ",
    "A": "Tính từ",
    "P": "Đại từ",
    "R": "Phó từ",
    "L": "Định từ",
    "M": "Số từ",
    "E": "Giới từ",
    "C": "Liên từ",
    "I": "Thán từ",
    "T": "Trợ từ / Tiểu từ",
    "B": "Từ gốc Hán-Việt",
    "Y": "Từ viết tắt",
    "S": "Từ ngoại lai",
    "X": "Từ không phân loại",
    "CH": "Dấu câu",
}

# =========================================================
# COLORS FOR POS TAGS
# =========================================================
POS_COLORS = {
    "N": "#FF6B6B",
    "Np": "#FF4444",
    "Nc": "#FF8888",
    "Nu": "#FFAAAA",
    "V": "#4ECDC4",
    "A": "#FFE66D",
    "P": "#A8E6CF",
    "R": "#95E1D3",
    "L": "#DDA0DD",
    "M": "#87CEEB",
    "E": "#FFA07A",
    "C": "#98D8C8",
    "I": "#F7DC6F",
    "T": "#BB8FCE",
    "B": "#F0B27A",
    "Y": "#AED6F1",
    "S": "#F5B7B1",
    "X": "#D5DBDB",
    "CH": "#BDC3C7",
}

# =========================================================
# SESSION STATE
# =========================================================
if analyze_clicked:

    # =========================================
    # HANDLE EMPTY INPUT
    # =========================================
    if not text.strip():
        st.error("⚠️ Vui lòng nhập nội dung!")
        st.session_state.pop("pos_result", None)

    else:
        try:
            # =========================================
            # TOKENIZE
            # =========================================
            tokens = word_tokenize(text)

            # =========================================
            # POS TAGGING
            # =========================================
            pos_result = pos_tag(text)

            # =========================================
            # SAVE SESSION
            # =========================================
            st.session_state["pos_text"] = text
            st.session_state["pos_tokens"] = tokens
            st.session_state["pos_result"] = pos_result

        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra: {e}")

# =========================================================
# DISPLAY RESULT
# =========================================================
if "pos_result" in st.session_state:

    pos_result = st.session_state["pos_result"]
    tokens = st.session_state["pos_tokens"]

    # =====================================================
    # COLUMN 1 - TOKENIZE
    # =====================================================
    with col1:

        st.subheader("✂️ Kết quả tách từ")

        st.write("### Danh sách token")

        token_df = pd.DataFrame({
            "STT": range(1, len(tokens) + 1),
            "Token": tokens
        })

        st.dataframe(
            token_df,
            use_container_width=True,
            hide_index=True
        )

        st.write("### Chuỗi sau khi tokenize")

        token_html = ""

        for token in tokens:
            token_html += f"""
            <span style="
                background-color:#f1f3f6;
                padding:8px 12px;
                margin:5px;
                border-radius:10px;
                display:inline-block;
                font-weight:600;
            ">
                {token}
            </span>
            """

        st.markdown(token_html, unsafe_allow_html=True)

    # =====================================================
    # COLUMN 2 - POS TAGGING
    # =====================================================
    with col2:

        st.subheader("🏷️ Kết quả POS Tagging")

        pos_data = []

        for word, tag in pos_result:

            meaning = POS_TAGS_EXPLANATION.get(
                tag,
                "Không xác định"
            )

            pos_data.append({
                "Từ": word,
                "POS": tag,
                "Ý nghĩa": meaning
            })

        pos_df = pd.DataFrame(pos_data)

        st.dataframe(
            pos_df,
            use_container_width=True,
            hide_index=True
        )

        # =============================================
        # HIGHLIGHT COLOR
        # =============================================
        st.write("### Highlight từ loại")

        highlight_html = ""

        for word, tag in pos_result:

            color = POS_COLORS.get(tag, "#D5DBDB")

            highlight_html += f"""
            <span style="
                background-color:{color};
                color:black;
                padding:8px 12px;
                margin:5px;
                border-radius:12px;
                display:inline-block;
                font-weight:bold;
                box-shadow:1px 1px 3px rgba(0,0,0,0.2);
            ">
                {word}
                <small style="margin-left:5px;">
                    ({tag})
                </small>
            </span>
            """

        st.markdown(highlight_html, unsafe_allow_html=True)

    # =====================================================
    # EXPORT CSV
    # =====================================================
    st.divider()

    st.subheader("⬇️ Export kết quả")

    csv = pos_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 Tải file CSV",
        data=csv,
        file_name="pos_tagging_result.csv",
        mime="text/csv",
        use_container_width=True
    )

    # =====================================================
    # POS TAG EXPLANATION TABLE
    # =====================================================
    st.divider()

    st.subheader("📚 Bảng giải thích nhãn từ loại")

    explain_df = pd.DataFrame(
        list(POS_TAGS_EXPLANATION.items()),
        columns=["POS Tag", "Ý nghĩa"]
    )

    st.dataframe(
        explain_df,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "Ứng dụng sử dụng thư viện Underthesea để xử lý NLP tiếng Việt."
)