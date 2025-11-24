import streamlit as st
import streamlit_authenticator as stauth
import os 
# Firestoreへのアクセスは後で st.secrets に移行します。
# import firebase_admin 

# --- 1. 認証設定 (簡略化) ---
# NOTE: 実際のパスワードハッシュ値に置き換える必要があります。
users_config = {
    'credentials': {
        'usernames': {
            'mizunadad': {'email': 'dev@example.com', 'name': '開発者 (あなた)', 'password': '$2b$12$R.S4wB7yXb5Y1Ew8o2sO7O7zY5O7wQ7C7wY7O7vQ7wY7E7sO7rY7O7wQ7'}, 
            'son_chem': {'email': 'son_chem@example.com', 'name': '長男 (化学系)', 'password': '$2b$12$R.S4wB7yXb5Y1Ew8o2sO7O7zY5O7wQ7C7wY7O7vQ7wY7E7sO7rY7O7wQ7'}
        }
    },
    'cookie': {'expiry_days': 30, 'key': 'rag_auth_key', 'name': 'rag_auth_cookie'},
    'preauthorized': {'emails': ['']}
}

authenticator = stauth.Authenticate(
    users_config['credentials'],
    users_config['cookie']['name'],
    users_config['cookie']['key'],
    users_config['cookie']['expiry_days'],
    # users_config['preauthorized']
)

# --- 2. ログイン処理とUI ---
# 修正後のクリーンな記述 (この形式に統一します)
#name, authentication_status, username = authenticator.login('家族向け技術相談システム ログイン', 'main')


name, authentication_status, username = authenticator.login('technology discussions login', 'main')


if authentication_status:
    # --- ログイン成功時の処理 ---
    st.sidebar.success(f'ようこそ, {name} さん!')
    st.sidebar.markdown('---')
    
    st.title("🔬 技術トレンド相談システム (Streamlit版)")
    st.markdown("#### 家族それぞれのキャリアサポートを目的としたRAGシステムです。")
    
    # RAGロジック（未実装部分）
    query = st.text_area("質問を入力してください", height=100)
    if st.button("🔍 検索実行", type="primary"):
        if query:
            st.info(f"質問内容: {query}")
            st.warning("🚨 RAG検索ロジックは次期開発で実装します。") 
        else:
            st.error("質問を入力してください。")
            
    # --- ログアウトボタン ---
    authenticator.logout('ログアウト', 'sidebar')
    
elif authentication_status is False:
    st.error('ユーザー名/パスワードが間違っています。')
elif authentication_status is None:
    st.warning('ユーザー名とパスワードを入力してログインしてください。')
