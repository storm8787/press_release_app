#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
from openai import OpenAI
import datetime

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_merit_report(name, position, start_date, award_type, achievement_area, career_list, merit_points, department):
    career_str = "\n".join([f"- {item}" for item in career_list])
    merit_str = "\n".join([f"{i+1}. {point}" for i, point in enumerate(merit_points)])

    prompt = f"""당신은 충주시의 공무원 공적조서를 작성하는 행정 전문가입니다.

아래 입력 정보를 바탕으로, 포상 대상 공무원의 공적조서를 다음 조건에 맞게 작성해주세요.

[기본 정보]
- 소속: {department}
- 직급: {position}
- 성명: {name}
- 임용일: {start_date}
- 표창 종류: {award_type}
- 공적 분야: {achievement_area}
- 주요경력:
{career_str}

- 공적요지 목록:
{merit_str}

[작성 조건]

1. 공적조서의 시작은 다음과 같이 구성합니다:
- 소속 : {department}
- 직급 : {position}
- 성명 : {name}

2. 도입부(서론)는 다음 기준에 따라 작성합니다:
- 첫 문장은 반드시 아래 형식을 따릅니다:
  "위 공무원은 {start_date} 임용된 이래로"  
- 서론에서는 "위 공무원은"이라는 표현만 사용하며, 성명(예: 이호진), 직급(예: 주사보)은 사용하지 않습니다.
- 공직자로서의 태도, 책임감, 전문성, 해당 분야에서의 헌신을 통합적으로 서술하십시오.
- 서론 마지막 문장은 반드시 아래 형식을 따릅니다:
  "{achievement_area} 발전에 지대한 공로가 인정되는 바, 그 공적을 나열하면 다음과 같습니다."

3. 본문은 각 공적요지 항목별로 다음 기준에 따라 작성합니다:
- 각 항목마다 제목과 함께 소챕터 2개로 나누어 작성하십시오.
- 각 소챕터는 최소 3~4문장 이상으로 풍부하게 구성해야 합니다.
- 본문에서는 "위 공무원"이라는 표현도 사용하지 마십시오.  
  (가능하면 주어 생략 또는 수동형 구조를 활용하여 문장을 자연스럽게 구성하십시오.)
- 성명과 직급은 본문 전체에서 절대 사용하지 않습니다.

4. 본문 마지막에는 아래 고정 챕터를 반드시 삽입하십시오:
- 제목: 공사생활에서 항상 남을 배려하는 모범 공직자
- 내용: 위 공무원은 평소 동료와 시민을 배려하는 따뜻한 성품을 바탕으로 직무를 수행해왔으며, 상사에게는 신뢰받는 직원으로, 동료에게는 친근한 동료로서 공직사회의 귀감이 되고 있습니다. 특히 맡은 업무에 대해서는 항상 성실하고 책임감 있게 수행하며, 조직의 분위기를 긍정적으로 이끄는 역할을 해왔습니다.

5. 마지막 문단은 다음 형식을 따르십시오:
"위와 같은 공로를 세운 상기인은 올바른 공직자상을 정립하고, 맡은 바 직분에 끊임없는 노력과 연구를 아끼지 않으며, 묵묵히 소신과 열정으로 {achievement_area} 업무를 추진해 온 바, {award_type}에 추천하고자 합니다."

[기타 작성 지침]
※ 문체 및 시제 지침:
- 공적조서 전 구간에 걸쳐, 모든 문장은 과거형 서술체(예: ~하였습니다, ~기여하였습니다, ~추진하였습니다 등)로 작성하십시오.
- "~같습니다", "~되었음", "~임" 등의 판단형·보고체 문장은 사용하지 마십시오.
- 서론, 본문, 마무리에 이르기까지 동일한 문체를 유지하여 일관성을 확보하십시오.

※ 기타지침
- 서론 외 구간에서는 성명 및 직급을 절대 사용하지 않습니다.
- 문장은 간결하면서도 구체적이고 사실 중심이어야 하며, 막연한 칭찬이 아닌 실적 기반의 기술을 원칙으로 합니다.

"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=3000
    )
    return response.choices[0].message.content

def create_official_merit_report():
    st.title("\U0001F3C5 공적심사의결서 생성기")
    st.markdown("공무원 정보를 입력하면 GPT가 공적사항 보고서를 자동으로 생성합니다.")

    with st.form("merit_form"):
        name = st.text_input("성명")
        position = st.text_input("직급")
        department = st.text_input("소속부서")

        start_date = st.date_input(
            "임용일",
            min_value=datetime.date(1980, 1, 1),
            max_value=datetime.date.today()
        ).strftime("%Y년 %m월 %d일")

        st.markdown("### 주요경력 (최근 3건 입력 가능)")
        career_entries = []
        for i in range(3):
            cols = st.columns([1, 3])
            with cols[0]:
                date = st.date_input(f"경력 {i+1} 날짜", key=f"career_date_{i}")
            with cols[1]:
                text = st.text_input(f"경력 {i+1} 내용 (부서 및 업무)", key=f"career_text_{i}")
            if text:
                formatted = f"{date.strftime('%Y.%m')} {text}"
                career_entries.append(formatted)

        st.markdown("### \U0001F3C6 표창 종류")
        award_type = st.text_input("예: 대통령, 국무총리, 장관, 도지사 등")

        st.markdown("### \U0001F4CC 공적 분야")
        achievement_area = st.text_input("예: 공공데이터 활용, 개인정보보호 등")

        st.markdown("### 공적요지 (한 줄에 하나씩 입력)")
        merit_raw = st.text_area("공적요지", height=200)
        merit_points = [line.strip() for line in merit_raw.splitlines() if line.strip()]

        submitted = st.form_submit_button("\U0001F4C4 공적사항 생성하기")

    if submitted:
        with st.spinner("GPT가 공적조서를 작성 중입니다..."):
            result = generate_merit_report(
                name, position, start_date, award_type, achievement_area, career_entries, merit_points, department
            )

            st.subheader("\U0001F4C4 생성된 공적사항")
            st.write(result)
            st.download_button(
                label="\U0001F4E5 결과 다운로드 (TXT)",
                data=result,
                file_name=f"{name}_공적조서.txt",
                mime="text/plain"
            )


# In[ ]:




