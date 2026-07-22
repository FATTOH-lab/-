import streamlit as st

# Добавляем стили оформления
st.markdown(
    """
    <style>
    /* Главный задний фон приложения */
    .stApp {
        background: linear-gradient(135deg, #fffefb 0%, #fdf6ed 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Стилизация верхнего заголовка */
    h1 {
        color: #d32f2f;
        text-align: center;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* Карточки рецептов */
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #ffe0b2;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }

    /* Красивые яркие кнопки */
    .stButton>button {
        background: linear-gradient(90deg, #ff5722 0%, #f44336 100%);
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(244, 67, 54, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(244, 67, 54, 0.4);
    }

    /* Баннер ИИ Шеф-повара */
    .stAlert {
        border-radius: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)