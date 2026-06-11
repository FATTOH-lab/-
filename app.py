import json
from pathlib import Path
import streamlit as st
from google import genai
from google.genai import types

# --- ИНИЦИАЛИЗАЦИЯ ЭКРАНОВ ПРИЛОЖЕНИЯ ---
if "step" not in st.session_state:
    st.session_state.step = "welcome_lang"  # Начинаем с первого экрана
if "lang" not in st.session_state:
    st.session_state.lang = "ru"
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

st.set_page_config(page_title="Chef AI", page_icon="🍳", layout="wide")

BASE_DIR = Path(__file__).parent
RECIPES_FILE = BASE_DIR / "recipes.json"

# --- КРАСИВЫЙ ФОН ПРИЛОЖЕНИЯ ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1600&auto=format&fit=crop");
    background-size: cover; background-position: center; background-attachment: fixed;
}
[data-testid="stAppViewContainer"]::before {
    content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.55); z-index: 0;
}
.block-container {
    position: relative; z-index: 1;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px; padding: 2.5rem !important; 
    margin-top: 2rem; max-width: 650px; margin-left: auto; margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

# --- СЛОВАРЬ ЯЗЫКОВ (РУССКИЙ И АНГЛИЙСКИЙ) ---
LANGUAGES = {
    "ru": {
        "title": "🍳 Что приготовить сегодня?",
        "subtitle": "Введи ингредиенты — мы подберём рецепты!",
        "placeholder": "яйца, помидор, сыр...",
        "search_btn": "🔍 Найти рецепты",
        "input_label": "Ингредиенты (через запятую)",
        "no_recipes": "🔍 В нашей базе нет рецепта с такими ингредиентами...",
        "ai_title": "👨‍🍳 Подключить ИИ Шеф-повара",
        "ai_desc": "Наш ИИ Gemini составит уникальный пошаговый рецепт специально под твои продукты!",
        "btn_ad": "📺 Смотреть рекламу",
        "instructions": "📋 Пошаговое приготовление"
    },
    "en": {
        "title": "🍳 What to cook today?",
        "subtitle": "Enter ingredients — we'll find recipes!",
        "placeholder": "eggs, tomato, cheese...",
        "search_btn": "🔍 Find Recipes",
        "input_label": "Ingredients (separated by commas)",
        "no_recipes": "🔍 No recipes found in our database with these ingredients...",
        "ai_title": "👨‍🍳 Connect AI Chef",
        "ai_desc": "Our Gemini AI will create a unique step-by-step recipe specifically for your ingredients!",
        "btn_ad": "📺 Watch Ad",
        "instructions": "📋 Step-by-step Instructions"
    }
}

t = LANGUAGES[st.session_state.lang]

# ==========================================
# ЭКРАН 1: ВЫБОР ЯЗЫКА (ПРИ СТАРТЕ)
# ==========================================
if st.session_state.step == "welcome_lang":
    st.markdown("<h2 style='text-align: center;'>🌐 Выберите язык / Choose Language</h2>", unsafe_allow_html=True)
    st.write("")
    
    lang_select = st.radio("Language", ["Русский 🇷🇺", "English 🇺🇸"], index=0, label_visibility="collapsed")
    
    st.write("")
    if st.button("Далее / Next ➡️", use_container_width=True, type="primary"):
        st.session_state.lang = "ru" if lang_select == "Русский 🇷🇺" else "en"
        st.session_state.step = "welcome_subscription"  # Переключаем на экран подписки
        st.rerun()

# ==========================================
# ЭКРАН 2: ВЫБОР ПОДПИСКИ (PREMIUM)
# ==========================================
elif st.session_state.step == "welcome_subscription":
    if st.session_state.lang == "ru":
        st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>👑 Стань Premium Шефом!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Открой безграничную кулинарную фантазию нашего ИИ Шеф-повара</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #ff4b4b;'>👑 Become a Premium Chef!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Unlock unlimited culinary imagination of our AI Chef</p>", unsafe_allow_html=True)
        
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.lang == "ru":
            st.markdown("### 🗓️ 1 Месяц")
            st.write("Доступ к ИИ без рекламы на 30 дней.")
        else:
            st.markdown("### 🗓️ 1 Month")
            st.write("Full AI access without ads for 30 days.")
            
        if st.button("Buy $2.99", key="btn_m", use_container_width=True):
            st.session_state.is_premium = True
            st.session_state.step = "main_app"
            st.rerun()
            
    with col2:
        if st.session_state.lang == "ru":
            st.markdown("### 👑 1 Год (Скидка 16%)")
            st.write("Доступ на 12 месяцев.")
        else:
            st.markdown("### 👑 1 Year (16% Discount)")
            st.write("Full access for 12 months.")
            
        if st.button("Buy $30.00", key="btn_y", use_container_width=True, type="primary"):
            st.session_state.is_premium = True
            st.session_state.step = "main_app"
            st.rerun()
            
    st.write("---")
    skip_text = "Попробовать бесплатно (с рекламой) ➡️" if st.session_state.lang == "ru" else "Try for Free (with ads) ➡️"
    if st.button(skip_text, use_container_width=True):
        st.session_state.is_premium = False
        st.session_state.step = "main_app"
        st.rerun()

# ==========================================
# ЭКРАН 3: ГЛАВНЫЙ ЭКРАН ПРИЛОЖЕНИЯ
# ==========================================
elif st.session_state.step == "main_app":
    st.markdown("<style>.block-container { max-width: none !important; }</style>", unsafe_allow_html=True)
    
    # Кнопка сброса настроек, чтобы протестировать экраны заново
    if st.sidebar.button("⚙️ Сбросить настройки / Reset"):
        st.session_state.step = "welcome_lang"
        st.session_state.search_clicked = False
        st.rerun()
        
    if st.session_state.is_premium:
        st.sidebar.success("👑 Premium Active")
    else:
        st.sidebar.info("💡 Free Version (Ads)")

    # Загружаем базу рецептов и берём первые 80
    def load_recipes():
        try:
            with open(RECIPES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)[:80]
        except:
            return []

    recipes = load_recipes()

    st.title(t["title"])
    st.write(t["subtitle"])

    ingredients_input = st.text_input(t["input_label"], placeholder=t["placeholder"])

    if st.button(t["search_btn"], type="primary"):
        if ingredients_input:
            st.session_state.search_clicked = True
        else:
            st.warning("Введите ингредиенты!")

    if st.session_state.search_clicked and ingredients_input:
        available = set(x.strip().lower() for x in ingredients_input.split(",") if x.strip())
        matches = []
        
        for recipe in recipes:
            req = set(ing.lower() for ing in recipe["ingredients"])
            common = len(req & available)
            if common == 0: continue
            
            score = common / len(req)
            matches.append({"recipe": recipe, "score": score, "common": common})

        matches.sort(key=lambda x: -x["score"])
        top_matches = matches[:10]

        # Если совпадений в базе нет — включается ИИ Шеф-повар
        if not top_matches:
            st.warning(t["no_recipes"])
            
            st.markdown(f"""
            <div style='border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px; background-color: rgba(255,75,75,0.05); text-align: center;'>
                <h3>{t['ai_title']}</h3>
                <p>{t['ai_desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            ai_trigger = False
            
            if st.session_state.is_premium:
                ai_trigger = True
            else:
                st.write("")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"### {t['btn_ad']}")
                    if st.button(t["btn_ad"], use_container_width=True):
                        st.info("Просмотр рекламы...")
                        ai_trigger = True
                with col2:
                    st.markdown("### 🗓️ 1 Month")
                    if st.button("Buy $2.99", key="ai_m", use_container_width=True):
                        st.session_state.is_premium = True
                        st.rerun()
                with col3:
                    st.markdown("### 👑 1 Year")
                    if st.button("Buy $30.00", key="ai_y", use_container_width=True):
                        st.session_state.is_premium = True
                        st.rerun()

            if ai_trigger:
                with st.spinner("👨‍🍳 AI Chef is cooking..."):
                    try:
                        api_key = st.secrets["GEMINI_API_KEY"]
                        client = genai.Client(api_key=api_key)
                        ai_lang = "Russian" if st.session_state.lang == "ru" else "English"
                        
                        config = types.GenerateContentConfig(
                            system_instruction=f"Ты — шеф-повар. Сделай рецепт из продуктов пользователя на языке: {ai_lang}.",
                            temperature=0.7,
                        )
                        response = client.models.generateContent(
                            model='gemini-2.5-flash', contents=f"Продукты: {ingredients_input}", config=config
                        )
                        st.success("✨ Вариант от ИИ:")
                        st.markdown(response.text)
                    except:
                        st.error("Пожалуйста, настройте GEMINI_API_KEY в Settings -> Secrets.")
        else:
            # Вывод рецептов из базы JSON
            for item in top_matches:
                r = item["recipe"]
                st.markdown(f"### {r['name']} ({r['time']})")
                st.write("**🛒 Ингредиенты:** " + ", ".join(r["ingredients"]))
                with st.expander(t["instructions"]):
                    for step in r.get("instructions", []): st.write(step)
                st.divider()
