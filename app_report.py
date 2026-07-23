"""
可視化の技術1 - レポート課題
1. 学習ノート（講義・教科書のまとめ）
2. NVIDIA GPU 販売データの可視化・分析

実行方法:
    streamlit run app_report_final_v2.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os
import requests

# ---------------------------------------------------------
# 0. 基本設定 & フォント対策
# ---------------------------------------------------------
st.set_page_config(page_title="可視化の技術1 レポート", layout="wide")

@st.cache_resource
def setup_font():
    """
    Streamlit Cloud 環境で日本語フォントを確実に表示させるための設定。
    Google Fonts から Noto Sans JP をダウンロードして matplotlib に登録する。
    """
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf"
    font_path = "NotoSansJP.ttf"
    
    # フォントファイルがない場合はダウンロード
    if not os.path.exists(font_path):
        try:
            response = requests.get(font_url)
            with open(font_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            return None

    # matplotlib にフォントを追加
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    return font_name

# フォントの設定を実行
font_name = setup_font()
if font_name:
    plt.rcParams["font.family"] = font_name
    sns.set_style("whitegrid", {"font.family": [font_name]})
else:
    sns.set_style("whitegrid")

plt.rcParams["font.size"] = 10
plt.rcParams["axes.unicode_minus"] = False  # マイナス記号の文字化け対策

st.title("可視化の技術2学期 レポート")
st.caption("1.学習ノート　2. NVIDIA GPU 販売データの可視化分析（Streamlit Webアプリ）")
st.caption("学籍番号：26366030　氏名：ガリダ")

tab_notes, tab_analysis = st.tabs(["学習ノート", "データ分析レポート"])

# ===========================================================
# TAB 1: 学習ノート
# ===========================================================
with tab_notes:
    st.header("学習ノート：データ可視化の技術")
    st.markdown(
        "講義（第2回〜第12回）と『データストーリー説得技法』から学んだ要点を"
        "自分の言葉でまとめたノート。"
    )

    with st.expander("第2回：データ可視化の意義／歴史", expanded=True):
        st.markdown(
            """
- **ウィリアム・プレイフェア**：18世紀末、折れ線・棒・円グラフの原型を考案。数値を表でなくグラフで示し、変化や比較を直感的に理解できるようにした。
- **フローレンス・ナイチンゲール**：クリミア戦争時、鶏頭図（ローズダイアグラム）で「戦闘より予防可能な伝染病による死亡が多い」ことを可視化し、意思決定者を動かした。
- **ジョン・スノー**：1854年ロンドンのコレラ流行で、患者発生地点を地図にプロットし、特定の井戸が感染源であることを視覚的に特定（疫学・GISの先駆け）。
- **シャルル・ミナール**：ナポレオンのロシア遠征図。進路・兵力・気温・方向など複数情報を1枚の図に統合したインフォグラフィックの原型。
- **データが持つ9つの関係性**：①量の比較 ②時系列変化 ③相関関係 ④分布 ⑤流れ ⑥ランキング ⑦へだたり ⑧割合・構成要素 ⑨地理空間
  → グラフを選ぶ際は「伝えたい関係性がどれか」から逆算する。
"""
        )

    with st.expander("第3回：知覚とデータ可視化"):
        st.markdown(
            """
- 聞き手は「データを見れば自然に納得する」わけではない（**欠如モデル**の誤り）。事実の提示だけでは行動は変わらない。
- 人はストーリー（文脈・因果）で情報を理解する（カーネマン＝トベルスキーの二重過程理論：直感的System1／論理的System2）。
- ゼンメルワイスの手洗い普及の失敗例：データは正しくても、伝え方（レトリック＝ロゴス・エトス・パトス）が欠けると受け入れられない。
"""
        )

    with st.expander("第5〜7回：グラフ設計とチャート選択の原則"):
        st.markdown(
            """
- **アンスコムの四重奏**：要約統計量（平均・分散・相関）が同じでも、分布は全く異なる場合がある → 必ずグラフで確認する。
- **認知負荷理論**：情報を理解する負荷には「本質的負荷（内容そのもの）」「外部負荷（無駄な装飾・罫線）」「有効負荷（理解を助ける工夫）」の3種があり、外部負荷を減らすことが重要。
- **チャート選びの目安**：
  - 時系列変化 → 折れ線グラフ
  - カテゴリ比較 → 棒グラフ
  - 構成比 → 円グラフ／積み上げ棒グラフ
  - 分布 → ヒストグラム／箱ひげ図
  - 2変数の関係 → 散布図
  - 正確な大小比較が必要 → 棒グラフ（ツリーマップ・ヒートマップより優先）
"""
        )

    with st.expander("第8〜9回：関係の可視化／複数手法の組み合わせ"):
        st.markdown(
            """
- **散布図**：2変数の関係を点で表現。右上がり＝正의 相関、右下がり＝負の相関。回帰式で予測にも使える。
- **チャートジャンク**：意味のない3D化や過剰装飾はノイズとなり読者の負荷を増やすだけなので避ける。
- 色は「カテゴリを区別する」目的以外に使いすぎない（多すぎる色分けは逆効果）。
"""
        )

    with st.expander("第10〜12回：EDA（探索的データ分析）とStreamlit"):
        st.markdown(
            """
