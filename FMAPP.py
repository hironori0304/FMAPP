import streamlit as st
import pandas as pd
import io
from datetime import datetime
import pytz

def main():
    st.title("回答履歴ファイルの統合")

    st.write("複数の CSV ファイルをアップロードし、すべてのファイルを1つのファイルにまとめます。")

    # 複数ファイルのアップロード
    uploaded_files = st.file_uploader("CSV ファイルをアップロード", type="csv", accept_multiple_files=True)

    if uploaded_files:
        # アップロードされたファイルをリストに格納
        dataframes = []

        for uploaded_file in uploaded_files:
            # ファイルの内容を読み込む（ファイルのエンコードもutf-8に統一）
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            dataframes.append(df)

        # データフレームを結合
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        # データフレームを表示
        st.write("結合された回答履歴")
        st.dataframe(combined_df)
        
        # 氏名の入力
        name = st.text_input("氏名を入力してください")       
        
        # 作成時間を取得（東京時刻）
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        current_time = datetime.now(tokyo_tz).strftime('%Y%m%d_%H%M%S')
        
        # ファイル名を作成
        file_name = f"{name}_回答履歴_{current_time}.csv" if name else f"回答履歴_{current_time}.csv"
        
        # ダウンロードボタンでエクスポート機能を模倣する
        csv = combined_df.to_csv(index=False, encoding='utf-8-sig')
        
        st.download_button(
            label="結合されたファイルをダウンロード",
            data=csv.encode('utf-8-sig'),
            file_name=file_name,
            mime='text/csv'
        )

if __name__ == "__main__":
    main()
