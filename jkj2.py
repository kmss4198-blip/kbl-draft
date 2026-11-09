import base64
import json
import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 및 테마 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="정관장 레드부스터스 드래프트 예측전",
    page_icon="🏀",
    layout="centered",
)

# 이미지의 레드/블랙 UI 테마를 적용하는 Custom CSS
st.markdown(
    """
<style>
    .stApp {
        background-color: #C8102E;
        color: #ffffff;
    }
    .preview-mode {
        background-color: #ffffff;
        color: #333333;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 13px;
        margin-bottom: 20px;
    }
    .schedule-box {
        background-color: #141414;
        border: 2px solid #282828;
        border-radius: 14px;
        padding: 16px;
        color: #ffffff;
        margin-bottom: 16px;
    }
    .schedule-box h5 {
        color: #888888;
        font-size: 13px;
        margin-bottom: 8px;
    }
    .schedule-box p {
        font-size: 16px;
        font-weight: bold;
        margin: 0;
    }
    .shared-card-box {
        background-color: #1e1e1e;
        border: 2px solid #FFD700;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 25px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. 공용 파일 데이터베이스 (DB) 로직
# ---------------------------------------------------------
DB_FILE = "shared_predictions.json"


def load_all_predictions():
    """모든 참가자의 예측 데이터를 파일에서 불러옵니다."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_prediction_to_db(nickname, picks):
    """새로운 참가자 예측을 공용 파일에 저장합니다."""
    data = load_all_predictions()
    # 기존 닉네임 중복 시 업데이트, 없으면 추가
    updated = False
    for item in data:
        if item["nickname"] == nickname:
            item["picks"] = picks
            updated = True
            break
    if not updated:
        data.append({"nickname": nickname, "picks": picks})

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def encode_share_data(nickname, picks):
    """예측 결과를 URL 전송용 단축 텍스트로 인코딩합니다."""
    payload = json.dumps({"nickname": nickname, "picks": picks})
    return base64.b64encode(payload.encode("utf-8")).decode("utf-8")


def decode_share_data(encoded_str):
    """URL로 전달받은 인코딩 데이터를 복호화합니다."""
    try:
        decoded_raw = base64.b64decode(encoded_str).decode("utf-8")
        return json.loads(decoded_raw)
    except Exception:
        return None


# ---------------------------------------------------------
# 3. 드래프트 지명 후보 선수 데이터 세트
# ---------------------------------------------------------
PLAYERS_DATA = [
    {"선수명": "이주석", "학교": "건국대", "포지션": "F", "신장": 187},
    {"선수명": "여찬영", "학교": "건국대", "포지션": "G", "신장": 182},
    {"선수명": "전기현", "학교": "건국대", "포지션": "F", "신장": 194},
    {"선수명": "이동근", "학교": "고려대", "포지션": "F", "신장": 197},
    {"선수명": "이경민", "학교": "중앙대", "포지션": "G", "신장": 183},
    {"선수명": "김두진", "학교": "중앙대", "포지션": "F", "신장": 197},
    {"선수명": "유형우", "학교": "중앙대", "포지션": "G", "신장": 185},
    {"선수명": "원건", "학교": "중앙대", "포지션": "G", "신장": 185},
    {"선수명": "장지민", "학교": "명지대", "포지션": "G", "신장": 183},
    {"선수명": "김서원파이팅", "학교": "경희대", "포지션": "G", "신장": 184},
    {"선수명": "임성채", "학교": "경희대", "포지션": "G", "신장": 185},
    {"선수명": "이해솔", "학교": "연세대", "포지션": "G", "신장": 188},
    {"선수명": "부드러운홍상민", "학교": "연세대", "포지션": "C", "신장": 199},
    {"선수명": "이채형", "학교": "연세대", "포지션": "G", "신장": 186},
    {"선수명": "이주영", "학교": "연세대", "포지션": "G", "신장": 188},
    {"선수명": "김태영", "학교": "단국대", "포지션": "G", "신장": 183},
    {"선수명": "최준환", "학교": "상명대", "포지션": "C", "신장": 195},
    {"선수명": "송정우", "학교": "상명대", "포지션": "F", "신장": 192},
    {"선수명": "이한결", "학교": "동국대", "포지션": "G", "신장": 181},
    {"선수명": "우성희", "학교": "동국대", "포지션": "C", "신장": 199},
    {"선수명": "유정원", "학교": "동국대", "포지션": "G", "신장": 191},
    {"선수명": "김상윤", "학교": "동국대", "포지션": "F", "신장": 187},
    {"선수명": "한재혁", "학교": "동국대", "포지션": "G", "신장": 180},
    {"선수명": "백승혁", "학교": "동국대wise", "포지션": "G", "신장": 185},
    {"선수명": "구인교", "학교": "성균관대", "포지션": "F", "신장": 194},
    {"선수명": "김태형", "학교": "성균관대", "포지션": "G", "신장": 180},
    {"선수명": "박상혁", "학교": "성균관대", "포지션": "F", "신장": 189},
    {"선수명": "원준석", "학교": "성균관대", "포지션": "F", "신장": 195},
    {"선수명": "김수오", "학교": "경희대", "포지션": "F", "신장": 199},
    {"선수명": "김승우", "학교": "연세대", "포지션": "F", "신장": 192},
    {"선수명": "류정열", "학교": "한양대", "포지션": "C", "신장": 207},
    {"선수명": "김현우", "학교": "한양대", "포지션": "G", "신장": 178},
    {"선수명": "마윤재", "학교": ".", "포지션": "F", "신장": 188},
    {"선수명": "오벨레제이슨", "학교": "동국대wise", "포지션": "G", "신장": 186},
    {"선수명": "임동일", "학교": "동국대wise", "포지션": "C", "신장": 214},
    {"선수명": "조풍", "학교": "동국대wise", "포지션": "G", "신장": 178},
    {"선수명": "심주언", "학교": "고려대", "포지션": "G/F", "신장": 190},
    {"선수명": "고찬유", "학교": "중앙대", "포지션": "G", "신장": 190},
    {"선수명": "이관우", "학교": "성균관대", "포지션": "G", "신장": 180},
    {"선수명": "구민교", "학교": "성균관대", "포지션": "F", "신장": 197},
    {"선수명": "손유찬", "학교": "한양대", "포지션": "G", "신장": 182},
    {"선수명": "이주민", "학교": "성균관대", "포지션": "F", "신장": 196},
    {"선수명": "김현빈", "학교": "한양대", "포지션": "F", "신장": 186},
    {"선수명": "이건희", "학교": "고려대", "포지션": "G", "신장": 186},

]

df_players = pd.DataFrame(PLAYERS_DATA)
player_options = ["선택 안 함"] + [
    f"{row['선수명']} ({row['학교']}, {row['포지션']}, {row['신장']})"
    for _, row in df_players.iterrows()
]

# ---------------------------------------------------------
# 4. 헤더 및 공유 링크 파싱
# ---------------------------------------------------------
st.markdown(
    '<span style="background:#000; color:#fff; padding:4px 10px; border-radius:12px; font-weight:bold; font-size:12px;">정관장 레드부스터스</span>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='color:white; margin-top:8px; font-size:38px;'>드래프트 예측전</h1>",
    unsafe_allow_html=True,
)
st.write(
    "정관장이 뽑을 추첨 순위와, 그 순위로 가장 먼저 지명할 선수를 맞히는 게임입니다."
)

# URL 쿼리 파라미터 확인 (친구가 공유한 링크로 접속한 경우)
query_params = st.query_params
shared_data = None
if "share" in query_params:
    shared_data = decode_share_data(query_params["share"])

if shared_data:
    st.markdown(
        f"""
    <div class="shared-card-box">
        <h4>📩 친구가 공유한 예측 카드 도착!</h4>
        <p><b>{shared_data.get('nickname')}</b> 님이 작성한 1~10순위 예측 결과입니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 공유받은 카드 출력
    with st.expander(
        f"⭐ {shared_data.get('nickname')} 님의 예측 보기", expanded=True
    ):
        r1_cols = st.columns(5)
        for r in range(1, 6):
            with r1_cols[r - 1]:
                p_name = shared_data["picks"]
                st.metric(
                    f"{r}순위",
                    p_name[f"{r}순위"].split(" (")[0]
                    if f"{r}순위" in p_name
                    else "-",
                )
        r2_cols = st.columns(5)
        for r in range(6, 11):
            with r2_cols[r - 6]:
                p_name = shared_data["picks"]
                st.metric(
                    f"{r}순위",
                    p_name[f"{r}순위"].split(" (")[0]
                    if f"{r}순위" in p_name
                    else "-",
                )

# 일정 안 함 박스
col_sch1, col_sch2 = st.columns(2)
with col_sch1:
    st.markdown(
        """
    <div class="schedule-box">
        <h5>순위 추첨 · 11/9(월)</h5>
        <p>1:KT, 2:현대모비스, 3:sk, 4:정관장, 5:가스공사, 6:DB, 7:삼성, 8:LG, 9:소노, 10:KCC </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
with col_sch2:
    st.markdown(
        """
    <div class="schedule-box">
        <h5>드래프트 첫 지명 · 11/20(금)</h5>
        <p>결과 대기 중</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# 5. 1~10순위 지명 예측 입력 폼
# ---------------------------------------------------------
st.markdown("### 🏀 내 예측 카드 작성 및 공유하기")

with st.form("draft_predict_form"):
    nickname = st.text_input(
        "참가자 닉네임", placeholder="닉네임을 입력하세요 (예: 레드부스터스팬)"
    )

    user_picks = {}
    cols = st.columns(2)
    for rank in range(1, 11):
        col_idx = (rank - 1) % 2
        with cols[col_idx]:
            user_picks[f"{rank}순위"] = st.selectbox(
                f"⚙️ {rank}순위 지명 선수",
                options=player_options,
                key=f"rank_{rank}",
            )

    submit_button = st.form_submit_button(
        "내 카드 만들기 & 공유하기 🎟️", use_container_width=True
    )

    if submit_button:
        if not nickname.strip():
            st.error("닉네임을 입력해 주세요!")
        else:
            selected_list = [
                v for k, v in user_picks.items() if v != "선택 안 함"
            ]

            if len(selected_list) != len(set(selected_list)):
                st.warning(
                    "⚠️ 동일한 선수를 여러 순위에 중복해서 선택할 수 없습니다."
                )
            elif len(selected_list) < 10:
                st.warning(
                    "⚠️ 1순위부터 10순위까지 모든 선수를 선택해 주세요."
                )
            else:
                # 공용 DB 파일에 저장
                save_prediction_to_db(nickname, user_picks)

                # 공유용 URL 코드 생성
                encoded_code = encode_share_data(nickname, user_picks)
                st.session_state["last_share_code"] = encoded_code
                st.success(
                    f"🎉 '{nickname}' 님의 카드가 성공적으로 등록되었습니다!"
                )

# ---------------------------------------------------------
# 6. 생성된 카드 공유 링크 표시
# ---------------------------------------------------------
if "last_share_code" in st.session_state:
    st.markdown("#### 🔗 친구에게 내 예측 카드 공유하기")
    share_code = st.session_state["last_share_code"]

    # 파라미터가 포함된 전체 URL 안내 (실제 배포 주소로 변경하여 사용)
    share_param_text = f"?share={share_code}"
    st.info(
        "아래 공유 파라미터 코드를 주소창 끝에 붙여 친구에게 전송하거나 복사하세요!"
    )
    st.code(share_param_text, language="text")

# ---------------------------------------------------------
# 7. 전체 참가자 예측 카드 리스트 (실시간 공용 목록)
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 👥 전체 참가자 예측 목록")

all_predictions = load_all_predictions()

if not all_predictions:
    st.markdown(
        """
    <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; color: #666; text-align: center;">
        🤖 아직 등록된 참가자가 없습니다. 첫 예측 카드를 만들어 보세요!
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    for item in reversed(all_predictions):
        p_name_user = item["nickname"]
        p_picks = item["picks"]

        with st.expander(
            f"👤 {p_name_user} 님의 1~10순위 예측 카드", expanded=False
        ):
            r1_cols = st.columns(5)
            for r in range(1, 6):
                with r1_cols[r - 1]:
                    name_only = (
                        p_picks[f"{r}순위"].split(" (")[0]
                        if f"{r}순위" in p_picks
                        else "-"
                    )
                    st.metric(f"{r}순위", name_only)

            r2_cols = st.columns(5)
            for r in range(6, 11):
                with r2_cols[r - 6]:
                    name_only = (
                        p_picks[f"{r}순위"].split(" (")[0]
                        if f"{r}순위" in p_picks
                        else "-"
                    )
                    st.metric(f"{r}순위", name_only)