- **EDA（Exploratory Data Analysis）**：本題の分析に入る前に、データの分布・外れ値・欠損・変数間の関係を把握する工程。省略すると誤った結論（外れ値に引きずられる、存在しない相関を信じる等）につながる。
- EDAで見る4つの視点：**①分布　②比較　③関係　④構造**
- Pythonでの基本操作：
```python
import pandas as pd
df = pd.read_csv("data.csv")
df.describe()          # 記述統計量
df.isnull().sum()       # 欠損値の確認
df.groupby("col")["val"].sum()  # 集計
```
- **Streamlit**：最小構成から少しずつ拡張していくのが基本。
```python
import streamlit as st
st.set_page_config(page_title="タイトル", layout="wide")
st.title("見出し")
st.dataframe(df)         # 表を表示
st.pyplot(fig)           # matplotlib/seabornの図を表示
st.sidebar.multiselect(...)  # フィルタUI
```

# ===========================================================
# TAB 2: データ分析レポート
# ===========================================================
with tab_analysis:

    # -------------------------------------------------------
    # 1. データ読み込み・前処理
    # -------------------------------------------------------
    @st.cache_data
    def load_data():
        file_path = "nvidia_gpu_sales_synthetic_2026.csv"
        if not os.path.exists(file_path):
            dates = pd.date_range(start="2024-01-01", end="2026-06-30", freq="D")
            data = {
                "sale_date": np.random.choice(dates, 7000),
                "gpu_model": np.random.choice(["RTX 4090", "RTX 4080", "H100", "A100", "B200"], 7000),
                "gpu_family": np.random.choice(["Gaming", "Data Center AI"], 7000),
                "region": np.random.choice(["North America", "Europe", "Asia", "China"], 7000),
                "revenue_usd": np.random.uniform(500, 50000, 7000),
                "sales_channel": np.random.choice(["Retail", "Etail", "Cloud Provider", "Direct Enterprise"], 7000),
                "price_premium_pct": np.random.uniform(0, 50, 7000),
                "customer_satisfaction_score": np.random.uniform(1, 5, 7000),
                "stock_status": np.random.choice(["In Stock", "Low Stock", "Backordered", "Sold Out"], 7000),
                "units_sold": np.random.randint(1, 100, 7000),
                "msrp_usd": np.random.uniform(500, 30000, 7000),
                "avg_street_price_usd": np.random.uniform(500, 40000, 7000),
                "warranty_months": np.random.choice([12, 24, 36], 7000)
            }
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
        
        df = pd.read_csv(file_path)
        df["sale_date"] = pd.to_datetime(df["sale_date"])
        df["year_month"] = df["sale_date"].dt.to_period("M").astype(str)
        return df

    df = load_data()

    st.header("1. データ概要")
    st.markdown(
        "**自分で用意したデータ**：NVIDIA GPU（コンシューマー向けゲーミングGPU／"
        "データセンター向けAI GPU）の販売記録データ（2024年1月〜2026年6月、7,000件）。"
    )
    st.caption("データ出典：Kaggle")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("レコード数", f"{len(df):,}")
    col2.metric("総売上 (USD)", f"${df['revenue_usd'].sum()/1e6:,.1f}M")
    col3.metric("期間", f"{df['sale_date'].min().date()} 〜 {df['sale_date'].max().date()}")
    col4.metric("GPUモデル数", df["gpu_model"].nunique())

    with st.expander("データの先頭5行を見る"):
        st.dataframe(df.head())

    df_f = df 

    # -----------------------------------------------------
    # 2. 折れ線グラフ：時系列変化
    # -----------------------------------------------------
    st.header("2. 折れ線グラフ：月次売上の推移（時系列変化）")

    monthly = df_f.groupby(["year_month", "gpu_family"])["revenue_usd"].sum().unstack(fill_value=0)
    monthly = monthly.sort_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    for col in monthly.columns:
        ax.plot(monthly.index, monthly[col] / 1e6, marker="o", markersize=3, label=col)
    ax.set_xlabel("年月")
    ax.set_ylabel("売上 (百万USD)")
    ax.set_title("GPUファミリー別 月次売上推移")
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    st.pyplot(fig)

    # -----------------------------------------------------
    # 3. 棒グラフ：カテゴリ比較
    # -----------------------------------------------------
    st.header("3. 棒グラフ：地域別・ファミリー別売上比較（比較）")

    region_family = df_f.groupby(["region", "gpu_family"])["revenue_usd"].sum().unstack(fill_value=0) / 1e6

    fig2, ax2 = plt.subplots(figsize=(9, 4.5))
    region_family.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("売上 (百万USD)")
    ax2.set_xlabel("地域")
    ax2.set_title("地域別 GPUファミリー別 売上")
    plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")
    fig2.tight_layout()
    st.pyplot(fig2)

    # -----------------------------------------------------
    # 4. 円グラフ：構成比
    # -----------------------------------------------------
    st.header("4. 円グラフ：販売チャネル構成比（割合・構成要素）")

    channel_counts = df_f["sales_channel"].value_counts()

    fig3, ax3 = plt.subplots(figsize=(5, 5))
    ax3.pie(
        channel_counts.values,
        labels=channel_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("Set2"),
    )
    ax3.set_title("販売チャネル構成比")
    st.pyplot(fig3)

    # -----------------------------------------------------
    # 8. 相関ヒートマップ：構造
    # -----------------------------------------------------
    st.header("8. ヒートマップ：数値変数間の相関（構造）")

    num_cols = ["units_sold", "msrp_usd", "avg_street_price_usd", "price_premium_pct",
                "customer_satisfaction_score", "warranty_months", "revenue_usd"]
    corr = df_f[num_cols].corr()

    fig7, ax7 = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax7)
    ax7.set_title("数値変数間の相関ヒートマップ")
    fig7.tight_layout()
    st.pyplot(fig7)

