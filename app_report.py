"""
可視化の技術1 - レポート課題
1. 学習ノート（講義・教科書のまとめ）
2. NVIDIA GPU 販売データの可視化・分析

実行方法:
    streamlit run app_report.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ---------------------------------------------------------
# 0. 基本設定
# ---------------------------------------------------------
st.set_page_config(page_title="可視化の技術1 レポート", layout="wide")
sns.set_style("whitegrid")
plt.rcParams["font.size"] = 10

st.title("可視化の技術1 レポート")
st.caption("① 学習ノート　② NVIDIA GPU 販売データの可視化分析（Streamlit Webアプリ）")

tab_notes, tab_analysis = st.tabs(["📓 学習ノート", "📊 データ分析レポート"])

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
- **散布図**：2変数の関係を点で表現。右上がり＝正の相関、右下がり＝負の相関。回帰式で予測にも使える。
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
"""
        )

    st.info(
        "💡 SQL初心者向けメモ：pandas の `groupby().agg()` は SQL の "
        "`GROUP BY` + `SUM()/AVG()` と同じ発想。`df[df.col=='X']` は "
        "`WHERE col='X'` に相当する。"
    )

# ===========================================================
# TAB 2: データ分析レポート
# ===========================================================
with tab_analysis:

    # -------------------------------------------------------
    # 1. データ読み込み・前処理
    # -------------------------------------------------------
    @st.cache_data
    def load_data():
        df = pd.read_csv("nvidia_gpu_sales_synthetic_2026.csv")
        df["sale_date"] = pd.to_datetime(df["sale_date"])
        df["year_month"] = df["sale_date"].dt.to_period("M").astype(str)
        return df

    df = load_data()

    st.header("1. データ概要")
    st.markdown(
        "**自分で用意したデータ**：NVIDIA GPU（コンシューマー向けゲーミングGPU／"
        "データセンター向けAI GPU）の販売記録シミュレーションデータ（2024年1月〜2026年6月、7,000件）。"
    )
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("レコード数", f"{len(df):,}")
    col2.metric("総売上 (USD)", f"${df['revenue_usd'].sum()/1e6:,.1f}M")
    col3.metric("期間", f"{df['sale_date'].min().date()} 〜 {df['sale_date'].max().date()}")
    col4.metric("GPUモデル数", df["gpu_model"].nunique())

    with st.expander("データの先頭5行を見る"):
        st.dataframe(df.head())

    # -----------------------------------------------------
    # サイドバー：フィルタ
    # -----------------------------------------------------
    st.sidebar.header("フィルタ")
    family_sel = st.sidebar.multiselect(
        "GPUファミリー", options=df["gpu_family"].unique(), default=list(df["gpu_family"].unique())
    )
    region_sel = st.sidebar.multiselect(
        "地域", options=df["region"].unique(), default=list(df["region"].unique())
    )
    df_f = df[df["gpu_family"].isin(family_sel) & df["region"].isin(region_sel)]

    # -----------------------------------------------------
    # 2. 折れ線グラフ：時系列変化
    # -----------------------------------------------------
    st.header("2. 折れ線グラフ：月次売上の推移（時系列変化）")

    monthly = df_f.groupby(["year_month", "gpu_family"])["revenue_usd"].sum().unstack(fill_value=0)

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

    st.markdown(
        "**考察：** Data Center AI 系（H100/H200/B200等）の売上は単価が高いため、"
        "件数は少なくても月次売上への影響が大きい。時期が進むにつれて両ファミリーとも"
        "取引が増加傾向にあることが読み取れる。"
    )

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

    st.markdown(
        "**考察：** 北米・欧州が売上の中心。中国は Data Center AI 向けの輸出規制の影響で"
        "在庫が絞られており（後述の在庫状況グラフ参照）、他地域と比べ AI GPU の比率が低い。"
    )

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

    st.markdown(
        "**考察：** Retail/Etail がコンシューマー向け販売の中心である一方、"
        "Cloud Provider や Direct Enterprise は AI GPU 特有のチャネルとして機能している。"
    )

    # -----------------------------------------------------
    # 5. 散布図：関係
    # -----------------------------------------------------
    st.header("5. 散布図：価格プレミアムと顧客満足度の関係（関係）")

    fig4, ax4 = plt.subplots(figsize=(7, 4.5))
    sns.scatterplot(
        data=df_f, x="price_premium_pct", y="customer_satisfaction_score",
        hue="gpu_family", alpha=0.4, s=20, ax=ax4
    )
    ax4.set_xlabel("価格プレミアム (%)")
    ax4.set_ylabel("顧客満足度スコア")
    ax4.set_title("価格プレミアム vs 顧客満足度")
    fig4.tight_layout()
    st.pyplot(fig4)

    st.markdown(
        "**考察：** 価格プレミアムが高いほど顧客満足度が下がる負の関係が見られる。"
        "特にコンシューマーゲーミング GPU は価格に敏感な傾向がある一方、"
        "Data Center AI は多少のプレミアムでも満足度の低下が緩やかである。"
    )

    # -----------------------------------------------------
    # 6. 箱ひげ図：分布
    # -----------------------------------------------------
    st.header("6. 箱ひげ図：在庫状況別の価格プレミアム分布（分布）")

    fig5, ax5 = plt.subplots(figsize=(8, 4.5))
    order = ["In Stock", "Low Stock", "Backordered", "Sold Out"]
    sns.boxplot(data=df_f, x="stock_status", y="price_premium_pct", order=order, ax=ax5)
    ax5.set_xlabel("在庫状況")
    ax5.set_ylabel("価格プレミアム (%)")
    ax5.set_title("在庫状況別 価格プレミアムの分布")
    fig5.tight_layout()
    st.pyplot(fig5)

    st.markdown(
        "**考察：** 在庫が少なくなるほど（Sold Out に近づくほど）価格プレミアムの"
        "中央値・ばらつきが大きくなっている。品薄状態が転売・値上がりに直結していることがわかる。"
    )

    # -----------------------------------------------------
    # 7. ヒストグラム：分布
    # -----------------------------------------------------
    st.header("7. ヒストグラム：一取引あたりの販売台数分布（分布）")

    fig6, ax6 = plt.subplots(figsize=(8, 4.5))
    ax6.hist(df_f["units_sold"], bins=30, color="steelblue", edgecolor="white")
    ax6.set_xlabel("販売台数（1取引あたり）")
    ax6.set_ylabel("件数")
    ax6.set_title("1取引あたりの販売台数の分布")
    fig6.tight_layout()
    st.pyplot(fig6)

    st.markdown(
        "**考察：** 分布は右に裾を引く形（右に歪んだ分布）になっており、多くの取引は"
        "少量（小売中心）だが、一部に大口注文（企業・クラウド事業者向け）が存在することを示している。"
    )

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

    st.markdown(
        "**考察：** `price_premium_pct` と `customer_satisfaction_score` は負の相関、"
        "`avg_street_price_usd` と `revenue_usd` は正の相関が明確。単価が高いDCモデルほど"
        "売上への寄与が大きい構造が数値からも裏付けられる。"
    )

    # -----------------------------------------------------
    # 9. まとめ
    # -----------------------------------------------------
    st.header("9. まとめ")
    st.markdown(
        """
- Data Center AI 系 GPU は取引数こそ少ないが、単価が非常に高く売上への貢献度が大きい
- 在庫が逼迫するほど価格プレミアムが上昇し、顧客満足度を押し下げる負の相関がある
- 地域によって GPUファミリー構成比・販売チャネルの傾向が異なる
- 販売台数の分布は右に歪んでおり、少数の大口注文が全体を牽引している
- 相関ヒートマップからも「単価↔売上」「価格プレミアム↔満足度」の関係が数値的に確認できた
"""
    )
